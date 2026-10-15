"""Structure: contrast template, stacked triads, connectors, repeated openings, rhetorical openers,
colon reveals, grand closing line, summary ending, trailing participle clauses."""

import re

from .. import text as textmod

PROSE = ("body",)
CONNECTOR_RATE = 6.0  # per 1,000 words; human p90 in the measured bands is 2.3 to 4.4


def _prose_sentences(doc, kinds=("paragraph", "list")):
    return [s for s in doc.sentences if s.block.zone in PROSE and s.block.kind in kinds]


def run(ctx):
    _contrast(ctx)
    _triads(ctx)
    _connectors(ctx)
    _same_openings(ctx)
    _rhetorical_openers(ctx)
    _colon_reveal(ctx)
    _ending(ctx)
    _participle_tail(ctx)


def _repeated(ctx, pid, hits, min_tell=2, single_hint=True):
    """hits: [(start, end)]. One hit: hint; from min_tell on: tell for each."""
    if not hits:
        return
    if len(hits) >= min_tell:
        for a, b in hits:
            ctx.add(pid, a, b)
    elif single_hint:
        for a, b in hits:
            ctx.add(pid, a, b, severity="hint")


def _contrast(ctx):
    src = ctx.doc.style_text
    hits = []
    for rx in ctx.lex["contrast"]:
        for m in re.finditer(rx, src, re.I):
            b = ctx.doc.block_at(m.start())
            if b is not None and b.zone in PROSE and m.group(0).strip():
                hits.append((m.start(), m.end()))
    _repeated(ctx, "T-01", sorted(set(hits)))


ITEM = r"[A-Za-zÄÖÜäöüß][\wÀ-ſ-]*(?: [\wÀ-ſ-]+){0,2}"


def _triads(ctx):
    doc = ctx.doc
    conj = r"(?:und|oder|sowie)" if ctx.lang == "de" else r"(?:and|or)"
    rx = re.compile(r"(?<!, )\b" + ITEM + r", " + ITEM + r",? " + conj + r" " + ITEM + r"\b")
    hits = []
    for s in _prose_sentences(doc, kinds=("paragraph",)):
        for m in rx.finditer(doc.style_text, s.start, s.end):
            if re.search(r"\d", m.group(0)):
                continue
            # a longer enumeration (four or more items) is a real list, not a rhetorical triad
            if doc.style_text[m.end():m.end() + 2] == ", ":
                continue
            hits.append((m.start(), m.end(), s.block.index))
    per_para = {}
    for h in hits:
        per_para.setdefault(h[2], []).append(h)
    words = max(1, doc.word_count())
    text_trigger = len(hits) >= 4 and len(hits) * 300.0 / words >= 1.0
    for a, b, bi in hits:
        if text_trigger or len(per_para[bi]) >= 2:
            ctx.add("T-02", a, b)


def _connectors(ctx):
    doc = ctx.doc
    conns = sorted(ctx.lex["connectors"], key=len, reverse=True)
    rx = re.compile(r"^[\s\"'„“(*_\[]*(" + "|".join(re.escape(c.rstrip(",")) for c in conns) + r")\b,?", re.I)
    hits = []
    for s in _prose_sentences(doc):
        m = rx.match(doc.style_text[s.start:s.end])
        if m:
            hits.append((s.start + m.start(1), s.start + m.end(1), s.block.index))
    # Connector openings did not separate human from generated text in the measurement
    # (one per 1,000 words is normal), so only a cluster counts: three in one paragraph,
    # or at least three in the text at a rate above CONNECTOR_RATE per 1,000 words.
    per_para = {}
    for h in hits:
        per_para.setdefault(h[2], []).append(h)
    words = max(1, doc.word_count())
    text_cluster = len(hits) >= 3 and len(hits) * 1000.0 / words > CONNECTOR_RATE
    for a, b, bi in hits:
        if text_cluster or len(per_para[bi]) >= 3:
            ctx.add("T-03", a, b)


def _same_openings(ctx):
    doc = ctx.doc
    p = ctx.pattern("T-04")
    run_len = (p or {}).get("match", {}).get("run", 3)
    sents = [s for s in doc.sentences if s.block.zone in PROSE and s.block.kind == "paragraph"]
    i = 0
    while i < len(sents):
        first = _first_word(doc, sents[i])
        j = i + 1
        while j < len(sents) and first and _first_word(doc, sents[j]) == first:
            j += 1
        if first and j - i >= run_len:
            ctx.add("T-04", sents[i].start, sents[j - 1].end, message=(
                "%d Sätze in Folge beginnen mit „%s“." % (j - i, first.capitalize()) if ctx.lang == "de" else
                "%d sentences in a row start with \"%s\"." % (j - i, first.capitalize())))
            i = j
        else:
            i += 1


def _first_word(doc, s):
    w = textmod.tokens(doc.style_text[s.start:s.end])
    return w[0].lower() if w else ""


def _rhetorical_openers(ctx):
    doc = ctx.doc
    hits = []
    for b in doc.blocks:
        if b.zone not in PROSE or b.kind != "paragraph":
            continue
        sents = [s for s in doc.sentences if s.block is b]
        n0 = len(textmod.tokens(sents[0].text)) if sents else 0
        if len(sents) >= 2 and sents[0].text.rstrip("*_ ").endswith("?") and 4 <= n0 <= 15:
            hits.append((sents[0].start, sents[0].end))
    _repeated(ctx, "T-05", hits)


QWORD = re.compile(r"^\W*(?:was|wie|warum|wieso|weshalb|wer|wen|wem|wo|wann|welche\w*|woran|wozu|ob|"
                   r"what|how|why|who|whom|where|when|which|whose|is|are|do|does|did|can|should)\b", re.I)


def _colon_reveal(ctx):
    doc = ctx.doc
    excl = set(ctx.lex["colon_heads_exclude"])
    rx = re.compile(r"^[\s*_]*((?:[\wÀ-ſ'’-]+\s){0,3}[\wÀ-ſ'’-]+)[*_]*\s?([:?])[*_]*\s+(?=[\wÀ-ſ\"„])")
    hits = []
    for s in _prose_sentences(doc, kinds=("paragraph",)):
        seg = doc.style_text[s.start:s.end]
        m = rx.match(seg)
        if not m:
            continue
        head = m.group(1).strip().lower()
        if head in excl or re.search(r"\d", head) or len(head.split()) > 3:
            continue
        if m.group(2) == "?" and QWORD.match(head):
            continue
        hits.append((s.start, s.start + m.end(2)))
    # "The result? More enquiries." : a question of one to three words, answered by the next sentence
    sents = _prose_sentences(doc, kinds=("paragraph",))
    for i, s in enumerate(sents[:-1]):
        seg = doc.style_text[s.start:s.end].strip(" *_")
        words = textmod.tokens(seg)
        if seg.endswith("?") and 1 <= len(words) <= 3 and sents[i + 1].block is s.block and not QWORD.match(seg):
            if " ".join(words).lower() not in excl:
                hits.append((s.start, s.end))
    _repeated(ctx, "T-06", sorted(set(hits)))


def _last_body_paragraph(doc):
    last = None
    for b in doc.blocks:
        if b.zone == "body" and b.kind == "paragraph":
            last = b
        elif b.zone in ("faq", "sources", "meta") and last is not None:
            break
    return last


def _ending(ctx):
    doc = ctx.doc
    last = _last_body_paragraph(doc)
    if last is None:
        return
    sents = [s for s in doc.sentences if s.block is last]
    if not sents:
        return
    final = sents[-1]
    seg = doc.style_text[final.start:final.end]
    for rx in ctx.lex["pathos_close"]:
        m = re.search(rx, seg, re.I)
        if m:
            ctx.add("T-07", final.start, final.end)
            break
    first = doc.style_text[sents[0].start:sents[0].end].strip().lstrip("*_ ").lower()
    opener = next((o for o in ctx.lex["summary_openers"] if first.startswith(o)), None)
    if opener:
        ctx.add("T-08", sents[0].start, sents[0].start + len(opener) + 1)


def _participle_tail(ctx):
    doc = ctx.doc
    hits = []
    for rx in ctx.lex["participle_tail"]:
        for m in re.finditer(rx, doc.style_text, re.I):
            b = doc.block_at(m.start())
            if b is not None and b.zone in PROSE:
                hits.append((m.start() + 1, m.end()))
    _repeated(ctx, "T-09", sorted(set(hits)))
