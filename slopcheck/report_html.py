"""Render an AI Slop Checker (slop-check) result as one self-contained HTML file.

The report has no external resources: CSS lives in a <style> block, there is
no JavaScript, no web font and no tracking. Everything that comes from the
checked text or from the result dict is escaped before it is written.

Public API: render_html(result: dict) -> str
"""

from html import escape

__all__ = ["render_html"]

CATEGORY_ORDER = ["substance", "facts", "phrases", "structure", "rhythm", "form"]

# Categories that are drawn as highlights inside the text. Rhythm is a
# property of the whole text and is shown as a table instead.
INLINE_CATEGORIES = {"substance", "facts", "form", "phrases", "structure"}

# When two findings overlap, the stronger category decides the colour.
CATEGORY_PRIORITY = {"substance": 0, "facts": 1, "form": 2, "phrases": 3, "structure": 4}

SEVERITY_ORDER = {"fail": 0, "tell": 1, "hint": 2}

LABELS = {
    "en": {
        "title": "AI Slop Checker report",
        "verdict": {"pass": "Pass", "revise": "Revise", "too_short": "Too short"},
        "verdict_hint": {
            "pass": "No blocking findings.",
            "revise": "Some findings should be fixed before publishing.",
            "too_short": "The text is too short for a reliable check.",
        },
        "words": "words",
        "lang_name": {"de": "German", "en": "English"},
        "register": "Register",
        "categories": {
            "substance": "Substance",
            "facts": "Facts",
            "phrases": "Stock phrases",
            "structure": "Structure",
            "rhythm": "Rhythm",
            "form": "Form",
        },
        "severity": {"fail": "fail", "tell": "tell", "hint": "hint"},
        "severity_long": {
            "fail": "Fail: fix this before publishing",
            "tell": "Tell: typical of generated text",
            "hint": "Hint: worth a second look",
        },
        "summary": "Findings by category",
        "none": "none",
        "text": "The text",
        "text_note": "Marked passages link to the matching note. Rhythm is measured on the whole text and shown further down.",
        "findings": "Notes",
        "no_findings": "No findings.",
        "line": "line",
        "fix": "Fix",
        "no_position": "Applies to the whole text",
        "people": "People to verify",
        "people_note": "Every named person should exist and have said what the text claims. The tool does not check this for you.",
        "sourced": "in your source",
        "unsourced": "not in your source",
        "facts_title": "Fact check against your source",
        "lost": "In the source, missing in the text",
        "added": "New in the text",
        "added_note": "Numbers and claims without a match in the source need a reference or should go.",
        "no_lost": "Nothing from the source went missing.",
        "no_added": "No new numbers or claims.",
        "rhythm_title": "Rhythm",
        "rhythm_note": "Each bar shows the range of human news texts (Wikinews, 10th to 90th percentile). The dot is this text. One value outside the range is common in human texts; only many values on the generated side at once count for the verdict.",
        "feature": "Measure",
        "value": "Value",
        "band": "Human range",
        "state": "State",
        "state_names": {"ok": "in range", "ai_side": "on the generated side", "overshot": "overshot"},
        "provisional": "provisional",
        "metrics": "Measurements",
        "metric_names": {
            "concreteness_per_100": "Concrete details per 100 words",
            "prose_words": "Words of running text",
            "mean_sentence_len": "Words per sentence",
            "cv_sentence_len_para": "Spread of sentence lengths",
            "words_per_paragraph": "Words per paragraph",
            "mattr50": "Vocabulary variety (MATTR 50)",
            "mean_word_len": "Letters per word",
            "nominalizations_1k": "Nominalisations per 1,000 words",
            "triads_1k": "Lists of three per 1,000 words",
            "colons_1k": "Colons per 1,000 words",
            "participle_tail_1k": "Trailing participles per 1,000 words",
            "ai_side_count": "Measures on the generated side",
            "ai_side_limit": "Limit for revise",
        },
        "disclaimer": "slop-check flags patterns, it does not prove who or what wrote a text. A clean report does not make a text good, and a finding is a prompt to look again, not a verdict.",
        "skip": "Skip to the text",
        "source": "Source",
    },
    "de": {
        "title": "AI Slop Checker Bericht",
        "verdict": {"pass": "Bestanden", "revise": "Überarbeiten", "too_short": "Zu kurz"},
        "verdict_hint": {
            "pass": "Keine Befunde, die eine Veröffentlichung aufhalten.",
            "revise": "Einige Befunde sollten vor der Veröffentlichung behoben werden.",
            "too_short": "Der Text ist für eine verlässliche Prüfung zu kurz.",
        },
        "words": "Wörter",
        "lang_name": {"de": "Deutsch", "en": "Englisch"},
        "register": "Textsorte",
        "categories": {
            "substance": "Substanz",
            "facts": "Fakten",
            "phrases": "Floskeln",
            "structure": "Struktur",
            "rhythm": "Rhythmus",
            "form": "Form",
        },
        "severity": {"fail": "Fehler", "tell": "Auffällig", "hint": "Hinweis"},
        "severity_long": {
            "fail": "Fehler: vor der Veröffentlichung beheben",
            "tell": "Auffällig: typisch für generierten Text",
            "hint": "Hinweis: ein zweiter Blick lohnt sich",
        },
        "summary": "Befunde nach Kategorie",
        "none": "keine",
        "text": "Der Text",
        "text_note": "Markierte Stellen führen zur passenden Anmerkung. Rhythmus wird über den ganzen Text gemessen und steht weiter unten.",
        "findings": "Anmerkungen",
        "no_findings": "Keine Befunde.",
        "line": "Zeile",
        "fix": "Tipp",
        "no_position": "Betrifft den ganzen Text",
        "people": "Genannte Personen prüfen",
        "people_note": "Jede genannte Person sollte existieren und gesagt haben, was der Text behauptet. Das prüft das Werkzeug nicht für dich.",
        "sourced": "in deiner Quelle",
        "unsourced": "nicht in deiner Quelle",
        "facts_title": "Fakten-Abgleich mit deiner Quelle",
        "lost": "In der Quelle, fehlt im Text",
        "added": "Neu im Text",
        "added_note": "Zahlen und Aussagen ohne Gegenstück in der Quelle brauchen einen Beleg oder fliegen raus.",
        "no_lost": "Aus der Quelle ist nichts verloren gegangen.",
        "no_added": "Keine neuen Zahlen oder Aussagen.",
        "rhythm_title": "Rhythmus",
        "rhythm_note": "Jeder Balken zeigt den Bereich menschlicher Nachrichtentexte (Wikinews, 10. bis 90. Perzentil). Der Punkt ist dieser Text. Ein Wert außerhalb kommt bei Menschen oft vor; erst viele Werte gleichzeitig auf der generierten Seite zählen für das Urteil.",
        "feature": "Messwert",
        "value": "Wert",
        "band": "Menschlicher Bereich",
        "state": "Lage",
        "state_names": {"ok": "im Bereich", "ai_side": "auf der generierten Seite", "overshot": "übers Ziel hinaus"},
        "provisional": "vorläufig",
        "metrics": "Kennzahlen",
        "metric_names": {
            "concreteness_per_100": "Konkrete Details je 100 Wörter",
            "prose_words": "Wörter Fließtext",
            "mean_sentence_len": "Wörter je Satz",
            "cv_sentence_len_para": "Streuung der Satzlängen",
            "words_per_paragraph": "Wörter je Absatz",
            "mattr50": "Wortvielfalt (MATTR 50)",
            "mean_word_len": "Buchstaben je Wort",
            "nominalizations_1k": "Nominalisierungen je 1.000 Wörter",
            "triads_1k": "Dreierlisten je 1.000 Wörter",
            "colons_1k": "Doppelpunkte je 1.000 Wörter",
            "participle_tail_1k": "Partizip-Anhängsel je 1.000 Wörter",
            "ai_side_count": "Messwerte auf der generierten Seite",
            "ai_side_limit": "Grenze für Überarbeiten",
        },
        "disclaimer": "slop-check zeigt Muster, es beweist nicht, wer oder was einen Text geschrieben hat. Ein Bericht ohne Befunde macht einen Text nicht gut, und ein Befund ist ein Anlass zum Hinsehen, kein Urteil.",
        "skip": "Zum Text springen",
        "source": "Quelle",
    },
}

CSS = """
:root {
  color-scheme: light dark;
  --paper: #ffffff;
  --canvas: #f6f5fa;
  --ink: #1c1a24;
  --muted: #5d5970;
  --rule: #e4e1ee;
  --accent: #7c3aed;
  --accent-soft: #f1eafe;
  --pass: #15803d;
  --pass-soft: #e8f6ed;
  --revise: #b42318;
  --revise-soft: #fdecea;
  --short: #5d5970;
  --short-soft: #efedf5;
  --substance: #c81e1e;
  --substance-bg: #fde3e1;
  --facts: #1d5fc9;
  --facts-bg: #e2ecfd;
  --form: #c2560c;
  --form-bg: #fde9d6;
  --phrases: #8a6a00;
  --phrases-bg: #fdf3c4;
  --structure: #6d28d9;
  --structure-bg: #ece3fd;
  --focus: #7c3aed;
  --serif: "Iowan Old Style", "Charter", "Bitstream Charter", "Sitka Text", Cambria, Georgia, serif;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #1b1924;
    --canvas: #121019;
    --ink: #ece9f5;
    --muted: #aaa4bf;
    --rule: #34304a;
    --accent: #a78bfa;
    --accent-soft: #2a2240;
    --pass: #4ade80;
    --pass-soft: #13291c;
    --revise: #f87171;
    --revise-soft: #3a1616;
    --short: #aaa4bf;
    --short-soft: #26233a;
    --substance: #fca5a5;
    --substance-bg: #4a1818;
    --facts: #93c5fd;
    --facts-bg: #172a4d;
    --form: #fdba74;
    --form-bg: #45250d;
    --phrases: #fde047;
    --phrases-bg: #3d3408;
    --structure: #c4b5fd;
    --structure-bg: #2e2050;
    --focus: #c4b5fd;
  }
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--canvas);
  color: var(--ink);
  font: 16px/1.55 var(--sans);
}
a { color: var(--accent); }
a:focus-visible, .mark:focus-visible, .notes-col:focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 2px;
  border-radius: 3px;
}
.skip { position: absolute; left: -9999px; }
.skip:focus { left: 16px; top: 16px; background: var(--paper); padding: 8px 12px; z-index: 10; }
.page { max-width: 1180px; margin: 0 auto; padding: 48px 32px 32px; }

/* Head */
.head {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(320px, 1fr);
  gap: 48px;
  align-items: end;
  padding-bottom: 36px;
  border-bottom: 1px solid var(--rule);
}
.brand { font-weight: 650; letter-spacing: -0.01em; color: var(--accent); margin: 0 0 28px; font-size: 15px; }
.verdict-word {
  font-family: var(--serif);
  font-weight: 600;
  font-size: clamp(48px, 6.2vw, 84px);
  overflow-wrap: anywhere;
  hyphens: manual;
  line-height: 0.95;
  letter-spacing: -0.035em;
  margin: 0;
}
.verdict-pass .verdict-word { color: var(--pass); }
.verdict-revise .verdict-word { color: var(--revise); }
.verdict-too_short .verdict-word { color: var(--short); }
.verdict-reason { font-size: 18px; margin: 16px 0 0; max-width: 34em; }
.facts-line { color: var(--muted); margin: 10px 0 0; font-size: 15px; }
.facts-line span + span::before { content: ""; display: inline-block; width: 4px; height: 4px; border-radius: 50%; background: var(--rule); margin: 0 10px 3px; }

.tally { width: 100%; border-collapse: collapse; font-size: 15px; }
.tally caption { text-align: left; color: var(--muted); font-size: 13px; padding-bottom: 8px; }
.tally th, .tally td { padding: 9px 0; border-bottom: 1px solid var(--rule); text-align: left; font-weight: 400; }
.tally th { font-weight: 600; }
.tally td.n { text-align: right; width: 4.5em; font-variant-numeric: tabular-nums; }
.tally td.zero { color: var(--muted); }
.tally .sw { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 10px; vertical-align: 0; }
.tally thead th { font-size: 12px; color: var(--muted); font-weight: 500; }
.tally tr.cat-substance th { font-size: 17px; }

.disclaimer {
  margin: 28px 0 0;
  padding: 14px 18px;
  background: var(--accent-soft);
  border-radius: 10px;
  font-size: 14px;
  color: var(--ink);
  max-width: 62em;
}

/* Body: manuscript + notes */
.work { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(300px, 1fr); gap: 40px; margin-top: 40px; }
h2 { font-size: 20px; letter-spacing: -0.01em; margin: 0 0 6px; }
.section-note { color: var(--muted); font-size: 14px; margin: 0 0 18px; max-width: 40em; }
.manuscript {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 14px;
  padding: 40px 44px;
  font-family: var(--serif);
  font-size: 18.5px;
  line-height: 1.75;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  max-width: 44em;
}
.mark {
  border-radius: 2px;
  padding: 0.08em 0;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  text-decoration: none;
  color: inherit;
}
.m-substance { background: var(--substance-bg); box-shadow: inset 0 -2px 0 var(--substance); }
.m-facts { background: var(--facts-bg); box-shadow: inset 0 -2px 0 var(--facts); }
.m-form { background: var(--form-bg); box-shadow: inset 0 -2px 0 var(--form); }
.m-phrases { background: var(--phrases-bg); box-shadow: inset 0 -2px 0 var(--phrases); }
.m-structure { background: var(--structure-bg); box-shadow: inset 0 -2px 0 var(--structure); }
.u-substance { box-shadow: inset 0 -2px 0 var(--substance); }
.u-facts { box-shadow: inset 0 -2px 0 var(--facts); }
.u-form { box-shadow: inset 0 -2px 0 var(--form); }
.u-phrases { box-shadow: inset 0 -2px 0 var(--phrases); }
.u-structure { box-shadow: inset 0 -2px 0 var(--structure); }
.ref {
  font-family: var(--sans);
  font-size: 0.6em;
  font-weight: 650;
  vertical-align: 0.6em;
  line-height: 0;
  margin-left: 1px;
  text-decoration: none;
  padding: 0 2px;
  white-space: nowrap;
}
.ref-substance { color: var(--substance); }
.ref-facts { color: var(--facts); }
.ref-form { color: var(--form); }
.ref-phrases { color: var(--phrases); }
.ref-structure { color: var(--structure); }

.notes { list-style: none; margin: 0; padding: 0; }
@media (min-width: 901px) {
  .notes-col { position: sticky; top: 16px; align-self: start; max-height: calc(100vh - 32px); overflow-y: auto; padding-right: 6px; overscroll-behavior: contain; }
}
.note {
  position: relative;
  padding: 14px 16px 14px 18px;
  border-left: 3px solid var(--rule);
  margin-bottom: 10px;
  background: var(--paper);
  border-radius: 0 10px 10px 0;
  scroll-margin-top: 24px;
}
.note:target { outline: 2px solid var(--accent); outline-offset: 0; }
.note.c-substance { border-left-color: var(--substance); }
.note.c-facts { border-left-color: var(--facts); }
.note.c-form { border-left-color: var(--form); }
.note.c-phrases { border-left-color: var(--phrases); }
.note.c-structure { border-left-color: var(--structure); }
.note.c-rhythm { border-left-color: var(--muted); }
.note-head { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; font-size: 14px; }
.note-num { font-weight: 700; font-variant-numeric: tabular-nums; }
.note-name { font-weight: 600; }
.note-meta { color: var(--muted); font-size: 13px; }
.sev { font-size: 12px; font-weight: 600; padding: 1px 8px; border-radius: 999px; border: 1px solid currentColor; }
.sev-fail { color: var(--revise); }
.sev-tell { color: var(--form); }
.sev-hint { color: var(--muted); }
.note-excerpt { font-family: var(--serif); font-style: italic; margin: 8px 0 0; color: var(--muted); font-size: 15px; }
.note-msg { margin: 6px 0 0; font-size: 15px; }
.note-fix { margin: 6px 0 0; font-size: 15px; }
.note-fix b { color: var(--accent); font-weight: 600; }
.back { font-size: 13px; margin-left: auto; }

/* Lower sections */
.lower { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 40px; margin-top: 56px; padding-top: 40px; border-top: 1px solid var(--rule); }
.lower .wide { grid-column: 1 / -1; }
.plain { list-style: none; padding: 0; margin: 0; }
.plain li { padding: 9px 0; border-bottom: 1px solid var(--rule); display: flex; gap: 12px; align-items: baseline; flex-wrap: wrap; }
.plain .val { font-weight: 600; font-variant-numeric: tabular-nums; }
.plain .meta { color: var(--muted); font-size: 14px; }
.tag { font-size: 12px; padding: 1px 8px; border-radius: 999px; }
.tag-ok { background: var(--pass-soft); color: var(--pass); }
.tag-warn { background: var(--revise-soft); color: var(--revise); }
.empty { color: var(--muted); font-size: 15px; margin: 0; }
h3 { font-size: 15px; margin: 18px 0 6px; }

.rhythm { width: 100%; border-collapse: collapse; font-size: 15px; }
.rhythm th, .rhythm td { text-align: left; padding: 10px 12px 10px 0; border-bottom: 1px solid var(--rule); vertical-align: middle; }
.rhythm thead th { font-size: 12px; color: var(--muted); font-weight: 500; }
.rhythm td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
.bar { position: relative; height: 10px; min-width: 160px; background: var(--rule); border-radius: 999px; }
.bar .band { position: absolute; top: 0; bottom: 0; background: var(--pass-soft); border: 1px solid var(--pass); border-radius: 999px; }
.bar .dot { position: absolute; top: 50%; width: 14px; height: 14px; margin: -7px 0 0 -7px; border-radius: 50%; background: var(--ink); border: 2px solid var(--paper); }
.state-ai_side .dot, .state-overshot .dot { background: var(--revise); }
.state-ok .dot { background: var(--pass); }
.prov { color: var(--muted); font-size: 12px; }

.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0 24px; margin: 0; }
.metrics div { padding: 10px 0; border-bottom: 1px solid var(--rule); }
.metrics dt { color: var(--muted); font-size: 13px; }
.metrics dd { margin: 2px 0 0; font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; }

.foot { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--rule); color: var(--muted); font-size: 13px; }
.foot a { color: var(--muted); }

@media (max-width: 900px) {
  .page { padding: 28px 16px; }
  .head, .work, .lower { grid-template-columns: minmax(0, 1fr); gap: 28px; }
  .manuscript { padding: 24px 20px; font-size: 17px; }
  .bar { min-width: 100px; }
}
@media print {
  :root { color-scheme: light; }
  body { background: #fff; color: #000; font-size: 11pt; }
  .page { max-width: none; padding: 0; }
  .work { grid-template-columns: minmax(0, 1fr); }
  .notes-col { position: static; max-height: none; overflow: visible; }
  .manuscript { border: 0; padding: 0; max-width: none; font-size: 11.5pt; }
  .note, .manuscript, .lower > section { break-inside: avoid; }
  .note { border: 1px solid #ccc; border-left-width: 3px; }
  .back, .skip { display: none; }
  .mark, .bar .band, .bar .dot, .tally .sw, .disclaimer { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  a { color: inherit; text-decoration: none; }
}
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
html { scroll-behavior: smooth; }
"""


def _e(value):
    """Escape any value for HTML text and attribute context."""
    if value is None:
        return ""
    return escape(str(value), quote=True)


def _num(value):
    if isinstance(value, bool) or value is None:
        return ""
    if isinstance(value, float):
        return "{:.2f}".format(value).rstrip("0").rstrip(".") if value != int(value) else str(int(value))
    return str(value)


def _as_int(value):
    try:
        if isinstance(value, bool):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _labels(result):
    lang = result.get("lang") if isinstance(result.get("lang"), str) else "en"
    return LABELS.get(lang, LABELS["en"]), lang if lang in LABELS else "en"


def _category(finding):
    cat = finding.get("category")
    return cat if cat in CATEGORY_ORDER else "structure"


def _sorted_findings(findings, text_len):
    """Number findings in reading order. Positioned ones first, by offset."""
    positioned, global_ = [], []
    for f in findings:
        if not isinstance(f, dict):
            continue
        start, end = _as_int(f.get("start")), _as_int(f.get("end"))
        cat = _category(f)
        if (
            cat in INLINE_CATEGORIES
            and start is not None
            and end is not None
            and 0 <= start < end <= text_len
        ):
            positioned.append((start, end, f))
        else:
            global_.append(f)
    positioned.sort(key=lambda t: (t[0], t[1]))
    global_.sort(key=lambda f: (CATEGORY_ORDER.index(_category(f)), SEVERITY_ORDER.get(f.get("severity"), 3)))
    numbered = []
    for i, (start, end, f) in enumerate(positioned, 1):
        numbered.append({"n": i, "start": start, "end": end, "f": f})
    offset = len(numbered)
    for j, f in enumerate(global_, 1):
        numbered.append({"n": offset + j, "start": None, "end": None, "f": f})
    return numbered


def _render_text(text, numbered, L):
    """Split the text at every finding boundary and wrap covered segments."""
    spans = [n for n in numbered if n["start"] is not None]
    if not spans:
        return _e(text)
    bounds = {0, len(text)}
    ends_at = {}
    for n in spans:
        bounds.add(n["start"])
        bounds.add(n["end"])
        ends_at.setdefault(n["end"], []).append(n)
    points = sorted(bounds)
    out = []
    for a, b in zip(points, points[1:]):
        segment = text[a:b]
        covering = [n for n in spans if n["start"] <= a and b <= n["end"]]
        if covering:
            top = min(covering, key=lambda n: (CATEGORY_PRIORITY.get(_category(n["f"]), 9), SEVERITY_ORDER.get(n["f"].get("severity"), 3)))
            cat = _category(top["f"])
            # The narrowest finding draws the underline, so a phrase inside a
            # longer substance passage stays visible.
            narrow = min(covering, key=lambda n: (n["end"] - n["start"], CATEGORY_PRIORITY.get(_category(n["f"]), 9)))
            under = _category(narrow["f"])
            names = "; ".join(
                "{} {}: {}".format(L["categories"].get(_category(n["f"]), ""), n["n"], n["f"].get("name") or n["f"].get("id") or "")
                for n in covering
            )
            out.append(
                '<a class="mark m-{cat} u-{under}" href="#note-{n}" title="{t}">{s}</a>'.format(
                    cat=cat, under=under, n=narrow["n"], t=_e(names), s=_e(segment)
                )
            )
        else:
            out.append(_e(segment))
        for n in sorted(ends_at.get(b, []), key=lambda n: n["n"]):
            cat = _category(n["f"])
            out.append(
                '<a class="ref ref-{cat}" id="ref-{n}" href="#note-{n}" aria-label="{label}">{n}</a>'.format(
                    cat=cat, n=n["n"], label=_e("{} {}".format(L["findings"], n["n"]))
                )
            )
    return "".join(out)


def _render_note(n, L):
    f = n["f"]
    cat = _category(f)
    sev = f.get("severity") if f.get("severity") in SEVERITY_ORDER else "hint"
    parts = ['<li class="note c-{cat}" id="note-{num}">'.format(cat=cat, num=n["n"])]
    meta = [L["categories"].get(cat, cat)]
    if f.get("id"):
        meta.append(str(f.get("id")))
    line = _as_int(f.get("line"))
    if n["start"] is not None and line is not None:
        meta.append("{} {}".format(L["line"], line))
    elif n["start"] is None:
        meta.append(L["no_position"] if line is None else "{} {}".format(L["line"], line))
    parts.append('<div class="note-head">')
    parts.append('<span class="note-num">{}</span>'.format(n["n"]))
    parts.append('<span class="note-name">{}</span>'.format(_e(f.get("name") or f.get("id") or "")))
    parts.append(
        '<span class="sev sev-{sev}" title="{long}">{short}</span>'.format(
            sev=sev, long=_e(L["severity_long"][sev]), short=_e(L["severity"][sev])
        )
    )
    if n["start"] is not None:
        parts.append('<a class="back" href="#ref-{0}" aria-label="{1}">&uarr;</a>'.format(n["n"], _e(L["skip"])))
    parts.append("</div>")
    parts.append('<div class="note-meta">{}</div>'.format(" / ".join(_e(m) for m in meta)))
    if f.get("excerpt"):
        quotes = ("\u201e", "\u201c") if L is LABELS["de"] else ("\u201c", "\u201d")
        parts.append('<p class="note-excerpt">{}{}{}</p>'.format(quotes[0], _e(f.get("excerpt")), quotes[1]))
    if f.get("message"):
        parts.append('<p class="note-msg">{}</p>'.format(_e(f.get("message"))))
    if f.get("fix"):
        parts.append('<p class="note-fix"><b>{}:</b> {}</p>'.format(_e(L["fix"]), _e(f.get("fix"))))
    parts.append("</li>")
    return "".join(parts)


def _render_tally(result, L):
    summary = result.get("summary") if isinstance(result.get("summary"), dict) else {}
    rows = []
    for cat in CATEGORY_ORDER:
        counts = summary.get(cat) if isinstance(summary.get(cat), dict) else {}
        cells = []
        for sev in ("fail", "tell", "hint"):
            v = _as_int(counts.get(sev)) or 0
            cells.append('<td class="n{z}">{v}</td>'.format(z=" zero" if v == 0 else "", v=v))
        swatch = "var(--{})".format(cat) if cat != "rhythm" else "var(--muted)"
        rows.append(
            '<tr class="cat-{cat}"><th scope="row"><span class="sw" style="background:{sw}" aria-hidden="true"></span>{name}</th>{cells}</tr>'.format(
                cat=cat, sw=swatch, name=_e(L["categories"][cat]), cells="".join(cells)
            )
        )
    head = '<thead><tr><td></td>{}</tr></thead>'.format(
        "".join('<th scope="col" class="n" title="{}">{}</th>'.format(_e(L["severity_long"][s]), _e(L["severity"][s])) for s in ("fail", "tell", "hint"))
    )
    return '<table class="tally"><caption>{}</caption>{}<tbody>{}</tbody></table>'.format(_e(L["summary"]), head, "".join(rows))


def _render_people(result, L):
    people = [p for p in (result.get("people") or []) if isinstance(p, dict)]
    items = []
    for p in people:
        sourced = p.get("sourced")
        tag = ""
        if sourced is True:
            tag = '<span class="tag tag-ok">{}</span>'.format(_e(L["sourced"]))
        elif sourced is False:
            tag = '<span class="tag tag-warn">{}</span>'.format(_e(L["unsourced"]))
        line = _as_int(p.get("line"))
        items.append(
            '<li><span class="val">{}</span>{}{}</li>'.format(
                _e(p.get("name")),
                '<span class="meta">{} {}</span>'.format(_e(L["line"]), line) if line is not None else "",
                tag,
            )
        )
    body = '<ul class="plain">{}</ul>'.format("".join(items)) if items else '<p class="empty">{}</p>'.format(_e(L["none"]))
    return '<section><h2>{}</h2><p class="section-note">{}</p>{}</section>'.format(_e(L["people"]), _e(L["people_note"]), body)


def _render_facts(result, L):
    facts = result.get("facts") if isinstance(result.get("facts"), dict) else {}
    lost = [x for x in (facts.get("lost") or []) if isinstance(x, dict)]
    added = [x for x in (facts.get("added") or []) if isinstance(x, dict)]
    if not lost and not added and not facts:
        return ""
    lost_items = "".join(
        '<li><span class="val">{}</span><span class="meta">{}{}</span></li>'.format(
            _e(x.get("value")),
            _e(x.get("type") or ""),
            (" / {} {}".format(_e(L["source"]), _e(x.get("source")))) if x.get("source") else "",
        )
        for x in lost
    )
    added_items = []
    for x in added:
        line = _as_int(x.get("line"))
        tag = ""
        if x.get("sourced") is True:
            tag = '<span class="tag tag-ok">{}</span>'.format(_e(L["sourced"]))
        elif x.get("sourced") is False:
            tag = '<span class="tag tag-warn">{}</span>'.format(_e(L["unsourced"]))
        added_items.append(
            '<li><span class="val">{}</span><span class="meta">{}{}</span>{}</li>'.format(
                _e(x.get("value")),
                _e(x.get("type") or ""),
                (" / {} {}".format(_e(L["line"]), line)) if line is not None else "",
                tag,
            )
        )
    return (
        '<section><h2>{title}</h2><p class="section-note">{note}</p>'
        "<h3>{lost_h}</h3>{lost}<h3>{added_h}</h3>{added}</section>"
    ).format(
        title=_e(L["facts_title"]),
        note=_e(L["added_note"]),
        lost_h=_e(L["lost"]),
        lost='<ul class="plain">{}</ul>'.format(lost_items) if lost_items else '<p class="empty">{}</p>'.format(_e(L["no_lost"])),
        added_h=_e(L["added"]),
        added='<ul class="plain">{}</ul>'.format("".join(added_items)) if added_items else '<p class="empty">{}</p>'.format(_e(L["no_added"])),
    )


def _bar(value, p10, p90):
    """Position band and dot on a shared scale that always contains both."""
    nums = [v for v in (value, p10, p90) if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if len(nums) < 3:
        return ""
    lo, hi = min(nums), max(nums)
    span = hi - lo or abs(hi) or 1.0
    lo -= span * 0.25
    hi += span * 0.25

    def pct(v):
        return max(0.0, min(100.0, (v - lo) / (hi - lo) * 100.0))

    left, right, dot = pct(p10), pct(p90), pct(value)
    return (
        '<div class="bar" aria-hidden="true"><span class="band" style="left:{:.1f}%;width:{:.1f}%"></span>'
        '<span class="dot" style="left:{:.1f}%"></span></div>'
    ).format(left, max(right - left, 1.0), dot)


def _render_rhythm(result, L):
    rows = [r for r in (result.get("rhythm") or []) if isinstance(r, dict)]
    if not rows:
        return ""
    out = []
    for r in rows:
        band = r.get("band") if isinstance(r.get("band"), dict) else {}
        p10, p90, value = band.get("p10"), band.get("p90"), r.get("value")
        state = r.get("state") if r.get("state") in L["state_names"] else "ok"
        name = L["metric_names"].get(r.get("feature"), r.get("feature"))
        prov = ' <span class="prov">({})</span>'.format(_e(L["provisional"])) if r.get("provisional") else ""
        out.append(
            '<tr class="state-{state}"><th scope="row">{name}</th><td class="num">{v}</td>'
            '<td>{bar}<span class="prov">{p10} / {p90}</span></td><td>{sname}{prov}</td></tr>'.format(
                state=state,
                name=_e(name),
                v=_e(_num(value)),
                bar=_bar(value, p10, p90),
                p10=_e(_num(p10)),
                p90=_e(_num(p90)),
                sname=_e(L["state_names"][state]),
                prov=prov,
            )
        )
    return (
        '<section class="wide"><h2>{t}</h2><p class="section-note">{n}</p>'
        '<table class="rhythm"><thead><tr><th scope="col">{f}</th><th scope="col">{v}</th>'
        '<th scope="col">{b}</th><th scope="col">{s}</th></tr></thead><tbody>{rows}</tbody></table></section>'
    ).format(
        t=_e(L["rhythm_title"]), n=_e(L["rhythm_note"]), f=_e(L["feature"]), v=_e(L["value"]),
        b=_e(L["band"]), s=_e(L["state"]), rows="".join(out),
    )


def _render_metrics(result, L):
    metrics = result.get("metrics") if isinstance(result.get("metrics"), dict) else {}
    items = []
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            items.append("<div><dt>{}</dt><dd>{}</dd></div>".format(_e(L["metric_names"].get(key, key)), _e(_num(value))))
    if not items:
        return ""
    return '<section class="wide"><h2>{}</h2><dl class="metrics">{}</dl></section>'.format(_e(L["metrics"]), "".join(items))


def render_html(result):
    """Return a complete, self-contained HTML document for one check result."""
    if not isinstance(result, dict):
        raise TypeError("render_html expects the result dict")
    L, lang = _labels(result)
    text = result.get("text") if isinstance(result.get("text"), str) else ""
    verdict = result.get("verdict") if result.get("verdict") in L["verdict"] else "revise"
    findings = result.get("findings") if isinstance(result.get("findings"), list) else []
    numbered = _sorted_findings(findings, len(text))

    words = _as_int(result.get("words"))
    facts_line = []
    if words is not None:
        facts_line.append("<span>{} {}</span>".format(words, _e(L["words"])))
    facts_line.append("<span>{}</span>".format(_e(L["lang_name"].get(lang, lang))))
    if result.get("register"):
        facts_line.append("<span>{}: {}</span>".format(_e(L["register"]), _e(result.get("register"))))
    if result.get("version"):
        facts_line.append("<span>slop-check {}</span>".format(_e(result.get("version"))))

    reason = result.get("verdict_reason") or L["verdict_hint"][verdict]
    notice = result.get("notice") or L["disclaimer"]

    notes_html = (
        '<ol class="notes">{}</ol>'.format("".join(_render_note(n, L) for n in numbered))
        if numbered
        else '<p class="empty">{}</p>'.format(_e(L["no_findings"]))
    )

    lower = "".join(
        part for part in (
            _render_people(result, L),
            _render_facts(result, L),
            _render_rhythm(result, L),
            _render_metrics(result, L),
        ) if part
    )

    return (
        "<!doctype html>\n"
        '<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="referrer" content="no-referrer">\n'
        "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; style-src 'unsafe-inline'; img-src data:\">\n"
        "<title>{title}: {verdict_word}</title>\n<style>{css}</style>\n</head>\n<body>\n"
        '<a class="skip" href="#text">{skip}</a>\n'
        '<main class="page">\n'
        '<header class="head verdict-{verdict}">\n<div>\n<p class="brand">AI Slop Checker</p>\n'
        '<h1 class="verdict-word">{verdict_word}</h1>\n'
        '<p class="verdict-reason">{reason}</p>\n<p class="facts-line">{facts_line}</p>\n</div>\n'
        "<div>{tally}</div>\n</header>\n"
        '<p class="disclaimer" role="note">{notice}</p>\n'
        '<div class="work">\n<section aria-labelledby="text-h">\n<h2 id="text-h">{text_h}</h2>\n'
        '<p class="section-note">{text_note}</p>\n<div class="manuscript" id="text" tabindex="-1">{body}</div>\n</section>\n'
        '<section class="notes-col" aria-labelledby="notes-h" tabindex="0">\n<h2 id="notes-h">{notes_h}</h2>\n{notes}\n</section>\n</div>\n'
        '<div class="lower">{lower}</div>\n'
        '<footer class="foot">AI Slop Checker \u00b7 <a href="https://github.com/simplifiers/ai-slop-checker">github.com/simplifiers/ai-slop-checker</a></footer>\n'
        "</main>\n</body>\n</html>\n"
    ).format(
        lang=_e(lang),
        title=_e(L["title"]),
        verdict=verdict,
        verdict_word=_e(L["verdict"][verdict]),
        css=CSS,
        skip=_e(L["skip"]),
        reason=_e(reason),
        facts_line="".join(facts_line),
        tally=_render_tally(result, L),
        notice=_e(notice),
        text_h=_e(L["text"]),
        text_note=_e(L["text_note"]),
        body=_render_text(text, numbered, L),
        notes_h=_e(L["findings"]),
        notes=notes_html,
        lower=lower,
    )
