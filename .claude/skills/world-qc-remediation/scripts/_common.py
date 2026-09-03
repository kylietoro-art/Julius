#!/usr/bin/env python3
"""Shared helpers for the world-qc-remediation scripts.

Kept tiny and dependency-free so every script can `import _common` (Python always puts a script's
own directory on sys.path, so this resolves no matter what the current working directory is).

The one thing here that matters most: `read_text` decodes real-world files that are NOT UTF-8.
Synthetic worlds are full of cp1252 CSV/TXT (accented vendor names, €, en-dashes, smart quotes).
Reading those with plain utf-8 + errors="ignore"/"replace" silently drops the very characters we
search for, so a value that IS present reads as absent, a false "all clear". The fallback chain
below decodes them correctly instead.
"""
import sys, os, shutil

def setup_console():
    """Make stdout/stderr tolerate non-ASCII on a cp1252 Windows console (— ✓ ② etc.) instead of
    crashing with UnicodeEncodeError. Call once at the top of each script."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def sniff_encoding(raw):
    """(encoding name, had a BOM). The name is what we must WRITE BACK to hand the file to the
    next reader unchanged.

    UTF-16 is checked first and by BOM, because cp1252 raises on only five byte values and will
    therefore happily "decode" UTF-16 into NUL-interleaved mojibake without ever erroring. Excel's
    "Unicode Text" export and PowerShell's Out-File both produce UTF-16, so this is not exotic on
    the Windows machines this toolkit runs on.
    """
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return ("utf-16", True)
    if raw.startswith(b"\xef\xbb\xbf"):
        return ("utf-8-sig", True)
    # A UTF-16 file written without a BOM still gives itself away: half its bytes are NUL.
    head = raw[:4096]
    if head and head.count(b"\x00") > len(head) // 3:
        return ("utf-16-le" if head[1:2] == b"\x00" else "utf-16-be", False)
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            raw.decode(enc)
            return (enc, False)
        except UnicodeDecodeError:
            continue
    return ("utf-8", False)


def decode_bytes(raw):
    """Decode bytes with a real-world fallback chain, UTF-16 included."""
    enc, _ = sniff_encoding(raw)
    try:
        return raw.decode(enc)
    except (UnicodeDecodeError, LookupError):
        return raw.decode("utf-8", errors="replace")


def detect_newline(path):
    """The line ending this file uses to end its RECORDS.

    Decode before looking. A UTF-16 file stores CRLF as "\r\x00\n\x00", so a raw byte scan for
    b"\r\n" never finds it and reports LF for a CRLF file.

    Judge on the FIRST line ending, not on whether one appears anywhere. A CRLF sitting inside a
    quoted CSV field would otherwise flip an entire LF file to CRLF on a one-cell edit.
    """
    try:
        with open(path, "rb") as fh:
            text = decode_bytes(fh.read(65536))
    except OSError:
        return "\n"
    i = text.find("\n")
    if i < 0:
        return "\n"
    return "\r\n" if i > 0 and text[i - 1] == "\r" else "\n"


def write_text(path, text, like=None, newline=None):
    """Write text back in the SAME encoding and line endings the file already had.

    Reading a cp1252 file and saving it as UTF-8 turns every accented vendor name, smart quote and
    euro sign into mojibake the moment Excel reopens it, on a file we only touched to change one
    name. The user did not ask for a re-encode and will not find out until much later.

    `like` is the path whose encoding to copy, defaulting to the file being written.

    `newline` follows open()'s meaning. Leave it None and we translate "\n" to whatever the file
    already used. Pass "" when the text ALREADY carries its final line endings: translation would
    otherwise also rewrite newlines that live INSIDE a quoted CSV field, turning a preserved
    "\r\n" into "\r\r\n" and corrupting the field it was trying to protect.
    """
    src = like or path
    enc, bom = "utf-8", False
    try:
        with open(src, "rb") as fh:
            raw = fh.read()
        enc, bom = sniff_encoding(raw)
        if newline is None:
            # decoded, not a byte scan: UTF-16 stores CRLF as "\r\x00\n\x00"
            _t = decode_bytes(raw[:65536])
            _i = _t.find("\n")
            newline = "\r\n" if (_i > 0 and _t[_i - 1] == "\r") else ""
    except OSError:
        pass
    if newline is None:
        newline = ""
    # utf-8-sig round-trips the BOM on write; plain utf-8 would silently drop it.
    if enc == "utf-8" and bom:
        enc = "utf-8-sig"

    # Do the line-ending conversion HERE, then write with no translation at all.
    #
    # read_text decodes bytes, so a CRLF file comes back with real "\r\n" in the string. Handing
    # that to open(newline="\r\n") makes Python translate the "\n" as well, producing "\r\r\n":
    # a blank record between every row, compounding on each pass. Normalise first, emit once.
    if newline:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        if newline != "\n":
            text = text.replace("\n", newline)
    try:
        with open(path, "w", encoding=enc, newline="") as fh:
            fh.write(text)
    except (UnicodeEncodeError, LookupError):
        # The edit introduced a character the original encoding cannot hold. Widening to UTF-8 is
        # the only way to keep the content, so do it, but never silently.
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        print(f"  NOTE: {os.path.basename(path)} was {enc} but the new text needs UTF-8. "
              f"Saved as UTF-8.")

def read_text(path):
    """Read a text file as a correctly-decoded str, whatever its encoding."""
    with open(path, "rb") as fh:
        return decode_bytes(fh.read())

QC_ARTIFACT_NAMES = {"change_manifest.md", "comments.txt"}

def is_qc_artifact(path):
    """True for files this skill itself writes (backups, the change log), so a world scan never
    re-flags its own output, and a builder who re-zips the world folder doesn't ship the backups.
    Every world-traversal in the skill filters on this."""
    parts = os.path.normpath(path).split(os.sep)
    if any(p.endswith("_qc_backup") or p == WORKSPACE for p in parts):
        return True
    return os.path.basename(path) in QC_ARTIFACT_NAMES

WORKSPACE = "qc_workspace"


def default_backup_dir(world_dir):
    """ONE folder beside the world holding everything this toolkit writes: backups, the change
    manifest, round history, tickets, inventory snapshots, the corpus cache.

    It used to be `<world>_qc_backup`, one per world folder, which meant a builder's working
    directory filled up with lookalike folders across a ten-round build: several manual copies,
    several tool folders, and a `<copy>_qc_backup` where a tool had run against a copy. A
    non-technical expert then cannot tell which folder is the one to upload, which is the single
    most expensive mistake available to them.

    Now: the world folder, and `qc_workspace` next to it. Nothing else.
    """
    ab = os.path.abspath(world_dir.rstrip("/\\"))
    new = os.path.join(os.path.dirname(ab), WORKSPACE)

    # Carry an in-progress build across the rename. Someone six rounds deep when they upgrade has
    # their whole round history in the old `<world>_qc_backup`. Without this the new build finds no
    # history, and round_log cheerfully reports "no repeat classes, last round's fixes held" about a
    # defect that has come back six times. That is worse than losing the history: it is a confident
    # wrong answer at the exact moment the expert needs the opposite.
    old = os.path.join(os.path.dirname(ab), os.path.basename(ab) + "_qc_backup")
    if not os.path.exists(new) and os.path.isdir(old):
        try:
            os.rename(old, new)
            print(f"  NOTE: moved your existing {os.path.basename(old)} to {WORKSPACE}. "
                  f"Round history is intact.")
        except OSError:
            return old          # could not move it, so keep using it rather than lose the history
    return new

def backup_file(path, backup_dir, root=None):
    """Copy path into backup_dir before we overwrite it, KEEPING its folder structure.

    Pass `root` (the world folder) and the copy lands at <backup>/<same relative path>. Without it,
    world/Summary.csv and world/q3/Summary.csv both reduce to "Summary.csv" and the second becomes
    "Summary__1.csv", so nothing on disk records which is which and a restore is guesswork. Real
    worlds repeat basenames constantly (Cover.csv, Notes.csv, Summary.csv per folder).

    Returns the backup path.
    """
    rel = None
    if root:
        try:
            r = os.path.relpath(os.path.abspath(path), os.path.abspath(root))
            if not r.startswith(".."):
                rel = r
        except ValueError:            # different drive on Windows
            rel = None
    # Backups live under <workspace>/backups/, so the workspace root stays readable: a person
    # opening it sees backups/, the round log and the change manifest, not a heap of loose copies.
    root_dir = os.path.join(backup_dir, "backups")
    dest = os.path.join(root_dir, rel) if rel else os.path.join(root_dir, os.path.basename(path))
    os.makedirs(os.path.dirname(dest) or root_dir, exist_ok=True)
    # avoid clobbering same-basename files from different folders
    n = 1
    base = dest
    while os.path.exists(dest):
        stem, ext = os.path.splitext(base)
        dest = f"{stem}__{n}{ext}"
        n += 1
    shutil.copy2(path, dest)
    return dest

def append_manifest(out_dir, tool, changes, review=None):
    """Record what a fixer changed, in two builder-facing files written to out_dir, which is the
    _qc_backup folder BESIDE the world, deliberately NOT inside it, so re-zipping the world to upload
    never ships a stray log/manifest (itself a filesystem-leakage tell):

      change_manifest.md, a table (file | location | old | -> | new) the builder skims to confirm
                            nothing legitimate was rewritten.
      comments.txt, one plain line per change, for pasting change comments into the review tool.

    Both are APPENDED to, so several fixers in one run accumulate into one record.
    changes: list of (file, location, old, new). review: optional list of plain-text strings
    (things left untouched for the builder to check by hand)."""
    if not changes and not review:
        return
    os.makedirs(out_dir, exist_ok=True)
    man = os.path.join(out_dir, "change_manifest.md")
    com = os.path.join(out_dir, "comments.txt")
    new_man = not os.path.exists(man)
    with open(man, "a", encoding="utf-8") as fh:
        if new_man:
            fh.write("# Change manifest\n\nEvery automated change to this world, newest tool last. "
                     "Skim it to confirm nothing legitimate was rewritten.\n")
        fh.write(f"\n## {tool}\n\n")
        if changes:
            fh.write("| File | Location | Old | → | New |\n|---|---|---|---|---|\n")
            for f, loc, old, new in changes:
                fh.write(f"| {f} | {loc} | {old} | → | {new} |\n")
        if review:
            fh.write("\n**Left for you to check (not changed):**\n")
            for r in review:
                fh.write(f"- {r}\n")
    with open(com, "a", encoding="utf-8") as fh:
        for f, loc, old, new in changes:
            fh.write(f"{f} ({loc}): changed \"{old}\" to \"{new}\"\n")


# ======================================================================================
# Saving a workbook without throwing away its answers.
#
# An xlsx stores each formula twice: the formula, and the number Excel last computed and
# cached beside it. Everything that reads VALUES reads the cache. AutoQC reads values. It
# does not calculate.
#
# openpyxl does not calculate either, and on save it writes `<f>SUM(A1:A2)</f><v></v>` for
# every formula cell in the book, not just the ones you touched. The formulas survive, the
# numbers do not, and the grader sees a page of blanks.
#
# The fixers that call this only swap TEXT inside cells. They never change a number a
# formula depends on, so every cached result is still correct. Snapshot them before the
# save and put them back after. No Excel, no LibreOffice, no recalculation, and nobody has
# to open the file.
# ======================================================================================
import re as _re
import zipfile as _zip

_XL_CELL = _re.compile(rb"<c\b([^>]*)>(.*?)</c>", _re.S)
_XL_REF = _re.compile(rb'r="([A-Z]+\d+)"')
_XL_T = _re.compile(rb'\st="([^"]*)"')
_XL_HAS_F = _re.compile(rb"<f[ />]")
_XL_V_FULL = _re.compile(rb"<v>\s*[^<\s].*?</v>", _re.S)
_XL_V_EMPTY = _re.compile(rb"<v\s*/>|<v>\s*</v>")
_XL_SHEET = _re.compile(rb"<sheet\b([^>]*)/?>")
_XL_REL = _re.compile(rb"<Relationship\b([^>]*)/?>")
_XL_ATTR = _re.compile(rb'([\w:]+)="([^"]*)"')


def _xl_attrs(blob):
    """Attributes as a dict. Never match them positionally: Excel, openpyxl and LibreOffice
    each emit a different attribute ORDER, so an ordered pattern works on the file you tested
    and silently returns nothing on the next one."""
    return {k.decode(): v for k, v in _XL_ATTR.findall(blob)}


def _xl_sheet_files(items):
    """{sheet name: 'xl/worksheets/sheetN.xml'}. Keyed on the NAME, because openpyxl is free
    to renumber the underlying files and a positional guess would silently cross two sheets."""
    wbx, rels = items.get("xl/workbook.xml"), items.get("xl/_rels/workbook.xml.rels")
    if not wbx or not rels:
        return {}
    rid = {}
    for m in _XL_REL.finditer(rels):
        a = _xl_attrs(m.group(1))
        if "Id" in a and "Target" in a:
            rid[a["Id"]] = a["Target"].decode()
    out = {}
    for m in _XL_SHEET.finditer(wbx):
        a = _xl_attrs(m.group(1))
        name = a.get("name")
        ref = a.get("r:id") or a.get("id")
        if name is None or ref is None:
            continue
        tgt = rid.get(ref)
        if not tgt:
            continue
        tgt = tgt.lstrip("/")
        out[name.decode()] = tgt if tgt.startswith("xl/") else "xl/" + tgt
    return out


def _xl_read(path):
    with _zip.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def _xl_cached(items):
    """{sheet name: {cell ref: (<v>..</v> bytes, t attribute or None)}} for formula cells
    that currently carry a computed result."""
    out = {}
    for name, xml in _xl_sheet_files(items).items():
        blob = items.get(xml)
        if not blob:
            continue
        cells = {}
        for m in _XL_CELL.finditer(blob):
            attrs, body = m.group(1), m.group(2)
            if not _XL_HAS_F.search(body):
                continue
            v = _XL_V_FULL.search(body)
            r = _XL_REF.search(attrs)
            if v and r:
                t = _XL_T.search(attrs)
                cells[r.group(1)] = (v.group(0), t.group(1) if t else None)
        if cells:
            out[name] = cells
    return out


# A cell or a RANGE, parsed as one unit: optional sheet, then A1, optionally :B9.
# Parsing endpoints separately and pairing adjacent matches invents ranges that are not in the
# formula: SUM(A1:A5)+SUM(C1:C5) would pair A5 with C1 and cover all of A1:C5, so an edit to B3
# looked like a dependency and the cached value was dropped for no reason.
_RANGE = _re.compile(
    r"(?:(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_.]*))!)?"      # optional sheet
    r"\$?([A-Za-z]{1,3})\$?(\d{1,7})"                      # first cell
    r"(?::\$?([A-Za-z]{1,3})\$?(\d{1,7}))?"                # optional second cell
)
_STRINGS = _re.compile(r'"[^"]*"')


def _col_num(letters):
    n = 0
    for ch in letters.upper():
        n = n * 26 + (ord(ch) - 64)
    return n


def _formula_refs(formula, sheet):
    """[(sheet, min_col, min_row, max_col, max_row)] for every cell or range in the formula.

    String literals are stripped first, so "Order A123 shipped" is not read as a reference.
    """
    body = _STRINGS.sub('""', formula)
    out = []
    for m in _RANGE.finditer(body):
        sh = m.group(1) or m.group(2) or sheet
        c1, r1 = _col_num(m.group(3)), int(m.group(4))
        if m.group(5):
            c2, r2 = _col_num(m.group(5)), int(m.group(6))
        else:
            c2, r2 = c1, r1
        out.append((sh, min(c1, c2), min(r1, r2), max(c1, c2), max(r1, r2)))
    return out


def _formula_touches(formula, sheet, changed_cells, changed_texts):
    """Could this formula's cached result be out of date after our edits?

    Two ways it can be. It can quote a string we rewrote, which is how COUNTIF, SUMIF, VLOOKUP and
    MATCH depend on TEXT. Or it can reference a cell we rewrote.

    When unsure, say yes. Saying yes drops the cached value, the cell reads blank, and the workbook
    scan flags it for the builder. Saying no wrongly leaves a stale NUMBER in the sheet that looks
    right and is not: a footing mismatch introduced by the tool that exists to remove them.

    But do not say yes carelessly either. Every formula wrongly judged dependent loses a correct
    number, and a page of blanks is itself a reported defect.
    """
    f = formula.lstrip("=")
    for t in changed_texts:
        if t and len(t) > 2 and t in f:
            return True
    if not changed_cells:
        return False
    for sh, c1, r1, c2, r2 in _formula_refs(f, sheet):
        for cs, ccol, crow in changed_cells:
            if cs == sh and c1 <= ccol <= c2 and r1 <= crow <= r2:
                return True
    return False


def save_xlsx_preserving_values(wb, path, changed=None):
    """openpyxl's save, with the cached formula results carried across where that is still true.

    openpyxl blanks the cached result of every formula in the book on save, and anything reading
    VALUES (AutoQC included) reads that cache rather than calculating. So a text-only edit would
    silently empty every computed cell in the workbook.

    `changed` is what this edit touched: an iterable of (sheet_name, coordinate, old_value). Pass
    it. Any formula that quotes a changed string or references a changed cell has its cached value
    DROPPED rather than restored, because after the edit that number is wrong. A COUNTIF on a name
    we just conformed is the common case, and restoring its old count would hand the builder a
    footing mismatch that looks like a genuine defect.

    Omit `changed` only when the edit provably cannot affect any formula result.

    Returns the number of cells whose value was carried over.
    """
    changed_cells, changed_texts = set(), set()
    for item in (changed or []):
        sheet, coord, old = (list(item) + [None, None, None])[:3]
        if coord:
            m = _re.match(r"\$?([A-Z]{1,3})\$?(\d+)$", str(coord).upper())
            if m:
                changed_cells.add((sheet, _col_num(m.group(1)), int(m.group(2))))
        if isinstance(old, str) and old.strip():
            changed_texts.add(old.strip())
    try:
        before = _xl_cached(_xl_read(path))
    except Exception:  # noqa: BLE001 - a workbook we cannot read is one we cannot protect
        before = {}

    wb.save(path)
    if not before:
        return 0

    items = _xl_read(path)
    restored = 0

    dropped = 0
    for name, xml in _xl_sheet_files(items).items():
        saved = before.get(name)
        blob = items.get(xml)
        if not saved or not blob:
            continue

        def fix(m, saved=saved, name=name):
            nonlocal restored
            attrs, body = m.group(1), m.group(2)
            if not _XL_HAS_F.search(body) or _XL_V_FULL.search(body):
                return m.group(0)
            r = _XL_REF.search(attrs)
            if not r or r.group(1) not in saved:
                return m.group(0)
            fm = _re.search(rb"<f[^>]*>(.*?)</f>", body, _re.S)
            ftext = fm.group(1).decode("utf-8", "replace") if fm else ""
            if ftext and _formula_touches(ftext, name, changed_cells, changed_texts):
                nonlocal dropped
                dropped += 1
                return m.group(0)          # leave it blank: wrong beats missing here
            v, t = saved[r.group(1)]
            # The type attribute travels with the value. A text result under a numeric cell
            # is a corrupt workbook, which is a worse outcome than the blank we started with.
            attrs = _XL_T.sub(b"", attrs)
            if t is not None:
                attrs = attrs + b' t="' + t + b'"'
            body = _XL_V_EMPTY.sub(b"", body) + v
            restored += 1
            return b"<c" + attrs + b">" + body + b"</c>"

        items[xml] = _XL_CELL.sub(fix, blob)

    if dropped:
        print(f"  NOTE: {dropped} formula cell(s) depend on what was just changed, so their old "
              f"result was not restored.\n        Open the workbook in Excel and save it, or run "
              f"verify_xlsx.py --scan, to put the new numbers in.")
    if restored:
        tmp = path + ".tmp_vals"
        with _zip.ZipFile(tmp, "w", _zip.ZIP_DEFLATED) as z:
            for n, b in items.items():
                z.writestr(n, b)
        os.replace(tmp, path)
    return restored
