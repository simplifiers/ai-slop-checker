"""Preprocessing: turn Markdown, HTML or plain text into a document model.

The document keeps one text (``Doc.text``). Every offset in a finding points
into this text. For Markdown and plain text it is the input with normalised
line endings. For HTML the tags are converted to a light Markdown form first,
and that converted text becomes ``Doc.text``.

Zones decide what each check may look at:

- body, list, heading, faq: prose, checked for style and substance
- quote (blockquotes) and inline quotations: not judged for style,
  still used for facts and numbers
- code, frontmatter, comment: ignored completely
- table: checked for numbers and facts, not for rhythm
- sources, meta: not judged for style; sources count as evidence
"""

import bisect
import re
from html.parser import HTMLParser

PROSE_ZONES = ("body", "list", "faq")

ABBREVIATIONS = {
    "de": (
        "z. b.", "z.b.", "u. a.", "u.a.", "d. h.", "d.h.", "ca.", "bzw.", "dr.", "prof.", "nr.", "s.",
        "vgl.", "etc.", "inkl.", "evtl.", "ggf.", "usw.", "bspw.", "mio.", "mrd.", "jh.", "abs.", "st.",
        "o. ä.", "u. ä.", "sog.", "art.", "zzgl.", "max.", "min.", "bzgl.", "hr.", "fr.", "abb.", "tab.",
    ),
    "en": (
        "e.g.", "i.e.", "etc.", "vs.", "dr.", "mr.", "mrs.", "ms.", "prof.", "approx.", "no.", "inc.",
        "ltd.", "co.", "st.", "jan.", "feb.", "aug.", "sept.", "oct.", "nov.", "dec.", "fig.", "cf.",
        "u.s.", "a.m.", "p.m.", "jr.", "sr.", "dept.", "est.",
    ),
}

FAQ_HEAD = re.compile(
    r"^(häufige fragen|häufig gestellte fragen|faq|faqs|fragen und antworten|"
    r"frequently asked questions|common questions|questions and answers)\b", re.I)
SOURCES_HEAD = re.compile(
    r"^(quellen|quellenverzeichnis|quellen und links|literatur|weiterführende links|einzelnachweise|"
    r"sources|references|further reading|bibliography|sources and links|notes and sources)\b", re.I)
META_HEAD = re.compile(r"^(meta|seo|meta-daten|metadata)\b", re.I)
META_LABEL = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?(seo-titel|seo titel|seo-title|seo title|meta-beschreibung|meta beschreibung|"
    r"meta-description|meta description)(?:\*\*)?\s*(?:\([^)]*\))?\s*:", re.I)

QUOTE_SPANS = re.compile(
    "„[^“”\"\n]{1,400}[“”\"]"   # German low-high quotes
    "|“[^”\n]{1,400}”"                     # English curly quotes
    "|\"[^\"\n]{1,400}\""                                 # straight quotes
    "|»[^«\n]{1,400}«|«[^»\n]{1,400}»"  # guillemets
)
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_TEXT_RE = re.compile(r"\[([^\]\n]{1,200})\]\(\s*(?:https?://|/|\.|#)[^)\s]*[^)]*\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
WORD_RE = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿĀ-žẞß]+(?:['’\-][0-9A-Za-zÀ-ÖØ-öø-ÿĀ-žẞß]+)*")


class Block(object):
    """A run of lines: one paragraph, heading, list item, quote, table, code block ..."""

    __slots__ = ("kind", "zone", "start", "end", "line", "level", "index")

    def __init__(self, kind, zone, start, end, line, level=0):
        self.kind = kind      # paragraph, heading, list, quote, table, code, frontmatter, comment
        self.zone = zone      # body, faq, sources, meta, frontmatter, code
        self.start = start
        self.end = end
        self.line = line
        self.level = level
        self.index = -1

    def __repr__(self):
        return "Block(%s,%s,%d-%d)" % (self.kind, self.zone, self.start, self.end)


class Sentence(object):
    __slots__ = ("start", "end", "block", "text")

    def __init__(self, start, end, block, text):
        self.start = start
        self.end = end
        self.block = block
        self.text = text


class Doc(object):
    def __init__(self, text, lang="de"):
        self.text = text
        self.lang = lang
        self.line_starts = [0] + [m.end() for m in re.finditer("\n", text)]
        self.blocks = []
        # masks: True means "excluded"
        self.ignore = bytearray(len(text))   # code, frontmatter, comments: no check at all
        self.quote = bytearray(len(text))    # quotations: no style judgement
        self.url = bytearray(len(text))      # URLs and link targets
        self.title = bytearray(len(text))    # link texts (titles of linked sources): no style judgement
        self.sentences = []
        self._style_text = None
        self._claim_text = None

    # -- positions --------------------------------------------------------
    def line_of(self, offset):
        return bisect.bisect_right(self.line_starts, offset)

    def block_at(self, offset):
        for b in self.blocks:
            if b.start <= offset < b.end:
                return b
        return None

    # -- derived texts ----------------------------------------------------
    def _masked(self, *masks):
        chars = list(self.text)
        for i, ch in enumerate(chars):
            if ch == "\n":
                continue
            for m in masks:
                if m[i]:
                    chars[i] = " "
                    break
        return "".join(chars)

    @property
    def style_text(self):
        """Text for style checks: code, quotes, URLs, sources, meta blanked out."""
        if self._style_text is None:
            extra = bytearray(len(self.text))
            for b in self.blocks:
                if b.zone in ("sources", "meta", "frontmatter", "code") or b.kind in ("quote", "code", "comment"):
                    for i in range(b.start, b.end):
                        extra[i] = 1
            self._style_text = self._masked(self.ignore, self.quote, self.url, self.title, extra)
        return self._style_text

    @property
    def claim_text(self):
        """Text for number and fact claims: quotes stay, code and URLs go."""
        if self._claim_text is None:
            extra = bytearray(len(self.text))
            for b in self.blocks:
                if b.zone in ("sources", "frontmatter", "code", "meta") or b.kind in ("code", "comment"):
                    for i in range(b.start, b.end):
                        extra[i] = 1
            self._claim_text = self._masked(self.ignore, self.url, extra)
        return self._claim_text

    def is_quoted(self, start, end):
        return any(self.quote[start:end])

    def is_ignored(self, start, end):
        return any(self.ignore[start:end]) or any(self.url[start:end])

    # -- convenience ------------------------------------------------------
    def prose_blocks(self, kinds=("paragraph", "list"), zones=PROSE_ZONES):
        return [b for b in self.blocks if b.kind in kinds and b.zone in zones]

    def words_in(self, start, end, masked=True):
        src = self.style_text if masked else self.text
        return [m for m in WORD_RE.finditer(src, start, end)]

    def word_count(self):
        """Words in prose, headings, quotes and tables. No code, meta, sources, frontmatter."""
        n = 0
        src = self._masked(self.ignore, self.url)
        for b in self.blocks:
            if b.zone in ("body", "faq") and b.kind in ("paragraph", "list", "heading", "quote", "table"):
                n += len(WORD_RE.findall(src, b.start, b.end))
        return n


# ---------------------------------------------------------------------------
# HTML to light Markdown
# ---------------------------------------------------------------------------

class _HtmlToMd(HTMLParser):
    BLOCK = {"p", "div", "section", "article", "header", "footer", "main", "aside", "figure", "figcaption",
             "table", "tr", "ul", "ol", "dl", "dd", "dt", "br", "hr", "form"}
    SKIP = {"script", "style", "noscript", "svg", "head", "title"}

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.out = []
        self.skip = 0
        self.prefix_stack = []
        self.in_pre = 0
        self.href = None

    def _nl(self, n=2):
        cur = "".join(self.out[-3:])
        have = len(cur) - len(cur.rstrip("\n"))
        if self.out:
            self.out.append("\n" * max(0, n - have))

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._nl()
            self.out.append("#" * int(tag[1]) + " ")
        elif tag == "li":
            self._nl(1)
            self.out.append("- ")
        elif tag == "blockquote":
            self._nl()
            self.out.append("> ")
        elif tag == "pre":
            self._nl()
            self.out.append("```\n")
            self.in_pre += 1
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            self.href = a.get("href")
            self.out.append("[")
        elif tag in ("td", "th"):
            self.out.append("| ")
        elif tag in self.BLOCK:
            self._nl(1 if tag in ("br", "tr") else 2)

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "blockquote"):
            self._nl()
        elif tag == "pre":
            self.out.append("\n```")
            self.in_pre = max(0, self.in_pre - 1)
            self._nl()
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            self.out.append("](" + self.href + ")" if self.href else "]")
            self.href = None
        elif tag == "tr":
            self.out.append(" |")
            self._nl(1)
        elif tag in self.BLOCK:
            self._nl()

    def handle_data(self, data):
        if self.skip:
            return
        if not self.in_pre:
            data = re.sub(r"\s+", " ", data)
            if self.out and self.out[-1].endswith(("\n", "# ", "- ", "> ")):
                data = data.lstrip()
        self.out.append(data)


def looks_like_html(raw):
    return len(re.findall(r"</?(p|h[1-6]|div|article|ul|ol|li|br|section|body|html|blockquote)\b[^>]*>", raw, re.I)) >= 2


def html_to_markdown(raw):
    p = _HtmlToMd()
    p.feed(raw)
    p.close()
    text = "".join(p.out)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def normalise(raw):
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("﻿"):
        text = text[1:]
    if looks_like_html(text):
        text = html_to_markdown(text)
    # HTML comments are not part of the text: drop them, keep their line breaks so that
    # line numbers still match the input file.
    text = HTML_COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return text.replace("\t", "    ")


# ---------------------------------------------------------------------------
# Block structure
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_RE = re.compile(r"^\s{0,6}([-*+•]|\d{1,3}[.)])\s+")
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
RULE_RE = re.compile(r"^\s*(---+|\*\*\*+|___+)\s*$")


def heading_text(line):
    s = line.strip().lstrip("#").strip()
    s = s.strip("*_ ").rstrip(":")
    return re.sub(r"^\d+[.)]\s*", "", s)


def parse(text, lang="de"):
    doc = Doc(text, lang)
    lines = text.split("\n")
    starts = doc.line_starts
    n = len(lines)

    def lstart(i):
        return starts[i]

    def lend(i):
        return starts[i] + len(lines[i])

    blocks = []
    i = 0
    # frontmatter
    if n and lines[0].strip() == "---":
        for k in range(1, min(n, 80)):
            if lines[k].strip() == "---":
                blocks.append(Block("frontmatter", "frontmatter", 0, lend(k), 1))
                i = k + 1
                break
    section = "body"
    section_level = 0
    para = None  # [start_line, end_line, kind]

    def flush():
        if para is not None:
            s, e, kind = para
            blocks.append(Block(kind, section, lstart(s), lend(e), s + 1))

    while i < n:
        line = lines[i]
        stripped = line.strip()
        if FENCE_RE.match(line):
            flush()
            para = None
            fence = FENCE_RE.match(line).group(1)
            k = i + 1
            while k < n and not lines[k].strip().startswith(fence):
                k += 1
            k = min(k, n - 1)
            blocks.append(Block("code", "code", lstart(i), lend(k), i + 1))
            i = k + 1
            continue
        if stripped.startswith("<!--"):
            flush()
            para = None
            k = i
            while k < n and "-->" not in lines[k]:
                k += 1
            k = min(k, n - 1)
            blocks.append(Block("comment", section, lstart(i), lend(k), i + 1))
            i = k + 1
            continue
        if not stripped or RULE_RE.match(line):
            flush()
            para = None
            i += 1
            continue
        hm = HEADING_RE.match(stripped)
        if hm:
            flush()
            para = None
            level = len(hm.group(1))
            htext = heading_text(stripped)
            if section != "body" and level <= section_level:
                section, section_level = "body", 0
            if section == "body":
                if FAQ_HEAD.match(htext):
                    section, section_level = "faq", level
                elif SOURCES_HEAD.match(htext):
                    section, section_level = "sources", level
                elif META_HEAD.match(htext):
                    section, section_level = "meta", level
            blocks.append(Block("heading", section, lstart(i), lend(i), i + 1, level))
            i += 1
            continue
        if stripped.startswith(">"):
            kind = "quote"
        elif stripped.startswith("|"):
            kind = "table"
        elif LIST_RE.match(line):
            kind = "list"
        else:
            kind = "paragraph"
        if META_LABEL.match(line):
            flush()
            para = None
            blocks.append(Block("paragraph", "meta", lstart(i), lend(i), i + 1))
            i += 1
            continue
        if kind == "list":
            flush()
            para = [i, i, "list"]
            i += 1
            continue
        if para is not None and (para[2] == kind or (para[2] == "list" and kind == "paragraph" and line.startswith((" ", "\t")))):
            para[1] = i
        else:
            flush()
            para = [i, i, kind]
        i += 1
    flush()
    for idx, b in enumerate(blocks):
        b.index = idx
    doc.blocks = blocks

    # masks
    for b in blocks:
        if b.kind in ("code", "frontmatter", "comment"):
            for p in range(b.start, b.end):
                doc.ignore[p] = 1
        if b.kind == "quote":
            for p in range(b.start, b.end):
                doc.quote[p] = 1
    for m in HTML_COMMENT_RE.finditer(text):
        for p in range(m.start(), m.end()):
            doc.ignore[p] = 1
    for m in INLINE_CODE_RE.finditer(text):
        for p in range(m.start(), m.end()):
            doc.ignore[p] = 1
    for m in LINK_TEXT_RE.finditer(text):
        for p in range(m.start(1), m.end(1)):
            doc.title[p] = 1
    for m in LINK_TARGET_RE.finditer(text):
        for p in range(m.start(1) - 1, m.end()):
            doc.url[p] = 1
    for m in URL_RE.finditer(text):
        for p in range(m.start(), m.end()):
            doc.url[p] = 1
    for m in QUOTE_SPANS.finditer(text):
        if not any(doc.ignore[m.start():m.end()]):
            for p in range(m.start(), m.end()):
                doc.quote[p] = 1
    doc.sentences = split_sentences(doc)
    return doc


# ---------------------------------------------------------------------------
# Sentences
# ---------------------------------------------------------------------------

_SPLIT = re.compile("([.!?…]+)([\"'“”«»)\\]*_]*)(\\s+)(?=[\"'„“»«(\\[*_]*[A-ZÀ-ÖØ-Þ0-9])")
_LIST_MARK = re.compile(r"^\s*(?:>\s*)?(?:[-*+•]|\d{1,3}[.)])\s+")


def _content_start(text, start, end, kind):
    seg = text[start:end]
    if kind == "heading":
        m = re.match(r"^\s*#{1,6}\s+", seg)
        return start + (m.end() if m else 0)
    if kind == "list":
        m = _LIST_MARK.match(seg)
        return start + (m.end() if m else 0)
    if kind == "quote":
        m = re.match(r"^\s*>\s*", seg)
        return start + (m.end() if m else 0)
    return start


def split_sentences(doc):
    out = []
    abbr = ABBREVIATIONS.get(doc.lang, ABBREVIATIONS["de"]) + ABBREVIATIONS["en" if doc.lang == "de" else "de"]
    text = doc.text
    for b in doc.blocks:
        if b.kind in ("code", "frontmatter", "comment", "table"):
            continue
        s = _content_start(text, b.start, b.end, b.kind)
        if b.kind == "heading":
            out.append(Sentence(s, b.end, b, text[s:b.end]))
            continue
        pos = s
        for m in _SPLIT.finditer(text, s, b.end):
            cut = m.end(2)
            raw_before = text[pos:m.start(1) + 1].strip()
            before = raw_before.lower()
            last_raw = raw_before.split()[-1] if raw_before.split() else ""
            if any(before.endswith(a) and (len(before) == len(a) or not before[-len(a) - 1].isalnum()) for a in abbr):
                continue
            if re.fullmatch(r"\(?\d{1,2}\.", last_raw) or re.fullmatch(r"[A-Za-zÄÖÜäöü]\.", last_raw):
                continue
            _add(out, text, pos, cut, b)
            pos = m.end(3)
        _add(out, text, pos, b.end, b)
    return out


def _add(out, text, start, end, block):
    seg = text[start:end]
    lead = len(seg) - len(seg.lstrip())
    seg_r = seg.rstrip()
    if not seg_r.strip():
        return
    st = start + lead
    en = start + len(seg_r)
    # quote markers inside a multi-line quote block
    out.append(Sentence(st, en, block, text[st:en]))


def tokens(text):
    return [m.group(0) for m in WORD_RE.finditer(text)]
