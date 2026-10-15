"""Substance: unsourced figures, vague attribution, people, portability, concreteness, advice, smoothing."""

import re

from .. import text as textmod
from . import numbers
from .people import find_people

CLAIM_ZONES = ("body", "faq")


def _first_person_re(lex):
    return re.compile(r"\b(?:" + "|".join(re.escape(w) for w in lex["first_person"]) + r")\b", re.I)


def _own_experience(sentence, lex, lang):
    """A figure in an I/we sentence is probably first-hand: hint instead of fail."""
    s = sentence.strip().lstrip("\"'„“»(*_[ ")
    words = textmod.tokens(s)[:7]
    fp = set(lex["first_person"])
    if any(w.lower() in fp for w in words):
        return True
    if lang == "de":
        return bool(re.search(r"\b(?:bei uns|in meiner (?:praxis|erfahrung)|in unserer (?:praxis|erfahrung)|unsere[nmr]? (?:kunden|daten|zahlen|messung|auswertung|erfahrung))\b", s, re.I))
    return bool(re.search(r"\b(?:at our|in my (?:practice|experience)|in our (?:practice|experience)|our (?:clients|customers|data|numbers|figures|measurements))\b", s, re.I))


def run(ctx):
    doc = ctx.doc
    _figures(ctx)
    _regex_pattern(ctx, "S-02", doc.claim_text, sourced_check=True)
    _regex_pattern(ctx, "S-07", doc.style_text, sourced_check=False, allow=True)
    _people(ctx)
    _portability_and_concreteness(ctx)
    _advice(ctx)


# ---------------------------------------------------------------------------

def _figures(ctx):
    doc, lex, lang = ctx.doc, ctx.lex, ctx.lang
    units = lex["units"]
    claim_text = doc.claim_text
    pending = []          # headings, faq, meta: checked against figures backed in the body
    backed = set(ctx.number_tokens_in_sources)
    units_list = []
    for sent in doc.sentences:
        b = sent.block
        if b.zone not in CLAIM_ZONES or b.kind == "code":
            continue
        units_list.append((sent.start, sent.end, b))
    # table rows as units
    for b in doc.blocks:
        if b.kind == "table" and b.zone in CLAIM_ZONES:
            pos = b.start
            for line in doc.text[b.start:b.end].split("\n"):
                if not re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", line):
                    units_list.append((pos, pos + len(line), b))
                pos += len(line) + 1
    for start, end, b in sorted(units_list, key=lambda u: u[0]):
        seg = claim_text[start:end]
        spans = numbers.find_claims(seg, lang, units)
        if not spans:
            continue
        sourced = ctx.sentence_sourced(start, end)
        toks = set()
        for a, e in spans:
            toks |= numbers.numbers_in(seg[a:e], lang, lex["number_words"])
        if sourced:
            backed |= toks
            continue
        if b.kind == "heading" or b.zone == "faq":
            pending.append((start, end, spans, toks))
            continue
        _report_figures(ctx, start, end, spans, toks, backed)
    for start, end, spans, toks in pending:
        if toks and toks <= backed:
            continue
        _report_figures(ctx, start, end, spans, toks, backed)


def _report_figures(ctx, start, end, spans, toks, backed):
    lang, lex = ctx.lang, ctx.lex
    if toks and toks <= ctx.number_tokens_in_sources:
        return  # the user's notes contain these figures
    sentence = ctx.doc.text[start:end]
    own = _own_experience(sentence, lex, lang)
    if not own:
        # narrative context: the previous sentence of the same paragraph is first-hand ("we laid ...")
        prev = [s for s in ctx.doc.sentences if s.end <= start and s.block.start <= start < s.block.end]
        if prev and _own_experience(prev[-1].text, lex, lang):
            own = True
    for a, e in spans:
        s, en = start + a, start + e
        val = re.sub(r"\s+", " ", ctx.doc.text[s:en]).strip()
        if own:
            ctx.add("S-08", s, en, message=(
                "Zahl „%s“ in einem Ich- oder Wir-Satz: eigene Erfahrung? Zeitraum und Messgröße ergänzen." % val
                if lang == "de" else
                "Figure \"%s\" in an I or we sentence: first-hand? Add the time span and what was measured." % val))
        else:
            ctx.add("S-01", s, en, message=(
                "Zahl „%s“ ohne Quelle im selben Satz." % val if lang == "de" else
                "Figure \"%s\" without a source in the same sentence." % val))


def _regex_pattern(ctx, pid, src, sourced_check=True, allow=False):
    p = ctx.pattern(pid)
    if not p or "_rx" not in p or not ctx.enabled(pid):
        return
    for sent in ctx.doc.sentences:
        if sent.block.zone not in CLAIM_ZONES:
            continue
        for m in p["_rx"].finditer(src, sent.start, sent.end):
            if not m.group(0).strip():
                continue
            if sourced_check and ctx.sentence_sourced(sent.start, sent.end):
                break
            if allow and ctx.allowed(m.start(), m.end()):
                continue
            ctx.add(pid, m.start(), m.end())


def _people(ctx):
    own = {n.lower() for n in ctx.config.get("own_names", [])}
    seen = {}
    for sent in ctx.doc.sentences:
        if sent.block.zone not in CLAIM_ZONES:
            continue
        for name, a, e, linked in find_people(ctx.doc.text, sent.start, sent.end, ctx.lang, ctx.lex):
            if name.lower() in own or name.split()[-1].lower() in own:
                continue
            sourced = linked or ctx.sentence_sourced(sent.start, sent.end)
            line = ctx.doc.line_of(a)
            if name not in seen:
                seen[name] = {"name": name, "line": line, "sourced": sourced}
                ctx.people.append(seen[name])
            elif sourced:
                seen[name]["sourced"] = True
            if not sourced:
                ctx.add("S-03", a, e, message=(
                    "%s wird ohne Quelle im Satz zitiert oder wiedergegeben. Gibt es die Person, und hat sie das gesagt?" % name
                    if ctx.lang == "de" else
                    "%s is quoted or paraphrased without a source in the sentence. Does the person exist, and did they say this?" % name))


# ---------------------------------------------------------------------------
# Concreteness
# ---------------------------------------------------------------------------

def concrete_markers(ctx, start, end):
    """Count concrete details in text[start:end]: numbers, names, dates, examples, first person, quotes, links."""
    doc, lex, lang = ctx.doc, ctx.lex, ctx.lang
    raw = doc.text[start:end]
    seg = doc.claim_text[start:end]
    n = 0
    n += len(re.findall(r"\d+", seg))
    low_words = [w.lower() for w in textmod.tokens(seg)]
    nw = {k for k in lex["number_words"] if k not in ("ein", "eine", "einen", "eins", "one")}
    months = set(lex["months"])
    fp = set(lex["first_person"])
    n += sum(1 for w in low_words if w in nw or w in months or w in fp)
    for cue in lex["example_cues"]:
        n += len(re.findall(cue, seg, re.I))
    n += len(textmod.QUOTE_SPANS.findall(raw))
    n += len(re.findall(r"https?://", raw))
    n += len(_proper_names(seg, lang, lex))
    return n


def _proper_names(seg, lang, lex):
    stop = set(lex["name_stop"])
    names = []
    for m in re.finditer(r"\b[A-Z][a-z]+[A-Z]\w*\b|\b[A-Za-z]+-?\d+[\w-]*\b", seg):   # HubSpot, GPT4
        if not m.group(0).isdigit():
            names.append(m.group(0))
    if lang == "en":
        for m in re.finditer(r"(?<=[a-z,;:)] )[A-Z][a-z]+(?:\s[A-Z][a-z]+)*", seg):
            if m.group(0).split()[0] not in stop:
                names.append(m.group(0))
    else:
        for m in re.finditer(r"\b(?:Herr|Frau|Dr\.|Prof\.)\s+[A-ZÄÖÜ][a-zäöüß]+", seg):
            names.append(m.group(0))
    return names


def _portability_and_concreteness(ctx):
    doc = ctx.doc
    p4 = ctx.pattern("S-04")
    min_words = (p4 or {}).get("match", {}).get("min_words", 35)
    total_words = 0
    total_markers = 0
    for b in doc.blocks:
        if b.zone not in ("body",) or b.kind not in ("paragraph", "list"):
            continue
        words = len(textmod.WORD_RE.findall(doc.claim_text, b.start, b.end))
        markers = concrete_markers(ctx, b.start, b.end)
        total_words += words
        total_markers += markers
        if b.kind == "paragraph" and words >= min_words and markers == 0:
            ctx.add("S-04", b.start, b.end, message=(
                "Absatz mit %d Wörtern ohne Zahl, Namen, Datum, Beispiel oder eigene Erfahrung: könnte in jedem Text stehen." % words
                if ctx.lang == "de" else
                "Paragraph of %d words with no number, name, date, example or first-hand experience: it could be in any text." % words))
    rate = round(100.0 * total_markers / total_words, 2) if total_words else 0.0
    ctx.metrics["concreteness_per_100"] = rate
    p5 = ctx.pattern("S-05")
    threshold = (p5 or {}).get("match", {}).get("min_per_100", 1.0)
    if doc.word_count() >= 120 and total_words and rate < threshold:
        first = next((b for b in doc.blocks if b.zone == "body" and b.kind == "paragraph"), None)
        if first is not None:
            ctx.add("S-05", first.start, first.start, excerpt="", message=(
                "Nur %.1f konkrete Angaben pro 100 Wörter im ganzen Text (vorläufige Grenze %.1f)." % (rate, threshold)
                if ctx.lang == "de" else
                "Only %.1f concrete details per 100 words across the text (provisional threshold %.1f)." % (rate, threshold)))


def _advice(ctx):
    doc, lex = ctx.doc, ctx.lex
    p = ctx.pattern("S-06")
    if not p:
        return
    min_cues = p["match"].get("min_cues", 3)
    cues = [re.compile(c, re.I) for c in lex["directive_cues"]]
    examples = [re.compile(c, re.I) for c in lex["example_cues"]]
    blocks = doc.blocks
    for i, b in enumerate(blocks):
        if b.zone != "body" or b.kind != "paragraph":
            continue
        seg = doc.style_text[b.start:b.end]
        n = sum(len(c.findall(seg)) for c in cues)
        if n < min_cues:
            continue
        if re.search(r"\d", seg) or any(e.search(seg) for e in examples):
            continue
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        if nxt is not None and nxt.kind == "list":
            continue
        if seg.rstrip().endswith(":"):
            continue
        ctx.add("S-06", b.start, b.end, message=(
            "%d Aufforderungen in einem Absatz, aber keine Schritte und kein Beispiel." % n if ctx.lang == "de" else
            "%d instructions in one paragraph, but no steps and no example." % n))
