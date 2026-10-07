#!/usr/bin/env python3
"""Validate the wordlists in the repository root.

Checks every *.txt file for: valid UTF-8, NFC normalization, LF line endings,
a trailing newline, no empty lines, no leading/trailing whitespace, no
duplicates and Hungarian collation order (hu_HU.UTF-8). Also checks that the
entry counts in the README table match the files.

Usage:
    python3 scripts/check.py          # report problems, exit 1 if any
    python3 scripts/check.py --fix    # rewrite files normalized, deduplicated and sorted

Needs the hu_HU.UTF-8 locale. On Debian/Ubuntu: sudo locale-gen hu_HU.UTF-8
Without root:
    localedef -i hu_HU -f UTF-8 ~/.locale/hu_HU.UTF-8 && export LOCPATH=~/.locale
"""
import argparse
import locale
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALE = "hu_HU.UTF-8"


def set_locale():
    try:
        locale.setlocale(locale.LC_COLLATE, LOCALE)
    except locale.Error:
        sys.exit(
            f"error: locale {LOCALE} is not available.\n"
            "  Debian/Ubuntu: sudo locale-gen hu_HU.UTF-8\n"
            "  without root:  localedef -i hu_HU -f UTF-8 ~/.locale/hu_HU.UTF-8 "
            "&& export LOCPATH=~/.locale"
        )


def sort_key(s):
    # Same order as `LC_ALL=hu_HU.UTF-8 sort`: collation first, bytes break ties.
    return (locale.strxfrm(s), s.encode("utf-8"))


def check_file(path):
    problems = []
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return [f"not valid UTF-8 ({e})"]
    if "\r" in text:
        problems.append("contains CR characters (use LF line endings)")
    if text and not text.endswith("\n"):
        problems.append("missing trailing newline")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    seen = set()
    for n, line in enumerate(lines, 1):
        if line.strip() == "":
            problems.append(f"line {n}: empty")
        elif line != line.strip():
            problems.append(f"line {n}: leading/trailing whitespace")
        if unicodedata.normalize("NFC", line) != line:
            problems.append(f"line {n}: not NFC")
        if line in seen:
            problems.append(f"line {n}: duplicate {line!r}")
        seen.add(line)

    for n in range(1, len(lines)):
        if sort_key(lines[n - 1]) > sort_key(lines[n]):
            problems.append(
                f"line {n + 1}: out of order ({lines[n - 1]!r} > {lines[n]!r})"
            )
            break
    return problems


def fix_file(path):
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    entries = {unicodedata.normalize("NFC", l.strip()) for l in text.split("\n")}
    entries.discard("")
    path.write_text("".join(e + "\n" for e in sorted(entries, key=sort_key)),
                    encoding="utf-8", newline="\n")


def check_readme(files):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    problems = []
    for name, count in re.findall(r"^\| `([^`]+\.txt)` \| ([\d,]+) \|", readme, re.M):
        path = ROOT / name
        if not path.exists():
            problems.append(f"README lists {name}, which does not exist")
            continue
        actual = len(path.read_text(encoding="utf-8").splitlines())
        if int(count.replace(",", "")) != actual:
            problems.append(f"README says {name} has {count} entries, file has {actual:,}")
    listed = set(re.findall(r"^\| `([^`]+\.txt)` \| [\d,]+ \|", readme, re.M))
    for path in files:
        if path.name not in listed:
            problems.append(f"{path.name} is missing from the README table")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--fix", action="store_true",
                        help="normalize, deduplicate and sort files in place")
    args = parser.parse_args()
    set_locale()

    files = sorted(ROOT.glob("*.txt"))
    failed = False
    for path in files:
        if args.fix:
            fix_file(path)
        problems = check_file(path)
        for p in problems[:20]:
            print(f"{path.name}: {p}")
        if len(problems) > 20:
            print(f"{path.name}: ... and {len(problems) - 20} more")
        failed |= bool(problems)

    for p in check_readme(files):
        print(f"README.md: {p}")
        failed = True

    if failed:
        return 1
    print(f"OK: {len(files)} files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
