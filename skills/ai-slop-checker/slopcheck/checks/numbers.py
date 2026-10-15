"""Numbers: claims, technical exclusions and normalisation (shared by substance and facts)."""

import re

NUM = r"\d+(?:[.,]\d+)?"

_CMP = {
    "de": r"(?:so|mehr|häufiger|öfter|höher|schneller|größer|weniger|besser|teurer|günstiger|länger|kürzer|wahrscheinlicher|viele|viel)",
    "en": r"(?:more|as|faster|higher|larger|bigger|better|likelier|likely|cheaper|longer|shorter|fewer|less|greater|lower|often|quicker|slower|many|much)",
}
_ZW = {
    "de": "zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|fünfzehn|zwanzig|dreißig|vierzig|fünfzig|sechzig|siebzig|achtzig|neunzig|hundert",
    "en": "two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|fifteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred",
}

_CACHE = {}


def claim_patterns(lang):
    if lang in _CACHE:
        return _CACHE[lang]
    cmp_ = _CMP[lang]
    zw = r"(?:" + _ZW[lang] + r")"
    if lang == "de":
        digit = [
            NUM + r"\s?(?:%|prozent\b|prozentpunkte\b)",
            NUM + r"\s?(?:mio\.?|millionen|milliarden|mrd\.?|tausend|tsd\.?)(?!\w)",
            r"\d[\d.,]*\s?(?:€|euro\b|eur\b|\$|dollar\b|chf\b|franken\b)",
            r"(?:€|\$)\s?\d[\d.,]*",
            r"\b" + NUM + r"\s?(?:x|-mal|mal)\s+(?:\w+\s+){0,2}?" + cmp_ + r"\b",
            r"(?<!schritt )(?<!teil )(?<!kapitel )(?<!frage )(?<!seite )(?<!folge )(?<!punkt )\b\d+\s+von\s+\d+\b",
            r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b",
            r"\b\d{5,}\b",
        ]
        words = [
            r"\b" + zw + r"\s+prozent\b",
            r"\b(?:ein|eine|einen|" + _ZW[lang] + r")\s+(?:drittel|viertel|fünftel|zehntel)\b",
            r"\b(?:die|zur|um die|über die|fast die|knapp die|gut die|mehr als die|weniger als die)\s+hälfte\s+"
            r"(?:der|aller|von|unserer|ihrer|deiner|meiner|seiner|eurer)\b",
            r"\bhalb so viele\b",
            r"\bjede[rsnm]?\s+(?:zweite|dritte|vierte|fünfte|sechste|siebte|achte|zehnte)[nrsm]?\b",
            r"\b(?:doppelt|dreimal|viermal|fünfmal|zehnmal|" + zw + r"\s?mal)\s+(?:\w+\s+){0,2}?" + cmp_ + r"\b",
            r"\b(?:die )?mehrheit (?:der|aller)\b",
            r"\b(?:um|auf) das (?:doppelte|dreifache|vierfache|fünffache|zehnfache|hundertfache)\b",
            r"\b(?:verdoppelt|verdreifacht|vervierfacht|verzehnfacht)\w*",
        ]
    else:
        digit = [
            NUM + r"\s?(?:%|percent\b|per cent\b|percentage points\b)",
            NUM + r"\s?(?:million|millions|billion|billions|bn|thousand)\b",
            r"\b\d+(?:\.\d+)?k\b",
            r"\d[\d.,]*\s?(?:€|\$|£|usd\b|eur\b|gbp\b|dollars?\b|euros?\b|pounds?\b)",
            r"(?:€|\$|£)\s?\d[\d,]*(?:\.\d+)?",
            r"\b" + NUM + r"\s?(?:x|times)\s+(?:\w+\s+){0,2}?" + cmp_ + r"\b",
            r"(?<!step )(?<!part )(?<!chapter )(?<!question )(?<!page )(?<!episode )(?<!day )(?<!week )(?<!point )"
            r"\b\d+\s+(?:of|out of)\s+\d+\b",
            r"\b\d+\s+in\s+\d{1,3}\b(?![\d,])",
            r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b",
            r"\b\d{5,}\b",
        ]
        words = [
            r"\b" + zw + r"\s+(?:percent|per cent)\b",
            r"\b(?:one|a|" + _ZW[lang] + r")[\s-]+(?:third|thirds|quarter|quarters|fifth|fifths|tenth|tenths)\s+of\b",
            r"\b(?:more than |less than |nearly |almost |over |about |roughly |around )?half of (?:the|all|our|your|their|those|these)\b",
            r"\b(?:one|" + _ZW[lang] + r")\s+in\s+(?:" + _ZW[lang] + r"|\d+)\b",
            r"\bevery (?:third|fourth|fifth|sixth|seventh|eighth|tenth)\b",
            r"\b(?:twice|" + zw + r"\s+times)\s+(?:\w+\s+){0,2}?" + cmp_ + r"\b",
            r"\bthe majority of\b",
            r"\b(?:doubled|tripled|quadrupled|tenfold|threefold|fourfold|twofold)\b",
        ]
    pats = [re.compile(p, re.I) for p in digit + words]
    _CACHE[lang] = pats
    return pats


def technical_patterns(lang, units):
    """Spans that look like numbers but are not claims: measurements, versions, times, dates, laws."""
    key = ("tech", lang)
    if key in _CACHE:
        return _CACHE[key]
    pats = [
        NUM + r"\s?[x×]\s?" + NUM + r"(?:\s?[x×]\s?" + NUM + r")?(?:\s?" + units + r"\b)?",  # 1920 x 1080 px
        r"\b(?:version|v\.?|release|update|ios|android|windows|php|python|node|gpt-?|iso|din|en|rfc|cve-)\s?\d+(?:[.-]\d+)*\b",
        r"\b\d+\.\d+\.\d+(?:\.\d+)*\b",                             # 1.2.3
        r"\b\d{1,2}[:.]\d{2}\s?(?:uhr|h|am|pm|a\.m\.|p\.m\.)(?!\w)|\b\d{1,2}:\d{2}(?::\d{2})?\b|\b\d{1,2}\s?(?:uhr|am|pm)\b",
        r"§§?\s*\d+[a-z]?(?:\s*(?:abs\.|absatz)\s*\d+)?(?:\s*(?:satz|nr\.|s\.)\s*\d+)?(?:\s*[a-zäöü]{2,}\b)?",
        r"\b(?:art\.|artikel|article|section|sec\.|kap\.|kapitel|chapter|rule|regel|step|schritt|teil|part|page|seite|s\.)\s*\d+[a-z]?\b",
        r"\b\d{1,2}\.\s?\d{1,2}\.\s?(?:\d{2,4})?\b",                 # 12.03.2026
        r"\b\d{4}-\d{2}-\d{2}\b",                                    # ISO date
        r"(?<![\d.,])" + NUM + r"(?:\s?(?:[\u2013-]|bis|to)\s?" + NUM + r")?\s?" + units + r"(?![\w%])",  # 5 km, 10-20 kg
        r"\b(?:plz|zip)\s?\d{4,5}\b|\b\d{5}\s+(?=[A-ZÄÖÜ][a-zäöü])",   # postcode before a town
        r"\+\d[\d ()/-]{6,}\d",                                       # phone numbers
        r"\bisbn[\s:-]*[\d-]{9,}\b",
    ]
    out = [re.compile(p, re.I if i != 9 else 0) for i, p in enumerate(pats)]
    _CACHE[key] = out
    return out


def blank_technical(s, lang, units):
    for rx in technical_patterns(lang, units):
        s = rx.sub(lambda m: " " * len(m.group(0)), s)
    return s


def find_claims(segment, lang, units):
    """Return list of (start, end) claim spans relative to ``segment``."""
    s = blank_technical(segment, lang, units)
    s = re.sub(r"^(\s*(?:[-*+]|\d{1,3}[.)]))\s+", lambda m: " " * len(m.group(0)), s)  # list number
    spans = []
    for rx in claim_patterns(lang):
        for m in rx.finditer(s):
            if not m.group(0).strip():
                continue
            spans.append((m.start(), m.end()))
    spans.sort()
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


NUM_TOKEN = re.compile(r"\d{1,3}(?:[.,  ]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?")


def norm_number(token, lang):
    t = token.strip().replace(" ", "").replace(" ", "")
    if lang == "en":
        if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", t):
            t = t.replace(",", "")
        t = t.replace(",", ".")
    else:
        if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", t):
            t = t.replace(".", "")
        t = t.replace(",", ".")
    if re.fullmatch(r"\d+\.0+", t):
        t = t.split(".")[0]
    if re.fullmatch(r"\d+", t):
        t = str(int(t))
    return t


def numbers_in(s, lang, number_words=None):
    vals = set()
    for m in NUM_TOKEN.finditer(s):
        vals.add(norm_number(m.group(0), lang))
    if number_words:
        for m in re.finditer(r"[A-Za-zÄÖÜäöüß]+", s):
            w = m.group(0).lower()
            if w in number_words and w not in ("ein", "eine", "einen", "eins", "one"):
                vals.add(str(number_words[w]))
    return vals
