#!/usr/bin/env python3
"""blast_radius.py - the structural pass. Why a defect class keeps coming back.

WHY THIS EXISTS
---------------
When round_log.py reports the same defect class for the third time, fixing the newly-named files
again is the wrong move. Something is making the class regenerate. This script finds out what,
without guessing and without reading the corpus with a model.

It answers the two questions a chronic class always turns on:

  1. Did the earlier sweeps actually finish?
     For every value this skill has ever changed, is the OLD value still sitting somewhere else in
     the corpus? If yes, the class was fixed file by file. That is the whole diagnosis, and the
     stale list is the fix list.

  2. Did fixing one thing break another?
     Every edit has a blast radius. A number that was changed in one file is very often a component
     of a total in that same file, a tie to a value in another file, or a date other dates derive
     from. This lists every file that carries the NEW value but was never edited, and re-foots every
     file this skill has touched across all rounds.

WHAT IT READS
-------------
`change_manifest.md` in the world's sibling `_qc_backup` folder. Every writer in this skill appends
to it, so it is the complete record of what has been changed, across every round. If the manifest is
missing, this skill has not written to the world yet and there is nothing to trace.

WHAT IT NEVER DOES
------------------
It does not edit anything. It is a read-only diagnostic. The fixing is still done by the class
fixers, at the value level, after this tells you what the level is.

USAGE
-----
    python blast_radius.py stale   <world>            # old values still present elsewhere
    python blast_radius.py touched <world>            # re-foot every file ever edited
    python blast_radius.py all     <world>            # both, with a verdict

Add --value "<string>" to trace one specific value instead of the whole manifest.
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import scan_world  # noqa: E402

_common.setup_console()

SCRIPTS = os.path.dirname(os.path.abspath(__file__))

# The change manifest table row written by _common.append_manifest:
#   | file | location | old | -> | new |
ROW = re.compile(r"^\|\s*(?P<file>[^|]+?)\s*\|\s*(?P<loc>[^|]*?)\s*\|\s*(?P<old>[^|]*?)\s*\|"
                 r"\s*(?:->|→)\s*\|\s*(?P<new>[^|]*?)\s*\|\s*$")

# A value has to be distinctive enough that finding it again means something. One or two characters,
# or a bare number under three digits, matches half the corpus by accident and would bury the real
# hits in noise.
def searchable(v):
    v = (v or "").strip()
    if len(v) < 3:
        return False
    if not re.search(r"[A-Za-z0-9]", v):
        return False
    if re.fullmatch(r"\d{1,2}", v):
        return False
    return True


def manifest_path(world):
    return os.path.join(_common.default_backup_dir(world), "change_manifest.md")


def read_manifest(world):
    """Return [(tool, file, location, old, new)] for every change ever recorded."""
    mp = manifest_path(world)
    if not os.path.exists(mp):
        print(f"No change manifest at {mp}.")
        print("This skill has not written to this world yet, so there are no earlier fixes to trace.")
        print("If a class is repeating and nothing has been changed by these scripts, the earlier")
        print("fixes were made by hand. Trace them with:  blast_radius.py stale <world> --value \"<old value>\"")
        sys.exit(2)
    tool = "(unknown)"
    out = []
    for line in _common.read_text(mp).splitlines():
        if line.startswith("## "):
            tool = line[3:].strip()
            continue
        m = ROW.match(line)
        if not m:
            continue
        d = m.groupdict()
        if d["file"].lower() in ("file", "---", ":---") or d["old"].lower() == "old":
            continue  # header/separator row
        out.append((tool, d["file"], d["loc"], d["old"], d["new"]))
    return out


def load_corpus(world):
    """Extract every file's text once. {abs_path: [(location, text), ...]}"""
    corpus = {}
    for f in scan_world.iter_files(world):
        chunks = scan_world.extract_chunks(f)
        if chunks:
            corpus[f] = chunks
    return corpus


def _occurrences(hay, needle):
    """Start offsets of `needle` in `hay`, as a WHOLE value.

    Plain substring matching made "327" match inside "3270" and "0.327", so a sweep that was
    complete reported as incomplete and the user went hunting for hits that do not exist.
    """
    if not needle:
        return []
    numeric = any(c.isdigit() for c in needle)
    if numeric:
        pat = r"(?<![\w.,])" + re.escape(needle) + r"(?![\w.,]?\d)"
    else:
        pat = r"(?<!\w)" + re.escape(needle) + r"(?!\w)"
    return [m.start() for m in re.finditer(pat, hay, re.I)]


def _stale_in(text, old, new):
    """True if `old` survives in `text` somewhere that is NOT part of an occurrence of `new`.

    The old test was `if old in new: hits = []`, which threw away EVERY hit for the whole run.
    Widening a number (1000 -> 10000) and extending a name (Reyas -> Marta Reyas Jr) are the two
    commonest replacement shapes, so the whack-a-mole detector went blind on exactly the cases it
    exists for: it reported "the sweeps were complete" over a file still carrying the old value.
    """
    hay = str(text)
    olds = _occurrences(hay, old)
    if not olds:
        return False
    if not new or old.lower() not in new.lower():
        return True
    # Cover the spans occupied by the replacement, then ask whether any old hit sits outside them.
    covered = []
    for st in _occurrences(hay, new):
        covered.append((st, st + len(new)))
    for st in olds:
        end = st + len(old)
        if not any(cs <= st and end <= ce for cs, ce in covered):
            return True
    return False


def find(corpus, value, world, new=None):
    """[(relative_path, location, text)] for every place `value` survives as a whole value."""
    hits = []
    for path, chunks in corpus.items():
        rel = os.path.relpath(path, world)
        if _stale_in(os.path.basename(path), value, new):
            hits.append((rel, "filename", os.path.basename(path)))
        for loc, text in chunks:
            if text and _stale_in(str(text), value, new):
                hits.append((rel, loc, str(text).strip()[:110]))
    return hits


def cmd_stale(args, corpus=None, quiet=False):
    """Old values that are still in the corpus. The whack-a-mole detector."""
    world = args.world
    corpus = corpus if corpus is not None else load_corpus(world)

    if args.value:
        pairs = [("(manual)", "", "", args.value, "")]
    else:
        pairs = read_manifest(world)

    # De-duplicate on the old value: the same swap applied to nine files is one thing to check.
    seen, checks = set(), []
    for tool, f, loc, old, new in pairs:
        if not searchable(old):
            continue
        if old in seen:
            continue
        seen.add(old)
        checks.append((old, new, tool))

    if not checks:
        print("Nothing in the manifest is distinctive enough to trace (all values too short).")
        return []

    findings = []
    for old, new, tool in checks:
        # `find` excludes hits that are part of the replacement text, per occurrence, so a
        # replacement that CONTAINS the old value no longer suppresses the whole file.
        hits = find(corpus, old, world, new=new)
        if hits:
            findings.append((old, new, tool, hits))

    if not quiet:
        print("=" * 78)
        print("STALE VALUES - old values this skill replaced that are still in the corpus")
        print("=" * 78)
    if not findings:
        if not quiet:
            print(f"\nChecked {len(checks)} replaced value(s). None of them are still present.")
            print("The earlier sweeps were complete. The repeat has a different cause - see the")
            print("verdict from `blast_radius.py all`.")
        return []

    if not quiet:
        print(f"\n{len(findings)} of {len(checks)} replaced value(s) are STILL PRESENT elsewhere.\n")
        for old, new, tool, hits in findings:
            files = sorted({h[0] for h in hits})
            print(f'  "{old}"  ->  "{new}"   ({tool})')
            print(f"    still in {len(files)} file(s):")
            for rel in files[:15]:
                locs = [h[1] for h in hits if h[0] == rel][:4]
                print(f"      {rel}   [{', '.join(locs)}]")
            if len(files) > 15:
                print(f"      ... and {len(files) - 15} more")
            print()
        print("-" * 78)
        print("This is the diagnosis. A value that was replaced in one file and left standing in")
        print("another was fixed at the instance level, not the class level - which is exactly why")
        print("the class keeps coming back. Fix every file listed above in one pass, then re-run.")
        print("-" * 78)
    return findings


def cmd_touched(args, corpus=None, quiet=False):
    """Every file this skill has ever edited: re-foot it, and find who else carries the new value."""
    world = args.world
    corpus = corpus if corpus is not None else load_corpus(world)
    pairs = read_manifest(world)
    if not pairs:
        print("The change manifest has no recorded changes.")
        return [], []

    edited = sorted({f for _, f, _, _, _ in pairs})
    edited_base = {os.path.basename(f).lower() for f in edited}

    if not quiet:
        print("=" * 78)
        print(f"BLAST RADIUS - {len(edited)} file(s) edited across all rounds")
        print("=" * 78)

    # 1. Re-foot every edited file. A changed number is very often a component of a total in its own
    #    file; fixing the number without re-footing the total is the commonest self-inflicted defect.
    foot_problems = []
    for f in edited:
        full = None
        for path in corpus:
            if os.path.basename(path).lower() == os.path.basename(f).lower():
                full = path
                break
        if not full:
            continue
        if os.path.splitext(full)[1].lower() not in (".xlsx", ".xlsm", ".csv", ".tsv"):
            continue
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "reconcile_entities.py"), "footing", full],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        # Parse the count out of reconcile_entities' summary line rather than grepping for the word
        # "mismatch" - its clean-run summary says "0 footing mismatch(es)", which a naive grep reads
        # as a problem and turns every clean file into a false alarm.
        m = re.search(r"(\d+)\s+footing mismatch", out, re.IGNORECASE)
        if m:
            if int(m.group(1)) > 0:
                foot_problems.append((os.path.relpath(full, world), out.strip()))
        elif re.search(r"^\[FOOTING\]", out, re.MULTILINE):
            foot_problems.append((os.path.relpath(full, world), out.strip()))

    if not quiet:
        if foot_problems:
            print(f"\nFOOTING BROKE IN {len(foot_problems)} EDITED FILE(S):\n")
            for rel, out in foot_problems:
                print(f"  {rel}")
                for ln in out.splitlines()[:6]:
                    print(f"      {ln}")
                print()
            print("  A value was changed without re-footing the total above or below it.")
        else:
            print("\nFooting: every edited spreadsheet still foots.")

    # 2. Who else carries the new value and was never edited? Those files were either already correct
    #    or they are the other half of a tie that nobody checked.
    untouched = []
    seen = set()
    for tool, f, loc, old, new in pairs:
        if not searchable(new) or new in seen:
            continue
        seen.add(new)
        hits = find(corpus, new, world)
        others = sorted({h[0] for h in hits
                         if os.path.basename(h[0]).lower() not in edited_base})
        if others:
            untouched.append((new, others))

    if not quiet:
        if untouched:
            print(f"\nDEPENDENCY SET - {len(untouched)} changed value(s) also appear in files that were")
            print("never edited. Confirm each of these agrees with the new value on purpose:\n")
            for new, others in untouched[:20]:
                print(f'  "{new}"  also in: {", ".join(others[:8])}'
                      + (f" (+{len(others) - 8} more)" if len(others) > 8 else ""))
            if len(untouched) > 20:
                print(f"  ... and {len(untouched) - 20} more values")
        else:
            print("\nDependency set: no changed value appears in an unedited file.")
    return foot_problems, untouched


def cmd_all(args):
    world = args.world
    if not os.path.isdir(world):
        print(f"ERROR: world folder not found: {world}")
        sys.exit(2)
    print(f"Loading the corpus from {world} ...")
    corpus = load_corpus(world)
    print(f"{len(corpus)} readable file(s).\n")

    stale = cmd_stale(args, corpus=corpus)
    print()
    foot, untouched = cmd_touched(args, corpus=corpus)

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    if stale:
        n = sum(len({h[0] for h in hits}) for _, _, _, hits in stale)
        print(f"\nThe sweeps were incomplete. {len(stale)} replaced value(s) are still standing in")
        print(f"{n} file reference(s). That is why the class keeps coming back.")
        print("\nWhat to do: fix every file in the stale list above, in one pass, before you upload.")
        print("Do not fix only the files this round's AutoQC report named.")
    elif foot:
        print(f"\nThe sweeps were complete, but {len(foot)} edited file(s) no longer foot. The earlier")
        print("fixes changed a component without re-footing its total, which generates a fresh")
        print("finding every round.")
        print("\nWhat to do: re-foot those files, then re-verify the totals against the spec's")
        print("canonical values with `spec_check.py ties`.")
    elif untouched:
        print("\nThe sweeps were complete and everything foots. The most likely remaining cause is a")
        print("tie: a value was corrected in the files that were edited, and the files listed in the")
        print("dependency set carry it too but were never checked.")
        print("\nWhat to do: run `spec_check.py ties <spec> <world>` and confirm every file in the")
        print("dependency set agrees with the canonical value.")
    else:
        print("\nNothing structural on this side. Earlier fixes were complete, files foot, and no")
        print("changed value is loose in an unedited file.")
        print("\nWhat to do: the cause is upstream of the files you can edit. Escalate to your world")
        print("lead with these specifics: the class name, the rounds it appeared in, and the fact")
        print("that a blast-radius pass found no stale values, no broken footing, and no loose")
        print("dependencies. Ask whether the corpus is being regenerated over remediated files, and")
        print("whether the spec declares the value the findings keep disputing.")
    print()


def main():
    p = argparse.ArgumentParser(
        description="Structural pass: why a defect class keeps coming back. Read-only.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Reads the change manifest in the world's sibling _qc_backup folder. Edits nothing.")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, fn, helptext in (
            ("stale", cmd_stale, "old values this skill replaced that are still in the corpus"),
            ("touched", cmd_touched, "re-foot every edited file; find who else carries the new values"),
            ("all", cmd_all, "both, with a plain-English verdict")):
        s = sub.add_parser(name, help=helptext)
        s.add_argument("world")
        s.add_argument("--value", default="", help="trace one specific value instead of the manifest")
        s.set_defaults(func=fn)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
