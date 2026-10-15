"""Form: dashes, emojis, bold, label headings, address switches (de), heading density, banned words."""

import re

from .. import text as textmod

EM = "\u2014"
EN = "\u2013"

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF☀-➿⭐⭕⬆⬇⬅←-⇿]")
ENDINGS = {
    "de": ("ern", "ens", "en", "er", "es", "em", "e", "n", "s"),
    "en": ("ings", "ing", "ers", "er", "ed", "es", "e", "s"),
}


def run(ctx):
    _dashes(ctx)
    _emojis(ctx)
    _bold(ctx)
    _headings(ctx)
    if ctx.lang == "de":
        _address(ctx)
    _heading_density(ctx)
    _forbidden(ctx)


def _checkable(ctx, a, b):
    doc = ctx.doc
    if doc.is_ignored(a, b) or doc.is_quoted(a, b):
        return False
    blk = doc.block_at(a)
    return blk is not None and blk.zone in ("body", "faq") and blk.kind != "code"


DASH_MESSAGE = {
    "de": "Stilregel: viele Leser empfinden lange Gedankenstriche als KI-typisch. Abschalten mit \"dashes\": \"off\".",
    "en": "Style rule: many readers see long dashes as typical of AI. Switch off with \"dashes\": \"off\".",
}


def _dashes(ctx):
    """Dashes are a style rule, not a measured AI signal. Config "dashes": off, tell (default) or fail.

    The mode sets the severity of F-01 (em dash); F-02 and F-03 stay tells and are
    switched off together with F-01.
    """
    mode = ctx.config.get("dashes") or "tell"
    if mode == "off":
        return
    doc = ctx.doc
    t = doc.text
    for m in re.finditer(EM, t):
        if _checkable(ctx, m.start(), m.end()):
            ctx.add("F-01", max(0, m.start() - 1), min(len(t), m.end() + 1), excerpt=_around(t, m.start()),
                    severity=mode, message=DASH_MESSAGE[ctx.lang])
    for m in re.finditer(EN, t):
        if not _checkable(ctx, m.start(), m.end()):
            continue
        left = t[:m.start()].rstrip()[-1:]
        right = t[m.end():].lstrip()[:1]
        if left.isdigit() and right.isdigit():
            continue
        ctx.add("F-02", max(0, m.start() - 1), min(len(t), m.end() + 1), excerpt=_around(t, m.start()))
    for b in doc.blocks:
        if b.zone not in ("body", "faq") or b.kind not in ("paragraph", "list", "heading"):
            continue
        for m in re.finditer(r"(?<=\S) - (?=\S)", t[b.start:b.end]):
            a = b.start + m.start()
            if not _checkable(ctx, a, a + 3):
                continue
            if t[a - 1].isdigit() and t[a + 3].isdigit():
                continue
            ctx.add("F-03", a, a + 3, excerpt=_around(t, a + 1))


def _around(t, pos, width=40):
    a = max(0, pos - width)
    e = min(len(t), pos + width)
    s = re.sub(r"\s+", " ", t[a:e]).strip()
    return ("..." if a > 0 else "") + s + ("..." if e < len(t) else "")


def _section_of(doc, pos):
    sec = 0
    for b in doc.blocks:
        if b.start > pos:
            break
        if b.kind == "heading":
            sec = b.index
    return sec


def _emojis(ctx):
    doc = ctx.doc
    mode = ctx.config.get("emojis") or "limit"
    if mode == "allow":
        return
    per_section = {}
    for m in EMOJI_RE.finditer(doc.text):
        if not _checkable(ctx, m.start(), m.end()) and not (doc.block_at(m.start()) and doc.block_at(m.start()).kind == "heading"):
            continue
        if doc.is_ignored(m.start(), m.end()):
            continue
        if mode == "no":
            ctx.add("F-04", m.start(), m.end(), severity="tell")
            continue
        sec = _section_of(doc, m.start())
        per_section.setdefault(sec, []).append(m)
    for sec, ms in per_section.items():
        if len(ms) > 1:
            for m in ms[1:]:
                ctx.add("F-04", m.start(), m.end(), severity="hint", message=(
                    "Mehr als ein Emoji in diesem Abschnitt." if ctx.lang == "de" else "More than one emoji in this section."))


BOLD_RE = re.compile(r"\*\*[^*\n]+?\*\*|__[^_\n]+?__")


def _bold(ctx):
    doc = ctx.doc
    total = 0
    spans = []
    for b in doc.blocks:
        if b.zone not in ("body", "faq") or b.kind not in ("paragraph", "list"):
            continue
        seg = doc.text[b.start:b.end]
        if BOLD_RE.fullmatch(seg.strip()):
            continue  # a bold line used as a heading
        found = [(b.start + m.start(), b.start + m.end()) for m in BOLD_RE.finditer(seg)]
        total += len(found)
        spans.append((b, found))
    words = max(1, doc.word_count())
    global_trigger = total >= 6 and total * 40.0 / words > 1.0
    for b, found in spans:
        if len(found) >= 3 or (global_trigger and found):
            for a, e in found:
                ctx.add("F-05", a, e)


def _headings(ctx):
    doc = ctx.doc
    label = re.compile(ctx.lex["heading_label"], re.I)
    whatis = re.compile(ctx.lex["heading_whatis"], re.I)
    for b in doc.blocks:
        if b.kind != "heading" or b.zone != "body":
            continue
        txt = textmod.heading_text(doc.text[b.start:b.end])
        if label.match(txt) or whatis.match(txt):
            ctx.add("F-06", b.start, b.end)


def _address(ctx):
    doc = ctx.doc
    du = re.compile(ctx.lex["address_du"], re.I)
    sie = re.compile(ctx.lex["address_sie"])
    src = doc.style_text
    du_hits, sie_hits = [], []
    for s in doc.sentences:
        if s.block.zone not in ("body", "faq"):
            continue
        seg = src[s.start:s.end]
        lead = len(re.match(r"^[\s\"'„“(*_\[#>-]*", seg).group(0))
        for m in du.finditer(seg):
            du_hits.append((s.start + m.start(), s.start + m.end()))
        for m in sie.finditer(seg):
            if m.start() <= lead:
                continue  # sentence start: could be "sie" (they)
            sie_hits.append((s.start + m.start(), s.start + m.end()))
    want = ctx.config.get("address")
    if want == "du":
        for a, b in sie_hits:
            ctx.add("F-07", a, b, severity="fail", message="Sie-Form „%s“ in einem Du-Text." % doc.text[a:b])
    elif want == "sie":
        for a, b in du_hits:
            ctx.add("F-07", a, b, severity="fail", message="Du-Form „%s“ in einem Sie-Text." % doc.text[a:b])
    elif du_hits and sie_hits:
        minority, form = (sie_hits, "Sie") if len(sie_hits) <= len(du_hits) else (du_hits, "du")
        for a, b in minority:
            ctx.add("F-07", a, b, message=(
                "Der Text nutzt du und Sie. „%s“ ist die seltenere Form (%s)." % (doc.text[a:b], form)))


def _heading_density(ctx):
    doc = ctx.doc
    p = ctx.pattern("F-08")
    if not p:
        return
    min_words = p["match"].get("min_words_per_heading", 80)
    min_head = p["match"].get("min_headings", 4)
    heads = [b for b in doc.blocks if b.kind == "heading" and b.zone == "body" and b.level >= 2]
    words = doc.word_count()
    if len(heads) >= min_head and words / float(len(heads)) < min_words:
        ctx.add("F-08", heads[0].start, heads[0].end, message=(
            "%d Zwischenüberschriften auf %d Wörter: eine alle %d Wörter." % (len(heads), words, words // len(heads))
            if ctx.lang == "de" else
            "%d subheadings for %d words: one every %d words." % (len(heads), words, words // len(heads))))


def inflected(term, lang):
    parts = []
    for w in term.split():
        stem = w
        for e in ENDINGS[lang]:
            if w.lower().endswith(e) and len(w) - len(e) >= 4:
                stem = w[:-len(e)]
                break
        parts.append(re.escape(stem) + r"(?:" + "|".join(ENDINGS[lang]) + r")?")
    return r"\s+".join(parts)


def _forbidden(ctx):
    terms = ctx.config.get("forbid") or []
    src = ctx.doc.style_text
    for t in terms:
        rx = re.compile(r"(?<!\w)" + inflected(t, ctx.lang) + r"(?!\w)", re.I)
        for m in rx.finditer(src):
            blk = ctx.doc.block_at(m.start())
            if blk is None or blk.zone in ("code", "frontmatter", "sources"):
                continue
            ctx.add("F-09", m.start(), m.end(), message=(
                "„%s“ steht auf deiner Verbotsliste." % m.group(0) if ctx.lang == "de" else
                "\"%s\" is on your banned list." % m.group(0)))
