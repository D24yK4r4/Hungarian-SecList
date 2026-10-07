#!/usr/bin/env python3
"""Write an accent-stripped (ASCII) copy of a Hungarian wordlist.

Many real Hungarian passwords are typed without accents, so an unaccented
twin of a list is useful for cracking and fuzzing. This folds the Hungarian
accents (a e i o o o u u u and their uppercase) to plain ASCII, lowercases
nothing, drops entries that still contain non-ASCII after folding, dedupes
and sorts the result in byte order (ASCII-only, so no locale needed).

Usage:
    python3 scripts/strip-accents.py hungarian-words.txt > ascii/hungarian-words.txt
    python3 scripts/strip-accents.py hungarian-words.txt ascii/hungarian-words.txt
"""
import sys
import unicodedata

# Hungarian long o/u (o" u") decompose to combining marks under NFKD; the rest
# (a e i o u + umlauts) fold the same way. 'ae' and typographic punctuation
# have no ASCII fold and those entries are dropped.
def fold(s):
    out = "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )
    return out if out.isascii() else None


def main(argv):
    if not 2 <= len(argv) <= 3:
        sys.exit(__doc__)
    src = open(argv[1], encoding="utf-8")
    seen = set()
    for line in src:
        folded = fold(line.strip())
        if folded:
            seen.add(folded)
    out = open(argv[2], "w", encoding="utf-8", newline="\n") if len(argv) == 3 else sys.stdout
    out.write("".join(w + "\n" for w in sorted(seen)))


if __name__ == "__main__":
    main(sys.argv)
