"""Catalog, JSON contract, verdict, facts, rhythm, text model, CLI and examples."""

import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

from helpers import FILLER_DE, FILLER_EN, ROOT, ids, run

from slopcheck import VERSION, meter
from slopcheck import text as textmod
from slopcheck.checks import numbers, rhythm
from slopcheck.cli import main
from slopcheck.engine import (REVISE_TELL_PATTERNS, SlopCheckError, check_text, detect_language, load_band,
                              load_catalog, verdict_for)

EM = "\u2014"
EN = "\u2013"
EXAMPLES = os.path.join(ROOT, "examples")


def read(name):
    with io.open(os.path.join(EXAMPLES, name), encoding="utf-8") as f:
        return f.read()


class CatalogTests(unittest.TestCase):
    PREFIX = {"substance": "S", "facts": "S", "phrases": "P", "structure": "T", "rhythm": "R", "form": "F"}

    def test_phrase_counts(self):
        for lang in ("de", "en"):
            n = sum(1 for p in load_catalog(lang)["patterns"] if p["category"] == "phrases")
            self.assertGreaterEqual(n, 60, lang)

    def test_schema_and_prefixes(self):
        for lang in ("de", "en"):
            seen = set()
            for p in load_catalog(lang)["patterns"]:
                for key in ("id", "category", "name", "description", "bad", "better", "severity", "match"):
                    self.assertIn(key, p, (lang, p.get("id"), key))
                self.assertNotIn(p["id"], seen)
                seen.add(p["id"])
                self.assertTrue(re.fullmatch(r"[SPTRF]-\d{2}", p["id"]), p["id"])
                self.assertEqual(p["id"][0], self.PREFIX[p["category"]], p["id"])
                self.assertIn(p["severity"], ("fail", "tell", "hint"))
                if p["category"] == "phrases":
                    self.assertIn(p["tier"], ("evidence", "cluster", "context"))

    def test_better_examples_invent_nothing(self):
        # "better" must not contain figures or studies; concrete details only as [placeholders]
        for lang in ("de", "en"):
            for p in load_catalog(lang)["patterns"]:
                outside = re.sub(r"\[[^\]]*\]", "", p["better"])
                self.assertFalse(re.search(r"\d", outside), (lang, p["id"], p["better"]))
                self.assertFalse(re.search(r"\b(studie|study|umfrage|survey)\b", outside, re.I) and "Link" not in outside
                                 and "link" not in outside, (lang, p["id"], p["better"]))

    def test_no_literal_dashes_in_sources(self):
        for folder, _dirs, files in os.walk(os.path.join(ROOT, "slopcheck")):
            for f in files:
                if f.endswith((".py", ".json")) and f != "report_html.py":
                    with io.open(os.path.join(folder, f), encoding="utf-8") as fh:
                        content = fh.read()
                    self.assertNotIn(EM, content, f)
                    self.assertNotIn(EN, content, f)

    def test_regexes_compile(self):
        for lang in ("de", "en"):
            cat = load_catalog(lang)
            for key in ("contrast", "pathos_close", "participle_tail", "directive_cues", "example_cues"):
                for rx in cat["lexicon"][key]:
                    re.compile(rx)

    def test_same_ids_in_both_languages(self):
        de = {p["id"] for p in load_catalog("de")["patterns"] if p["category"] != "phrases"}
        en = {p["id"] for p in load_catalog("en")["patterns"] if p["category"] != "phrases"}
        self.assertEqual(de - en, {"F-07"})  # address switch is German only
        self.assertEqual(en - de, set())

    def test_unknown_language(self):
        with self.assertRaises(SlopCheckError):
            load_catalog("fr")


class ContractTests(unittest.TestCase):
    KEYS = ["tool", "version", "lang", "register", "words", "verdict", "verdict_reason", "notice", "findings",
            "summary", "facts", "people", "metrics", "rhythm", "text"]
    FINDING_KEYS = ["id", "category", "severity", "name", "line", "start", "end", "excerpt", "message", "fix"]

    def setUp(self):
        self.r = run(read("de-bad.md"))

    def test_top_level_keys(self):
        self.assertEqual(list(self.r.keys()), self.KEYS)
        self.assertEqual(self.r["tool"], "slop-check")
        self.assertEqual(self.r["version"], VERSION)
        self.assertEqual(self.r["register"], "article")

    def test_finding_keys(self):
        for f in self.r["findings"]:
            self.assertEqual(list(f.keys()), self.FINDING_KEYS)
            self.assertIsInstance(f["line"], int)
            self.assertIsInstance(f["start"], int)
            self.assertIsInstance(f["end"], int)

    def test_offsets_point_into_text(self):
        t = self.r["text"]
        for f in self.r["findings"]:
            self.assertTrue(0 <= f["start"] <= f["end"] <= len(t))
            if f["category"] in ("substance", "phrases") and f["id"] not in ("S-04", "S-05", "S-06"):
                self.assertEqual(re.sub(r"\s+", " ", t[f["start"]:f["end"]]).strip(), f["excerpt"], f)

    def test_line_numbers(self):
        t = self.r["text"]
        for f in self.r["findings"]:
            if f["line"]:
                self.assertEqual(t.count("\n", 0, f["start"]) + 1, f["line"], f)

    def test_summary_matches_findings(self):
        total = sum(v for c in self.r["summary"].values() for v in c.values())
        self.assertEqual(total, len(self.r["findings"]))
        self.assertEqual(set(self.r["summary"]), {"substance", "facts", "phrases", "structure", "rhythm", "form"})

    def test_rhythm_entries(self):
        for x in self.r["rhythm"]:
            self.assertEqual(set(x), {"feature", "value", "band", "state", "provisional"})
            self.assertIn(x["state"], ("ok", "ai_side", "overshot"))
            self.assertFalse(x["provisional"])

    def test_notice_always_present(self):
        self.assertIn("nicht, ob eine KI", run("Kurz.", lang="de")["notice"])
        self.assertIn("does not tell whether AI", run("Short.", lang="en")["notice"])

    def test_json_serialisable(self):
        json.dumps(self.r, ensure_ascii=False)

    def test_examples_json_files_match(self):
        for name in ("de-bad", "de-good", "en-bad", "en-good"):
            with io.open(os.path.join(EXAMPLES, name + ".json"), encoding="utf-8") as f:
                stored = json.load(f)
            self.assertEqual(list(stored.keys()), self.KEYS, name)
            fresh = run(read(name + ".md"))
            self.assertEqual(stored["verdict"], fresh["verdict"], name)
            self.assertEqual(stored["text"], fresh["text"], name)


class VerdictTests(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(run(read("de-bad.md"))["verdict"], "revise")
        self.assertEqual(run(read("en-bad.md"))["verdict"], "revise")
        self.assertEqual(run(read("de-good.md"))["verdict"], "pass")
        self.assertEqual(run(read("en-good.md"))["verdict"], "pass")

    def test_good_examples_have_no_fail_or_tell(self):
        for name, lang in (("de-good.md", "de"), ("en-good.md", "en")):
            r = run(read(name), lang=lang)
            self.assertEqual(ids(r, "fail"), [], name)
            self.assertLessEqual(len(set(ids(r, "tell"))), 1, name)

    def test_too_short(self):
        r = run("Studien zeigen, dass 73 % der Kunden lesen.", lang="de")
        self.assertEqual(r["verdict"], "too_short")
        self.assertIn("S-01", ids(r))

    def test_rule_fail(self):
        f = [{"id": "S-01", "severity": "fail"}]
        self.assertEqual(verdict_for(f, 500, "en")[0], "revise")

    def test_rule_tells(self):
        f = [{"id": "P-%02d" % i, "severity": "tell"} for i in range(REVISE_TELL_PATTERNS)]
        self.assertEqual(verdict_for(f, 500, "de")[0], "revise")
        self.assertEqual(verdict_for(f[:-1], 500, "de")[0], "pass")

    def test_rule_same_pattern_counts_once(self):
        f = [{"id": "P-01", "severity": "tell"}] * 10
        self.assertEqual(verdict_for(f, 500, "de")[0], "pass")

    def test_hints_do_not_count(self):
        f = [{"id": "P-%02d" % i, "severity": "hint"} for i in range(20)]
        self.assertEqual(verdict_for(f, 500, "en")[0], "pass")

    def test_pass_long_clean_text(self):
        r = run(FILLER_DE * 6, lang="de")
        self.assertEqual(r["verdict"], "pass", [(f["id"], f["severity"]) for f in r["findings"]])


class LanguageTests(unittest.TestCase):
    def test_detect_de(self):
        self.assertEqual(detect_language(FILLER_DE), "de")

    def test_detect_en(self):
        self.assertEqual(detect_language(FILLER_EN), "en")

    def test_override(self):
        self.assertEqual(run(FILLER_DE, lang="en")["lang"], "en")


class FactsTests(unittest.TestCase):
    NOTES = "Notizen:\n- 15.000 Abonnenten\n- Start im März 2026\n- Quelle https://example.org/a\n- Kundin aus Kassel\n"

    def test_lost_number(self):
        r = run("Wir haben viele Abonnenten. Start war im März 2026.", lang="de", sources=[("notizen.md", self.NOTES)])
        lost = [x["value"] for x in r["facts"]["lost"]]
        self.assertIn("15.000", lost)
        self.assertNotIn("März 2026", lost)
        self.assertEqual(r["facts"]["lost"][0]["source"], "notizen.md")
        self.assertIn("S-11", ids(r))

    def test_lost_finding_has_no_position(self):
        r = run("Kein Fakt hier.", lang="de", sources=[("n.md", self.NOTES)])
        f = [x for x in r["findings"] if x["id"] == "S-11"][0]
        self.assertEqual((f["line"], f["start"], f["end"]), (0, 0, 0))

    def test_added_number_fail(self):
        r = run("Wir haben 15.000 Abonnenten und 73 % bleiben.", lang="de", sources=[("n.md", self.NOTES)])
        added = r["facts"]["added"]
        self.assertTrue(any(x["value"].startswith("73") and not x["sourced"] for x in added), added)
        self.assertIn("S-12", ids(r, "fail"))

    def test_number_from_notes_not_flagged_by_s01(self):
        r = run("Das Portal hat 15.000 Abonnenten.", lang="de", sources=[("n.md", self.NOTES)])
        self.assertNotIn("S-01", ids(r))
        self.assertNotIn("S-12", ids(r))

    def test_added_url_fail(self):
        r = run("Mehr dazu unter https://example.com/erfunden im Netz.", lang="de", sources=[("n.md", self.NOTES)])
        self.assertTrue(any(x["type"] == "url" for x in r["facts"]["added"]))
        self.assertIn("S-12", ids(r, "fail"))

    def test_known_url_ok(self):
        r = run("Mehr dazu unter https://example.org/a im Netz.", lang="de", sources=[("n.md", self.NOTES)])
        self.assertFalse([x for x in r["facts"]["added"] if x["type"] == "url"])

    def test_added_name_tell(self):
        r = run("Die Kundin Maria Hofmann sagt, es passe.", lang="de", sources=[("n.md", self.NOTES)])
        self.assertIn("S-13", ids(r, "tell"))

    def test_added_sourced_number_is_listed_but_not_flagged(self):
        r = run("Laut Erhebung bleiben 73 % ([Erhebung](https://example.org/a)).", lang="de", sources=[("n.md", self.NOTES)])
        self.assertTrue(any(x["sourced"] for x in r["facts"]["added"] if x["type"] == "percent"))
        self.assertNotIn("S-12", [f["id"] for f in r["findings"] if "73" in f["excerpt"]])

    def test_number_word_matches_digits(self):
        r = run("Vorher kamen zwei Anfragen, danach elf.", lang="de", sources=[("n.md", "vorher 2, danach 11 Anfragen")])
        self.assertFalse(r["facts"]["lost"])

    def test_english_thousands(self):
        r = run("We now have 15,000 subscribers.", lang="en", sources=[("n.md", "15000 subscribers")])
        self.assertFalse([x for x in r["facts"]["added"] if x["type"] == "number"])

    def test_multiple_sources(self):
        r = run("We have 15,000 readers and 40% stay.", lang="en",
                sources=[("a.md", "15,000 readers"), ("b.md", "40% stay")])
        self.assertFalse(r["facts"]["added"])

    def test_no_sources_no_facts(self):
        r = run("73 % bleiben.", lang="de")
        self.assertEqual(r["facts"], {"lost": [], "added": []})


class RhythmTests(unittest.TestCase):
    LONG_DE = ("Im Mai haben wir in Kassel mit Anna Lange aus unserem Team einen Testlauf gemacht, weil die alten "
               "Artikel kaum Anfragen brachten und niemand genau wusste, woran das lag. ") * 20

    def _band_file(self, lang, provisional=False):
        band = load_band(lang)
        for spec in band["features"].values():
            if spec["ai_side"] == "low":
                spec["p10"], spec["p90"] = 1e9, 2e9
            else:
                spec["p10"], spec["p90"] = -2e9, -1e9
        band["provisional"] = provisional
        path = os.path.join(tempfile.mkdtemp(), "band.json")
        with io.open(path, "w", encoding="utf-8") as f:
            json.dump(band, f)
        return path, band

    def test_classify(self):
        spec = {"p10": 0.4, "p50": 0.6, "p90": 0.9, "ai_side": "low"}
        self.assertEqual(rhythm.classify(0.5, spec), "ok")
        self.assertEqual(rhythm.classify(0.2, spec), "ai_side")
        self.assertEqual(rhythm.classify(1.2, spec), "overshot")
        self.assertEqual(rhythm.classify(1.2, dict(spec, ai_side="high")), "ai_side")
        self.assertEqual(rhythm.classify(0.1, dict(spec, ai_side="none")), "overshot")
        self.assertIsNone(rhythm.classify(None, spec))

    def test_mattr(self):
        self.assertAlmostEqual(meter.mattr(["a"] * 60), 1 / 50.0)
        self.assertEqual(meter.mattr([str(i) for i in range(80)]), 1.0)
        self.assertIsNone(meter.mattr(["a"] * 10))

    def test_colons_skip_times_and_links(self):
        text = ("Wir starten um 10:30 Uhr, siehe https://example.org/plan. Der Plan steht fest. " * 40)
        f = meter.extract([("p", text)], "de")
        self.assertEqual(f["colons_1k"], 0)

    def test_measured_public_bands(self):
        for lang in ("de", "en"):
            b = load_band(lang)
            self.assertFalse(b["provisional"])
            self.assertEqual(b["band_register"], "news")
            self.assertGreaterEqual(b["n_human"], 150)
            self.assertEqual(b["revise_limit"], 6)
            self.assertTrue(b["sources"])
            for src in b["sources"]:
                self.assertIn("license", src)
            self.assertTrue(set(b["features"]) <= set(rhythm.FEATURE_IDS), lang)
            for spec in b["features"].values():
                self.assertIn(spec["ai_side"], ("low", "high"))
                self.assertLessEqual(spec["p10"], spec["p50"])
                self.assertLessEqual(spec["p50"], spec["p90"])
        self.assertNotIn("participle_tail_1k", load_band("de")["features"])
        self.assertIn("participle_tail_1k", load_band("en")["features"])

    def test_no_private_or_unseparating_features(self):
        folder = os.path.join(ROOT, "slopcheck", "bands")
        for name in os.listdir(folder):
            self.assertNotIn("article", name)
            with io.open(os.path.join(folder, name), encoding="utf-8") as f:
                band = json.load(f)
            for bad in ("dashes_1k", "passive_1k", "connector_starts_1k", "parens_1k", "headings_1k", "list_share"):
                self.assertNotIn(bad, band["features"], name)

    def test_short_text_not_measured(self):
        r = run(FILLER_DE * 2, lang="de")
        self.assertIsNone(r["metrics"]["ai_side_count"])
        self.assertEqual([f for f in r["findings"] if f["category"] == "rhythm"], [])
        self.assertEqual(r["rhythm"], [])

    def test_single_feature_is_hint(self):
        r = run(self.LONG_DE, lang="de")
        self.assertIsNotNone(r["metrics"]["ai_side_count"])
        for f in r["findings"]:
            if f["category"] == "rhythm" and f["id"] != "R-10":
                self.assertEqual(f["severity"], "hint")

    def test_ai_side_count_gives_revise(self):
        path, band = self._band_file("de")
        r = run(self.LONG_DE, lang="de", bands=path)
        self.assertEqual(r["metrics"]["ai_side_count"], len(band["features"]))
        self.assertIn("R-10", ids(r, "tell"))
        self.assertEqual(r["verdict"], "revise")

    def test_provisional_band_never_counts(self):
        path, _band = self._band_file("de", provisional=True)
        r = run(self.LONG_DE, lang="de", bands=path)
        self.assertIsNone(r["metrics"]["ai_side_count"])
        self.assertNotIn("R-10", ids(r))
        self.assertTrue(r["rhythm"][0]["provisional"])

    def test_verdict_rule_ai_side(self):
        self.assertEqual(verdict_for([], 500, "de", 6, 6)[0], "revise")
        self.assertEqual(verdict_for([], 500, "de", 5, 6)[0], "pass")
        self.assertEqual(verdict_for([], 500, "en", 9, None)[0], "pass")

    def test_rhythm_tells_not_in_pattern_count(self):
        f = [{"id": "P-%02d" % i, "severity": "tell"} for i in range(REVISE_TELL_PATTERNS - 1)]
        f.append({"id": "R-10", "severity": "tell"})
        self.assertEqual(verdict_for(f, 500, "de")[0], "pass")

    def test_metrics_present(self):
        r = run(read("en-good.md"))
        for key in ("concreteness_per_100", "prose_words", "ai_side_count", "ai_side_limit") + tuple(rhythm.FEATURE_IDS):
            self.assertIn(key, r["metrics"])


class TextModelTests(unittest.TestCase):
    def test_zones(self):
        md = ("---\ntitle: x\n---\n\n# Titel\n\nAbsatz eins.\n\n> Zitat\n\n```\ncode\n```\n\n| a | b |\n|---|---|\n\n"
              "## Häufige Fragen\n\n### Frage?\n\nAntwort.\n\n## Quellen\n\n- https://example.org\n")
        doc = textmod.parse(textmod.normalise(md), "de")
        kinds = [(b.kind, b.zone) for b in doc.blocks]
        self.assertIn(("frontmatter", "frontmatter"), kinds)
        self.assertIn(("quote", "body"), kinds)
        self.assertIn(("code", "code"), kinds)
        self.assertIn(("table", "body"), kinds)
        self.assertIn(("heading", "faq"), kinds)
        self.assertIn(("list", "sources"), kinds)

    def test_sentence_split_abbreviations(self):
        doc = textmod.parse("Das gilt z. B. für Holz. Am 3. Mai kam Dr. Krüger vorbei. Gut.", "de")
        self.assertEqual(len(doc.sentences), 3)

    def test_sentence_split_en(self):
        doc = textmod.parse("This works, e.g. for wood. Mr. Smith came by. Good!", "en")
        self.assertEqual(len(doc.sentences), 3)

    def test_html_input(self):
        r = run("<html><body><h2>Fazit</h2><p>Studien zeigen, dass das stimmt.</p><p>Zweiter Absatz.</p></body></html>", lang="de")
        self.assertTrue(r["text"].startswith("## Fazit"))
        self.assertIn("S-02", ids(r))
        self.assertIn("F-06", ids(r))

    def test_crlf(self):
        r = run("Erste Zeile.\r\n\r\nStudien zeigen das.\r\n", lang="de")
        self.assertNotIn("\r", r["text"])
        self.assertEqual([f["line"] for f in r["findings"] if f["id"] == "S-02"], [3])

    def test_word_count_excludes_code_and_meta(self):
        doc = textmod.parse(textmod.normalise("Eins zwei drei.\n\n```\nvier fünf\n```\n\n## Quellen\n\n- sechs sieben\n"), "de")
        self.assertEqual(doc.word_count(), 3)

    def test_quote_mask(self):
        doc = textmod.parse("Er sagte „ganzheitlich“ dazu.", "de")
        self.assertNotIn("ganzheitlich", doc.style_text)
        self.assertIn("ganzheitlich", doc.claim_text)

    def test_numbers_normalise(self):
        self.assertEqual(numbers.norm_number("15.000", "de"), "15000")
        self.assertEqual(numbers.norm_number("3,5", "de"), "3.5")
        self.assertEqual(numbers.norm_number("15,000", "en"), "15000")
        self.assertEqual(numbers.norm_number("3.50", "en"), "3.50")


class ScoreTests(unittest.TestCase):
    def test_score_without_share(self):
        r = check_text(read("de-bad.md"), score=True)
        self.assertIsNone(r["score"]["slop_score"])
        self.assertGreater(r["score"]["sum_without_expert_share"], 0)

    def test_score_with_share(self):
        r = check_text(read("de-bad.md"), score=True, expert_share=100)
        self.assertEqual(r["score"]["slop_score"], r["score"]["sum_without_expert_share"])
        r0 = check_text(read("de-bad.md"), score=True, expert_share=0)
        self.assertEqual(r0["score"]["parts"]["expert_share"]["points"], 30)

    def test_score_caps(self):
        text = " ".join("%d %% der Leute." % (10 + i) for i in range(10))
        r = check_text(text, lang="de", score=True)
        self.assertEqual(r["score"]["parts"]["unsourced_figures"]["points"], 20)

    def test_no_score_key_by_default(self):
        self.assertNotIn("score", check_text("Kurz.", lang="de"))


class CliTests(unittest.TestCase):
    def _run(self, args, stdin=None):
        cmd = [sys.executable, "-m", "slopcheck"] + args
        p = subprocess.run(cmd, cwd=ROOT, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8")

    def test_text_output(self):
        code, out, _ = self._run(["examples/de-bad.md"])
        self.assertEqual(code, 0)
        self.assertIn("ÜBERARBEITEN", out)
        self.assertIn("slop-check sagt nicht, ob eine KI einen Text geschrieben hat.", out)

    def test_json_output(self):
        code, out, _ = self._run(["examples/en-good.md", "--format", "json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["verdict"], "pass")

    def test_fail_on(self):
        self.assertEqual(self._run(["examples/en-bad.md", "--fail-on", "revise"])[0], 1)
        self.assertEqual(self._run(["examples/en-good.md", "--fail-on", "revise"])[0], 0)

    def test_stdin(self):
        code, out, _ = self._run(["-", "--lang", "en", "--format", "json"], stdin="Studies show this.".encode("utf-8"))
        self.assertEqual(code, 0)
        self.assertIn("S-02", out)

    def test_missing_file_message(self):
        code, out, err = self._run(["does-not-exist.md"])
        self.assertEqual(code, 2)
        self.assertIn("error", err)
        self.assertNotIn("Traceback", err)

    def test_missing_file_json(self):
        code, out, err = self._run(["does-not-exist.md", "--format", "json"])
        self.assertEqual(code, 2)
        self.assertIn("error", json.loads(out))

    def test_bad_option(self):
        code, _out, err = self._run(["examples/de-bad.md", "--lang", "fr"])
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)

    def test_source_option(self):
        code, out, _ = self._run(["examples/de-good.md", "--source", "examples/notes-de.md", "--format", "json"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(out)["facts"]["lost"])

    def test_forbid_and_address(self):
        code, out, _ = self._run(["-", "--lang", "de", "--address", "sie", "--forbid", "Holz", "--format", "json"],
                                 stdin="Du kaufst Holz.".encode("utf-8"))
        found = [f["id"] for f in json.loads(out)["findings"]]
        self.assertIn("F-07", found)
        self.assertIn("F-09", found)

    def test_config_file(self):
        d = tempfile.mkdtemp()
        with io.open(os.path.join(d, ".slopcheck.json"), "w", encoding="utf-8") as f:
            json.dump({"forbid": ["Holz"], "address": "du"}, f)
        with io.open(os.path.join(d, "t.md"), "w", encoding="utf-8") as f:
            f.write("Wir verkaufen Holz.")
        code, out, _ = self._run([os.path.join(d, "t.md"), "--format", "json", "--lang", "de"])
        self.assertIn("F-09", [x["id"] for x in json.loads(out)["findings"]])

    def test_bad_config(self):
        d = tempfile.mkdtemp()
        path = os.path.join(d, "c.json")
        with io.open(path, "w", encoding="utf-8") as f:
            f.write("{\"nonsense\": 1}")
        code, _out, err = self._run(["examples/de-good.md", "--config", path])
        self.assertEqual(code, 2)
        self.assertIn("Unknown config keys", err)

    def test_html_out(self):
        path = os.path.join(tempfile.mkdtemp(), "r.html")
        code, _out, _err = self._run(["examples/de-bad.md", "--format", "html", "--out", path])
        self.assertEqual(code, 0)
        with io.open(path, encoding="utf-8") as f:
            self.assertIn("<html", f.read().lower())

    def test_score_flag(self):
        code, out, _ = self._run(["examples/de-bad.md", "--score", "--expert-share", "20", "--format", "json"])
        self.assertIsNotNone(json.loads(out)["score"]["slop_score"])

    def test_expert_share_range(self):
        self.assertEqual(self._run(["examples/de-bad.md", "--expert-share", "120"])[0], 2)

    def test_main_returns_code(self):
        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            code = main(["examples/does-not-exist.md", "--format", "json"])
            out = sys.stdout.getvalue()
        finally:
            sys.stdout = old
        self.assertEqual(code, 2)
        self.assertIn("error", json.loads(out))


if __name__ == "__main__":
    unittest.main()


class FalseAlarmFixtureTests(unittest.TestCase):
    """Self-written texts in a human expert style must pass without fail findings."""

    def _check(self, name, lang):
        with io.open(os.path.join(ROOT, "tests", "fixtures", name), encoding="utf-8") as f:
            r = run(f.read(), lang=lang)
        self.assertEqual(ids(r, "fail"), [], name)
        self.assertEqual(r["verdict"], "pass", [(x["id"], x["severity"], x["excerpt"]) for x in r["findings"]])
        return r

    def test_human_de(self):
        r = self._check("human-de.md", "de")
        self.assertNotIn("T-06", ids(r))

    def test_human_en(self):
        r = self._check("human-en.md", "en")
        self.assertNotIn("P-36", ids(r))   # robust standard errors
        self.assertNotIn("P-24", ids(r))   # single cluster word: not reported

    def test_narrative_reading_is_own_experience(self):
        r = run("Last January we laid a screed in Bath. After three weeks the meter still read 2.8%.", lang="en")
        self.assertIn("S-08", ids(r))
        self.assertNotIn("S-01", ids(r))

    def test_plain_doppelte_is_no_claim(self):
        self.assertNotIn("S-01", ids(run("Bei Kälte kannst du locker das Doppelte einplanen.", lang="de")))

    def test_w_question_is_no_colon_reveal(self):
        self.assertNotIn("T-06", ids(run("Was hilft wirklich? Drei Dinge helfen. Wie geht das? So geht das.", lang="de")))


class HtmlCommentTests(unittest.TestCase):
    """HTML comments are removed from the checked and displayed text; line numbers keep matching the file."""

    def _assert(self, raw, lang, pid, line):
        r = run(raw, lang=lang)
        self.assertNotIn("<!--", r["text"])
        self.assertNotIn("Gamechanger", r["text"].split("\n")[0])
        found = [f for f in r["findings"] if f["id"] == pid]
        self.assertTrue(found, r["findings"])
        f = found[0]
        self.assertEqual(f["line"], line)
        self.assertEqual(re.sub(r"\s+", " ", r["text"][f["start"]:f["end"]]).strip(), f["excerpt"])
        return r

    def test_de_single_line(self):
        r = self._assert("<!-- Studien zeigen: Gamechanger -->\n\nStudien zeigen das.", "de", "S-02", 3)
        self.assertEqual(len([f for f in r["findings"] if f["id"] == "S-02"]), 1)
        self.assertNotIn("P-18", ids(r))

    def test_de_multi_line(self):
        r = self._assert("<!-- Beispiel\nStudien zeigen 73 %\nGamechanger -->\n\nStudien zeigen das.", "de", "S-02", 5)
        self.assertNotIn("S-01", ids(r))

    def test_en_single_line(self):
        r = self._assert("<!-- Studies show: a game-changer -->\nStudies show this.", "en", "S-02", 2)
        self.assertNotIn("P-21", ids(r))

    def test_en_multi_line(self):
        r = self._assert("Intro line.\n<!--\nStudies show 73%\n-->\nStudies show this.", "en", "S-02", 5)
        self.assertNotIn("S-01", ids(r))

    def test_inline_comment(self):
        r = run("Wir arbeiten <!-- ganzheitlich --> sorgfältig.", lang="de")
        self.assertEqual(r["text"].strip(), "Wir arbeiten  sorgfältig.")

    def test_examples_have_no_comment(self):
        self.assertNotIn("<!--", run(read("de-bad.md"))["text"])
