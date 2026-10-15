"""Tests for scripts/build_docs.py using a small pattern fixture."""

import importlib.util
import json
import os
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("build_docs", os.path.join(ROOT, "scripts", "build_docs.py"))
build_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_docs)


class BuildDocsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patterns = os.path.join(self.tmp.name, "patterns")
        self.out = os.path.join(self.tmp.name, "docs")
        os.makedirs(self.patterns)
        with open(os.path.join(self.patterns, "substance.json"), "w", encoding="utf-8") as fh:
            json.dump({
                "category": "substance",
                "patterns": [{
                    "id": "S-02",
                    "name": {"en": "Vague attribution", "de": "Vage Zuschreibung"},
                    "description": {"en": "Who exactly?", "de": "Wer genau?"},
                    "bad": {"en": "Experts agree.", "de": "Experten sind sich einig."},
                    "better": {"en": "[Name], [role], said [claim].", "de": "[Name], [Rolle], sagte [Aussage]."},
                    "severity": "fail",
                }],
            }, fh)
        with open(os.path.join(self.patterns, "phrases.json"), "w", encoding="utf-8") as fh:
            json.dump([{"id": "P-01", "name": "Delve", "lang": "en", "bad": "Let us delve into it.", "better": "Here is how it works."}], fh)

    def tearDown(self):
        self.tmp.cleanup()

    def test_write_and_check(self):
        self.assertEqual(build_docs.main(["--patterns", self.patterns, "--out", self.out]), 0)
        with open(os.path.join(self.out, "patterns.md"), encoding="utf-8") as fh:
            en = fh.read()
        with open(os.path.join(self.out, "patterns.de.md"), encoding="utf-8") as fh:
            de = fh.read()
        self.assertIn("### S-02 Vague attribution", en)
        self.assertIn("> Experts agree.", en)
        self.assertIn("### S-02 Vage Zuschreibung", de)
        self.assertIn("**Besser:**", de)
        self.assertIn("### P-01 Delve", de)
        self.assertLess(en.index("## Substance"), en.index("## Phrases"))
        self.assertEqual(build_docs.main(["--check", "--patterns", self.patterns, "--out", self.out]), 0)

    def test_check_fails_when_stale(self):
        build_docs.main(["--patterns", self.patterns, "--out", self.out])
        with open(os.path.join(self.out, "patterns.md"), "a", encoding="utf-8") as fh:
            fh.write("edited by hand\n")
        self.assertEqual(build_docs.main(["--check", "--patterns", self.patterns, "--out", self.out]), 1)


if __name__ == "__main__":
    unittest.main()
