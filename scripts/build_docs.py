"""Generate docs/patterns.md (English) and docs/patterns.de.md (German).

The pattern files (slopcheck/patterns/*.json, or patterns/*.json) are the single source. This script reads
them and writes one Markdown page per language. Standard library only.

Accepted file shapes (one file per category is the convention):

  [ {pattern}, ... ]
  { "category": "...", "intro": "..." | {"en": "...", "de": "..."},
    "patterns": [ {pattern}, ... ] }

A file may carry a top-level "lang" ("de" or "en"); each page then lists the
patterns of its own language. A pattern has at least "id" and "name".
Optional: "category", "description", "bad", "better", "fix", "severity", "lang". Text fields are a string, a list of
strings, or a dict keyed by language ({"en": ..., "de": ...}). Fields with a
language suffix such as "name_de" are understood as well.

Usage:
  python scripts/build_docs.py                  write the docs
  python scripts/build_docs.py --check          exit 1 if the docs are stale
  python scripts/build_docs.py --patterns DIR   read patterns from DIR
  python scripts/build_docs.py --out DIR        write into DIR
"""

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORY_ORDER = ["substance", "facts", "phrases", "structure", "rhythm", "form"]

TEXT = {
    "en": {
        "file": "patterns.md",
        "other": ("Deutsche Fassung", "patterns.de.md"),
        "title": "Patterns",
        "generated": "This page is generated from `slopcheck/patterns/*.json` by `scripts/build_docs.py`. Edit the JSON files, not this page.",
        "intro": "Each pattern has an ID, a short name, a description and two examples. The better example never adds facts that the bad one does not have. Where a real detail is needed, it shows a placeholder in square brackets.",
        "contents": "Contents",
        "bad": "Bad",
        "better": "Better",
        "fix": "Fix",
        "severity": "Severity",
        "lang": "Language",
        "lang_names": {"de": "German", "en": "English"},
        "count": "{n} patterns",
        "count_one": "1 pattern",
        "categories": {
            "substance": ("Substance", "Passages that sound like content but carry none: vague attributions, sentences that would fit any article on any topic, advice without steps, smoothed-over specifics. These matter most."),
            "facts": ("Facts", "Numbers, studies and named people that need a source, and facts from your notes that went missing on the way into the text."),
            "phrases": ("Phrases", "Stock wording that shows up far more often in generated text than in edited writing. Strong single words are flagged on their own, weaker ones only in clusters."),
            "structure": ("Structure", "Recurring shapes: the setup and reveal, lists of three everywhere, headings that ask questions the paragraph never answers, a summary after every section."),
            "rhythm": ("Rhythm", "Measured on the whole text and compared with a range from human-written reference texts. Too even is a finding, and so is overshooting the other way."),
            "form": ("Form", "Typography and layout: long dashes used as a stylistic device, emoji bullets, bold words scattered through running text."),
        },
        "other_cat": ("Other", ""),
    },
    "de": {
        "file": "patterns.de.md",
        "other": ("English version", "patterns.md"),
        "title": "Muster",
        "generated": "Diese Seite wird von `scripts/build_docs.py` aus `slopcheck/patterns/*.json` erzeugt. Bitte die JSON-Dateien bearbeiten, nicht diese Seite.",
        "intro": "Jedes Muster hat eine ID, einen kurzen Namen, eine Beschreibung und zwei Beispiele. Das bessere Beispiel ergänzt nie Fakten, die im schlechten fehlen. Wo ein echtes Detail nötig ist, steht ein Platzhalter in eckigen Klammern.",
        "contents": "Inhalt",
        "bad": "Schlecht",
        "better": "Besser",
        "fix": "Vorschlag",
        "severity": "Stufe",
        "lang": "Sprache",
        "lang_names": {"de": "Deutsch", "en": "Englisch"},
        "count": "{n} Muster",
        "count_one": "1 Muster",
        "categories": {
            "substance": ("Substanz", "Stellen, die nach Inhalt klingen, aber keinen tragen: vage Zuschreibungen, Sätze, die in jeden Artikel zu jedem Thema passen, Rat ohne Schritte, glattgebügelte Einzelheiten. Diese Kategorie zählt am meisten."),
            "facts": ("Fakten", "Zahlen, Studien und genannte Personen, die einen Beleg brauchen, und Fakten aus deinen Notizen, die auf dem Weg in den Text verloren gingen."),
            "phrases": ("Phrasen", "Formulierungen, die in generiertem Text deutlich häufiger vorkommen als in redigierten Texten. Starke Einzelwörter werden allein markiert, schwächere nur gehäuft."),
            "structure": ("Struktur", "Wiederkehrende Formen: Aufbau und Auflösung, Dreierlisten überall, Zwischenüberschriften als Frage ohne Antwort im Absatz, eine Zusammenfassung nach jedem Abschnitt."),
            "rhythm": ("Rhythmus", "Gemessen über den ganzen Text und verglichen mit dem Bereich menschlich geschriebener Vergleichstexte. Zu gleichförmig ist ein Befund, übers Ziel hinaus auch."),
            "form": ("Form", "Typografie und Layout: lange Gedankenstriche als Stilmittel, Emoji-Aufzählungen, fett gesetzte Wörter mitten im Fließtext."),
        },
        "other_cat": ("Sonstige", ""),
    },
}


def pick(entry, field, lang):
    """Return a field in the wanted language, falling back to any language."""
    suffixed = entry.get("{}_{}".format(field, lang))
    if suffixed not in (None, "", []):
        return suffixed
    value = entry.get(field)
    if isinstance(value, dict):
        for key in (lang, "en", "de"):
            if value.get(key) not in (None, "", []):
                return value[key]
        for v in value.values():
            if v not in (None, "", []):
                return v
        return None
    if value in (None, "", []):
        other = "de" if lang == "en" else "en"
        return entry.get("{}_{}".format(field, other))
    return value


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v not in (None, "")]
    return [str(value)]


def load_patterns(pattern_dir):
    """Read all pattern files. Returns (patterns, intros by category)."""
    files = sorted(glob.glob(os.path.join(pattern_dir, "**", "*.json"), recursive=True))
    patterns, intros = [], {}
    for path in files:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        base = os.path.splitext(os.path.basename(path))[0]
        parent = os.path.basename(os.path.dirname(path))
        file_lang = parent if parent in ("de", "en") else None
        file_cat = base if base in CATEGORY_ORDER else None
        if isinstance(data, dict):
            file_cat = data.get("category") or file_cat
            file_lang = data.get("lang") or file_lang
            if file_cat and data.get("intro"):
                intros[file_cat] = data.get("intro")
            entries = data.get("patterns") or data.get("items") or []
        elif isinstance(data, list):
            entries = data
        else:
            entries = []
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get("id"):
                continue
            item = dict(entry)
            item.setdefault("category", file_cat or "other")
            if file_lang:
                item["_file_lang"] = file_lang
            patterns.append(item)
    return patterns, intros


def md_escape_inline(text):
    return str(text).replace("\r", "").strip()


def quote_block(text):
    lines = md_escape_inline(text).split("\n")
    return "\n".join("> " + line if line else ">" for line in lines)


def anchor(text):
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -":
            out.append("-")
    return "".join(out).strip("-")


def render(patterns, intros, lang):
    T = TEXT[lang]
    # Per-language catalogues (de.json, en.json): each page shows its own.
    own = [p for p in patterns if p.get("_file_lang") in (None, lang)]
    if own:
        patterns = own
    by_cat = {}
    for p in patterns:
        by_cat.setdefault(p.get("category") or "other", []).append(p)
    order = [c for c in CATEGORY_ORDER if c in by_cat] + sorted(c for c in by_cat if c not in CATEGORY_ORDER)

    lines = [
        "# {}".format(T["title"]),
        "",
        "[{}]({})".format(*T["other"]),
        "",
        "<!-- {} -->".format(T["generated"]),
        "",
        T["intro"],
        "",
    ]
    if order:
        lines += ["## {}".format(T["contents"]), ""]
        for cat in order:
            name = T["categories"].get(cat, (cat.capitalize(), ""))[0]
            n = len(by_cat[cat])
            count = T["count_one"] if n == 1 else T["count"].format(n=n)
            lines.append("- [{}](#{}) ({})".format(name, anchor(name), count))
        lines.append("")

    for cat in order:
        name, default_intro = T["categories"].get(cat, (cat.capitalize(), ""))
        intro = intros.get(cat)
        if isinstance(intro, dict):
            intro = intro.get(lang) or default_intro
        intro = intro or default_intro
        lines += ["## {}".format(name), ""]
        if intro:
            lines += [md_escape_inline(intro), ""]
        for p in sorted(by_cat[cat], key=lambda x: str(x.get("id"))):
            title = md_escape_inline(pick(p, "name", lang) or "")
            lines += ["### {} {}".format(md_escape_inline(p.get("id")), title).rstrip(), ""]
            meta = []
            if p.get("severity"):
                meta.append("{}: `{}`".format(T["severity"], md_escape_inline(p.get("severity"))))
            plang = p.get("lang")
            if isinstance(plang, str) and plang in T["lang_names"]:
                meta.append("{}: {}".format(T["lang"], T["lang_names"][plang]))
            elif isinstance(plang, list):
                meta.append("{}: {}".format(T["lang"], ", ".join(T["lang_names"].get(x, x) for x in plang)))
            if meta:
                lines += [" / ".join(meta), ""]
            desc = pick(p, "description", lang)
            if desc:
                lines += [md_escape_inline(desc), ""]
            for key in ("bad", "better"):
                for example in as_list(pick(p, key, lang)):
                    lines += ["**{}:**".format(T[key]), "", quote_block(example), ""]
            fix = pick(p, "fix", lang)
            if fix:
                lines += ["**{}:** {}".format(T["fix"], md_escape_inline(fix)), ""]
    return "\n".join(lines).rstrip() + "\n"


def default_pattern_dir():
    """patterns/ in the repo root, or inside the package if it lives there."""
    for candidate in (os.path.join(ROOT, "slopcheck", "patterns"), os.path.join(ROOT, "patterns")):
        if glob.glob(os.path.join(candidate, "**", "*.json"), recursive=True):
            return candidate
    return os.path.join(ROOT, "slopcheck", "patterns")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate the pattern docs from patterns/*.json.")
    parser.add_argument("--check", action="store_true", help="exit 1 if the generated docs differ from the files")
    parser.add_argument("--patterns", default=default_pattern_dir(), help="pattern directory")
    parser.add_argument("--out", default=os.path.join(ROOT, "docs"), help="output directory")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.patterns):
        print("no pattern directory at {}".format(args.patterns), file=sys.stderr)
        return 1
    patterns, intros = load_patterns(args.patterns)
    if not patterns:
        print("no patterns found in {}".format(args.patterns), file=sys.stderr)
        return 1

    stale = []
    for lang in ("en", "de"):
        content = render(patterns, intros, lang)
        path = os.path.join(args.out, TEXT[lang]["file"])
        if args.check:
            current = None
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as fh:
                    current = fh.read()
            if current != content:
                stale.append(os.path.relpath(path, ROOT))
        else:
            os.makedirs(args.out, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(content)
            print("wrote {} ({} patterns)".format(os.path.relpath(path, ROOT), len(patterns)))
    if stale:
        print("out of date: {}. Run: python scripts/build_docs.py".format(", ".join(stale)), file=sys.stderr)
        return 1
    if args.check:
        print("docs are up to date ({} patterns)".format(len(patterns)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
