#!/usr/bin/env python3
"""log_edit.py, record a change you made by hand.

WHY THIS EXISTS
---------------
`change_manifest.md` is the memory the whole toolkit runs on. `blast_radius.py` reads it to answer the
two questions that decide a round: is a value you replaced still standing somewhere else, and did an
edit break a total.

Until this script existed, only `a_scrub.py` and `entity_conformer.py` wrote to that manifest. Every
edit the model made by hand during a judgment fix was invisible to it.

That is backwards. The mechanical fixers are the safe changes: one class, one rule, applied
everywhere at once. **The hand edits are the dangerous ones.** A number changed in one file because a
finding named it is exactly the change most likely to break a total in that file and a tie in three
others, and it was the one change nothing was recording.

So: call this after every edit made outside the class fixers. One call per value changed.

USAGE
-----
    python log_edit.py <world> --file <path> --old "<old value>" --new "<new value>"
                              [--where "<cell or section>"] [--why "<finding or ticket>"]

    python log_edit.py <world> --file Finance/rollup.xlsx --old 398100 --new 412500 \\
                               --where "Sheet1!B12" --why "AQC round 3, North region total"

Append several at once by calling it several times. It never overwrites.

WHAT IT WRITES
--------------
The same table row the automated fixers write, into the same file, so `blast_radius.py` reads a hand
edit and a scripted edit identically:

    <world>_qc_backup/change_manifest.md
    <world>_qc_backup/comments.txt

The manifest sits beside the world, never inside it, so re-zipping the world to upload cannot ship it.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

_common.setup_console()


def main():
    p = argparse.ArgumentParser(
        description="Record a hand edit in the change manifest so blast_radius.py can see it.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Call this after every edit you make outside the class fixers. One call per value.")
    p.add_argument("world", help="the world folder")
    p.add_argument("--file", required=True, help="the file you edited, relative to the world")
    p.add_argument("--old", required=True, help="the value as it was")
    p.add_argument("--new", required=True, help="the value as it is now")
    p.add_argument("--where", default="", help="cell, page, section or line")
    p.add_argument("--why", default="", help="the finding or ticket this fix came from")
    p.add_argument("--tool", default="manual edit", help="who made it (default: manual edit)")
    a = p.parse_args()

    if not os.path.isdir(a.world):
        print(f"ERROR: world folder not found: {a.world}")
        sys.exit(2)

    if a.old == a.new:
        print("ERROR: old and new are the same. Nothing changed, so there is nothing to record.")
        sys.exit(2)

    # A warning, not a refusal. The file may legitimately have been renamed by this very edit, and
    # refusing would push the model into skipping the log, which is the failure this script exists
    # to prevent.
    target = os.path.join(a.world, a.file)
    if not os.path.exists(target):
        matches = []
        base = os.path.basename(a.file).lower()
        for root, _, files in os.walk(a.world):
            for f in files:
                if f.lower() == base:
                    matches.append(os.path.relpath(os.path.join(root, f), a.world))
        if matches:
            print(f"NOTE: '{a.file}' not found at that path, but the name matches: {', '.join(matches[:3])}")
        else:
            print(f"NOTE: '{a.file}' is not in the world folder. Recording it anyway, but check the path.")

    loc = a.where or "(not stated)"
    if a.why:
        loc = f"{loc} [{a.why}]"

    out = _common.default_backup_dir(a.world)
    _common.append_manifest(out, a.tool, [(a.file, loc, a.old, a.new)])

    print(f"Recorded: {a.file} ({loc})  \"{a.old}\" -> \"{a.new}\"")
    print(f"  in {os.path.join(out, 'change_manifest.md')}")
    print("\nblast_radius.py will now check whether the old value is still standing anywhere else,")
    print("and re-foot this file when you run it before upload.")


if __name__ == "__main__":
    main()
