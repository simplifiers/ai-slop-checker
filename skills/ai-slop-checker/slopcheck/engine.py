"""Core of slop-check: load the catalog, run the checks, build the result.

The result is a plain dict that follows the JSON contract documented in
``docs/`` (see also ``build_result``). Nothing here prints or exits.
"""

import json
import os
import re

from . import VERSION
from . import text as textmod

PKG_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = ("substance", "facts", "phrases", "structure", "rhythm", "form")
SEVERITIES = ("fail", "tell", "hint")
SHORT_TEXT_WORDS = 120

# Verdict rule (documented in README/docs):
#   revise  if at least one finding has severity "fail",
#           or tells come from at least REVISE_TELL_PATTERNS different patterns
#           (rhythm patterns not counted here, they have their own rule),
#           or at least the band's revise_limit measured features are on the AI side
#   pass    otherwise
#   too_short if the text has fewer than SHORT_TEXT_WORDS words (findings are still listed)
REVISE_TELL_PATTERNS = 5
DASH_MODES = ("off", "tell", "fail")

NOTICE = {
    "de": "slop-check sagt nicht, ob eine KI einen Text geschrieben hat. Es zeigt Muster, die du prüfen kannst.",
    "en": "slop-check does not tell whether AI wrote a text. It shows patterns you can check.",
}


class SlopCheckError(Exception):
    """Expected error with a message for the user (bad option, unreadable file ...)."""


# ---------------------------------------------------------------------------
# Catalog and bands
# ---------------------------------------------------------------------------

_CATALOG_CACHE = {}


def load_catalog(lang):
    if lang not in ("de", "en"):
        raise SlopCheckError("Unsupported language: %s (use de or en)" % lang)
    if lang not in _CATALOG_CACHE:
        path = os.path.join(PKG_DIR, "patterns", lang + ".json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["by_id"] = {p["id"]: p for p in data["patterns"]}
        for p in data["patterns"]:
            m = p.get("match", {})
            if m.get("type") == "regex" and m.get("pattern"):
                flags = 0 if m.get("case") else re.I
                p["_rx"] = re.compile(m["pattern"], flags)
        _CATALOG_CACHE[lang] = data
    return _CATALOG_CACHE[lang]


def load_band(lang, register="basic", path=None):
    """Load a rhythm band. Format: {"lang","register","provisional","features":{name:{p10,p50,p90,ai_side}}}."""
    if path is None:
        path = os.path.join(PKG_DIR, "bands", "%s-%s.json" % (lang, register))
    try:
        with open(path, encoding="utf-8") as f:
            band = json.load(f)
    except (IOError, OSError, ValueError) as exc:
        raise SlopCheckError("Cannot read band file %s: %s" % (path, exc))
    if "features" not in band:
        raise SlopCheckError("Band file %s has no 'features'" % path)
    band.setdefault("provisional", False)
    return band


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def detect_language(text):
    words = [w.lower() for w in textmod.tokens(text)]
    if not words:
        return "en"
    de_fw = set(load_catalog("de")["lexicon"]["function_words"])
    en_fw = set(load_catalog("en")["lexicon"]["function_words"])
    de = sum(1 for w in words if w in de_fw)
    en = sum(1 for w in words if w in en_fw)
    umlauts = len(re.findall("[äöüßÄÖÜ]", text))
    de += umlauts * 0.5
    return "de" if de > en else "en"


# ---------------------------------------------------------------------------
# Context passed to the checks
# ---------------------------------------------------------------------------

SOURCE_MARK = re.compile(
    r"\[[^\]]+\]\(\s*https?://[^)\s]+[^)]*\)"     # [text](https://...)
    r"|https?://\S+"                              # bare URL
    r"|\(\s*(?:quelle|quellen|source|sources|via)\s*:?[^)]*\)"   # (Quelle: Name)
    r"|\b(?:quelle|source)\s*:\s*\S"              # Quelle: Name
    r"|\[\^[\w-]+\]",                             # footnote [^1]
    re.I)
NUMBERED_REF = re.compile(r"\[\d{1,3}\]")


class Context(object):
    def __init__(self, doc, lang, catalog, config, sources=None):
        self.doc = doc
        self.lang = lang
        self.catalog = catalog
        self.lex = catalog["lexicon"]
        self.config = config
        self.sources = sources or []          # list of (name, Doc)
        self.findings = []
        self.people = []
        self.facts = {"lost": [], "added": []}
        self.metrics = {}
        self.rhythm = []
        self.number_tokens_in_sources = set()
        self._allow_spans = None
        self.has_sources_section = any(b.zone == "sources" for b in doc.blocks) or bool(
            re.search(r"^\s*\[\d{1,3}\]\s*\S", doc.text, re.M))

    # -- catalog ------------------------------------------------------------
    def pattern(self, pid):
        return self.catalog["by_id"].get(pid)

    def enabled(self, pid):
        return pid not in self.config.get("disable", ()) and pid in self.catalog["by_id"]

    # -- allowlist ----------------------------------------------------------
    def allow_spans(self):
        if self._allow_spans is None:
            spans = []
            terms = list(self.catalog.get("allow", [])) + list(self.config.get("allow", []))
            low = self.doc.text.lower()
            for t in terms:
                t = t.strip().lower()
                if not t:
                    continue
                for m in re.finditer(r"(?<!\w)" + re.escape(t) + r"\w*", low):
                    spans.append((m.start(), m.end()))
            self._allow_spans = spans
        return self._allow_spans

    def allowed(self, start, end):
        for s, e in self.allow_spans():
            if s < end and start < e:  # any overlap with an allowed term
                return True
        return False

    # -- sources in a sentence ---------------------------------------------
    def sentence_sourced(self, start, end):
        seg = self.doc.text[start:end]
        if SOURCE_MARK.search(seg):
            return True
        if self.has_sources_section and NUMBERED_REF.search(seg):
            return True
        b = self.doc.block_at(start)
        if b is not None and b.kind == "table":
            return self.table_sourced(b, start)
        return False

    def table_sourced(self, block, offset):
        text = self.doc.text
        line_start = text.rfind("\n", 0, offset) + 1
        line_end = text.find("\n", offset)
        line_end = len(text) if line_end < 0 else line_end
        if SOURCE_MARK.search(text[line_start:line_end]):
            return True
        header = text[block.start:text.find("\n", block.start) if "\n" in text[block.start:block.end] else block.end]
        if re.search(r"\b(quelle|source)", header, re.I):
            cells = [c.strip() for c in text[line_start:line_end].strip().strip("|").split("|")]
            hcells = [c.strip() for c in header.strip().strip("|").split("|")]
            for i, h in enumerate(hcells):
                if re.search(r"\b(quelle|source)", h, re.I) and i < len(cells) and re.search(r"\w", cells[i]):
                    return True
        after = text[block.end:block.end + 300].lstrip("\n")
        first = after.split("\n", 1)[0]
        if re.match(r"^\s*[*_(>]*\s*(quelle|quellen|source|sources)\s*:", first, re.I):
            return True
        return False

    # -- findings -----------------------------------------------------------
    def add(self, pid, start, end, message=None, severity=None, fix=None, excerpt=None, line=None):
        p = self.pattern(pid)
        if p is None or not self.enabled(pid):
            return None
        text = self.doc.text
        if excerpt is None:
            excerpt = re.sub(r"\s+", " ", text[start:end]).strip()
            if len(excerpt) > 160:
                excerpt = excerpt[:157].rstrip() + "..."
        f = {
            "id": pid,
            "category": p["category"],
            "severity": severity or p["severity"],
            "name": p["name"],
            "line": line if line is not None else self.doc.line_of(start),
            "start": start,
            "end": end,
            "excerpt": excerpt,
            "message": message or p["description"],
            "fix": fix or p.get("fix") or p.get("better", ""),
        }
        self.findings.append(f)
        return f


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CONFIG_KEYS = {"lang", "address", "forbid", "allow", "emojis", "disable", "own_names", "fail_on", "bands",
               "sources", "register", "dashes"}


def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (IOError, OSError) as exc:
        raise SlopCheckError("Cannot read config %s: %s" % (path, exc))
    except ValueError as exc:
        raise SlopCheckError("Config %s is not valid JSON: %s" % (path, exc))
    if not isinstance(data, dict):
        raise SlopCheckError("Config %s must be a JSON object" % path)
    unknown = set(data) - CONFIG_KEYS
    if unknown:
        raise SlopCheckError("Unknown config keys in %s: %s" % (path, ", ".join(sorted(unknown))))
    return data


def split_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).split(",") if v.strip()]


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def check_text(raw, lang=None, sources=None, config=None, score=False, expert_share=None):
    """Check a text. ``sources`` is a list of (name, raw_text). Returns the result dict."""
    from .checks import substance, facts, phrases, structure, rhythm, form

    config = dict(config or {})
    for key in ("forbid", "allow", "disable", "own_names"):
        config[key] = split_list(config.get(key))
    if config.get("address") not in (None, "", "du", "sie"):
        raise SlopCheckError("address must be du or sie")
    if config.get("emojis") not in (None, "", "allow", "no", "limit"):
        raise SlopCheckError("emojis must be allow, no or limit")
    if config.get("dashes") in (None, ""):
        config["dashes"] = "tell"
    if config["dashes"] not in DASH_MODES:
        raise SlopCheckError("dashes must be off, tell or fail")

    text = textmod.normalise(raw)
    lang = (lang or config.get("lang") or "").lower() or detect_language(text)
    catalog = load_catalog(lang)
    doc = textmod.parse(text, lang)
    src_docs = []
    for name, sraw in (sources or []):
        src_docs.append((name, textmod.parse(textmod.normalise(sraw), lang)))
    ctx = Context(doc, lang, catalog, config, src_docs)
    band = load_band(lang, config.get("register") or "basic", config.get("bands"))

    facts.run(ctx)          # first: tells substance which numbers the notes cover
    substance.run(ctx)
    phrases.run(ctx)
    structure.run(ctx)
    rhythm.run(ctx, band)
    form.run(ctx)
    _dedupe(ctx)

    words = doc.word_count()
    result = build_result(ctx, words)
    if score:
        result["score"] = lite_score(ctx, expert_share)
    return result


def _dedupe(ctx):
    """Drop S-01 where S-12 already reports the same span, and exact duplicates."""
    s12 = {(f["start"], f["end"]) for f in ctx.findings if f["id"] == "S-12"}
    seen = set()
    out = []
    for f in ctx.findings:
        if f["id"] == "S-01" and any(s <= f["start"] < e or f["start"] <= s < f["end"] for s, e in s12):
            continue
        key = (f["id"], f["start"], f["end"], f["excerpt"] if f["line"] == 0 else "")
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    out.sort(key=lambda f: (f["line"], f["start"], f["id"]))
    ctx.findings = out


def verdict_for(findings, words, lang, ai_side_count=0, ai_side_limit=None):
    de = lang == "de"
    fails = [f for f in findings if f["severity"] == "fail"]
    tell_ids = sorted({f["id"] for f in findings if f["severity"] == "tell" and not f["id"].startswith("R-")})
    if words < SHORT_TEXT_WORDS:
        return "too_short", (
            "Unter %d Wörtern gibt es kein Gesamturteil, nur die einzelnen Funde." % SHORT_TEXT_WORDS if de else
            "Below %d words there is no overall verdict, only the individual findings." % SHORT_TEXT_WORDS)
    if fails:
        ids = sorted({f["id"] for f in fails})
        return "revise", (
            "%d harte Funde (%s). Regel: ein harter Fund oder Auffälligkeiten aus mindestens %d verschiedenen Mustern bedeuten überarbeiten."
            % (len(fails), ", ".join(ids), REVISE_TELL_PATTERNS) if de else
            "%d hard findings (%s). Rule: one hard finding, or tells from at least %d different patterns, means revise."
            % (len(fails), ", ".join(ids), REVISE_TELL_PATTERNS))
    if len(tell_ids) >= REVISE_TELL_PATTERNS:
        return "revise", (
            "Auffälligkeiten aus %d verschiedenen Mustern (%s). Regel: ab %d Mustern überarbeiten."
            % (len(tell_ids), ", ".join(tell_ids), REVISE_TELL_PATTERNS) if de else
            "Tells from %d different patterns (%s). Rule: %d or more patterns means revise."
            % (len(tell_ids), ", ".join(tell_ids), REVISE_TELL_PATTERNS))
    if ai_side_limit and ai_side_count >= ai_side_limit:
        return "revise", (
            "%d gemessene Merkmale liegen auf der Seite generierter Texte. Regel: ab %d Merkmalen überarbeiten."
            % (ai_side_count, ai_side_limit) if de else
            "%d measured features are on the generated-text side. Rule: %d or more means revise."
            % (ai_side_count, ai_side_limit))
    measured = ""
    if ai_side_limit:
        measured = (" Gemessene Merkmale auf der KI-Seite: %d (Grenze %d)." % (ai_side_count, ai_side_limit) if de else
                    " Measured features on the AI side: %d (limit %d)." % (ai_side_count, ai_side_limit))
    return "pass", (
        "Kein harter Fund und Auffälligkeiten aus %d Mustern (Grenze %d).%s Hinweise zählen nicht."
        % (len(tell_ids), REVISE_TELL_PATTERNS, measured) if de else
        "No hard finding and tells from %d patterns (limit %d).%s Hints do not count."
        % (len(tell_ids), REVISE_TELL_PATTERNS, measured))


def build_result(ctx, words):
    summary = {c: {"fail": 0, "tell": 0, "hint": 0} for c in CATEGORIES}
    for f in ctx.findings:
        summary[f["category"]][f["severity"]] += 1
    limit = ctx.metrics.get("ai_side_limit") if ctx.metrics.get("ai_side_count") is not None else None
    verdict, reason = verdict_for(ctx.findings, words, ctx.lang, ctx.metrics.get("ai_side_count") or 0, limit)
    return {
        "tool": "slop-check",
        "version": VERSION,
        "lang": ctx.lang,
        "register": "article",
        "words": words,
        "verdict": verdict,
        "verdict_reason": reason,
        "notice": NOTICE[ctx.lang],
        "findings": ctx.findings,
        "summary": summary,
        "facts": ctx.facts,
        "people": ctx.people,
        "metrics": ctx.metrics,
        "rhythm": ctx.rhythm,
        "text": ctx.doc.text,
    }


# ---------------------------------------------------------------------------
# Optional: Lite slop score (compatibility with AI Redaktion Lite)
# ---------------------------------------------------------------------------

LITE_SCORE = {
    "expert_share": {"max": 30},          # (100 minus share) times 0.3
    "unsourced_figures": {"each": 5, "max": 20},
    "people_without_source": {"each": 5, "max": 10},
    "phrases": {"each": 3, "max": 12},
    "dashes": {"each": 1, "max": 4},
    "headings": {"each": 3, "max": 6},
    "address_switches": {"each": 2, "max": 6},
    "form_errors": {"each": 2, "max": 6},
}


def lite_score(ctx, expert_share=None):
    f = ctx.findings

    def count(pred):
        return sum(1 for x in f if pred(x))

    counts = {
        "unsourced_figures": count(lambda x: (x["id"] in ("S-01", "S-02", "S-12")) and x["severity"] == "fail"),
        "people_without_source": len([p for p in ctx.people if not p["sourced"]]),
        "phrases": count(lambda x: x["category"] == "phrases" and x["severity"] != "hint"),
        "dashes": count(lambda x: x["id"] in ("F-01", "F-02", "F-03")),
        "headings": count(lambda x: x["id"] == "F-06"),
        "address_switches": count(lambda x: x["id"] == "F-07" and x["severity"] != "hint"),
        "form_errors": count(lambda x: x["id"] == "F-09" or (x["id"] == "F-04" and x["severity"] != "hint")),
    }
    parts = {}
    total = 0
    for key, n in counts.items():
        rule = LITE_SCORE[key]
        pts = min(n * rule["each"], rule["max"])
        parts[key] = {"count": n, "each": rule["each"], "max": rule["max"], "points": pts}
        total += pts
    if expert_share is None:
        parts["expert_share"] = {"share_percent": None, "max": 30, "points": None}
        score = None
    else:
        pts = max(0, min(30, int(round((100 - float(expert_share)) * 0.3))))
        parts["expert_share"] = {"share_percent": expert_share, "max": 30, "points": pts}
        score = min(100, total + pts)
    return {"slop_score": score, "sum_without_expert_share": total, "parts": parts,
            "formula": "Lite slop score: 0 is best, 100 worst; parts capped as listed."}
