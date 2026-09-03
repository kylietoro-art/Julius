#!/usr/bin/env python3
"""leak_scan.py, find files that give away a task's answer or defuse a trap.

WHY THIS EXISTS
---------------
Answer leakage was present in 61% of the worlds that went past 20 AutoQC rounds, the third most common
defect class. Until now this toolkit had a rule against writing it and nothing at all that found it.

There are two sources and both matter:

  1. The pipeline generated it. A document states the conclusion the task is supposed to derive.
  2. **Remediation added it.** This is the one that surprised people. A finding says two figures do
     not reconcile, and the cheapest way to close that finding is to write a sentence explaining why
     they differ. Real case:

         "Added an explicit bridge to note 4 stating that the capex plan's $14.0M is gross D&A on
          FY2025 additions while the AOP's $12.0M is the net increase over FY2024, and that the two
          are not additive."

     That is three violations at once. It added text rather than replacing. It hands the solver the
     reconciliation they were meant to work out. And if that pair was a registered trap, it killed it.

WHAT THIS IS NOT
----------------
Not a verdict. Leakage is semantic and no pattern match settles it. Every hit is a **candidate** with
the file, the line and the reason, for a human to judge. Same contract as `pdf_markup_scan.py`.

The trap check is the exception worth trusting most: it uses the spec's own declared trap values, so
a hit means a file states two sides of a designed discrepancy in one breath.

USAGE
-----
    python leak_scan.py <world>                    phrase and filename checks only
    python leak_scan.py <world> --spec <spec.xlsx> adds the trap-defusal check, much stronger

EXIT CODES
----------
    0  nothing flagged
    1  candidates found, read them
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import corpus  # noqa: E402
import scan_world  # noqa: E402

_common.setup_console()

# --------------------------------------------------------------------------------------------------
# 1. Reconciling language. The signature of the bridge-note failure: a sentence that carries two
#    different figures and a connective whose job is to explain the gap between them. A real in-world
#    document states a number. It does not usually pause to explain why it differs from another
#    document's number, because the in-world author had no reason to compare them.
# --------------------------------------------------------------------------------------------------
BRIDGE = [
    (r"\bnot\s+additive\b", "says two figures are not additive"),
    (r"\bbridge\b", "the word bridge"),
    (r"\breconcil\w*\b", "reconciliation language"),
    (r"\bthe\s+difference\s+(?:between|is|represents|reflects)\b", "explains the difference"),
    (r"\bwhereas\s+the\b", "whereas the"),
    (r"\bwhile\s+the\s+\w+(?:'s)?\s+\$?[\d,.]+", "while the X is Y"),
    (r"\bgross\b[^.]{0,60}\bwhile\b[^.]{0,60}\bnet\b", "gross versus net in one sentence"),
    (r"\bfor\s+clarity\b", "for clarity"),
    (r"\bto\s+clarify\b", "to clarify"),
    (r"\bshould\s+not\s+be\s+(?:added|combined|summed)\b", "tells the reader not to combine"),
    (r"\brepresents\s+the\s+(?:net|gross|difference)\b", "represents the net/gross/difference"),
]

# 2. Conclusion voice. A document announcing the answer rather than recording a fact.
CONCLUSION = [
    (r"\bthe\s+correct\s+(?:answer|value|figure|amount|treatment)\b", "states the correct answer"),
    (r"\bthe\s+answer\s+is\b", "the answer is"),
    (r"\bas\s+calculated\s+above\b", "as calculated above"),
    (r"\btherefore\s+the\s+\w+\s+(?:is|should)\b", "therefore the X is"),
    (r"\bthis\s+confirms\s+that\b", "this confirms that"),
    (r"\bwhich\s+governs\b", "says which source governs"),
    (r"\bis\s+authoritative\b", "declares a source authoritative"),
    (r"\btakes\s+precedence\s+over\b", "takes precedence over"),
    (r"\bsupersedes\s+the\b", "supersedes the"),
    (r"\bthe\s+governing\s+(?:figure|value|number|source)\b", "the governing figure"),
    (r"\bunderstates?\s+(?:the\s+)?\w+\s+by\b", "understates X by"),
    (r"\boverstates?\s+(?:the\s+)?\w+\s+by\b", "overstates X by"),
    (r"\bcorrected\b", "the word corrected"),
    (r"\(\s*see\s+also\b", "see also pointer"),
]

# 3. Filenames a model will preferentially open, because they announce themselves as the answer.
FILENAME_TELLS = ["validated", "final", "approved", "correct", "answer", "solution", "reconciled",
                  "verified", "master copy", "goldenttruth", "ground truth", "truth"]


def sentences(text):
    """Rough sentence split. Good enough to keep a hit and its context together."""
    for part in re.split(r"(?<=[.!?])\s+|\n", text):
        p = part.strip()
        if p:
            yield p


MONEY = re.compile(r"\$?\s?\d[\d,]*(?:\.\d+)?\s?(?:%|[MBK]\b|million|billion|thousand)?")


def two_figures(s):
    """Does one sentence carry two DIFFERENT numbers? The bridge note always does."""
    vals = {m.group(0).strip() for m in MONEY.finditer(s) if any(c.isdigit() for c in m.group(0))}
    return len(vals) >= 2


def trap_values(spec):
    """Every number the spec declares as part of a trap, grouped by trap.

    Reuses `spec_check.canonical_rows` and `build_manifest` rather than reading the sheet by hand.
    The first version of this parsed its own headers, asked find_header for only two columns, and so
    never saw the Type or Note columns: it returned an empty trap list and the strongest check in the
    script silently did nothing. Reuse the readers the tie checks already use, so a spec layout that
    works there works here.

    These are the strongest signal in the whole script. A file that states two sides of a declared
    trap in one sentence is not describing a world, it is explaining the puzzle away.
    """
    import spec_check
    groups = []
    try:
        wb = spec_check.load(spec)
    except Exception as e:  # noqa: BLE001
        print(f"[note] could not open the spec: {e}", file=sys.stderr)
        return groups

    def nums_in(*parts):
        blob = " ".join(str(p or "") for p in parts)
        return sorted({m.group(0).strip() for m in MONEY.finditer(blob)
                       if any(c.isdigit() for c in m.group(0))})

    # Read ② directly, asking for every column we need INCLUDING Note. `canonical_rows` only maps
    # the needles it is given and Note is not one of them, so its `note` field is always empty. The
    # trap's second figure usually lives in exactly that Note, so going through canonical_rows here
    # loses the very thing this check is looking for.
    try:
        cv = spec_check.sheet(wb, "Canonical", "②")
        if cv:
            hi, cm = spec_check.find_header(cv, ["Value name", "Type", "Value", "Note"])
            if not hi:
                print("[WARNING] The spec's Canonical Values tab has no row containing all of "
                      "'Value name', 'Type', 'Value' and 'Note'.\n"
                      "          The trap-defusal check, the strongest one here, did NOTHING. "
                      "A clean report below is not evidence.\n"
                      "          Check those column names in the spec.", file=sys.stderr)
            if hi:
                for row in spec_check.rows_after(cv, hi):
                    typ = spec_check.cell(row, cm.get(spec_check.norm("Type")))
                    if "trap" not in (typ or "").lower():
                        continue
                    name = spec_check.cell(row, cm.get(spec_check.norm("Value name")))
                    val = spec_check.cell(row, cm.get(spec_check.norm("Value")))
                    note = spec_check.cell(row, cm.get(spec_check.norm("Note")))
                    nums = nums_in(val, note)
                    if len(nums) >= 2:
                        groups.append((name or val or "declared trap", nums))
    except Exception as e:  # noqa: BLE001
        print(f"[note] could not read canonical trap rows: {e}", file=sys.stderr)

    # Trap prose on ③ Tasks and ④ Artifacts often names both sides too.
    try:
        for m in spec_check.build_manifest(wb):
            nums = nums_in(m.get("detail"))
            if len(nums) >= 2:
                label = f"{m.get('source','')} {m.get('artifact','')}".strip()
                groups.append((label or "declared trap", nums))
    except Exception as e:  # noqa: BLE001
        print(f"[note] could not read the trap manifest: {e}", file=sys.stderr)

    return groups


def _is_year(v):
    """A four-digit year on its own, e.g. 2025 but not 2,025 or $2025.00."""
    d = re.sub(r"[^\d]", "", v)
    return len(d) == 4 and 1900 <= int(d) <= 2100 and not re.search(r"[.,$%]", v)


def _num_present(v, blob):
    """Whole-value match. A raw substring test made '670.0' match inside '1,670.05', so ordinary
    unrelated figures were reported as leaked answers."""
    vl = v.lower().strip()
    if not vl:
        return False
    # Case-insensitive on its own account. This used to depend on the caller having lowercased
    # the haystack first, an implicit contract that would silently stop matching the day a new
    # caller forgot it: "$670.0M" would simply never be found and the check would read clean.
    if not any(c.isdigit() for c in vl):
        return vl in blob.lower()
    return re.search(r"(?<![\d.,])" + re.escape(vl) + r"(?![\d.,]?\d)", blob, re.I) is not None


def task_answers(spec):
    """[(task_id, [answer values], {artifact ids the agent is meant to derive it from})].

    This is the check that catches the leak a pattern scanner never will. Bryan found $670.0M sitting
    on slide 22 of a board pack. It is T1's answer, and the agent is supposed to derive it from the
    Credit Agreement. There is no reconciling language, no conclusion voice, no filename tell: it is a
    bare number in a bullet, and no amount of phrase matching finds it.

    But the spec knows the answer, and the spec knows which artifacts carry the derivation. So the
    check is not "does this sentence look like leakage", it is "is a task's answer sitting in a file
    that is not part of that task's evidence".
    """
    import spec_check
    out = []
    try:
        wb = spec_check.load(spec)
        t = spec_check.sheet(wb, "Tasks", "③")
        if not t:
            return out
        hi, cm = spec_check.find_header(t, ["Task", "Primary Artifacts", "Expected Output"])
        if not hi:
            hi, cm = spec_check.find_header(t, ["Task", "Expected Output"])
        if not hi:
            print("[WARNING] The spec's Tasks tab has no row containing all of 'Task', "
                  "'Primary Artifacts' and 'Expected Output'.\n"
                  "          The task-answer leak check did NOTHING. A clean report below "
                  "is not evidence.", file=sys.stderr)
            return out
        for row in spec_check.rows_after(t, hi):
            tid = spec_check.cell(row, cm.get(spec_check.norm("Task")))
            if not tid or spec_check.PLACEHOLDER.match(tid):
                continue
            exp = spec_check.cell(row, cm.get(spec_check.norm("Expected Output"))) or ""
            prim = spec_check.cell(row, cm.get(spec_check.norm("Primary Artifacts"))) or ""
            vals = sorted({m.group(0).strip() for m in MONEY.finditer(str(exp))
                           if any(c.isdigit() for c in m.group(0))
                           # a bare 1 or 2 digit number is not an answer worth tracing
                           and len(re.sub(r"[^\d]", "", m.group(0))) >= 3
                           # and neither is a bare year: every file in the world mentions the
                           # fiscal year, so keeping those flagged all of them under the report's
                           # loudest heading and buried the real leak among the noise
                           and not _is_year(m.group(0).strip())})
            if vals:
                out.append((tid, vals, set(spec_check.ID_RE.findall(prim))))
    except Exception as e:  # noqa: BLE001
        print(f"[note] could not read task answers from the spec: {e}", file=sys.stderr)
    return out


def scan(world, spec=None):
    hits = {"answer": [], "trap": [], "trap_weak": [], "bridge": [], "conclusion": [], "filename": []}
    traps = trap_values(spec) if spec else []
    answers = task_answers(spec) if spec else []
    art_of = {}
    if spec:
        try:
            import spec_check
            for aid, a in spec_check.artifact_index(spec_check.load(spec)).items():
                pth = spec_check.resolve_path(world, a.get("loc"), a.get("name"))
                if pth:
                    art_of[os.path.relpath(pth, world).replace("\\", "/")] = aid
        except Exception as e:  # noqa: BLE001
            print(f"[note] could not map artifacts to files: {e}", file=sys.stderr)

    # One cached extraction shared by every check below. Re-extracting a 51-file corpus per run is
    # what made an earlier version of this time out.
    docs = corpus.load(world)

    for rel, chunks in docs.items():
        base = os.path.basename(rel).lower()

        for tell in FILENAME_TELLS:
            if tell in base:
                hits["filename"].append((rel, tell))
                break

        if not chunks:
            continue

        # A task's answer sitting in a file that is not that task's evidence.
        this_art = art_of.get(rel)
        blob = " ".join(str(t) for _, t in chunks if t).lower()
        for tid, vals, prim in answers:
            if this_art and this_art in prim:
                continue                      # this file IS the derivation, the value belongs here
            found = [v for v in vals if _num_present(v, blob)]
            if found:
                where = next((l for l, t in chunks if t and any(v.lower() in str(t).lower()
                                                                for v in found)), "?")
                hits["answer"].append((rel, where, tid, found, this_art or "unregistered"))

        for loc, text in chunks:
            if not text:
                continue
            for s in sentences(str(text)):
                if len(s) > 600:
                    s = s[:600]
                low = s.lower()

                # Does this sentence carry reconciling language? Used twice below.
                bridge_why = None
                for rx, why in BRIDGE:
                    if re.search(rx, low):
                        bridge_why = why
                        break

                # Trap check, two tiers. Both values plus reconciling language means the discrepancy
                # is being explained away, and that is near-certain trap death. Both values on their
                # own is much weaker: a real document can legitimately put two figures side by side,
                # like revenue against plan, without touching the trap at all. Reporting those two at
                # the same volume would bury the real hits, so they are separated.
                for tval, nums in traps:
                    present = [n for n in nums if n.lower() in low]
                    if len(present) >= 2:
                        if bridge_why:
                            hits["trap"].append((rel, loc, tval, present, bridge_why, s.strip()[:220]))
                        else:
                            hits["trap_weak"].append((rel, loc, tval, present, s.strip()[:220]))
                        break

                if bridge_why and two_figures(s):
                    hits["bridge"].append((rel, loc, bridge_why, s.strip()[:220]))
                for rx, why in CONCLUSION:
                    if re.search(rx, low):
                        hits["conclusion"].append((rel, loc, why, s.strip()[:220]))
                        break
    return hits


def main():
    p = argparse.ArgumentParser(
        description="Find candidate answer leakage and defused traps. Reports, never fixes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Every hit is a candidate for a human to judge, not a verdict.")
    p.add_argument("world")
    p.add_argument("--spec", help="the World Spec .xlsx, enables the trap-defusal check")
    a = p.parse_args()

    if not os.path.isdir(a.world):
        print(f"ERROR: world folder not found: {a.world}")
        sys.exit(2)

    print("=" * 78)
    print("LEAK SCAN")
    print("=" * 78)
    if not a.spec:
        print("\nNo --spec given, so the trap-defusal check is OFF. That is the strongest check here.")
        print("Re-run with --spec <spec.xlsx> to enable it.\n")

    h = scan(a.world, a.spec)
    total = sum(len(v) for v in h.values())
    strong = len(h["answer"]) + len(h["trap"]) + len(h["bridge"])

    if h["answer"]:
        print(f"\nA TASK ANSWER IS SITTING WHERE IT SHOULD NOT BE  ({len(h['answer'])})")
        print("-" * 78)
        print("The spec says this value is a task's expected answer, and here it is in a file that is")
        print("not listed among that task's primary artifacts. An agent that opens this file gets the")
        print("answer without doing the work. This is the leak class that has no linguistic tell, so")
        print("nothing else here would catch it.\n")
        for rel, loc, tid, found, aid in h["answer"][:30]:
            print(f"  {rel}  [{loc}]   ({aid})")
            print(f"    {tid} answer value(s) present: {', '.join(found)}\n")
        print("  Check each: if the file has no business stating the figure, remove it. If it does,")
        print("  the task's primary artifact list in the spec is probably incomplete.\n")

    if h["trap"]:
        print(f"\nTRAP POSSIBLY DEFUSED  ({len(h['trap'])})")
        print("-" * 78)
        print("A file states two sides of a declared trap in one sentence. A real in-world document")
        print("has no reason to compare two figures it was never meant to reconcile. Check each one:")
        print("if the discrepancy is now explained, the trap is dead and the task stops discriminating.\n")
        for rel, loc, tval, present, why, s in h["trap"][:25]:
            print(f"  {rel}  [{loc}]  ({why})")
            print(f"    trap: {tval}   both sides present: {', '.join(present)}")
            print(f"    \"{s}\"\n")

    if h["trap_weak"]:
        print(f"\nBOTH SIDES OF A TRAP IN ONE SENTENCE, no explaining language  ({len(h['trap_weak'])})")
        print("-" * 78)
        print("Weaker signal. A real document can put two figures side by side legitimately, revenue")
        print("against plan for instance. Worth a look, but most of these will be fine.\n")
        for rel, loc, tval, present, s in h["trap_weak"][:15]:
            print(f"  {rel}  [{loc}]   trap: {tval}   ({', '.join(present)})")
            print(f"    \"{s}\"\n")

    if h["bridge"]:
        print(f"\nRECONCILING LANGUAGE  ({len(h['bridge'])})")
        print("-" * 78)
        print("Two different figures in one sentence, plus wording whose job is to explain the gap.")
        print("This is the shape of a bridge note added to close a consistency finding. If it was")
        print("added during remediation, remove it. The reconciliation is the solver's work.\n")
        for rel, loc, why, s in h["bridge"][:25]:
            print(f"  {rel}  [{loc}]  ({why})")
            print(f"    \"{s}\"\n")

    if h["conclusion"]:
        print(f"\nCONCLUSION VOICE  ({len(h['conclusion'])})")
        print("-" * 78)
        print("A document announcing an answer rather than recording a fact. Some of these are fine")
        print("in a real document, so read them. The test is whether the in-world author would have")
        print("written it, or whether it exists to help the reader.\n")
        for rel, loc, why, s in h["conclusion"][:30]:
            print(f"  {rel}  [{loc}]  ({why})")
            print(f"    \"{s}\"\n")

    if h["filename"]:
        print(f"\nFILENAMES THAT ANNOUNCE THEMSELVES  ({len(h['filename'])})")
        print("-" * 78)
        print("A model preferentially opens a file called FINAL or VALIDATED. Rename them.\n")
        for rel, tell in h["filename"][:25]:
            print(f"  {rel}   (contains \"{tell}\")")

    print("\n" + "=" * 78)
    if total:
        print(f"{total} candidate(s), {strong} of them in the two strong categories.")
        print("None of these is a verdict. Read each one and decide.")
        print("Anything you remove: delete the give-away, do not add a hedge.")
    else:
        print("No candidates. That is not proof the corpus is clean: this finds patterns, and the")
        print("worst leakage is a plain statement of fact with no tell in it at all.")
    print("=" * 78)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
