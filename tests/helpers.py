"""Shared helpers for the slop-check tests."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slopcheck.engine import check_text  # noqa: E402


def run(text, lang=None, sources=None, **config):
    return check_text(text, lang=lang, sources=sources, config=config)


def ids(result, severity=None):
    return [f["id"] for f in result["findings"] if severity is None or f["severity"] == severity]


def add_cases(cls, cases):
    """Turn (name, lang, text, pid, expected, config) tuples into test methods.

    expected: True  -> pid must be reported (any severity except where a severity string is given)
              False -> pid must not be reported with severity fail or tell (hints are allowed)
              "fail"/"tell"/"hint" -> pid must be reported with exactly this severity
              "none" -> pid must not be reported at all
    """
    for case in cases:
        name, lang, text, pid, expected = case[:5]
        config = case[5] if len(case) > 5 else {}

        def make(lang=lang, text=text, pid=pid, expected=expected, config=config):
            def test(self):
                r = run(text, lang=lang, **config)
                found = [f for f in r["findings"] if f["id"] == pid]
                sev = [f["severity"] for f in found]
                msg = "%s: %s -> %s" % (pid, text[:80], [(f["id"], f["severity"], f["excerpt"]) for f in r["findings"]])
                if expected is True:
                    self.assertTrue(found, msg)
                elif expected is False:
                    self.assertFalse([s for s in sev if s in ("fail", "tell")], msg)
                elif expected == "none":
                    self.assertFalse(found, msg)
                else:
                    self.assertIn(expected, sev, msg)
            return test

        method = "test_%s" % name
        assert not hasattr(cls, method), method
        setattr(cls, method, make())
    return cls


FILLER_DE = (
    "Im Mai 2024 haben wir in Kassel mit Anna Lange aus unserem Team einen Testlauf gemacht. "
    "Ich habe dafür elf alte Artikel ausgewertet und notiert, welche zu einer Anfrage geführt hatten. "
    "Zwei davon kamen von Lesern aus Hamburg, die anderen aus der Region. "
)
FILLER_EN = (
    "In May 2024 we ran a test in Leeds with Anna Lane from our team. "
    "I went through eleven old articles and noted which ones had led to an enquiry. "
    "Two came from readers in Bristol, the others from the region. "
)
