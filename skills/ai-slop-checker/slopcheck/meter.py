"""Measured style features, computed exactly like the calibration corpus.

The rhythm bands in ``bands/`` were measured with these definitions. Changing a
definition here without measuring the bands again makes the comparison wrong.

Input is a list of blocks (kind, text) with kind "p" (paragraph) or "li" (one list
item). Only running prose goes in: no headings, quotes, code, tables, FAQ or author
boxes. Rates are per 1,000 prose words. Below MIN_WORDS prose words nothing is measured.
Standard library only.
"""

import math
import re

MIN_WORDS = 300

FEATURES = (
    "mean_sentence_len", "cv_sentence_len_para", "words_per_paragraph", "mattr50",
    "mean_word_len", "nominalizations_1k", "triads_1k", "colons_1k", "participle_tail_1k",
)

_WORD = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*|\d+(?:[.,:/]\d+)*%?", re.U)
_ALPHA = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.U)

_ABBREV = {
    "de": {
        "z", "b", "d", "h", "u", "a", "s", "o", "ca", "dr", "prof", "nr", "bzw", "usw",
        "etc", "vgl", "ggf", "inkl", "evtl", "abs", "art", "bspw", "sog", "zzgl", "max",
        "min", "mio", "mrd", "jh", "jhd", "str", "tel", "hr", "fr", "dipl", "ing", "bzgl",
        "gem", "lt", "mind", "rd", "v", "chr", "st", "okt", "nov", "dez", "jan", "feb",
        "aug", "sept", "sep", "allg", "ebd", "u.a", "i.d.r", "z.b", "d.h", "o.ä",
    },
    "en": {
        "e", "g", "i", "mr", "mrs", "ms", "dr", "prof", "inc", "ltd", "co", "corp", "vs",
        "etc", "no", "st", "jr", "sr", "jan", "feb", "mar", "apr", "aug", "sep", "sept",
        "oct", "nov", "dec", "fig", "approx", "dept", "est", "u.s", "e.g", "i.e", "u.k",
    },
}

_SENT_END = re.compile("([.!?…]+)([\"'”“»«)\\]]*)(\\s+)(?=[\"'„“»«(\\[]?[A-ZÄÖÜ0-9])")

_NOMINAL = {
    "de": re.compile(r"^[A-ZÄÖÜ][\w\-]{2,}(ung|ungen|heit|heiten|keit|keiten|tion|tionen|ität|itäten|schaft|schaften|ismus|ismen)$"),
    "en": re.compile(r"^[a-z][a-z\-]{3,}(tion|tions|sion|sions|ment|ments|ness|nesses|ity|ities)$"),
}
_NOMINAL_STOP_EN = {"moment", "moments", "comment", "comments", "city", "cities", "ment",
                    "element", "elements", "segment", "segments", "cement", "pity", "garment",
                    "fragment", "fragments", "unity", "nation", "nations", "station", "stations",
                    "lotion", "potion", "ration", "mansion", "pension", "pensions", "version",
                    "versions", "witness", "business", "businesses", "question", "questions",
                    "mention", "mentions", "section", "sections", "option", "options"}
_TRIAD = {
    "de": re.compile(r"\b[^\W\d_][\w\-]*(?: [\w\-]+){0,2}, [^\W\d_][\w\-]*(?: [\w\-]+){0,2},? (und|oder|sowie) [^\W\d_][\w\-]*", re.U),
    "en": re.compile(r"\b[^\W\d_][\w\-]*(?: [\w\-]+){0,2}, [^\W\d_][\w\-]*(?: [\w\-]+){0,2},? (and|or) [^\W\d_][\w\-]*", re.U),
}
_TAIL = {
    "de": re.compile(r",\s+(um\b[^,.;:!?]{2,80}\bzu\s+\w+|wodurch\b|womit\b|was\s+(?:\w+\s+){0,4}(ermöglicht|sorgt|führt|beiträgt|erleichtert|unterstützt|verbessert)\b)", re.I),
    "en": re.compile(r",\s+(?!including\b|according\b)([a-z]+ing)\b", re.I),
}


def md_inline(s):
    """Strip inline Markdown (images, links, bold, italics, code ticks)."""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)
    s = re.sub(r"(?<!\w)[*_](.+?)[*_](?!\w)", r"\1", s)
    s = s.replace("`", "")
    return s.strip()


def split_sentences(text, lang):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    abbrev = _ABBREV[lang]
    out = []
    start = 0
    for m in _SENT_END.finditer(text):
        end = m.end(2)
        before = text[start:m.start(1)]
        last = before.split(" ")[-1].lower().strip("(\"'") if before else ""
        if m.group(1) == ".":
            if last.rstrip(".") in abbrev or (len(last) == 1 and last.isalpha()):
                continue
            if re.fullmatch(r"\d{1,3}", last) and lang == "de":
                continue  # German ordinal: "am 3. Mai"
            if re.fullmatch(r"(?:[a-zäöü]\.)+[a-zäöü]", last):
                continue
        out.append(text[start:end].strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return [s for s in out if _WORD.search(s)]


def words(text):
    return _WORD.findall(text)


def mattr(tokens, window=50):
    if len(tokens) < window:
        return None
    counts = {}
    for t in tokens[:window]:
        counts[t] = counts.get(t, 0) + 1
    acc = len(counts)
    n = 1
    for i in range(window, len(tokens)):
        out_t, in_t = tokens[i - window], tokens[i]
        counts[out_t] -= 1
        if counts[out_t] == 0:
            del counts[out_t]
        counts[in_t] = counts.get(in_t, 0) + 1
        acc += len(counts)
        n += 1
    return acc / float(n) / window


def _mean(values):
    return sum(values) / float(len(values))


def _cv(values):
    if len(values) < 3:
        return None
    m = _mean(values)
    if not m:
        return None
    return math.sqrt(sum((v - m) ** 2 for v in values) / float(len(values))) / m


def extract(blocks, lang):
    """Return {feature: value or None, "_words": n} or None below MIN_WORDS prose words."""
    prose = [(k, t) for k, t in blocks if k in ("p", "li") and t.strip()]
    sentences = []
    para_sent_lens = []
    para_lens = []
    tokens = []
    for kind, text in prose:
        sents = split_sentences(text, lang)
        sentences.extend(sents)
        w = words(text)
        tokens.extend(w)
        if kind == "p":
            para_lens.append(len(w))
            para_sent_lens.extend(x for x in (len(words(s)) for s in sents) if x > 0)
    n = len(tokens)
    if n < MIN_WORDS or not sentences:
        return None
    per_k = 1000.0 / n
    sent_lens = [x for x in (len(words(s)) for s in sentences) if x > 0]
    alpha = [t for t in tokens if _ALPHA.fullmatch(t)]
    lower = [a.lower() for a in alpha]

    f = {}
    f["mean_sentence_len"] = _mean(sent_lens) if sent_lens else None
    f["cv_sentence_len_para"] = _cv(para_sent_lens) if len(para_sent_lens) >= 10 else None
    f["words_per_paragraph"] = _mean(para_lens) if para_lens else None
    f["mattr50"] = mattr(lower)
    f["mean_word_len"] = _mean([len(a) for a in alpha]) if alpha else None
    if lang == "de":
        nom = sum(1 for a in alpha if _NOMINAL["de"].match(a))
    else:
        nom = sum(1 for a in lower if _NOMINAL["en"].match(a) and a not in _NOMINAL_STOP_EN)
    f["nominalizations_1k"] = nom * per_k
    f["triads_1k"] = sum(len(_TRIAD[lang].findall(s)) for s in sentences) * per_k
    f["participle_tail_1k"] = sum(len(_TAIL[lang].findall(s)) for s in sentences) * per_k
    prose_text = " ".join(t for _, t in prose)
    f["colons_1k"] = len(re.findall(r":(?!\d|//)", prose_text)) * per_k
    out = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in f.items()}
    out["_words"] = n
    return out
