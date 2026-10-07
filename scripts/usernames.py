#!/usr/bin/env python3
"""Generate Hungarian username candidates for account enumeration.

Combines surnames with given names into the login formats common at
Hungarian companies, schools and webmail. Hungarian name order is
family-name-first, but logins usually follow the Western given.family
convention, so both orders are emitted. Accents are folded to ASCII, which
is what login systems almost always store.

Usage:
    python3 scripts/usernames.py                         # built-in seed lists
    python3 scripts/usernames.py --surnames src/surnames-top.txt \
        --given names-male.txt names-female.txt > usernames.txt

By default it uses a small seed of the 20 most common surnames
(src/surnames-top.txt) and the given-name lists in the repo root.
"""
import argparse
import pathlib
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent


def ascii_lower(s):
    folded = "".join(
        c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)
    )
    return folded.lower() if folded.isascii() else None


def formats(surname, given):
    s, g = surname, given
    yield f"{g}.{s}"      # janos.kovacs
    yield f"{s}.{g}"      # kovacs.janos
    yield f"{g[0]}{s}"    # jkovacs
    yield f"{s}{g[0]}"    # kovacsj
    yield f"{g}{s}"       # janoskovacs
    yield f"{g}_{s}"      # janos_kovacs
    yield f"{s}.{g[0]}"   # kovacs.j


def load(paths):
    out = []
    for p in paths:
        for line in open(p, encoding="utf-8"):
            a = ascii_lower(line.strip())
            if a:
                out.append(a)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--surnames", nargs="+", default=[str(ROOT / "src/surnames-top.txt")])
    ap.add_argument("--given", nargs="+",
                    default=[str(ROOT / "names-male.txt"), str(ROOT / "names-female.txt")])
    ap.add_argument("--limit-given", type=int, default=0,
                    help="use only the first N given names (keeps output small)")
    args = ap.parse_args(argv)

    surnames = load(args.surnames)
    given = load(args.given)
    if args.limit_given:
        given = given[: args.limit_given]

    seen = set()
    for s in surnames:
        for g in given:
            for u in formats(s, g):
                seen.add(u)
    sys.stdout.write("".join(u + "\n" for u in sorted(seen)))


if __name__ == "__main__":
    main()
