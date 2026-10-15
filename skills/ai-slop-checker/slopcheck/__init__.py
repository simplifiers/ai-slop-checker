"""slop-check: a deterministic quality checker for AI-assisted expert texts in German and English.

slop-check does not tell whether AI wrote a text. It shows patterns you can check.
"""

VERSION = "0.1.0"
__version__ = VERSION


def check(text, **kwargs):
    """Check a text and return the result dict (see slopcheck.engine.check_text)."""
    from .engine import check_text
    return check_text(text, **kwargs)
