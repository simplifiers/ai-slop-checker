"""Rhythm: measured style features compared with a percentile band of human texts.

Features are computed by ``slopcheck.meter`` with the same definitions the band was
measured with. Each feature is compared with {p10, p50, p90, ai_side}:
  ok        value within [p10, p90]
  ai_side   outside the band on the side typical for generated text
  overshot  outside the band on the other side (shown, not reported)

A single feature outside the band is common in human texts, so each one is only a
hint. The verdict uses the count of features on the AI side (``ai_side_count``):
from the band's ``revise_limit`` on, R-10 is reported as a tell and the verdict is
revise. Provisional bands never count.

Features that did not separate human from generated text in the measurement
(dashes, passive voice, connector openings, parentheses) are not part of the band.
"""

import re

from .. import meter

FEATURE_IDS = {
    "mean_sentence_len": "R-01",
    "cv_sentence_len_para": "R-02",
    "words_per_paragraph": "R-03",
    "mattr50": "R-04",
    "mean_word_len": "R-05",
    "nominalizations_1k": "R-06",
    "triads_1k": "R-07",
    "colons_1k": "R-08",
    "participle_tail_1k": "R-09",
}
SUMMARY_ID = "R-10"
DEFAULT_REVISE_LIMIT = 6

LABELS = {
    "de": {
        "mean_sentence_len": "Wörter je Satz",
        "cv_sentence_len_para": "Streuung der Satzlängen",
        "words_per_paragraph": "Wörter je Absatz",
        "mattr50": "Wortvielfalt (MATTR)",
        "mean_word_len": "Buchstaben je Wort",
        "nominalizations_1k": "Nominalisierungen je 1.000 Wörter",
        "triads_1k": "Dreierlisten je 1.000 Wörter",
        "colons_1k": "Doppelpunkte je 1.000 Wörter",
        "participle_tail_1k": "Partizip-Anhängsel je 1.000 Wörter",
    },
    "en": {
        "mean_sentence_len": "words per sentence",
        "cv_sentence_len_para": "spread of sentence lengths",
        "words_per_paragraph": "words per paragraph",
        "mattr50": "vocabulary variety (MATTR)",
        "mean_word_len": "letters per word",
        "nominalizations_1k": "nominalisations per 1,000 words",
        "triads_1k": "lists of three per 1,000 words",
        "colons_1k": "colons per 1,000 words",
        "participle_tail_1k": "trailing participles per 1,000 words",
    },
}

_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_BOLD_LINE = re.compile(r"^\*\*[^*]+\*\*:?$")


def prose_blocks(doc):
    """Running prose of the body as (kind, text) blocks for the meter.

    Paragraphs become "p", every list item becomes its own "li". Headings, quotes,
    code, tables, FAQ, sources and meta sections are left out, as in the corpus.
    """
    out = []
    for b in doc.blocks:
        if b.zone != "body" or b.kind not in ("paragraph", "list"):
            continue
        raw = doc.text[b.start:b.end]
        if b.kind == "paragraph":
            lines = [line.strip() for line in raw.splitlines() if line.strip()]
            if lines and _BOLD_LINE.match(lines[0]):
                lines = lines[1:]  # a bold first line works as a heading, as in the corpus
            text = meter.md_inline(" ".join(lines))
            if text:
                out.append(("p", text))
            continue
        items = []
        for line in raw.splitlines():
            if _ITEM.match(line):
                items.append(_ITEM.sub("", line, count=1).strip())
            elif line.strip() and items:
                items[-1] += " " + line.strip()
            elif line.strip():
                items.append(line.strip())
        for it in items:
            text = meter.md_inline(it)
            if text:
                out.append(("li", text))
    return out


def measure(ctx):
    blocks = prose_blocks(ctx.doc)
    f = meter.extract(blocks, ctx.lang)
    m = {}
    if f is None:
        m["prose_words"] = sum(len(meter.words(t)) for _, t in blocks)
        for name in FEATURE_IDS:
            m[name] = None
        return m
    m["prose_words"] = f["_words"]
    for name in FEATURE_IDS:
        m[name] = f.get(name)
    return m


def _fmt(x):
    return ("%.3f" % x).rstrip("0").rstrip(".") if abs(x) < 10 else ("%.1f" % x).rstrip("0").rstrip(".")


def classify(value, spec):
    if value is None:
        return None
    lo, hi, side = spec["p10"], spec["p90"], spec.get("ai_side", "none")
    if lo <= value <= hi:
        return "ok"
    if side == "low":
        return "ai_side" if value < lo else "overshot"
    if side == "high":
        return "ai_side" if value > hi else "overshot"
    return "overshot"


def run(ctx, band):
    m = measure(ctx)
    ctx.metrics.update(m)
    provisional = bool(band.get("provisional"))
    limit = int(band.get("revise_limit") or DEFAULT_REVISE_LIMIT)
    anchor = next((b for b in ctx.doc.blocks if b.zone == "body" and b.kind == "paragraph"), None)
    de = ctx.lang == "de"
    labels = LABELS[ctx.lang]
    on_ai_side = []
    for feat, pid in FEATURE_IDS.items():
        spec = band["features"].get(feat)
        if spec is None:
            continue
        value = m.get(feat)
        state = classify(value, spec)
        if state is None:
            continue
        ctx.rhythm.append({"feature": feat, "value": value,
                           "band": {"p10": spec["p10"], "p50": spec.get("p50"), "p90": spec["p90"],
                                    "ai_side": spec.get("ai_side", "none")},
                           "state": state, "provisional": provisional})
        if state != "ai_side":
            continue  # outside on the other side is shown in the table, not reported
        on_ai_side.append(feat)
        if anchor is None:
            continue
        v, lo, hi = _fmt(value), _fmt(spec["p10"]), _fmt(spec["p90"])
        if de:
            v, lo, hi = v.replace(".", ","), lo.replace(".", ","), hi.replace(".", ",")
            where = "unter" if value < spec["p10"] else "über"
            msg = "%s: %s liegt %s dem Band %s bis %s, auf der Seite generierter Texte%s." % (
                labels[feat], v, where, lo, hi, " (vorläufige Grenzen)" if provisional else "")
        else:
            where = "below" if value < spec["p10"] else "above"
            msg = "%s: %s is %s the band %s to %s, on the generated-text side%s." % (
                labels[feat], v, where, lo, hi, " (provisional bands)" if provisional else "")
        ctx.add(pid, anchor.start, anchor.start, severity="hint", message=msg, excerpt="")
    measured = any(m.get(f) is not None for f in band["features"])
    count = None if provisional or not measured else len(on_ai_side)
    ctx.metrics["ai_side_count"] = count
    ctx.metrics["ai_side_limit"] = limit
    if count is not None and count >= limit and anchor is not None:
        names = ", ".join(labels[f] for f in on_ai_side)
        n_feats = len(band["features"])
        ctx.add(SUMMARY_ID, anchor.start, anchor.start, severity="tell", excerpt="", message=(
            "%d von %d gemessenen Merkmalen liegen auf der Seite generierter Texte (Grenze %d): %s."
            % (count, n_feats, limit, names) if de else
            "%d of %d measured features are on the generated-text side (limit %d): %s."
            % (count, n_feats, limit, names)))
