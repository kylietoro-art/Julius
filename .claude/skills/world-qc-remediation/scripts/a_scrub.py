#!/usr/bin/env python3
"""A## build-artifact scrub, the headline class-level fixer.

Synthetic worlds are built from a spec whose ④ Artifacts tab gives every artifact an internal code
(A01, A26, A123...). Those codes are BUILD scaffolding, a solver should never see them. When they
leak into world files ("System-of-record per Policy A09", "occupant loads mirror A26 verbatim"),
that's the Type-G defect. This tool fixes the whole class in one pass:

  1. Build the map A## -> human-readable artifact name from the spec's ④ Artifacts tab (same reader
     spec_check uses, so the map matches `refs`).
  2. Enumerate every A## occurrence across the world's readable files (csv/xlsx/txt/md/html/json/docx;
     PDFs too if a PDF lib is present).
  3. CLASSIFY each: a code that IS in the ④ registry -> resolvable, swap it for the artifact name.
     A code that is NOT in ④ (a real invoice number, a room code, a part code that merely looks like
     A##) -> REVIEW list, NEVER changed automatically.
  4. With `apply --write`: make the swaps, back up every file first, and record every change to
     change_manifest.md / comments.txt so you can skim for any phrasing that needs a human polish
     (e.g. "per Policy A09" -> "per Policy the System-of-Record Policy" reads doubled, the manifest
     shows you exactly which lines to smooth).

  scan  <spec.xlsx> <world_dir>
  apply <spec.xlsx> <world_dir> [--write] [--backup-dir DIR]

Default is a DRY RUN. PDFs are routed through pdf_replace.py (full non-incremental save, cp1252 guard).
After --write, run metadata_hygiene.py clean on every changed file.

Deps: openpyxl (spec + xlsx); python-docx for docx; PyMuPDF/pypdf for PDFs (optional, PDFs listed
for manual handling if absent).
"""
import argparse, os, re, sys, glob, csv, subprocess
import _common
import spec_check
_common.setup_console()

CODE_RE = spec_check.ID_RE  # \bA\d{2,3}\b
HERE = os.path.dirname(os.path.abspath(__file__))

def build_map(spec):
    wb = spec_check.load(spec)
    idx = spec_check.artifact_index(wb)
    amap = {aid: meta.get("name", "").strip() for aid, meta in idx.items()}
    resolvable = {k: v for k, v in amap.items() if v}
    nameless = {k for k, v in amap.items() if not v}  # in ④ but no readable name
    return resolvable, nameless

_STOP = {"the", "a", "an", "of", "and", "for", "per", "to", "in", "on", "by", "or", "with"}

def _phrase(name):
    """How the artifact name reads when it replaces a bare code. Prefix a bare noun phrase with
    'the' so 'cites A41' -> 'cites the Reorganization Announcement' reads naturally. Names that
    already start with an article/determiner are left as-is."""
    if re.match(r"^(the|a|an|our|its|this)\b", name, re.I):
        return name
    return "the " + name

def _keywords(name):
    return {w for w in re.findall(r"[a-z0-9]+", name.lower()) if len(w) > 3 and w not in _STOP}

def _swap(text, resolvable):
    """Replace each resolvable A## with its artifact name, but ONLY where that reads cleanly.
    If the code sits next to words the artifact name already contains (e.g. "per Policy A09", where
    the name is "System-of-Record Policy"), a blind swap doubles the descriptor
    ("per Policy the System-of-Record Policy"). Collapsing that needs judgment, so we leave the code
    in place and flag the occurrence for a human rewrite instead of mangling the prose.

    Returns (new_text, applied[(code, replacement)], review[(code, reason)])."""
    applied, review, out, last = [], [], [], 0
    for m in CODE_RE.finditer(text):
        code = m.group(0)
        out.append(text[last:m.start()])
        if code in resolvable:
            name = resolvable[code]
            ctx = (text[max(0, m.start() - 45):m.start()] + " " + text[m.end():m.end() + 45]).lower()
            if any(kw in ctx for kw in _keywords(name)):
                review.append((code, f"context already names \"{name}\", rewrite by hand "
                                     f"(drop the adjacent descriptor, e.g. \"…the {name}\")"))
                out.append(code)
            else:
                rep = _phrase(name)
                applied.append((code, rep))
                out.append(rep)
        else:
            review.append((code, "not in the ④ registry, real invoice/room/part code? left unchanged"))
            out.append(code)
        last = m.end()
    out.append(text[last:])
    return "".join(out), applied, review

# ---- per-format apply ---------------------------------------------------------------------------

TEXT_EXTS = ("txt", "md", "html", "htm", "json", "eml", "csv", "tsv")

def _apply_textfile(path, resolvable, write):
    old = _common.read_text(path)
    new, applied, review = _swap(old, resolvable)
    if applied and write:
        _common.write_text(path, new)
    return applied, review

def _apply_xlsx(path, resolvable, write):
    import openpyxl
    wb = openpyxl.load_workbook(path)  # keep formulas
    applied, review = [], []
    changed = False
    touched = []          # (sheet, coord, old value) so the save knows what may now be stale
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                # A26 is a valid CELL REFERENCE as well as a build code. Rewriting it inside a
                # formula turns =SUM(A26:A30) into =SUM(the Occupant Load Table:A30), which is a
                # broken workbook. Worse, the cached result is preserved by the save, so the sheet
                # still shows the old number and no downstream check notices.
                if isinstance(c.value, str) and c.value.lstrip().startswith("="):
                    # Report only what a human could plausibly need to look at. Every code here
                    # is a syntactic cell reference, so reporting them all buries the genuine
                    # review items: one workbook of =SUM(A2:A400) formulas produced 58 review
                    # lines and one real finding. Flag only a code that appears OUTSIDE any
                    # reference, e.g. inside a quoted string in the formula.
                    bare = _common._STRINGS.findall(c.value)
                    for quoted in bare:
                        m = CODE_RE.search(quoted)
                        if m and m.group(0) in resolvable:
                            review.append((m.group(0),
                                           f"appears inside a quoted string in the formula in "
                                           f"{ws.title}!{c.coordinate}: {c.value!r}. Left alone, "
                                           f"editing a formula here would break it. Fix by hand."))
                    continue
                if isinstance(c.value, str) and CODE_RE.search(c.value):
                    new, ap, rv = _swap(c.value, resolvable)
                    applied += ap; review += rv
                    if ap and new != c.value:
                        if write:
                            touched.append((ws.title, c.coordinate, c.value))
                            c.value = new
                        changed = True
    if changed and write:
        # Not wb.save(). A plain openpyxl save blanks the cached result of every formula in
        # the book, and AutoQC reads those cached results, so a text-only scrub would come
        # back next round as a page of empty cells. This swap only touches text, so the
        # cached numbers are all still correct and get carried across.
        _common.save_xlsx_preserving_values(wb, path, changed=touched)
    return applied, review

def _apply_docx(path, resolvable, write):
    try:
        import docx
    except ImportError:
        return None, None  # signal: needs python-docx
    d = docx.Document(path)
    applied, review = [], []
    def do_paragraphs(paragraphs):
        nonlocal applied, review
        for p in paragraphs:
            for run in p.runs:
                if run.text and CODE_RE.search(run.text):
                    new, ap, rv = _swap(run.text, resolvable)
                    applied += ap; review += rv
                    if ap and write:
                        run.text = new
    do_paragraphs(d.paragraphs)
    for table in d.tables:
        for row in table.rows:
            for cellobj in row.cells:
                do_paragraphs(cellobj.paragraphs)
    if applied and write:
        d.save(path)
    return applied, review

def _apply_pdf(path, resolvable, write):
    """Enumerate codes in the PDF's text, then route each swap through pdf_replace.py (which does a
    full non-incremental save and guards cp1252). Returns (applied, review) or (None, None) if no
    PDF text lib is available to even read it."""
    txt = spec_check.extract_text(path)
    if txt is None:
        return None, None
    _, applied, review = _swap(txt, resolvable)
    if applied and write:
        # de-dup codes; apply each once (pdf_replace swaps all occurrences on all pages)
        for code, rep in {c: r for c, r in applied}.items():
            try:
                subprocess.run([sys.executable, os.path.join(HERE, "pdf_replace.py"),
                                path, code, rep, "-o", path],
                               check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"  ! pdf_replace failed on {os.path.basename(path)} for {code}: "
                      f"{(e.stderr or e.stdout or '').strip()[:160]}", file=sys.stderr)
    return applied, review

def _apply_any(path, ext, resolvable, write):
    """One dispatcher for every format, so the dry-run probe and the real pass cannot drift."""
    if ext in TEXT_EXTS:
        return _apply_textfile(path, resolvable, write)
    if ext in ("xlsx", "xlsm"):
        return _apply_xlsx(path, resolvable, write)
    if ext == "docx":
        return _apply_docx(path, resolvable, write)
    if ext == "pdf":
        return _apply_pdf(path, resolvable, write)
    return [], []


def _world_files(world_dir, spec=None):
    """Every file in the world, minus this skill's own output, minus the spec itself.

    Builders routinely drop World_Spec.xlsx inside the world folder. Scrubbing it rewrites the ID
    column of its own ④ Artifacts registry ("A26" becomes "the Occupant Load Table"), which makes
    the spec unusable by every other tool here and is not something the user would ever spot.
    """
    spec_abs = os.path.abspath(spec) if spec else None
    out = []
    for f in glob.glob(os.path.join(world_dir, "**", "*"), recursive=True):
        if not os.path.isfile(f) or _common.is_qc_artifact(f):
            continue
        if spec_abs and os.path.abspath(f) == spec_abs:
            print(f"  NOTE: skipping {os.path.basename(f)}, that is the spec, not a world file.")
            continue
        out.append(f)
    return out

def run(spec, world_dir, write, backup_dir):
    if not os.path.isfile(spec):
        sys.exit(f"a_scrub: spec file not found: {spec}")
    if not os.path.isdir(world_dir):
        sys.exit(f"a_scrub: world_dir not found or not a directory: {world_dir}")
    resolvable, nameless = build_map(spec)
    if not resolvable:
        sys.exit("a_scrub: no artifacts with names found in the spec's ④ Artifacts tab, nothing to map. "
                 "Check that the spec has an Artifacts tab with an ID column and a Name column.")
    mode = "WRITE" if write else "DRY RUN (no files changed; add --write to apply)"
    print(f"A## SCRUB, {mode}, {len(resolvable)} artifact codes mapped from the spec.\n")
    changes, review_lines, needs_lib = [], [], []
    total_fixed = 0
    review_codes = set()
    for f in sorted(_world_files(world_dir, spec)):
        base = os.path.relpath(f, world_dir)
        ext = f.lower().rsplit(".", 1)[-1] if "." in f else ""
        # Copy the file BEFORE anything touches it. Every _apply_* writes in place, so a backup
        # taken afterwards is a copy of the damaged file and the original is gone for good.
        #
        # Only for files this run will actually change: a dry-run pass first tells us which. Backing
        # up everything deposited a full duplicate of the world on every --write, and the collision
        # suffixes from successive runs made it impossible to tell which copy came from which round.
        #
        # A backup failure SKIPS that one file. It must not exit: the loop has already edited
        # earlier files, so exiting here leaves the world half-scrubbed and jumps over the manifest
        # write at the end, destroying the only record of what changed.
        if write:
            try:
                probe, _ = _apply_any(f, ext, resolvable, False)
            except Exception:  # noqa: BLE001
                probe = None
            if probe:
                try:
                    _common.backup_file(f, backup_dir, root=world_dir)
                except OSError as e:
                    review_lines.append(f"{base}: NOT CHANGED, could not back it up ({e}). "
                                        f"Nothing is edited without a backup.")
                    continue
        try:
            if ext in TEXT_EXTS:
                applied, review = _apply_textfile(f, resolvable, write)
            elif ext in ("xlsx", "xlsm"):
                applied, review = _apply_xlsx(f, resolvable, write)
            elif ext == "docx":
                applied, review = _apply_docx(f, resolvable, write)
            elif ext == "pdf":
                applied, review = _apply_pdf(f, resolvable, write)
            else:
                continue
        except Exception as e:
            review_lines.append(f"{base}: could not process ({e}), check by hand")
            continue
        if applied is None:  # needed a lib we don't have
            needs_lib.append(base); continue
        if applied:
            if write:
                # The backup is taken above, BEFORE the write. Copying the file at this point
                # would copy the version we just edited, so "Backups in <dir>" would be true and
                # useless: a bad swap or a wrong spec would be unrecoverable for every format.
                pass
            for code, rep in applied:
                total_fixed += 1
                print(f"[FIX] {base}: {code} -> {rep!r}")
                changes.append((base, "in-text code", code, rep))
        for code, reason in review:
            review_codes.add(code)
            review_lines.append(f"{base}: {code}, {reason}")
    if needs_lib:
        for b in needs_lib:
            review_lines.append(f"{b}: contains A## codes but needs python-docx / a PDF lib to edit, install it and re-run")
    if write and changes:
        _common.append_manifest(backup_dir, "a_scrub", changes, review_lines)
    verb = "Fixed" if write else "Would fix"
    print(f"\n--- {verb} {total_fixed} A## occurrence(s). "
          f"{len(review_codes)} distinct code(s) left for review"
          f"{'; ' + str(len(needs_lib)) + ' file(s) need a library' if needs_lib else ''}. ---")
    if review_lines:
        print("\nLeft for you to check (NOT changed):")
        for r in review_lines[:40]:
            print(f"  · {r}")
        if len(review_lines) > 40:
            print(f"  · … and {len(review_lines) - 40} more (see change_manifest.md)")
    if write and total_fixed:
        print(f"\nBackups + change_manifest.md / comments.txt in {backup_dir} (beside your world, not inside it).")
        print("Skim change_manifest.md for any doubled/awkward phrasing.")
        print("NEXT: run metadata_hygiene.py clean on every changed file.")
    elif not write and total_fixed:
        print("\nThis was a dry run. Re-run with `apply … --write` to apply the swaps above.")
    return total_fixed

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("spec"); s.add_argument("world_dir")
    a = sub.add_parser("apply"); a.add_argument("spec"); a.add_argument("world_dir")
    a.add_argument("--write", action="store_true", help="actually modify files (default: dry run)")
    a.add_argument("--backup-dir", default=None)
    args = ap.parse_args()
    backup_dir = (getattr(args, "backup_dir", None) or _common.default_backup_dir(args.world_dir))
    write = getattr(args, "write", False) and args.cmd == "apply"
    run(args.spec, args.world_dir, write, backup_dir)

if __name__ == "__main__":
    main()
