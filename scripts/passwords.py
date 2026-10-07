#!/usr/bin/env python3
"""Expand a list of base words into Hungarian password candidates.

For each base word this emits the variants that show up again and again in
real Hungarian password dumps:

  * the word itself, Capitalised and UPPERCASE
  * a trailing "!"
  * trailing "1", "12", "123"
  * a trailing year (recent years by default)
  * for an accented base, the unaccented twin gets all of the above too
    (many people type "laszlo" for "László")

It is deliberately conservative: broader mangling (leetspeak, more years,
birthday PINs) belongs in a hashcat rule, see rules/hungarian.rule.

Usage:
    python3 scripts/passwords.py src/password-bases.txt > candidates.txt

    # regenerate the shipped list from its base words and merge in anything
    # already there, then sort with scripts/check.py --fix:
    python3 scripts/passwords.py src/password-bases.txt > /tmp/new.txt
    cat hungarian-passwords.txt /tmp/new.txt | sort -u > /tmp/m && mv /tmp/m hungarian-passwords.txt
    python3 scripts/check.py --fix
"""
import pathlib
import sys
import unicodedata

YEARS = [str(y) for y in range(2020, 2027)]
NUM_SUFFIXES = ["1", "12", "123"]


def unaccented(word):
    folded = "".join(
        c for c in unicodedata.normalize("NFKD", word) if not unicodedata.combining(c)
    )
    return folded if folded.isascii() and folded != word else None


def expand_one(base):
    """All candidates for a single spelling of a base word."""
    cap = base[:1].upper() + base[1:]
    out = [base, cap, base.upper(), base + "!", cap + "!"]
    for n in NUM_SUFFIXES:
        out.append(base + n)
        out.append(cap + n)
    for y in YEARS:
        out.append(base + y)
        out.append(cap + y)
    return out


def expand(base):
    forms = [base.lower()]
    plain = unaccented(base.lower())
    if plain:
        forms.append(plain)
    out = []
    for f in forms:
        out.extend(expand_one(f))
    return out


def read_bases(path):
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if line:
            yield line


def main(argv):
    if len(argv) != 2:
        sys.exit(__doc__)
    seen = set()
    for base in read_bases(argv[1]):
        for cand in expand(base):
            seen.add(cand)
    sys.stdout.write("".join(c + "\n" for c in sorted(seen)))


if __name__ == "__main__":
    main(sys.argv)
