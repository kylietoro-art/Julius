#!/usr/bin/env python3
"""Detect and strip tool fingerprints from file metadata, the openpyxl/reportlab/python-docx author
strings and build/today dates that reveal a file was machine-generated (AQC: openpyxl 3.1.5 leak).

Also catches two adjacent tells that are easy to introduce while EDITING a file in this skill (not
just at original build time): a stray Title field carrying the original working filename (e.g. a
Google Docs export leaving "Foo_Revised.docx" in /Title), and PDF incremental-save revision history,
every raw PyMuPDF redact-and-reinsert edit that ends with doc.saveIncr() (rather than a full rewrite)
appends a new revision onto the file. The old revision, including any discarded intermediate edit,
stays physically present (extra %%EOF sections) even though viewers only render the latest one.

Run `clean` on every file you edit. It fully rewrites the file, which also collapses any
incremental-save history back to one revision as a side effect.

  scan <dir|file>
        Report files whose metadata leaks a tool fingerprint, a build/today date, a stray
        Title/filename, or (PDFs) more than one incremental-save revision.

  clean <dir|file> [--app NAME] [--date YYYY-MM-DD] [--no-backup]
        Set a neutral Application (defaulted to the correct native app for the file type, Excel for
        .xlsx, Word for .docx, PowerPoint for .pptx; stripped for PDF), clear tool creator/lastModifiedBy,
        set the modified/created date to --date, and (PDFs) collapse incremental-save history to one
        revision. Give a DIRECTORY to clean every Office/PDF file under it. Each file is backed up
        first (into a sibling _qc_backup folder) unless --no-backup.

        IMPORTANT: without --date, the build/today date is LEFT IN PLACE (we can't guess your world's
        in-world date) and you get a warning. Pass --date with a date that fits your world's timeline.

Deps: stdlib for Office; pypdf for PDFs.
"""
import argparse, os, re, sys, glob, zipfile, datetime
import _common
_common.setup_console()

FINGERPRINTS = re.compile(r"openpyxl|reportlab|python-docx|python-pptx|LibreOffice|Aspose|xlsxwriter|Apache POI", re.I)
FILENAME_LIKE = re.compile(r"\.(docx?|xlsx?|pptx?|pdf|csv)$", re.I)
OFFICE_EXTS = ("xlsx", "xlsm", "docx", "pptx")
NATIVE_APP = {"xlsx": "Microsoft Excel", "xlsm": "Microsoft Excel",
              "docx": "Microsoft Word", "pptx": "Microsoft PowerPoint"}

def _default_app(ext):
    """The Application string a real file of this type would carry. A cleaned .docx must NOT claim
    'Microsoft Excel', that's a louder tell than the python-docx string it replaced."""
    return NATIVE_APP.get(ext, "")

def _have_pypdf():
    try:
        import pypdf  # noqa: F401
        return True
    except ImportError:
        return False

def _office_meta(path):
    meta = {}
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if "docProps/app.xml" in names:
                app = z.read("docProps/app.xml").decode("utf-8", "ignore")
                m = re.search(r"<Application>(.*?)</Application>", app)
                if m: meta["app"] = m.group(1)
            if "docProps/core.xml" in names:
                core = z.read("docProps/core.xml").decode("utf-8", "ignore")
                for tag in ("dc:creator", "cp:lastModifiedBy", "dc:description", "dc:title"):
                    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", core)
                    if m: meta[tag] = m.group(1)
                for tag in ("dcterms:modified", "dcterms:created"):
                    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", core)
                    if m: meta[tag] = m.group(1)
    except Exception:
        pass
    return meta

def _pdf_meta(path):
    """Return (meta_dict, error). error is None on success, else a short reason string."""
    try:
        import pypdf
    except ImportError:
        return {}, "pypdf-missing"
    try:
        r = pypdf.PdfReader(path)
        if r.is_encrypted:
            return {}, "encrypted"
        return {k.lstrip("/"): str(v) for k, v in (r.metadata or {}).items()}, None
    except Exception as e:
        return {}, f"unreadable ({type(e).__name__})"

def _pdf_revision_count(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        return max(1, data.count(b"%%EOF"))
    except Exception:
        return 1

def _leaks(meta, today):
    reasons = []
    for k, v in meta.items():
        if v and FINGERPRINTS.search(str(v)):
            reasons.append(f"{k}={v}")
    today_pdf = today.replace("-", "")
    for k in ("dcterms:modified", "dcterms:created", "ModDate", "CreationDate"):
        v = str(meta.get(k, ""))
        if v and (today in v or today_pdf in v):
            reasons.append(f"{k}={v} (build/today date)")
    for k in ("Title", "Subject", "dc:description", "dc:title"):
        v = str(meta.get(k, ""))
        if v and FILENAME_LIKE.search(v):
            reasons.append(f"{k}={v} (stray original filename)")
    return reasons

def _world_files(path, exts):
    if os.path.isfile(path):
        return [path]
    return [f for f in glob.glob(os.path.join(path, "**", "*"), recursive=True)
            if os.path.isfile(f) and f.lower().rsplit(".", 1)[-1] in exts
            and not _common.is_qc_artifact(f)]

def scan(path):
    if not os.path.exists(path):
        sys.exit(f"! path not found: {path}")
    today = datetime.date.today().isoformat()
    files = _world_files(path, OFFICE_EXTS + ("pdf",))
    flagged = unchecked = 0
    pdf_present = any(f.lower().endswith(".pdf") for f in files)
    have_pdf = _have_pypdf()
    if pdf_present and not have_pdf:
        print("[NOTE] pypdf not installed, PDF metadata NOT checked. Install it (pip install pypdf) "
              "and re-run, or PDF fingerprints/revisions will be missed.", file=sys.stderr)
    base_root = path if os.path.isdir(path) else os.path.dirname(path)
    for f in sorted(files):
        ext = f.lower().rsplit(".", 1)[-1]
        base = os.path.relpath(f, base_root)
        if ext == "pdf":
            meta, err = _pdf_meta(f)
            if err == "pypdf-missing":
                unchecked += 1; continue
            if err:
                unchecked += 1
                print(f"[UNCHECKED] {base}: {err}, could not read metadata")
                continue
            reasons = _leaks(meta, today)
            revs = _pdf_revision_count(f)
            if revs > 1:
                reasons.append(f"{revs} incremental-save revisions (editing residue, run `clean` to collapse)")
        else:
            reasons = _leaks(_office_meta(f), today)
        if reasons:
            flagged += 1
            print(f"[METADATA] {base}: {'; '.join(reasons)}")
    tail = f"; {unchecked} PDF(s) not checked" if unchecked else ""
    print(f"\n--- {flagged} file(s) leaking a tool fingerprint, build date, stray filename, or "
          f"multi-revision editing residue{tail}. Clean before shipping. ---")
    return flagged

def _clean_pdf(path, app, date):
    import pypdf
    revs_before = _pdf_revision_count(path)
    r = pypdf.PdfReader(path)
    if r.is_encrypted:
        raise RuntimeError("PDF is encrypted; cannot clean, regenerate from source")
    # clone_from preserves the document catalog (outline/bookmarks, named destinations, AcroForm),
    # which append_pages_from_reader silently drops.
    try:
        w = pypdf.PdfWriter(clone_from=path)
    except TypeError:  # very old pypdf without clone_from
        w = pypdf.PdfWriter(); w.append_pages_from_reader(r)
    d = f"D:{date.replace('-', '')}000000Z" if date else None
    # For a PDF, "Application" isn't a field; strip Producer/Creator (empty) unless caller forced one.
    info = {"/Producer": app or "", "/Creator": app or ""}
    if d:
        info["/ModDate"] = d; info["/CreationDate"] = d
    w.add_metadata(info)
    tmp = path + ".qc_tmp"
    with open(tmp, "wb") as fh:
        w.write(fh)
    os.replace(tmp, path)  # atomic on Windows
    revs_after = _pdf_revision_count(path)
    note = f", collapsed {revs_before} -> {revs_after} revision(s)" if revs_before > 1 else ""
    print(f"cleaned PDF metadata: {path}{note}")

def _clean_office(path, app, date):
    modts = f"{date}T00:00:00Z" if date else None
    tmp = path + ".qc_tmp"
    try:
        with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.namelist():
                data = zin.read(item)
                if item == "docProps/app.xml":
                    txt = data.decode("utf-8", "ignore")
                    if app:
                        txt = re.sub(r"<Application>.*?</Application>", f"<Application>{app}</Application>", txt)
                    txt = re.sub(r"<Company>.*?</Company>", "<Company></Company>", txt)
                    data = txt.encode("utf-8")
                elif item == "docProps/core.xml":
                    txt = data.decode("utf-8", "ignore")
                    txt = re.sub(r"(<dc:creator[^>]*>).*?(</dc:creator>)", r"\g<1>\g<2>", txt)
                    txt = re.sub(r"(<cp:lastModifiedBy[^>]*>).*?(</cp:lastModifiedBy>)", r"\g<1>\g<2>", txt)
                    txt = re.sub(r"(<dc:description[^>]*>).*?(</dc:description>)", r"\g<1>\g<2>", txt)
                    if modts:
                        txt = re.sub(r"(<dcterms:modified[^>]*>).*?(</dcterms:modified>)", rf"\g<1>{modts}\g<2>", txt)
                        txt = re.sub(r"(<dcterms:created[^>]*>).*?(</dcterms:created>)", rf"\g<1>{modts}\g<2>", txt)
                    data = txt.encode("utf-8")
                zout.writestr(item, data)
        os.replace(tmp, path)  # inside the try: a failure here must still hit the cleanup below
    except PermissionError:
        _rm(tmp)
        raise RuntimeError(f"cannot write {os.path.basename(path)}, is it open in Excel/Word, or read-only? Close it and retry")
    except Exception as e:
        _rm(tmp)
        raise RuntimeError(f"Office clean failed ({e}); regenerate from source instead")
    print(f"cleaned Office metadata: {path}  (Application={app or 'unchanged'}, date={date or 'unchanged'})")

def _rm(p):
    try:
        if os.path.exists(p): os.remove(p)
    except Exception:
        pass

def _resolve_backup_root(path, world=None):
    """Where backups go. Must land OUTSIDE the delivered world, whatever depth `path` sits at.

    Order:
      1. --world was given: <world>_qc_backup, beside the root. Unambiguous, so the skill passes it.
      2. Walk UP from the target looking for an existing "<dir>_qc_backup" beside an ancestor. The
         other fixers create that at world level, so on a normal round it is already there and this
         finds the same place.
      3. Nothing to go on: stop and ask for --world rather than guess. Guessing is what put ten
         backup folders inside a builder's delivered world.
    """
    if world:
        return _common.default_backup_dir(world)

    start = os.path.abspath(path if os.path.isdir(path) else os.path.dirname(path) or ".")
    cur = start
    found = None
    # Bounded climb, three levels. Walking to the filesystem root finds an unrelated workspace
    # belonging to a DIFFERENT world in a shared parent (a Downloads folder, a projects folder)
    # and quietly files this world's backups into it.
    #
    # Three is the number that works: a file at world/a/b/c.xlsx reaches the workspace that sits
    # beside `world` on the third step, and stops before the folder that holds the world itself.
    for _ in range(3):
        cand = _common.default_backup_dir(cur)
        if os.path.isdir(cand):
            found = cand                      # keep climbing: prefer the OUTERMOST match
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    if found:
        return found

    sys.exit(
        "metadata_hygiene: I cannot tell where this world's root is, so I do not know where to put\n"
        "backups without risking writing them inside the world you are about to deliver.\n\n"
        f"  target: {path}\n\n"
        "Re-run with --world pointing at the top of the world folder, e.g.\n"
        "  python metadata_hygiene.py clean <file> --world <world_folder>\n\n"
        "Or pass --backup-dir to name the location yourself, or --no-backup if another tool has\n"
        "already backed these files up this round.")



def clean_many(paths, app, date, no_backup, world=None, backup_dir=None):
    """Clean an explicit list of files. This is the normal case.

    Editing a file is what creates a fresh tool fingerprint, so only the files you actually edited
    need cleaning. Running `clean` across a whole world rewrites metadata on every file, which shows
    up as dozens of unexplained changed files in the next round's diff and buries the real edits.
    """
    total = 0
    for p in paths:
        total += clean(p, app, date, no_backup, world, backup_dir) or 0
    return total


def clean(path, app, date, no_backup, world=None, backup_dir=None):
    if not os.path.exists(path):
        sys.exit(f"! path not found: {path}")
    if not date:
        print("! WARNING: no --date given, the build/today date (if present) is LEFT IN PLACE and "
              "will still be flagged. Re-run with --date YYYY-MM-DD (a date that fits your world).",
              file=sys.stderr)
    files = _world_files(path, OFFICE_EXTS + ("pdf",))
    if not files:
        print("(nothing to clean, no Office/PDF files found)"); return 0
    # Backups go beside the WORLD ROOT, never anywhere inside the delivered tree.
    #
    # This has now been wrong twice. First it joined "_qc_backup" onto the target path, so backups
    # landed inside the world. That was "fixed" by putting them BESIDE the target path, which is
    # correct only when the target is the world root. Clean a file three folders down, which is the
    # normal case, and "beside it" is still deep inside the delivered tree:
    #
    #     filesystem/deliver/budgets/q3.xlsx  ->  filesystem/deliver/budgets_qc_backup/
    #
    # A builder found ten of those in a delivered world. They also make inventory_check report
    # false "unregistered file" and "duplicate artifact claim" errors, and clearing them needs a
    # recursive delete inside the world, which is exactly the operation nobody should be running there.
    backup_root = backup_dir or (None if no_backup else _resolve_backup_root(path, world))
    cleaned = failed = 0
    for f in sorted(files):
        ext = f.lower().rsplit(".", 1)[-1]
        try:
            if not no_backup:
                _common.backup_file(f, backup_root)
            if ext == "pdf":
                _clean_pdf(f, app, date)   # app=None -> strip producer/creator
            else:
                _clean_office(f, app or _default_app(ext), date)
            cleaned += 1
        except Exception as e:
            failed += 1
            print(f"! {f}: {e}", file=sys.stderr)
    if not no_backup and cleaned:
        print(f"(originals backed up in {backup_root})")
    if failed:
        print(f"--- cleaned {cleaned}, {failed} failed (see messages above) ---")
    return cleaned

def sweep(world, write=False):
    """List, and with --write remove, this toolkit's own residue from inside a world folder.

    Only ever touches two things: directories named "*_qc_backup" and known OS junk files. It does
    not delete anything else, so it is safe to run on a delivered world, and it exists so that
    clearing this mess never requires a recursive delete typed by hand.
    """
    import shutil
    world = os.path.abspath(world.rstrip("/\\"))
    if not os.path.isdir(world):
        sys.exit(f"! not a folder: {world}")

    strays, junk = [], []
    for dp, dns, fns in os.walk(world):
        for d in list(dns):
            if d.endswith("_qc_backup"):
                strays.append(os.path.join(dp, d))
                dns.remove(d)                      # do not descend into what we are removing
        for f in fns:
            if f.lower() in ("​.ds_store", ".ds_store", "thumbs.db", "desktop.ini"):
                junk.append(os.path.join(dp, f))

    print("=" * 78)
    print("STRAY BUILD RESIDUE INSIDE THE WORLD")
    print("=" * 78)
    if not strays and not junk:
        print("\n  None. Nothing of this toolkit's is inside the world folder.")
        return 0

    for d in strays:
        n = sum(len(f) for _, _, f in os.walk(d))
        print(f"\n  backup folder   {os.path.relpath(d, world)}   ({n} file(s) inside)")
    for f in junk:
        print(f"  OS junk file    {os.path.relpath(f, world)}")

    if not write:
        print("\n  Nothing removed. Re-run with --write to remove them.")
        print("  Every one of these is a copy or an OS artifact. None is world content.")
        return len(strays) + len(junk)

    removed = 0
    for d in strays:
        try:
            shutil.rmtree(d); removed += 1
        except OSError as e:
            print(f"  ! could not remove {d}: {e}", file=sys.stderr)
    for f in junk:
        try:
            os.remove(f); removed += 1
        except OSError as e:
            print(f"  ! could not remove {f}: {e}", file=sys.stderr)
    print(f"\n  Removed {removed} item(s). The world folder now holds world content only.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("scan"); sc.add_argument("path")
    cl = sub.add_parser("clean"); cl.add_argument("path")
    cl.add_argument("--app", default=None, help="Application string (default: native app for the file type)")
    cl.add_argument("--date", default=None, help="in-world date YYYY-MM-DD for modified/created")
    cl.add_argument("--no-backup", action="store_true", help="do not copy originals into _qc_backup first")
    cl.add_argument("--also", nargs="*", default=[], metavar="FILE",
                    help="more files to clean; pass every file you edited this round rather than "
                         "pointing this at the whole world")
    cl.add_argument("--world", default=None, metavar="DIR",
                    help="the world's TOP folder. Backups go beside it, never inside it. Always "
                         "pass this: without it, a file nested in subfolders leaves a stray "
                         "_qc_backup folder in the delivered tree.")
    cl.add_argument("--backup-dir", default=None, metavar="DIR",
                    help="put backups exactly here instead")

    sw = sub.add_parser("sweep", help="remove stray _qc_backup folders and OS junk from inside a world")
    sw.add_argument("world")
    sw.add_argument("--write", action="store_true", help="actually remove them (default: list only)")
    a = ap.parse_args()
    if a.cmd == "sweep":
        sys.exit(1 if sweep(a.world, a.write) else 0)
    if a.cmd == "scan": scan(a.path)
    elif a.cmd == "clean":
        targets = [a.path] + list(a.also or [])
        if os.path.isdir(a.path) and not a.also:
            print("NOTE: cleaning a whole directory rewrites metadata on every file in it, which")
            print("      shows up as unexplained changes in the next round's diff. Prefer naming the")
            print("      files you edited:  clean <file1> --also <file2> <file3>\n")
        clean_many(targets, a.app, a.date, a.no_backup, a.world, a.backup_dir)

if __name__ == "__main__":
    main()
