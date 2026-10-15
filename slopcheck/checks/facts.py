"""Fact comparison between the draft and the user's sources (--source notes.md).

lost:  in a source, missing from the draft
added: in the draft, in no source, and without a citation in the sentence
"""

import re

from . import numbers
from .people import find_people

URL_ANY = re.compile(r"https?://[^\s)\]>\"'<]+")


def _norm_url(u):
    u = u.rstrip(".,;:!?)")
    u = re.sub(r"^https?://(?:www\.)?", "", u.lower())
    return u.rstrip("/")


def _dates(text, lang, lex):
    months = [m for m in lex["months"] if len(m) > 3][:12]
    mon = r"(?:" + "|".join(months) + r")"
    if lang == "de":
        pats = [r"\b\d{1,2}\.\s?\d{1,2}\.\s?\d{4}\b", r"\b\d{1,2}\.\s?" + mon + r"(?:\s+\d{4})?\b", r"\b" + mon + r"\s+\d{4}\b",
                r"\b\d{4}-\d{2}-\d{2}\b"]
    else:
        pats = [r"\b" + mon + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b", r"\b\d{1,2}(?:st|nd|rd|th)?\s+" + mon + r"\s+\d{4}\b",
                r"\b" + mon + r"\s+\d{4}\b", r"\b\d{4}-\d{2}-\d{2}\b"]
    out = []
    for p in pats:
        for m in re.finditer(p, text, re.I):
            out.append((m.start(), m.end()))
    for m in re.finditer(r"(?<![\d.,/-])(?:19|20)\d{2}(?![\d.,/-]*\d)", text):
        out.append((m.start(), m.end()))
    out.sort()
    merged = []
    for a, b in out:
        if merged and a < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def _names(doc, lang, lex, src):
    """Proper names: people, CamelCase brands, multi-word capitalised sequences."""
    stop = set(lex["name_stop"])
    out = []
    text = src
    for sent in doc.sentences:
        if sent.block.zone in ("code", "frontmatter"):
            continue
        for name, a, e, _l in find_people(doc.text, sent.start, sent.end, lang, lex):
            out.append(("name", name, a, e))
    for m in re.finditer(r"\b[A-Z][a-z]+[A-Z][A-Za-z]*\b", text):
        out.append(("name", m.group(0), m.start(), m.end()))
    seq = r"[A-ZÄÖÜ][a-zäöüß]+(?:[-'][A-ZÄÖÜ]?[a-zäöüß]+)?"
    for m in re.finditer(r"(?<=[a-zäöüß,;:)] )" + seq + r"(?:\s+" + seq + r")+", text):
        toks = m.group(0).split()
        before = text[max(0, m.start() - 12):m.start()].lower()
        if any(t in stop for t in toks):
            continue
        if lang == "de" and re.search(r"\b(der|die|das|dem|den|des|ein|eine|einem|einen|einer|zum|zur|im|am|beim|vom)\s$", before):
            continue
        if re.search(r"(?:\d|\b(?:" + "|".join(lex["number_words"]) + r"))\s$", before, re.I):
            continue
        suf = tuple(lex.get("noun_suffixes") or ())
        if suf and any(t.lower().endswith(suf) for t in toks):
            continue
        out.append(("name", m.group(0), m.start(), m.end()))
    return out


def extract(doc, lang, lex):
    """Facts in a parsed document: list of dicts {type, value, key, start, end}."""
    src = doc.claim_text
    units = lex["units"]
    items = []
    taken = bytearray(len(src))
    for m in URL_ANY.finditer(doc._masked(doc.ignore)):
        items.append({"type": "url", "value": m.group(0).rstrip(".,;:)"), "key": _norm_url(m.group(0)),
                      "start": m.start(), "end": m.end()})
    for a, b in _dates(src, lang, lex):
        val = re.sub(r"\s+", " ", src[a:b]).strip()
        items.append({"type": "date", "value": val, "key": val.lower(), "start": a, "end": b})
        for i in range(a, b):
            taken[i] = 1
    tech = numbers.blank_technical(src, lang, units)
    num_rx = re.compile(r"(?:(?:€|\$|£)\s?)?(?:\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
                        r"(?:\s?(?:%|prozent\b|percent\b|mio\.?|millionen|million|milliarden|billion|mrd\.?|tausend|thousand|€|euro\b|eur\b|\$|dollar\b|usd\b|£))?",
                        re.I)
    for m in num_rx.finditer(tech):
        a, b = m.start(), m.end()
        if any(taken[a:b]) or not m.group(0).strip():
            continue
        raw = m.group(0).strip()
        digits = re.findall(r"\d[\d.,]*", raw)
        if not digits:
            continue
        key = numbers.norm_number(digits[0].rstrip(".,"), lang)
        unit = raw[raw.find(digits[0]) + len(digits[0]):].strip().lower()
        has_unit = bool(unit) or raw[0] in "€$£"
        if not has_unit and len(key.replace(".", "")) < 2:
            continue   # single digits: too common to compare
        if src[max(0, a - 2):a].strip().endswith("#") or re.match(r"\s*[.)]\s", src[b:b + 3]) and src[:a].rstrip().endswith("\n"):
            continue
        typ = "percent" if ("%" in unit or "prozent" in unit or "percent" in unit) else (
            "money" if has_unit and re.search(r"[€$£]|euro|eur|dollar|usd", raw, re.I) else "number")
        items.append({"type": typ, "value": raw, "key": key, "start": a, "end": b})
    for typ, val, a, e in _names(doc, lang, lex, src):
        items.append({"type": "name", "value": val, "key": val.lower(), "start": a, "end": e})
    # dedupe by span and key
    seen = set()
    out = []
    for it in sorted(items, key=lambda x: x["start"]):
        k = (it["type"], it["key"], it["start"])
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out


def _present(item, keys_by_type, plain_text, num_keys):
    t = item["type"]
    if t in ("number", "percent", "money"):
        return item["key"] in num_keys
    if t == "url":
        return item["key"] in keys_by_type.get("url", set())
    if t == "date":
        if item["key"] in keys_by_type.get("date", set()):
            return True
        nums = re.findall(r"\d+", item["value"])
        return bool(nums) and all(str(int(n)) in num_keys for n in nums) or item["key"] in plain_text
    if t == "name":
        low = item["value"].lower()
        if low in plain_text:
            return True
        last = low.split()[-1]
        return len(low.split()) > 1 and len(last) > 3 and re.search(r"\b" + re.escape(last) + r"\b", plain_text) is not None
    return False


def run(ctx):
    if not ctx.sources:
        return
    doc, lang, lex = ctx.doc, ctx.lang, ctx.lex
    draft_items = extract(doc, lang, lex)
    draft_plain = doc.text.lower()
    draft_nums = numbers.numbers_in(doc.claim_text, lang, lex["number_words"])
    d_keys = {}
    for it in draft_items:
        d_keys.setdefault(it["type"], set()).add(it["key"])

    src_items = []
    src_plain = ""
    src_nums = set()
    s_keys = {}
    for name, sdoc in ctx.sources:
        items = extract(sdoc, lang, lex)
        for it in items:
            it["source"] = name
            s_keys.setdefault(it["type"], set()).add(it["key"])
        src_items.extend(items)
        src_plain += "\n" + sdoc.text.lower()
        src_nums |= numbers.numbers_in(sdoc.claim_text, lang, lex["number_words"])
    ctx.number_tokens_in_sources = src_nums

    # lost
    reported = set()
    for it in src_items:
        k = (it["type"], it["key"])
        if k in reported:
            continue
        if _present(it, d_keys, draft_plain, draft_nums):
            continue
        reported.add(k)
        ctx.facts["lost"].append({"type": it["type"], "value": it["value"], "source": it["source"]})
        ctx.add("S-11", 0, 0, line=0, excerpt=it["value"],
                severity="hint" if it["type"] == "name" else None,
                message=("„%s“ steht in %s, aber nicht im Entwurf." % (it["value"], it["source"]) if lang == "de" else
                         "\"%s\" is in %s but not in the draft." % (it["value"], it["source"])))

    # added
    reported = set()
    for it in draft_items:
        b = doc.block_at(it["start"])
        if b is None or b.zone in ("code", "frontmatter", "meta"):
            continue
        k = (it["type"], it["key"])
        if k in reported:
            continue
        if _present(it, s_keys, src_plain, src_nums):
            continue
        reported.add(k)
        sent = next((s for s in doc.sentences if s.start <= it["start"] < s.end + 1), None)
        if b.zone == "sources" or it["type"] == "url":
            sourced = False
        elif sent is not None:
            sourced = ctx.sentence_sourced(sent.start, sent.end)
        else:
            sourced = ctx.sentence_sourced(b.start, b.end)
        line = doc.line_of(it["start"])
        ctx.facts["added"].append({"type": it["type"], "value": it["value"], "line": line, "sourced": sourced})
        if sourced:
            continue
        if it["type"] in ("number", "percent", "money", "url"):
            ctx.add("S-12", it["start"], it["end"], message=(
                "„%s“ steht in keiner Quelle und hat keinen Beleg im Satz." % it["value"] if lang == "de" else
                "\"%s\" is in none of the sources and has no citation in the sentence." % it["value"]))
        else:
            ctx.add("S-13", it["start"], it["end"], message=(
                "„%s“ steht in keiner Quelle." % it["value"] if lang == "de" else
                "\"%s\" is in none of the sources." % it["value"]))
