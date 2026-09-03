#!/usr/bin/env python3
"""Deterministic, diff-only reconciliation of tabular app-data (Step 8 booster).

An LLM consistency pass *samples* rows and can under-count wide structured drift (the "50 of 84 rows
don't tie" class of defect). This script checks tabular data EXHAUSTIVELY and prints ONLY the diffs,
so the model reviews a short report instead of loading every CSV/xlsx into context. Cheap in tokens,
seconds in wall-clock.

It does two things:

  entities <world_dir>   For every ID key shared by two or more tables, join the tables on that key
                         and report every field that carries DIFFERENT values for the SAME entity
                         across files. (Cross-file personnel/number drift.)

  footing  <path>        Within each table, find "total"-labeled rows/columns and check they equal
                         the sum of their numeric components. Reports every total that does not foot.

  all      <world_dir>   Run both over a folder.

Each reported diff is a CANDIDATE, not a verdict: classify it as a spec-declared trap (leave it) or
real drift (fix it). Deliberately conservative, it flags, it never edits.

Deps: pandas + openpyxl (xlsx). CSVs work with pandas alone. Missing openpyxl -> xlsx skipped w/ note.

Examples:
  python reconcile_entities.py entities /path/to/world
  python reconcile_entities.py entities /path/to/world --key employee_id
  python reconcile_entities.py footing  /path/to/world/payroll.xlsx
  python reconcile_entities.py all      /path/to/world
"""
import argparse
import io
import os
import re
import sys
import _common
_common.setup_console()

try:
    import pandas as pd
except ImportError:
    sys.exit("reconcile_entities.py needs pandas: pip install pandas openpyxl")

# The separator class must include SPACE and the other things humans put in a header. Requiring
# start-of-string or an underscore made "Employee ID", "Invoice Number" and "Vendor Code" invisible,
# so on any world using ordinary spaced headers the entity join found no key columns, skipped every
# comparison, and printed a clean summary.
# Anchored at the END. A key column is named for what it is LAST: "Employee ID", "Invoice Number",
# "Vendor Code", "Account No.". Matching the token anywhere pulled in "Number of Units", which then
# joined two tables on a quantity and compared unrelated rows.
ID_HINT = re.compile(r"(?:^|[\s_\-.])(id|record|number|no|num|code|key|uid|ssn)[\s_\-.]*$", re.I)
TOTAL_HINT = re.compile(r"\b(total|grand\s*total|sum|subtotal)\b", re.I)
# Columns that hold numbers but do NOT sum to a total, foot-checking them is pure noise.
NONADDITIVE = re.compile(r"\b(year|yr|date|rate|ratio|pct|percent|id|no|num(ber)?|qty|quantity|"
                         r"unit|per[\s_-]?unit|hours?|age|zip|postal|phone|week|day|month|"
                         r"count|headcount|fte|score|index)\b", re.I)


def norm(col):
    return re.sub(r"[^a-z0-9]", "", str(col).lower())


def load_tables(path):
    """Yield (label, DataFrame). A .csv is one table; an .xlsx yields one per sheet."""
    tables = []
    if os.path.isfile(path):
        files = [path]
    else:
        files = []
        for root, _, names in os.walk(path):
            for n in names:
                if n.lower().endswith((".csv", ".tsv", ".xlsx", ".xlsm")):
                    files.append(os.path.join(root, n))
    skipped = 0
    for f in sorted(files):
        if _common.is_qc_artifact(f):
            continue
        base = os.path.relpath(f, path if os.path.isdir(path) else os.path.dirname(f))
        try:
            if f.lower().endswith((".csv", ".tsv")):
                sep = "\t" if f.lower().endswith(".tsv") else ","
                # decode with the real-world fallback chain (cp1252 CSVs are common and would
                # otherwise be silently dropped), then hand pandas a decoded buffer.
                text = _common.read_text(f)
                tables.append((base, pd.read_csv(io.StringIO(text), sep=sep, dtype=str, keep_default_na=False)))
            else:
                xl = pd.ExcelFile(f)
                for sh in xl.sheet_names:
                    df = xl.parse(sh, dtype=str, keep_default_na=False)
                    tables.append((f"{base}::{sh}", df))
        except Exception as e:  # noqa
            skipped += 1
            print(f"  ! skipped {base}: {e}", file=sys.stderr)
    if skipped:
        print(f"({skipped} file(s) unreadable and skipped, see messages above; results are INCOMPLETE)")
    return tables


def id_columns(df):
    return [c for c in df.columns if ID_HINT.search(str(c)) and df[c].astype(str).str.strip().ne("").any()]


def reconcile_entities(path, forced_key=None):
    tables = load_tables(path)
    if not tables:
        print("No tabular files found.")
        return
    # Map normalized-key -> list of (label, df, actual_col)
    key_index = {}
    for label, df in tables:
        cols = [c for c in df.columns if norm(c) == norm(forced_key)] if forced_key else id_columns(df)
        for c in cols:
            key_index.setdefault(norm(c), []).append((label, df, c))

    diffs = 0
    for keyn, carriers in sorted(key_index.items()):
        if len(carriers) < 2:
            continue  # a key present in only one table can't be cross-checked
        # Shared non-key columns (by normalized name) present in >=2 carriers
        colsets = []
        for label, df, kc in carriers:
            colsets.append({norm(c): c for c in df.columns if norm(c) != keyn})
        counts = {}
        for cs in colsets:
            for name in cs:
                counts[name] = counts.get(name, 0) + 1
        shared = {name for name, cnt in counts.items() if cnt >= 2}
        if not shared:
            continue
        # Build per-entity value maps
        print(f"\n=== key '{keyn}' across {len(carriers)} tables: "
              f"{', '.join(l for l,_,_ in carriers)} ===")
        # entity -> field -> {value: [tables]}
        for fieldn in sorted(shared):
            entity_vals = {}
            for (label, df, kc), cs in zip(carriers, colsets):
                if fieldn not in cs:
                    continue
                fc = cs[fieldn]
                for _, row in df.iterrows():
                    ent = str(row[kc]).strip()
                    if ent == "":
                        continue
                    val = str(row[fc]).strip()
                    entity_vals.setdefault(ent, {}).setdefault(val, []).append(label)
            for ent, vals in sorted(entity_vals.items()):
                nonempty = {v: t for v, t in vals.items() if v != ""}
                if len(nonempty) > 1:
                    diffs += 1
                    field_disp = next(cs[fieldn] for cs in colsets if fieldn in cs)
                    print(f"  [MISMATCH] {ent} · field '{field_disp}':")
                    for v, ts in nonempty.items():
                        print(f"      {v!r:<30} in {', '.join(ts)}")
    print(f"\n--- {diffs} cross-file field mismatch(es). Classify each: spec-declared trap vs. drift. ---")


def _to_num(x):
    x = str(x).replace(",", "").replace("$", "").strip()
    neg = x.startswith("(") and x.endswith(")")
    if neg:
        x = x[1:-1].strip()
    if x in ("", "-", "—"):
        return None
    try:
        v = float(x)
        return -v if neg else v
    except ValueError:
        return None


def check_footing(path):
    tables = load_tables(path)
    if not tables:
        print("No tabular files found.")
        return
    problems = 0
    for label, df in tables:
        # numeric columns that are plausibly ADDITIVE (skip year/rate/qty/id/percent etc, they hold
        # numbers but never sum to a total, so foot-checking them is noise that buries real misses).
        numcols = []
        for c in df.columns:
            if NONADDITIVE.search(str(c)):
                continue
            nums = [_to_num(v) for v in df[c]]
            if sum(1 for n in nums if n is not None) >= 2:
                numcols.append((c, nums))
        # find rows whose any cell matches TOTAL_HINT
        first_col = df.columns[0] if len(df.columns) else None
        for ridx in range(len(df)):
            rowvals = [str(v) for v in df.iloc[ridx].tolist()]
            if any(TOTAL_HINT.search(v) for v in rowvals):
                for c, nums in numcols:
                    total = nums[ridx]
                    if total is None:
                        continue
                    # BLOCK-AWARE: only sum the contiguous run of numbers directly ABOVE this total,
                    # stopping at a blank/non-numeric row or another total row. Real report sheets
                    # stack several sub-tables in one column, so summing the whole column is wrong.
                    block = []
                    for i in range(ridx - 1, -1, -1):
                        rlabel = " ".join(str(v) for v in df.iloc[i].tolist())
                        if TOTAL_HINT.search(rlabel):
                            break                      # previous total = block boundary
                        if nums[i] is None:
                            # An ENTIRELY EMPTY row is a spacer, not the end of the schedule.
                            # Treating it as a boundary reported correct totals as broken, and the
                            # cheap way people close a false footing finding is to add a
                            # reconciling sentence, which is real answer leakage. A row that has
                            # text but no number in this column is still a genuine boundary.
                            if rlabel.replace("nan", "").strip():
                                break
                            continue
                        block.append(nums[i])
                    # Second reading: a GRAND total that legitimately spans one or more subtotals.
                    # "A 10 / B 20 / Subtotal 30 / C 40 / D 50 / Total 120" foots perfectly, but
                    # the contiguous block stops at the subtotal and sees only 90. Sum the plain
                    # component rows back to the section start instead, skipping every total row.
                    # A total is a mismatch only if NEITHER reading explains it.
                    spanning = []
                    for i in range(ridx - 1, -1, -1):
                        rlabel2 = " ".join(str(v) for v in df.iloc[i].tolist())
                        if nums[i] is None:
                            if rlabel2.replace("nan", "").strip():
                                break
                            continue
                        if TOTAL_HINT.search(rlabel2):
                            continue                   # a subtotal is not a component
                        spanning.append(nums[i])

                    if len(block) < 2:
                        continue                       # not a real footed block
                    # A block of equal values is NOT proof that the column is a constant rather
                    # than components: monthly rent, equal instalments and repeated fees are
                    # everywhere in these corpora, and skipping them hid real breaks
                    # (500 + 500 stated as 1,200 reported clean). Only skip when the total also
                    # equals one component, which is the actual constant-column signature.
                    if len(set(block)) == 1 and abs(block[0] - total) <= 0.01:
                        continue
                    component = sum(block)
                    delta = round(component - total, 2)
                    # If the spanning reading foots, the total is fine and this is not a finding.
                    if len(spanning) >= 2 and abs(round(sum(spanning) - total, 2)) <= 0.01:
                        continue
                    if abs(delta) > 0.01:
                        problems += 1
                        keyname = rowvals[0] if first_col is not None else "?"
                        print(f"[FOOTING] {label} · total row '{keyname}' · col '{c}': "
                              f"stated {total:,.2f} vs. block of {len(block)} above = {component:,.2f} "
                              f"(delta {delta:+,.2f})")
    print(f"\n--- {problems} footing mismatch(es). Classify each: spec-declared vs. real drift. ---")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("entities"); e.add_argument("path"); e.add_argument("--key", default=None)
    f = sub.add_parser("footing"); f.add_argument("path")
    a = sub.add_parser("all"); a.add_argument("path"); a.add_argument("--key", default=None)
    args = ap.parse_args()
    if args.cmd == "entities":
        reconcile_entities(args.path, args.key)
    elif args.cmd == "footing":
        check_footing(args.path)
    elif args.cmd == "all":
        print("### ENTITY RECONCILIATION ###")
        reconcile_entities(args.path, args.key)
        print("\n### FOOTING ###")
        check_footing(args.path)


if __name__ == "__main__":
    main()
