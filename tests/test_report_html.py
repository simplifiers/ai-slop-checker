"""Tests for the HTML report (slopcheck/report_html.py)."""

import glob
import json
import os
import re
import unittest

from slopcheck.report_html import render_html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEXT = (
    "Viele Experten sind sich einig: Content ist King.\n\n"
    "Laut einer Studie steigern 73 % der Teams ihren Umsatz. "
    "Thomas Weber sagt, das sei erst der Anfang.\n"
    "<script>alert(1)</script> & \"Zitat\" 'x'"
)


def _span(text, needle):
    start = text.index(needle)
    return start, start + len(needle)


def fixture():
    s1, e1 = _span(TEXT, "Viele Experten sind sich einig")
    s2, e2 = _span(TEXT, "73 %")
    s3, e3 = _span(TEXT, "Content ist King")
    s4, e4 = _span(TEXT, "<script>alert(1)</script>")
    return {
        "tool": "slop-check",
        "version": "0.1.0",
        "lang": "de",
        "register": "article",
        "words": 31,
        "verdict": "revise",
        "verdict_reason": "Zwei Substanz-Befunde <b>ohne</b> Beleg.",
        "notice": "Hinweis <i>kein</i> Urteil.",
        "findings": [
            {"id": "S-02", "category": "substance", "severity": "fail", "name": "Vage Zuschreibung",
             "line": 1, "start": s1, "end": e1, "excerpt": TEXT[s1:e1],
             "message": "Wer genau?", "fix": "Nenne die Quelle."},
            {"id": "F-01", "category": "facts", "severity": "fail", "name": "Zahl ohne Quelle",
             "line": 3, "start": s2, "end": e2, "excerpt": "73 %", "message": "Neu im Text.", "fix": "Beleg ergänzen."},
            {"id": "P-07", "category": "phrases", "severity": "tell", "name": "Floskel",
             "line": 1, "start": s3, "end": e3, "excerpt": "Content ist King", "message": "Abgegriffen.", "fix": "Streichen."},
            {"id": "X-99", "category": "form", "severity": "hint", "name": "<img src=x onerror=alert(2)>",
             "line": 4, "start": s4, "end": e4, "excerpt": "<script>", "message": "m", "fix": "f"},
            {"id": "R-01", "category": "rhythm", "severity": "tell", "name": "Gleichförmige Sätze",
             "line": None, "start": None, "end": None, "message": "Satzlängen ähneln sich.", "fix": "Variieren."},
            {"id": "BAD", "category": "structure", "severity": "hint", "name": "Out of range",
             "line": 9, "start": 5, "end": 99999, "message": "kaputter Offset"},
        ],
        "summary": {
            "substance": {"fail": 1, "tell": 0, "hint": 0},
            "facts": {"fail": 1, "tell": 0, "hint": 0},
            "phrases": {"fail": 0, "tell": 1, "hint": 0},
            "structure": {"fail": 0, "tell": 0, "hint": 1},
            "rhythm": {"fail": 0, "tell": 1, "hint": 0},
            "form": {"fail": 0, "tell": 0, "hint": 1},
        },
        "facts": {
            "lost": [{"type": "number", "value": "15.000", "source": "notizen.md"}],
            "added": [{"type": "number", "value": "73 %", "line": 3, "sourced": False}],
        },
        "people": [{"name": "Thomas <Weber>", "line": 3, "sourced": False}],
        "metrics": {"concreteness_per_100": 3.1, "sentence_cv": 0.52, "mean_sentence_len": 14.2, "mattr50": 0.71},
        "rhythm": [{"feature": "sentence_cv", "value": 0.31, "band": {"p10": 0.4, "p90": 0.9},
                    "state": "ai_side", "provisional": True}],
        "text": TEXT,
    }


def strip_tags(html_fragment):
    import html as _html
    return _html.unescape(re.sub(r"<[^>]+>", "", html_fragment))


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.result = fixture()
        self.html = render_html(self.result)

    def test_document_shape(self):
        self.assertTrue(self.html.startswith("<!doctype html>"))
        self.assertIn('<html lang="de">', self.html)
        self.assertIn("Überarbeiten", self.html)
        self.assertIn("github.com/simplifiers/ai-slop-checker", self.html)

    def test_user_text_is_escaped(self):
        self.assertNotIn("<script>alert(1)</script>", self.html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", self.html)
        self.assertNotIn("<img src=x", self.html)
        self.assertNotIn("<b>ohne</b>", self.html)
        self.assertNotIn("<i>kein</i>", self.html)
        self.assertNotIn("Thomas <Weber>", self.html)
        self.assertNotIn("<script", self.html.lower().replace("&lt;script", ""))

    def test_no_external_resources(self):
        self.assertIsNone(re.search(r'\b(src|href)\s*=\s*"(https?:)?//', self.html.replace(
            'href="https://github.com/simplifiers/ai-slop-checker"', "")))
        self.assertNotIn("@import", self.html)
        self.assertNotIn("url(", self.html)
        self.assertNotIn("<link", self.html)
        self.assertNotIn("<script", self.html)

    def test_marks_wrap_exact_offsets(self):
        manuscript = re.search(r'<div class="manuscript"[^>]*>(.*?)</div>', self.html, re.S).group(1)
        marks = re.findall(r'<a class="mark m-(\w+) u-\w+"[^>]*>(.*?)</a>', manuscript, re.S)
        by_cat = {}
        for cat, inner in marks:
            by_cat.setdefault(cat, "")
            by_cat[cat] += strip_tags(inner)
        self.assertEqual(by_cat.get("substance"), "Viele Experten sind sich einig")
        self.assertEqual(by_cat.get("facts"), "73 %")
        self.assertEqual(by_cat.get("phrases"), "Content ist King")
        self.assertEqual(by_cat.get("form"), "<script>alert(1)</script>")
        self.assertNotIn("rhythm", by_cat)

    def test_text_survives_round_trip(self):
        manuscript = re.search(r'<div class="manuscript"[^>]*>(.*?)</div>', self.html, re.S).group(1)
        without_refs = re.sub(r'<a class="ref[^"]*"[^>]*>\d+</a>', "", manuscript)
        self.assertEqual(strip_tags(without_refs), TEXT)

    def test_notes_and_refs_link_up(self):
        refs = set(re.findall(r'id="ref-(\d+)"', self.html))
        notes = set(re.findall(r'id="note-(\d+)"', self.html))
        self.assertTrue(refs)
        self.assertTrue(refs <= notes)
        self.assertEqual(len(notes), len(self.result["findings"]))

    def test_out_of_range_finding_is_listed_not_marked(self):
        self.assertIn("Out of range", self.html)
        self.assertNotIn("m-structure", self.html.split('<div class="manuscript"')[1].split("</div>")[0])

    def test_lower_sections(self):
        self.assertIn("15.000", self.html)
        self.assertIn("notizen.md", self.html)
        self.assertIn("Thomas &lt;Weber&gt;", self.html)
        self.assertIn('class="rhythm"', self.html)
        self.assertIn("vorläufig", self.html)

    def test_english_labels_and_minimal_input(self):
        html = render_html({"lang": "en", "verdict": "pass", "text": "Short.", "findings": []})
        self.assertIn('<html lang="en">', html)
        self.assertIn(">Pass<", html)
        self.assertIn("No findings.", html)

    def test_no_dashes_in_output_chrome(self):
        html = render_html({"lang": "en", "verdict": "too_short", "text": "", "findings": []})
        self.assertNotIn("\u2014", html)
        self.assertNotIn("\u2013", html)

    def test_example_results_render(self):
        for path in sorted(glob.glob(os.path.join(ROOT, "examples", "*.json"))):
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict) or data.get("tool") != "slop-check":
                continue
            with self.subTest(example=os.path.basename(path)):
                html = render_html(data)
                self.assertIn("<!doctype html>", html)
                self.assertNotIn("<script", html)


if __name__ == "__main__":
    unittest.main()
