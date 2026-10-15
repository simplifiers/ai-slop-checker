"""Named people quoted or paraphrased in a sentence."""

import re

NAME = {
    "de": r"[A-ZÄÖÜ][a-zäöüß]+(?:-[A-ZÄÖÜ][a-zäöüß]+)?",
    "en": r"[A-Z][a-z]+(?:[-'][A-Z]?[a-z]+)?",
}
TITLE = {
    "de": r"(?:(?:Prof\.|Dr\.|Dipl\.-[\w]+\.?|Herr|Frau)\s+)*",
    "en": r"(?:(?:Prof\.|Dr\.|Mr\.|Mrs\.|Ms\.)\s+)*",
}
_CACHE = {}


def _patterns(lang, lex):
    if lang in _CACHE:
        return _CACHE[lang]
    N, T = NAME[lang], TITLE[lang]
    sv, role = lex["speech_verbs"], lex["roles"]
    pair = T + r"(?P<vn>" + N + r")\s+(?P<nn>" + N + r")"
    plain = [
        r"(?:(?<=\s)|^|(?<=[(\"„“]))" + pair + r"\s*,?\s+" + sv + r"\b",
        r"\b" + sv + r"\s+(?:der\s+|die\s+|the\s+)?(?:" + role + r"\s+)?" + pair + r"\b",
        r"\b(?:[Ll]aut|[Ww]ie|[Ss]o|[Aa]ccording to|[Aa]s)\s+(?:der\s+|die\s+|dem\s+|the\s+)?" + role + r",?\s+" + pair + r"\b",
        r"\b" + role + r",?\s+" + pair + r"\b",
        r"(?:(?<=\s)|^)" + pair + r",\s+(?:\w+\s+){0,3}" + role + r"(?:\s+\w+){0,4},\s+" + sv + r"\b",
        r"\b(?:[Ll]aut|[Aa]ccording to)\s+" + pair + r"\b(?!\s+[A-ZÄÖÜ])",
        r"\b(?:Herr|Frau|Dr\.|Prof\.)\s+(?P<vn>" + N + r")\s+(?P<nn>" + N + r")\b",
    ]
    linked = [
        r"\[\s*" + pair + r"\s*\]\(\s*https?://[^)]*\)",
    ]
    out = ([re.compile(p) for p in plain], [re.compile(p) for p in linked])
    _CACHE[lang] = out
    return out


def find_people(text, start, end, lang, lex):
    """Return [(name, abs_start, abs_end, linked)] for people named in text[start:end]."""
    plain, linked = _patterns(lang, lex)
    stop = set(lex["name_stop"])
    inst = re.compile(lex["institution_suffix"], re.I)
    seg = text[start:end]
    found = []
    seen = set()
    for rx in linked:
        for m in rx.finditer(seg):
            vn, nn = m.group("vn"), m.group("nn")
            if vn in stop or nn in stop:
                continue
            name = vn + " " + nn
            if name not in seen:
                seen.add(name)
                found.append((name, start + m.start("vn"), start + m.end("nn"), True))
    for rx in plain:
        pos = 0
        while True:
            m = rx.search(seg, pos)
            if not m:
                break
            vn, nn = m.group("vn"), m.group("nn")
            before = seg[:m.start("vn")]
            article = re.search(r"\b(?:der|die|das|dem|den|des|the|a|an)\s*\[?\s*$", before, re.I) and not re.search(
                r"\b(?:[Ee]xpert\w*|CEO|[Gg]ründer\w*|[Pp]rofessor\w*|[Aa]utor\w*|[Bb]erater\w*|[Cc]oach|Herr|Frau|Dr\.|Prof\.)\s*$", before)
            if vn in stop or nn in stop or inst.search(vn) or inst.search(nn) or article:
                pos = m.start() + 1
                continue
            name = vn + " " + nn
            if name not in seen:
                seen.add(name)
                found.append((name, start + m.start("vn"), start + m.end("nn"), False))
            pos = m.end()
    return found
