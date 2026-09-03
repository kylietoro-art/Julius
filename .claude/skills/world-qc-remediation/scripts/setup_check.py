#!/usr/bin/env python3
"""setup_check.py, run this before anything else.

WHY THIS EXISTS
---------------
A half-extracted toolkit does not error. It gives silent wrong answers. A missing library makes a
checker print "not installed, skipping" and a builder reads that as a pass. A missing spec makes the
whole session unable to tell a defect from a registered trap, which is how traps get deleted.

Every one of those costs at least one AutoQC round, and none of them announces itself.

This checks the lot in one command and prints a plain list of what passed and what did not.

USAGE
-----
    python setup_check.py
    python setup_check.py --spec <spec.xlsx> --world <world_folder>

With no arguments it checks the toolkit and the environment. Add --spec and --world and it also
checks the world is present, the spec is readable, and the trap manifest is populated.

A hand-made copy of the whole world is NOT required. Studio holds the last uploaded revision, and
every fixer copies a file before it changes it.

EXIT CODES
----------
    0  everything needed is present
    1  something is missing, do not start work
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import _common  # noqa: E402

# The complete file manifest for the toolkit. If a file is added to the skill, add it here too,
# otherwise a builder with a half-extracted zip passes this check.
MANIFEST = {
    ".": ["SKILL.md", "CHANGELOG.md"],
    "references": ["aqc-dimensions.md", "error-taxonomy.md", "file-formats.md",
                   "round-economics.md", "traps-and-facts.md"],
    "scripts": ["_common.py", "a_scrub.py", "blast_radius.py", "entity_conformer.py",
                "corpus.py", "gen_realistic_values.py", "inventory_check.py", "leak_scan.py",
                "log_edit.py",
                "metadata_hygiene.py",
                "pdf_markup_scan.py",
                "pdf_replace.py", "reconcile_entities.py", "requirements.txt", "round_log.py",
                "scan_world.py", "selftest.py", "setup_check.py", "spec_check.py",
                "verify_xlsx.py"],
    "assets": ["README.md", "verification_bench.html", "verification_bench_README.txt"],
}

# Import name mapped to the pip name, because they differ often enough to matter.
LIBS = [("openpyxl", "openpyxl"), ("pandas", "pandas"), ("pypdf", "pypdf"),
        ("pdfplumber", "pdfplumber"), ("docx", "python-docx"), ("pptx", "python-pptx"),
        ("fitz", "PyMuPDF")]

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if detail and not ok:
        for line in detail.splitlines():
            print(f"        {line}")


def present(base, name):
    """Is `name` in directory `base`?

    Three ways, because one is not enough. `os.path.exists` goes through a stat call, and on Windows
    a packaged-app install (MSIX/Store) can redirect that path so stat reports False on a file that is
    really there and really readable. Directory enumeration and open() take different code paths and
    see through the redirect, so a negative from stat alone is not trusted.

    Getting this wrong tells a builder their toolkit is broken and to stop work, when nothing is wrong.
    """
    p = os.path.join(base, name)
    if os.path.exists(p):
        return True
    try:                                     # enumeration, survives the redirect
        entries = os.listdir(base)
        if name in entries:
            return True
        low = name.lower()                   # and Windows is case-insensitive
        if any(e.lower() == low for e in entries):
            return True
    except OSError:
        pass
    try:                                     # last resort: can we actually open it?
        with open(p, "rb"):
            return True
    except OSError:
        return False


def files_present():
    missing = []
    for folder, names in MANIFEST.items():
        base = ROOT if folder == "." else os.path.join(ROOT, folder)
        if not (os.path.isdir(base) or (folder != "." and present(ROOT, folder))):
            missing.append(f"the whole {folder}/ folder is missing")
            continue
        for n in names:
            if not present(base, n):
                missing.append(f"{folder}/{n}" if folder != "." else n)
    total = sum(len(v) for v in MANIFEST.values())
    detail = ""
    if missing:
        detail = (f"{len(missing)} of {total} files are missing:\n  "
                  + "\n  ".join(missing[:20])
                  + ("\n  ..." if len(missing) > 20 else "")
                  + "\n\nThis usually means the zip was opened rather than extracted, or only the\n"
                    "top folder was extracted. Delete what you have and extract the whole thing again.")
    check(f"Toolkit complete ({total - len(missing)} of {total} files)", not missing, detail)
    return not missing


def frontmatter_ok():
    """The skill will not load at all if SKILL.md's frontmatter is malformed or the description runs
    over the 1024 character limit. That failure looks like the skill simply not existing, which is
    hard to diagnose from the symptom, so it is checked here."""
    import re
    p = os.path.join(ROOT, "SKILL.md")
    if not os.path.exists(p):
        check("SKILL.md frontmatter is valid", False, "SKILL.md is missing.")
        return False
    t = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        check("SKILL.md frontmatter is valid", False,
              "No --- frontmatter block at the top of SKILL.md.")
        return False
    body = m.group(1)
    name = re.search(r"^name:\s*(\S+)", body, re.M)
    dm = re.search(r"^description:\s*>-\s*\n((?:[ \t]+.*\n?)+)", body, re.M)
    desc = " ".join(l.strip() for l in dm.group(1).splitlines()).strip() if dm else ""
    if not dm:
        one = re.search(r"^description:\s*(.+)$", body, re.M)
        desc = one.group(1).strip() if one else ""
    ok = bool(name) and 0 < len(desc) <= 1024
    check(f"SKILL.md frontmatter is valid (description {len(desc)}/1024 chars)", ok,
          ("No name: field." if not name else
           "description is empty." if not desc else
           f"description is {len(desc)} characters, over the 1024 limit. The skill will not load.\n"
           "Move the detail into the body and keep the trigger phrases in the description."))
    return ok


def python_ok():
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 8)
    check(f"Python {v.major}.{v.minor} is recent enough (need 3.8+)", ok,
          "Install a current Python. This is the one thing you have to do by hand.")
    return ok


def libs_ok():
    missing = []
    for mod, pipname in LIBS:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pipname)
    detail = ""
    if missing:
        detail = ("missing: " + ", ".join(missing)
                  + "\n\nRun this from the scripts folder:\n"
                    "  pip install -r requirements.txt\n\n"
                  "Do not start work without these. A script with a missing library prints\n"
                  "'not installed, skipping' and that reads like a pass when it is not.")
    check(f"Libraries installed ({len(LIBS) - len(missing)} of {len(LIBS)})", not missing, detail)
    return not missing


def selftest_ok():
    # The self-test runs setup_check, and setup_check runs the self-test. Without this guard that
    # is an infinite recursion that presents as the terminal simply hanging, with no error, which
    # is the worst possible thing to hand a non-technical builder.
    if os.environ.get("WQC_IN_SELFTEST"):
        check("Self-test passes", True, "skipped, already running inside the self-test")
        return True
    p = os.path.join(HERE, "selftest.py")
    if not os.path.exists(p):
        check("Self-test passes", False, "selftest.py is missing, so the toolkit is incomplete.")
        return False
    r = subprocess.run([sys.executable, p], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    line = [l for l in out.splitlines() if "LAYER 1 BATTERY" in l]
    ok = r.returncode == 0
    detail = ""
    if not ok:
        fails = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
        detail = ((line[0].strip() if line else "the self-test did not finish")
                  + ("\n" + "\n".join(fails[:10]) if fails else "")
                  + "\n\nThe toolkit is damaged. Extract it again from a fresh copy.")
    check(f"Self-test passes  {line[0].strip() if line else ''}".rstrip(), ok, detail)
    return ok


def world_ok(world):
    if not os.path.isdir(world):
        check("World folder found", False, f"not a folder: {world}")
        return False
    n = sum(len(f) for _, _, f in os.walk(world))
    check(f"World folder found ({n} files)", n > 0,
          "The folder is empty. Download the world from the left-hand panel in Studio and unzip it.")

    # A hand-made copy of the whole world is NOT required, and is no longer checked.
    #
    # There are three recovery layers and two of them cover the same moment. Studio holds the last
    # uploaded revision, so re-downloading restores the start of the round. A hand-made local copy
    # restores exactly the same moment, just faster. The layer that is not duplicated is the tool's
    # own per-file backup, which restores a single bad EDIT without costing the round's other work,
    # and that one happens automatically.
    #
    # Demanding a manual copy on top of that was one more thing for a non-technical builder to get
    # right, for a moment Studio already covers. Dropped deliberately.
    return n > 0


def spec_ok(spec):
    if not os.path.exists(spec):
        check("Spec file found", False, f"not found: {spec}")
        return False
    check("Spec file found", True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "spec_check.py"), "traps", spec],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    readable = "declared" in out.lower() or "trap" in out.lower()
    check("Spec is readable by the toolkit", readable,
          out.strip()[:400] + "\n\nIf this is not the World Spec, point --spec at the right .xlsx.")
    if readable:
        # Parse the integer. "0 declared" as a substring matches 10, 20, 50, 100 and every other
        # count ending in zero, which told well-trapped worlds they had no traps and to stop work.
        m = re.search(r"(\d+)\s+declared", out)
        zero = (int(m.group(1)) == 0) if m else ("no traps" in out.lower() or "none found" in out.lower())
        check("Spec declares at least one trap", not zero,
              "The spec declares no traps.\n\n"
              "Without a trap manifest nothing can tell an intentional divergence from an error,\n"
              "and every consistency finding becomes a coin flip. Get the spec's trap columns\n"
              "populated before starting remediation. Raise it in your world thread.")
    return readable



# ==================================================================================================
# Auto-discovery.
#
# The expert should not have to type a path, name a folder, or know what a "spec" file is called.
# Most of them are not technical, and every path they have to supply is a chance to supply the wrong
# one and lose a round. Point this at the folder and it works out what is what.
# ==================================================================================================
SPEC_TABS = ("canonical", "artifact")          # the ② and ④ tabs, matched loosely
JUNK_DIRS = {"__pycache__", "__macosx", ".git", ".idea", ".vscode", "node_modules"}


def _count_files(d):
    n = 0
    for _, dn, fn in os.walk(d):
        dn[:] = [x for x in dn if x.lower() not in JUNK_DIRS]
        n += len([f for f in fn if not f.startswith("~$")])
    return n


def find_toolkit(folder):
    """(toolkit path, is it where Claude Code will auto-load it). Both matter and they differ."""
    for dp, dn, fn in os.walk(folder):
        dn[:] = [x for x in dn if x.lower() not in JUNK_DIRS]
        if "setup_check.py" in fn and dp.replace(os.sep, "/").endswith("world-qc-remediation/scripts"):
            tk = os.path.abspath(os.path.join(dp, ".."))
            return tk, "/.claude/skills/" in tk.replace(os.sep, "/") + "/"
    return None, False


def looks_like_spec(path):
    """A World Spec has the ② Canonical Values and ④ Artifacts tabs. Nothing else in the folder does,
    which makes this a far better test than guessing from the filename."""
    try:
        import openpyxl
        names = " ".join(openpyxl.load_workbook(path, read_only=True).sheetnames).lower()
        return all(t in names for t in SPEC_TABS)
    except Exception:  # noqa: BLE001
        return False


def discover(folder):
    """Everything the round needs, worked out from the folder alone."""
    folder = os.path.abspath(folder)
    out = {"folder": folder, "worlds": [], "backups": [], "specs": [], "findings": [],
           "other_xlsx": []}
    out["toolkit"], out["toolkit_autoloads"] = find_toolkit(folder)
    tk = (out["toolkit"] or "").replace(os.sep, "/")

    try:
        entries = [(n, os.path.join(folder, n)) for n in sorted(os.listdir(folder))]
    except OSError:
        return out

    # Also look one level inside the workspace: `tidy` moves the spec and the findings files there,
    # and discovery has to keep finding them afterwards or tidying would break the next round.
    ws = os.path.join(folder, _common.WORKSPACE)
    if os.path.isdir(ws):
        try:
            entries += [(n, os.path.join(ws, n)) for n in sorted(os.listdir(ws))
                        if not os.path.isdir(os.path.join(ws, n))]
        except OSError:
            pass

    for name, full in entries:
        if os.path.isdir(full):
            if name.startswith(".") or name.lower() in JUNK_DIRS or name == _common.WORKSPACE:
                continue
            if tk and full.replace(os.sep, "/") in tk:
                continue                                   # that is the toolkit, not a world
            low = name.lower()
            n = _count_files(full)
            # Match the marker ANYWHERE in the name, not just at the end. Real builders name their
            # copies "filesystem_BACKUP_pre_r7" and "filesystem_metadata_originals_r5", so a
            # suffix-only test classified six copies as six candidate worlds and made the layout
            # report ask which was which.
            if any(w in low for w in ("backup", "_orig", "originals", "copy", "_old", "archive")):
                out["backups"].append((name, n))
            elif n:
                out["worlds"].append((name, n))
        elif name.lower().endswith((".xlsx", ".xlsm")) and not name.startswith("~$"):
            (out["specs"] if looks_like_spec(full) else out["other_xlsx"]).append(name)
        elif name.lower().endswith((".txt", ".md")):
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    head = fh.read(4000).lower()
                if any(k in head for k in ("autoqc", "finding", "[p0]", "[p1]", "[p2]",
                                           "dimension", "severity")):
                    out["findings"].append(name)
            except OSError:
                pass

    out["worlds"].sort(key=lambda t: -t[1])
    return out


def tidy(folder, write=False):
    """Reduce the working folder to three things: .claude, the world, and qc_workspace.

    A ten-round build leaves a builder looking at this:

        filesystem/                       <- the one to upload
        filesystem_BACKUP_pre_r1/ ... _r10/
        filesystem_BACKUP_pre_r10_qc_backup/
        filesystem_metadata_originals_r5/
        filesystem_qc_backup/
        autoqc_round1.txt ... round10.txt
        anchor_detach_list_round7.md

    Eight folders whose names all begin "filesystem". Asking a non-technical expert to pick the
    right one to upload, under time pressure, is asking for the most expensive mistake available.

    This MOVES everything that is not the world or the skill into qc_workspace. It never deletes.
    """
    import shutil
    folder = os.path.abspath(folder.rstrip("/\\"))
    d = discover(folder)
    if not d["worlds"]:
        sys.exit("tidy: I cannot tell which folder is the world, so I will not move anything.\n"
                 "Run this from the folder that holds the world, or name the world with --world.")
    if len(d["worlds"]) > 1:
        names = ", ".join(n for n, _ in d["worlds"])
        sys.exit(f"tidy: more than one folder could be the world ({names}).\n"
                 f"Tell me which one with --world before I move anything.")

    world = d["worlds"][0][0]
    keep = {world, ".claude", _common.WORKSPACE}
    moves = [e for e in sorted(os.listdir(folder))
             if e not in keep and not e.startswith(".claude")]

    print("=" * 78)
    print("TIDY THE WORKING FOLDER")
    print("=" * 78)
    print(f"\n  Keeping at the top level:")
    print(f"    {world}/            the world. This is the folder you upload.")
    print(f"    .claude/            the skill")
    print(f"    {_common.WORKSPACE}/       everything else\n")

    if not moves:
        print("  Already tidy. Nothing to move.")
        return 0

    print(f"  Moving {len(moves)} item(s) into {_common.WORKSPACE}/:")
    for e in moves:
        kind = "folder" if os.path.isdir(os.path.join(folder, e)) else "file"
        print(f"    {e}   ({kind})")

    if not write:
        print("\n  Nothing moved. Re-run with --write to move them.")
        print("  Nothing is deleted, only moved, so this is safe to run.")
        return len(moves)

    dest_root = os.path.join(folder, _common.WORKSPACE)
    os.makedirs(dest_root, exist_ok=True)
    moved = 0
    for e in moves:
        src = os.path.join(folder, e)
        dst = os.path.join(dest_root, e)
        n = 1
        while os.path.exists(dst):
            stem, ext = os.path.splitext(e)
            dst = os.path.join(dest_root, f"{stem}__{n}{ext}")
            n += 1
        try:
            shutil.move(src, dst); moved += 1
        except OSError as err:
            print(f"  ! could not move {e}: {err}", file=sys.stderr)
    print(f"\n  Moved {moved} item(s).")
    print(f"  The top level now holds {world}/, .claude/ and {_common.WORKSPACE}/ only.")
    print(f"  Upload {world}/. Nothing else.")
    return 0


def report_layout(folder):
    """Print what is in the folder in plain English, and exactly what to do about anything missing.

    Returns (world, spec) if the folder is usable, else (None, None).
    """
    d = discover(folder)
    print("=" * 60)
    print("YOUR FOLDER")
    print("=" * 60)
    print(f"\n  Looking in: {d['folder']}\n")

    todo = []

    # 1. the toolkit
    if not d["toolkit"]:
        print("  MISSING   The remediation toolkit")
        todo.append("Extract world-qc-remediation-vX.Y.Z-claude-folder.zip into this folder.\n"
                    "     Extract it. Do not just double-click and look inside the zip.")
    elif not d["toolkit_autoloads"]:
        print(f"  WRONG SPOT  Toolkit is at {os.path.relpath(d['toolkit'], d['folder'])}")
        todo.append("The toolkit is here but not where Claude Code looks for it, so the skill\n"
                    "     will not load by itself. Extract the '-claude-folder.zip' version instead\n"
                    "     of the '.skill' file. It creates a .claude folder, which is the one that\n"
                    "     works.")
    else:
        print("  OK        Toolkit installed where Claude Code will load it")

    # 2. the world
    if not d["worlds"]:
        print("  MISSING   The world files")
        todo.append("Put the unzipped world folder from Studio into this folder.")
    elif len(d["worlds"]) == 1:
        print(f"  OK        World folder: {d['worlds'][0][0]}  ({d['worlds'][0][1]} files)")
    else:
        print("  ASK       More than one folder could be the world:")
        for n, c in d["worlds"][:6]:
            print(f"              {n}  ({c} files)")
        todo.append("Ask the expert which of those folders is the world before doing anything.")

    # 3. the spec
    if not d["specs"]:
        print("  MISSING   The World Spec")
        extra = ""
        if d["other_xlsx"]:
            extra = ("\n     These spreadsheets are here but are not the spec (no Canonical Values\n"
                     "     or Artifacts tabs): " + ", ".join(d["other_xlsx"][:4]))
        todo.append("Put the World Spec .xlsx into this folder." + extra +
                    "\n     Without it you cannot tell a real defect from a deliberate trap, and\n"
                    "     traps get deleted. Do not start the round without it.")
    elif len(d["specs"]) == 1:
        print(f"  OK        World Spec: {d['specs'][0]}")
    else:
        print("  ASK       More than one file looks like a spec: " + ", ".join(d["specs"]))
        todo.append("Ask the expert which spec is the current one.")

    # 4. the backup, informational only
    #
    # Not required. Studio holds the last uploaded revision, so the start of the round is already
    # recoverable, and the fixers copy each file before they change it. A hand-made copy of the
    # whole world duplicates the first of those, so asking for one was friction with no cover.
    if d["backups"]:
        print(f"  OK        Backup of the world: {d['backups'][0][0]}")
    else:
        print("  NOTE      No local copy of the world. Not needed: Studio holds the last uploaded")
        print("            revision, and each file is copied before it is changed.")

    # 5. the findings, optional
    if d["findings"]:
        print(f"  OK        AutoQC findings file: {d['findings'][0]}")
    else:
        print("  NOTE      No AutoQC findings file. Fine if they are pasting them into the chat.")

    if todo:
        print("\n" + "=" * 60)
        print("WHAT TO FIX FIRST")
        print("=" * 60)
        for i, t in enumerate(todo, 1):
            print(f"\n  {i}. {t}")
        print("\n  Tell the expert this in plain words. Do not show them this output raw.")
        return None, None

    world = os.path.join(d["folder"], d["worlds"][0][0])
    spec = os.path.join(d["folder"], d["specs"][0])
    print(f"\n  Everything is here. Using world '{d['worlds'][0][0]}' and spec '{d['specs'][0]}'.")
    return world, spec


def main():
    p = argparse.ArgumentParser(
        description="Check the toolkit and environment before starting File System fixes.")
    p.add_argument("--spec", help="path to the World Spec .xlsx")
    p.add_argument("--world", help="path to the unzipped world folder")
    p.add_argument("--tidy", action="store_true",
                   help="reduce the working folder to three things: the world, .claude, and "
                        "qc_workspace. Lists what it would move; add --tidy-write to move it. "
                        "Never deletes.")
    p.add_argument("--tidy-write", action="store_true",
                   help="with --tidy, actually move the files")
    p.add_argument("--folder", default=".", metavar="DIR",
                   help="the expert's working folder (default: where you are). With neither "
                        "--spec nor --world, the world and spec are found here automatically.")
    a = p.parse_args()

    # Nothing supplied means: work it out. The expert should not have to name a path, and every
    # path they type is a chance to type the wrong one and lose a round.
    if getattr(a, "tidy", False):
        sys.exit(1 if tidy(a.folder, a.tidy_write) else 0)

    auto = not (a.world or a.spec)
    if auto:
        print()
        world, spec = report_layout(a.folder)
        if world is None:
            print("\n" + "=" * 60)
            print("Stop here. Get the folder right first, then run this again.")
            print("Nothing below this point is worth doing until the layout is fixed.")
            sys.exit(1)
        a.world, a.spec = world, spec

    print("\nSETUP CHECK\n" + "=" * 60 + "\n")
    print("Toolkit and environment")
    files_present()
    frontmatter_ok()
    python_ok()
    have_libs = libs_ok()
    if have_libs:
        selftest_ok()
    else:
        check("Self-test passes", False, "skipped, libraries are missing. Install them and re-run.")

    if a.world or a.spec:
        print("\nThis world")
        if a.world:
            world_ok(a.world)
        else:
            check("World folder found", False, "not given. Re-run with --world <folder>.")
        if a.spec:
            spec_ok(a.spec)
        else:
            check("Spec file found", False,
                  "not given. Re-run with --spec <spec.xlsx>.\n"
                  "Working without the spec means you cannot tell a defect from a registered\n"
                  "trap, and traps get deleted. Do not start without it.")
    else:
        print("\nNOTE: run again with --spec and --world to check this particular world.")

    passed = sum(1 for _, ok, _ in results if ok)
    failed = len(results) - passed
    print("\n" + "=" * 60)
    print(f"{passed} passed, {failed} failed")
    if failed:
        print("\nDo not start work. Fix the failures above first. Every one of them causes a\n"
              "silent wrong answer rather than an error message, which costs a full AutoQC round.")
    else:
        print("\nReady. Log the round with round_log.py and go to Gate 1.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
