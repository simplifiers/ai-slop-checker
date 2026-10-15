"""Command line: slop-check FILE [options]"""

import argparse
import io
import json
import os
import sys

from . import VERSION
from .engine import SlopCheckError, check_text, load_config, split_list

LABELS = {
    "de": {
        "verdict": {"pass": "BESTANDEN", "revise": "ÜBERARBEITEN", "too_short": "ZU KURZ FÜR EIN URTEIL"},
        "words": "Wörter", "findings": "Funde", "none": "Keine Funde.",
        "cat": {"substance": "Substanz", "facts": "Fakten-Abgleich", "phrases": "Floskeln", "structure": "Struktur",
                "rhythm": "Rhythmus", "form": "Form"},
        "sev": {"fail": "FEHLER", "tell": "AUFFÄLLIG", "hint": "HINWEIS"},
        "line": "Zeile", "fix": "Tipp", "people": "Genannte Personen", "sourced": "mit Quelle", "unsourced": "ohne Quelle",
        "lost": "Aus den Quellen, fehlt im Entwurf", "added": "Neu im Entwurf, in keiner Quelle",
        "rhythm": "Rhythmus (Band: menschliche Nachrichtentexte)", "ai_side": "Messwerte auf der KI-Seite", "metrics": "Kennzahlen",
        "state": {"ok": "ok", "ai_side": "KI-Seite", "overshot": "außerhalb"},
    },
    "en": {
        "verdict": {"pass": "PASS", "revise": "REVISE", "too_short": "TOO SHORT FOR A VERDICT"},
        "words": "words", "findings": "Findings", "none": "No findings.",
        "cat": {"substance": "Substance", "facts": "Fact check", "phrases": "Stock phrases", "structure": "Structure",
                "rhythm": "Rhythm", "form": "Form"},
        "sev": {"fail": "FAIL", "tell": "TELL", "hint": "HINT"},
        "line": "line", "fix": "Fix", "people": "People named", "sourced": "sourced", "unsourced": "no source",
        "lost": "In the sources, missing from the draft", "added": "New in the draft, in no source",
        "rhythm": "Rhythm (band: human news texts)", "ai_side": "Measures on the AI side", "metrics": "Metrics",
        "state": {"ok": "ok", "ai_side": "AI side", "overshot": "outside"},
    },
}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise SlopCheckError(message)


def build_parser():
    p = _Parser(prog="slop-check", description="AI Slop Checker: deterministic quality check for AI-assisted expert texts (de/en).")
    p.add_argument("file", help="Markdown, HTML or text file, or - for stdin")
    p.add_argument("--lang", choices=("de", "en"), help="language (default: detect)")
    p.add_argument("--source", action="append", default=[], metavar="FILE",
                   help="notes or source file to compare facts against (repeatable)")
    p.add_argument("--format", choices=("text", "json", "html"), default="text")
    p.add_argument("--out", metavar="FILE", help="write the report to FILE instead of stdout")
    p.add_argument("--address", choices=("du", "sie"), help="German form of address the text should use")
    p.add_argument("--forbid", metavar="LIST", help="comma-separated banned words")
    p.add_argument("--allow", metavar="LIST", help="comma-separated terms never reported as stock phrases")
    p.add_argument("--emojis", choices=("allow", "no", "limit"))
    p.add_argument("--dashes", choices=("off", "tell", "fail"),
                   help="style rule for long dashes: off, tell (default) or fail")
    p.add_argument("--config", metavar="FILE", help="config file (default: .slopcheck.json next to the file or in cwd)")
    p.add_argument("--fail-on", choices=("revise", "never"), dest="fail_on",
                   help="exit with code 1 when the verdict is revise")
    p.add_argument("--score", action="store_true", help="also compute the Lite slop score (0 best, 100 worst)")
    p.add_argument("--expert-share", type=float, metavar="0-100", dest="expert_share",
                   help="estimated share of expert material in percent, for --score")
    p.add_argument("--version", action="version", version="slop-check " + VERSION)
    return p


def _read(path):
    if path == "-":
        data = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read()
    else:
        try:
            with open(path, "rb") as f:
                data = f.read()
        except (IOError, OSError) as exc:
            raise SlopCheckError("Cannot read %s: %s" % (path, exc.strerror or exc))
    if isinstance(data, bytes):
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
    return data


def _find_config(args):
    if args.config:
        return load_config(args.config)
    cands = []
    if args.file != "-":
        cands.append(os.path.join(os.path.dirname(os.path.abspath(args.file)), ".slopcheck.json"))
    cands.append(os.path.join(os.getcwd(), ".slopcheck.json"))
    for c in cands:
        if os.path.isfile(c):
            return load_config(c)
    return {}


def run(argv=None):
    args = build_parser().parse_args(argv)
    config = _find_config(args)
    if args.address:
        config["address"] = args.address
    if args.emojis:
        config["emojis"] = args.emojis
    if args.dashes:
        config["dashes"] = args.dashes
    if args.forbid:
        config["forbid"] = split_list(config.get("forbid")) + split_list(args.forbid)
    if args.allow:
        config["allow"] = split_list(config.get("allow")) + split_list(args.allow)
    fail_on = args.fail_on or config.get("fail_on")
    if args.expert_share is not None and not 0 <= args.expert_share <= 100:
        raise SlopCheckError("--expert-share must be between 0 and 100")
    raw = _read(args.file)
    source_files = list(config.get("sources") or []) + list(args.source)
    sources = [(os.path.basename(s), _read(s)) for s in source_files]
    result = check_text(raw, lang=args.lang, sources=sources, config=config,
                        score=args.score or args.expert_share is not None, expert_share=args.expert_share)
    if args.format == "json":
        out = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == "html":
        try:
            from .report_html import render_html
        except ImportError:
            raise SlopCheckError("HTML report is not available in this installation")
        out = render_html(result)
    else:
        out = format_text(result)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as f:
            f.write(out if out.endswith("\n") else out + "\n")
    else:
        _write(out)
    if fail_on == "revise" and result["verdict"] == "revise":
        return 1
    return 0


def _write(s):
    try:
        sys.stdout.write(s if s.endswith("\n") else s + "\n")
    except UnicodeEncodeError:
        sys.stdout.buffer.write((s + "\n").encode("utf-8"))


def format_text(r):
    L = LABELS[r["lang"]]
    lines = []
    lines.append("slop-check %s  |  %s  |  %d %s" % (r["version"], L["verdict"][r["verdict"]], r["words"], L["words"]))
    lines.append(r["verdict_reason"])
    lines.append("")
    if not r["findings"]:
        lines.append(L["none"])
    for cat in ("substance", "facts", "phrases", "structure", "rhythm", "form"):
        fs = [f for f in r["findings"] if f["category"] == cat]
        if not fs:
            continue
        s = r["summary"][cat]
        lines.append("== %s (%s %d, %s %d, %s %d)" % (L["cat"][cat], L["sev"]["fail"], s["fail"], L["sev"]["tell"], s["tell"],
                                                  L["sev"]["hint"], s["hint"]))
        for f in fs:
            where = ("%s %d" % (L["line"], f["line"])) if f["line"] else "-"
            lines.append("  [%s] %s %s (%s)" % (L["sev"][f["severity"]], f["id"], f["name"], where))
            if f["excerpt"]:
                lines.append("      > %s" % f["excerpt"])
            lines.append("      %s" % f["message"])
            if f["fix"]:
                lines.append("      %s: %s" % (L["fix"], f["fix"]))
        lines.append("")
    if r["people"]:
        lines.append("== " + L["people"])
        for p in r["people"]:
            lines.append("  %s (%s %d, %s)" % (p["name"], L["line"], p["line"], L["sourced"] if p["sourced"] else L["unsourced"]))
        lines.append("")
    if r["facts"]["lost"] or r["facts"]["added"]:
        if r["facts"]["lost"]:
            lines.append("== " + L["lost"])
            for x in r["facts"]["lost"]:
                lines.append("  %s: %s (%s)" % (x["type"], x["value"], x["source"]))
        if r["facts"]["added"]:
            lines.append("== " + L["added"])
            for x in r["facts"]["added"]:
                lines.append("  %s: %s (%s %d, %s)" % (x["type"], x["value"], L["line"], x["line"],
                                                      L["sourced"] if x["sourced"] else L["unsourced"]))
        lines.append("")
    if r["rhythm"]:
        lines.append("== " + L["rhythm"])
        for x in r["rhythm"]:
            lines.append("  %-22s %8s   %s .. %s   %s" % (x["feature"], x["value"], x["band"]["p10"], x["band"]["p90"],
                                                       L["state"][x["state"]]))
        if r["metrics"].get("ai_side_count") is not None:
            lines.append("  %s: %d / %d" % (L["ai_side"], r["metrics"]["ai_side_count"], r["metrics"]["ai_side_limit"]))
        lines.append("")
    if "concreteness_per_100" in r["metrics"]:
        lines.append("%s: concreteness_per_100 = %s" % (L["metrics"], r["metrics"]["concreteness_per_100"]))
    if "score" in r:
        sc = r["score"]
        lines.append("Lite slop score: %s (%s)" % (sc["slop_score"] if sc["slop_score"] is not None else "-",
                                                    "ohne Expertenanteil %d" % sc["sum_without_expert_share"] if r["lang"] == "de"
                                                    else "without expert share %d" % sc["sum_without_expert_share"]))
    lines.append("")
    lines.append(r["notice"])
    return "\n".join(lines)


def main(argv=None):
    want_json = argv is not None and "--format" in argv and "json" in argv
    if argv is None:
        want_json = "--format" in sys.argv and "json" in sys.argv[sys.argv.index("--format") + 1:sys.argv.index("--format") + 2]
    try:
        return run(argv)
    except SlopCheckError as exc:
        _error(str(exc), want_json)
        return 2
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # never show a stack trace to users
        _error("Internal error: %s: %s" % (type(exc).__name__, exc), want_json)
        return 3


def _error(msg, as_json):
    if as_json:
        sys.stdout.write(json.dumps({"tool": "slop-check", "version": VERSION, "error": msg}, ensure_ascii=False) + "\n")
    else:
        sys.stderr.write("slop-check: error: %s\n" % msg)
