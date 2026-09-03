#!/usr/bin/env python3
"""Generate realistic, randomized identifiers to replace synthetic placeholders.

Real systems randomize record locators, order numbers, invoice numbers, etc. Sequential or
patterned placeholders (ABCD12, 123456) are a synthetic tell. Use this to mint replacements that
look genuine, and use --avoid to guarantee your replacement does not collide with a value already
present in the world (pass the existing values, or feed them from scan_world.py output).

Examples:
  python gen_realistic_values.py --type pnr --n 3
  python gen_realistic_values.py --type order --prefix 'ORD-' --n 5
  python gen_realistic_values.py --type invoice --n 2 --avoid INV-2025-0001 INV-2025-0002
  python gen_realistic_values.py --type alnum --length 10 --n 4
"""
import argparse
import secrets
import string
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Airline record locators / PNRs: 6 uppercase alphanumerics, randomized. Many GDSs avoid the
# visually-ambiguous 0/O/1/I. Kept configurable via --ambiguous to include them.
PNR_SAFE = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"          # no 0 O 1 I
PNR_FULL = string.ascii_uppercase + string.digits
ALNUM_UPPER = string.ascii_uppercase + string.digits
ALNUM_MIXED = string.ascii_letters + string.digits
HEXCHARS = "0123456789abcdef"


def rand(chars, n):
    return "".join(secrets.choice(chars) for _ in range(n))


def gen_one(kind, args):
    if kind == "pnr":
        charset = PNR_FULL if args.ambiguous else PNR_SAFE
        return args.prefix + rand(charset, args.length if args.length is not None else 6) + args.suffix
    if kind == "confirmation":
        # e.g. 8-char uppercase alnum confirmation code
        return args.prefix + rand(ALNUM_UPPER, args.length if args.length is not None else 8) + args.suffix
    if kind == "order":
        # numeric order id, realistic magnitude (not 1, 2, 3); default 7 digits
        digits = args.length if args.length is not None else 7
        first = secrets.choice("123456789")
        return args.prefix + first + rand(string.digits, digits - 1) + args.suffix
    if kind == "invoice":
        # INV-YYYY-##### style if no prefix given; else prefix + serial
        serial = rand(string.digits, args.length if args.length is not None else 5)
        return (args.prefix or "INV-2025-") + serial + args.suffix
    if kind == "hex":
        return args.prefix + rand(HEXCHARS, args.length if args.length is not None else 12) + args.suffix
    if kind == "alnum":
        return args.prefix + rand(ALNUM_UPPER if args.upper else ALNUM_MIXED,
                                  args.length if args.length is not None else 8) + args.suffix
    raise ValueError(kind)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--type", required=True,
                   choices=["pnr", "confirmation", "order", "invoice", "hex", "alnum"],
                   help="kind of identifier to generate")
    p.add_argument("--n", type=int, default=1, help="how many to generate (default 1)")
    p.add_argument("--length", type=int, default=None,
                   help="override the character/digit length for the type")
    p.add_argument("--prefix", default="", help="string to prepend (e.g. 'ORD-')")
    p.add_argument("--suffix", default="", help="string to append")
    p.add_argument("--upper", action="store_true",
                   help="for --type alnum, force uppercase-only")
    p.add_argument("--ambiguous", action="store_true",
                   help="for --type pnr, allow 0/O/1/I (default excludes them)")
    p.add_argument("--avoid", nargs="*", default=[],
                   help="values to never emit (collision avoidance); case-insensitive")
    args = p.parse_args()

    avoid = {a.strip().lower() for a in args.avoid}
    out, tries = [], 0
    while len(out) < args.n and tries < args.n * 1000 + 1000:
        tries += 1
        v = gen_one(args.type, args)
        if v.lower() in avoid or v in out:
            continue
        out.append(v)
    if len(out) < args.n:
        print("ERROR: could not generate enough collision-free values; loosen constraints",
              file=sys.stderr)
        sys.exit(1)
    print("\n".join(out))


if __name__ == "__main__":
    main()
