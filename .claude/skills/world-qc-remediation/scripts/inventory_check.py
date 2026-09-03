#!/usr/bin/env python3
"""inventory_check.py, does the world still contain what the spec says it contains?

WHY THIS EXISTS
---------------
The spec's Artifacts registry is the definitive list of what the world holds, and it is what the
"Built Files Match Spec Inventory" dimension is graded against. Nothing else in this toolkit checks
the corpus against it.

Two separate problems this catches:

1. **The build does not match the spec.** A registered artifact that never got generated, a file
   nobody registered, two registry rows pointing at the same file, a row that says .docx over a file
   that is actually .pdf.

2. **Drift across rounds.** The inventory is a fixed list at the first AutoQC run, but it moves during
   remediation: a file gets renamed while fixing a name collision, a PDF gets regenerated under a new
   name, or somebody adds a file. Each round is snapshotted, so the next run can say exactly what
   appeared, disappeared or was renamed since last time.

**A file that appeared is the one to look hardest at.** Adding files during remediation is against
the replace-not-add rule, and it has a measured cost: one world added ambient "no trap" files while
fixing findings and they reopened judgment forks that were already closed, because every new file is
a new place for a number to drift.

USAGE
-----
    python inventory_check.py check <spec.xlsx> <world_folder> [--round N]
    python inventory_check.py drift <world_folder>

`check` reconciles the world against the spec, writes a snapshot, and reports drift since the last
one. `drift` reports drift only and needs no spec.

Snapshots live in the world's sibling `_qc_backup/inventory/` folder, never inside the world.

EXIT CODES
----------
    0  the world matches the spec and nothing drifted unexpectedly
    1  a mismatch or an unexplained change was found
"""
import argparse
import hashlib
import json
import os
import time
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import scan_world  # noqa: E402
import spec_check  # noqa: E402

_common.setup_console()

# Files the build pipeline or the operating system leaves behind that are not world content. They
# should never be reported as unregistered artifacts, but they SHOULD be reported as junk to remove,
# because a grader that walks the tree will see them.
JUNK = {".ds_store", "thumbs.db", "desktop.ini", ".gitkeep"}
JUNK_DIRS = {"__macosx", ".git", "__pycache__", ".meta"}


def is_junk(rel):
    parts = [p.lower() for p in rel.replace("\\", "/").split("/")]
    if any(p in JUNK_DIRS for p in parts[:-1]):
        return True
    return parts[-1].lower() in JUNK or parts[-1].startswith("._")


def world_files(world):
    """[(relative_path, absolute_path)] for everything under the world, QC artifacts excluded.

    Junk folders are NOT pruned from the walk. They have to be visible to be reported as junk to
    delete, and a grader walking the tree sees them too. `is_junk` classifies them afterwards.
    """
    out = []
    for root, dirs, files in os.walk(world):
        for f in files:
            p = os.path.join(root, f)
            if _common.is_qc_artifact(p):
                continue
            out.append((os.path.relpath(p, world).replace("\\", "/"), p))
    return sorted(out)


def text_len(path):
    """Extracted text length, not byte size.

    Byte size is useless for growth: docx and xlsx are zips, so re-saving a file with no content
    change moves the size, and adding a sentence may not. Extracted text is what a grader reads and
    what "did this file grow" actually means.
    """
    try:
        chunks = scan_world.extract_chunks(path)
    except Exception:  # noqa: BLE001
        return None
    if not chunks:
        return None
    return sum(len(str(t)) for _, t in chunks if t)


def spec_hash(spec):
    """SHA-256 of the spec file, so a change to it is detectable between rounds."""
    h = hashlib.sha256()
    with open(spec, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def snap_dir(world):
    return os.path.join(_common.default_backup_dir(world), "inventory")


def write_snapshot(world, files, rnd=None, spec_sha=None):
    d = snap_dir(world)
    os.makedirs(d, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-") + f"{int(time.time()*1e6)%1000000:06d}"
    name = f"round{rnd:03d}-{stamp}.json" if rnd is not None else f"{stamp}.json"
    payload = {"taken": datetime.now().isoformat(timespec="seconds"), "round": rnd,
               "spec_sha256": spec_sha,
               "files": {rel: os.path.getsize(p) for rel, p in files},
               "text": {rel: n for rel, p in files for n in [text_len(p)] if n is not None}}
    path = os.path.join(d, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return path


def previous_snapshot(world, exclude=None):
    d = snap_dir(world)
    if not os.path.isdir(d):
        return None
    # Order by WRITE TIME, not by filename. Snapshots are named "round003-<stamp>.json" when a round
    # number is given and "<stamp>.json" when it is not, and a plain string sort puts every "r..."
    # name after every digit-leading one. So a stale round-prefixed snapshot always beat a newer
    # bare one, and drift was reported against the wrong baseline: files already present came back
    # as APPEARED, and growth and spec-change alarms measured from the wrong round too.
    snaps = [f for f in os.listdir(d) if f.endswith(".json")]
    if exclude:
        snaps = [s for s in snaps if os.path.join(d, s) != exclude]
    if not snaps:
        return None
    snaps.sort(key=lambda f: (os.path.getmtime(os.path.join(d, f)), f))
    with open(os.path.join(d, snaps[-1]), encoding="utf-8") as fh:
        return snaps[-1], json.load(fh)


def read_spec_rows(spec):
    """Artifact rows with the Format column, which spec_check.artifact_index does not carry."""
    wb = spec_check.load(spec)
    idx = spec_check.artifact_index(wb)
    a = spec_check.sheet(wb, "Artifacts", "④")
    fmts = {}
    if a:
        hi, cm = spec_check.find_header(a, ["ID", "Format"])
        key = None
        for k in cm or {}:
            if "format" in k:
                key = k
                break
        if hi and key:
            for row in spec_check.rows_after(a, hi):
                aid = spec_check.cell(row, cm.get(spec_check.norm("ID")))
                if aid in idx:
                    fmts[aid] = spec_check.cell(row, cm.get(key)) or ""
    for aid in idx:
        idx[aid]["fmt"] = fmts.get(aid, "")
    return idx


def ext_of(s):
    s = (s or "").strip().lower().lstrip(".")
    for e in ("xlsx", "xlsm", "docx", "pptx", "pdf", "csv", "tsv", "txt", "md", "html", "eml", "json"):
        if e in s:
            return e
    return ""


def cmd_check(args):
    world, spec = args.world, args.spec
    if not os.path.isdir(world):
        print(f"ERROR: world folder not found: {world}")
        sys.exit(2)
    if not os.path.exists(spec):
        print(f"ERROR: spec not found: {spec}")
        sys.exit(2)

    files = world_files(world)
    by_rel = dict(files)
    idx = read_spec_rows(spec)

    print("=" * 78)
    print("INVENTORY CHECK")
    print("=" * 78)
    print(f"\nSpec registers {len(idx)} artifacts. The world holds {len(files)} files.\n")

    missing, claimed, fmt_bad = [], {}, []
    for aid, a in sorted(idx.items()):
        p = spec_check.resolve_path(world, a.get("loc"), a.get("name"))
        if not p:
            missing.append((aid, a.get("name") or a.get("loc") or "(unnamed)"))
            continue
        rel = os.path.relpath(p, world).replace("\\", "/")
        claimed.setdefault(rel, []).append(aid)
        want = ext_of(a.get("fmt"))
        got = os.path.splitext(rel)[1].lstrip(".").lower()
        if want and got and want != got:
            fmt_bad.append((aid, rel, want, got))

    unregistered = [rel for rel, _ in files if rel not in claimed and not is_junk(rel)]
    junk = [rel for rel, _ in files if is_junk(rel)]
    collisions = {rel: ids for rel, ids in claimed.items() if len(ids) > 1}

    problems = 0

    def block(title, rows, note=""):
        nonlocal problems
        if not rows:
            print(f"  PASS  {title}")
            return
        problems += len(rows)
        print(f"  FAIL  {title}  ({len(rows)})")
        for r in rows[:25]:
            print(f"          {r}")
        if len(rows) > 25:
            print(f"          ... and {len(rows) - 25} more")
        if note:
            for line in note.splitlines():
                print(f"        {line}")
        print()

    block("Every registered artifact resolves to a real file",
          [f"{aid}  {nm}" for aid, nm in missing],
          "These are registered in the spec but no matching file exists in the world.\n"
          "Either the pipeline did not generate them, or a rename during remediation broke\n"
          "the match. This is what the Built Files Match Spec Inventory dimension grades.")

    block("No two artifacts claim the same file",
          [f"{rel}  claimed by {', '.join(ids)}" for rel, ids in collisions.items()],
          "Two registry rows resolving to one file means one of them has no artifact.")

    block("Registered format matches the file on disk",
          [f"{aid}  {rel}  spec says .{w}, file is .{g}" for aid, rel, w, g in fmt_bad])

    block("Every file in the world is registered in the spec",
          unregistered,
          "These files exist but no spec row claims them.\n"
          "Some are legitimate: folders the pipeline adds, or a file the spec names loosely.\n"
          "But a file that appeared during remediation is a defect. Adding files reopens\n"
          "closed judgment forks. Check the drift report below before accepting any of these.")

    if junk:
        problems += len(junk)
        print(f"  FAIL  No build junk in the corpus  ({len(junk)})")
        for r in junk[:15]:
            print(f"          {r}")
        print("        Delete these. A grader walking the tree will see them.\n")
    else:
        print("  PASS  No build junk in the corpus")

    prev = previous_snapshot(world)
    sha = spec_hash(spec)
    path = write_snapshot(world, files, args.round, sha)
    print()
    problems += report_spec_change(prev, sha)
    print()
    now_text = {rel: n for rel, p in files for n in [text_len(p)] if n is not None}
    problems += report_growth(prev, now_text)
    print()
    # Count drift toward `problems`. This was called bare, so a file that appeared or disappeared
    # between rounds never affected the problem count or the exit code, even though the documented
    # contract is that an unexplained change exits 1. A registered file quietly regenerated under a
    # different name was therefore invisible to anything gating on the exit status.
    problems += report_drift(prev, {rel: os.path.getsize(p) for rel, p in files}) or 0
    print(f"\nSnapshot written: {path}")

    print("\n" + "=" * 78)
    if problems:
        print(f"{problems} inventory problem(s). Work them before you upload.")
    else:
        print("The world matches the spec's registry.")
    print("=" * 78)
    sys.exit(1 if problems else 0)


def report_spec_change(prev, sha):
    """Has the local spec file been edited since the last snapshot?

    This is not a style rule. The spec RL Studio holds is the one AutoQC reads; the copy in the
    builder's folder is a download. Edit the copy and it silently diverges from the grader's, so every
    tie check for the rest of the session is measured against a spec that does not exist. That is a
    doom-loop generator and it is invisible while it happens.

    A genuine spec defect is fixed by an EPM re-uploading, never by editing the local copy.
    """
    print("THE SPEC FILE")
    print("-" * 78)
    if not prev:
        print("  Recorded. From the next run this will report if the local copy has been edited.")
        return 0
    old = (prev[1] or {}).get("spec_sha256")
    if not old:
        print("  No hash in the previous snapshot, nothing to compare. Recorded for next time.")
        return 0
    if old == sha:
        print("  Unchanged since the last snapshot, which is correct.")
        return 0
    print("  THE LOCAL SPEC FILE HAS BEEN EDITED SINCE THE LAST SNAPSHOT.")
    print()
    print("  Studio holds the spec AutoQC actually reads. Your copy is a download. Now that they")
    print("  disagree, every tie and trap check in this session is being measured against a spec")
    print("  the grader does not have, and the findings will not make sense.")
    print()
    print("  If the spec genuinely needed a fix, that is legitimate, but it goes to an EPM to")
    print("  re-upload. Restore your copy from the backup, write up the exact change (cell, old,")
    print("  new, and every file that carries the value), and post it in your world thread.")
    return 1


def report_growth(prev, now_text):
    """Files whose extracted text grew since the last round.

    Replace-not-add is the rule that stops the corpus explaining its own answers, and until now it was
    only ever a rule. This makes it measurable. A replacement leaves length about the same. A sentence
    added to reconcile two figures makes the file longer, and that is exactly the edit that leaks an
    answer or kills a trap.

    Growth is not proof of anything. It is a short list of files to justify.
    """
    print("TEXT GROWTH")
    print("-" * 78)
    if not prev:
        print("  Recorded. From the next run this reports which files got longer.")
        return 0
    old = (prev[1] or {}).get("text") or {}
    if not old:
        print("  No text lengths in the previous snapshot, nothing to compare. Recorded for next time.")
        return 0
    grew = []
    for rel, n in now_text.items():
        o = old.get(rel)
        if o is None or n <= o:
            continue
        delta = n - o
        # Ignore trivial movement: a value swap of different digit-width changes a few characters.
        if delta >= 40:
            grew.append((rel, o, n, delta))
    if not grew:
        print("  No file gained meaningful text. That is what a round of replacements should look like.")
        return 0
    grew.sort(key=lambda r: -r[3])
    print(f"  {len(grew)} file(s) gained text since the last round:\n")
    for rel, o, n, d in grew[:20]:
        print(f"    +{d:>6} chars   {rel}   ({o} -> {n})")
    if len(grew) > 20:
        print(f"    ... and {len(grew) - 20} more")
    print()
    print("  Every one of these needs a reason. Replacing a wrong value does not make a file longer.")
    print("  Text added to explain, reconcile or clarify a discrepancy is answer leakage, and if the")
    print("  figures involved are a declared trap it has killed the trap. Run:")
    print("    python scripts/leak_scan.py <world> --spec <spec.xlsx>")
    return len(grew)


def report_drift(prev, now):
    print("DRIFT SINCE THE LAST SNAPSHOT")
    print("-" * 78)
    if not prev:
        print("  No earlier snapshot. This is the baseline; the next run will compare against it.")
        return 0
    name, data = prev
    old = data.get("files", {})
    added = sorted(set(now) - set(old))
    removed = sorted(set(old) - set(now))
    resized = sorted(f for f in set(now) & set(old) if now[f] != old[f])

    print(f"  Comparing against {name}"
          + (f" (round {data['round']})" if data.get("round") is not None else ""))
    if not (added or removed):
        print(f"  No files added or removed. {len(resized)} file(s) edited.")
        return 0

    if added:
        print(f"\n  APPEARED ({len(added)}):")
        for f in added[:25]:
            print(f"    + {f}")
        if len(added) > 25:
            print(f"    ... and {len(added) - 25} more")
        print("\n    A file that appeared during remediation is the thing to look hardest at.")
        print("    Adding files is against the replace-not-add rule. One world added ambient")
        print("    'no trap' files while fixing findings and they reopened judgment forks that")
        print("    were already closed. If you did not add these on purpose, remove them.")
    if removed:
        print(f"\n  DISAPPEARED ({len(removed)}):")
        for f in removed[:25]:
            print(f"    - {f}")
        if len(removed) > 25:
            print(f"    ... and {len(removed) - 25} more")
        print("\n    A registered artifact that disappeared fails Built Files Match Spec Inventory.")
    if added and removed:
        print("\n    Files in both lists are usually one rename. Confirm each rename was")
        print("    deliberate, and that the spec's Location still points at the new name.")
    print(f"\n  {len(resized)} file(s) edited in place.")
    return len(added) + len(removed)


def cmd_drift(args):
    world = args.world
    if not os.path.isdir(world):
        print(f"ERROR: world folder not found: {world}")
        sys.exit(2)
    files = world_files(world)
    prev = previous_snapshot(world)
    n = report_drift(prev, {rel: os.path.getsize(p) for rel, p in files})
    sys.exit(1 if n else 0)


def main():
    p = argparse.ArgumentParser(
        description="Reconcile the world's files against the spec's Artifacts registry, and track "
                    "what changed between rounds.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="reconcile against the spec, snapshot, and report drift")
    c.add_argument("spec")
    c.add_argument("world")
    c.add_argument("--round", type=int, default=None)
    c.set_defaults(func=cmd_check)

    d = sub.add_parser("drift", help="report what changed since the last snapshot; no spec needed")
    d.add_argument("world")
    d.set_defaults(func=cmd_drift)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
