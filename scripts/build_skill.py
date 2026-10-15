"""Bundle the slopcheck package into the Claude skill and build a ZIP.

Copies slopcheck/ (and patterns/ if the package reads them from the repo root)
into skills/ai-slop-checker/, then writes dist/ai-slop-checker-skill.zip whose root is
the folder ai-slop-checker/.

The copy inside skills/ai-slop-checker/ is committed on purpose: skill installers
such as `npx skills add` fetch only the skill folder, so the code has to be in it.

Usage:
  python scripts/build_skill.py           copy the package and build the ZIP
  python scripts/build_skill.py --check   fail if the committed copy is stale
"""

import filecmp
import os
import shutil
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "skills", "ai-slop-checker")
DIST = os.path.join(ROOT, "dist")
ZIP_PATH = os.path.join(DIST, "ai-slop-checker-skill.zip")

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store")


def copy_tree(name):
    src = os.path.join(ROOT, name)
    dst = os.path.join(SKILL_DIR, name)
    if not os.path.isdir(src):
        return False
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=IGNORE)
    return True


def build_zip():
    os.makedirs(DIST, exist_ok=True)
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder, dirs, files in os.walk(SKILL_DIR):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__")
            for name in sorted(files):
                if name.endswith((".pyc", ".pyo")) or name == ".DS_Store":
                    continue
                full = os.path.join(folder, name)
                arc = os.path.join("ai-slop-checker", os.path.relpath(full, SKILL_DIR))
                zf.write(full, arc)
    return ZIP_PATH


def stale(name):
    """Return differing paths between ROOT/name and SKILL_DIR/name."""
    src, dst = os.path.join(ROOT, name), os.path.join(SKILL_DIR, name)
    if not os.path.isdir(src):
        return []
    if not os.path.isdir(dst):
        return [name + "/"]
    out = []

    def walk(cmp, prefix):
        skip = lambda n: n == "__pycache__" or n.endswith((".pyc", ".pyo")) or n == ".DS_Store"
        out.extend(prefix + n for n in cmp.left_only + cmp.right_only + cmp.diff_files if not skip(n))
        for sub, c in cmp.subdirs.items():
            if not skip(sub):
                walk(c, prefix + sub + "/")

    walk(filecmp.dircmp(src, dst), name + "/")
    return out


def bundled_names():
    names = ["slopcheck"]
    if os.path.isdir(os.path.join(ROOT, "patterns")) and not os.path.isdir(os.path.join(ROOT, "slopcheck", "patterns")):
        names.append("patterns")
    return names


def main():
    if "--check" in sys.argv[1:]:
        diffs = [d for n in bundled_names() for d in stale(n)]
        if diffs:
            print("skills/ai-slop-checker/ is out of date, run: python scripts/build_skill.py")
            for d in diffs:
                print("  " + d)
            sys.exit(1)
        print("skills/ai-slop-checker/ is up to date")
        return
    if not os.path.isfile(os.path.join(SKILL_DIR, "SKILL.md")):
        sys.exit("skills/ai-slop-checker/SKILL.md is missing")
    for name in bundled_names():
        if not copy_tree(name):
            sys.exit("{}/ not found in the repository root".format(name))
    path = build_zip()
    print("wrote {}".format(os.path.relpath(path, ROOT)))


if __name__ == "__main__":
    main()
