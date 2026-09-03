#!/usr/bin/env python3
"""Scan a synthetic-world folder for value occurrences and synthetic tells.

Plain `grep -r` cannot see inside .xlsx/.pdf/.docx (zip/binary) or into metadata. This does.

Two modes:

  occurrences <value> <path>   Find every place <value> appears across all files under <path>
                               (or a single file): text bodies, spreadsheet cells, PDF pages,
                               docx paragraphs/headers, filenames, and metadata. Run BEFORE editing
                               to enumerate everything to change; run AFTER to confirm zero stale
                               hits (or only intended ones).

  tells <path>                 Flag common synthetic tells (sequential placeholders, Lorem ipsum,
                               John Doe, 555 numbers, example.com, TODO/PLACEHOLDER literals,
                               tool-signature metadata) in a file or across a folder.

Optional deps enable more file types: openpyxl (.xlsx), pdfplumber or pypdf (.pdf),
python-docx (.docx), python-pptx (.pptx). Missing ones are skipped with a note rather than crashing.

Examples:
  python scan_world.py occurrences "ABCD12" /path/to/world_folder
  python scan_world.py occurrences "rtw_sky_alliance_booking_pnr_abcd12.pdf" /path/to/world
  python scan_world.py tells /path/to/world_folder
"""
import argparse
import os
import re
import sys

import _common
_common.setup_console()

TEXT_EXT = {".txt", ".md", ".markdown", ".csv", ".tsv", ".eml", ".json", ".html", ".htm",
            ".xml", ".yaml", ".yml", ".log", ".ini", ".cfg", ".py", ".js", ".ts", ".sql"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def note(msg):
    print(f"[note] {msg}", file=sys.stderr)


# Files we could not read. A stderr note scrolls past and the summary still says "0 occurrences",
# which reads as clean. Anything that lands here is surfaced loudly in the summary instead.
UNREAD = []

# Types nothing here can open. Naming them explicitly is the point: silence made a whole class of
# spreadsheet look empty and therefore fine.
UNSUPPORTED = {".xls": "old Excel format", ".doc": "old Word format", ".ppt": "old PowerPoint format",
               ".rtf": "rich text", ".pages": "Apple Pages", ".numbers": "Apple Numbers",
               ".key": "Apple Keynote", ".odt": "OpenDocument text",
               ".ods": "OpenDocument spreadsheet"}


# ---------- text + metadata extraction: returns list of (location, text) ----------

def extract_chunks(path):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".xlsx", ".xlsm"):
            return _xlsx(path)
        if ext == ".pdf":
            return _pdf(path)
        if ext == ".docx":
            return _docx(path)
        if ext == ".pptx":
            return _pptx(path)
        if ext in TEXT_EXT or ext == "":
            return _textfile(path)
    except Exception as e:  # noqa: BLE001
        UNREAD.append((path, str(e)))
        note(f"could not read {path}: {e}")
        return []
    if ext in UNSUPPORTED:
        UNREAD.append((path, f"{UNSUPPORTED[ext]}, nothing here can open it. Convert it and re-run."))
        note(f"cannot open {path} ({UNSUPPORTED[ext]})")
    return []  # unknown binary type



def report_unread():
    """Say loudly when files could not be opened.

    "0 occurrences" and "0 tells" are the summary lines people act on. If half the spreadsheets in
    the world were never opened, that zero is not a clean result, it is an absence of evidence, and
    nothing in the old output distinguished the two.
    """
    if not UNREAD:
        return 0
    print("\n" + "!" * 78)
    print(f"{len(UNREAD)} FILE(S) COULD NOT BE READ. The result above does not cover them.")
    print("!" * 78)
    for p, why in UNREAD[:20]:
        print(f"  {os.path.basename(p)}: {why}")
    if len(UNREAD) > 20:
        print(f"  ... and {len(UNREAD) - 20} more")
    print("\n  A clean scan is only clean for the files that opened. Deal with these before you\n"
          "  treat this world as checked.")
    return len(UNREAD)


def _textfile(path):
    text = _common.read_text(path)
    return [(f"line{i}", line) for i, line in enumerate(text.splitlines(), 1)]


def _xlsx(path):
    try:
        from openpyxl import load_workbook
    except ImportError:
        note("openpyxl not installed; skipping .xlsx content (pip install openpyxl)")
        return []
    chunks = []
    # Read the file TWICE: once for formulas, once for the values Excel computed. A figure that
    # lives in a formula cell (=A1+A2) has its number only in the cached value, so a values-blind
    # scan reports "0 occurrences" for a value that is plainly in the sheet, and the builder
    # confirms their fix against a false negative.
    wb = load_workbook(path, read_only=True, data_only=False)
    try:
        wbv = load_workbook(path, read_only=True, data_only=True)
    except Exception:  # noqa: BLE001
        wbv = None

    # openpyxl's read_only mode yields EmptyCell for blank cells, and EmptyCell has NO .coordinate.
    # Reading it raised on the first blank cell in the sheet, the caller swallowed the exception,
    # and EVERY spreadsheet in the world came back as zero chunks. Scans then reported "0
    # occurrences" and read as clean. Reported from the field as "it doesn't process spreadsheets".
    def _coord(cell):
        c = getattr(cell, "coordinate", None)
        if c:
            return c
        r, col = getattr(cell, "row", None), getattr(cell, "column_letter", None)
        return f"{col}{r}" if col and r else None

    values = {}
    if wbv is not None:
        for ws in wbv.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is None:
                        continue
                    co = _coord(cell)
                    if co:
                        values[(ws.title, co)] = str(cell.value)

    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                co = _coord(cell)
                if co is None:
                    continue
                if cell.value is not None:
                    chunks.append((f"{ws.title}!{co}", str(cell.value)))
                # For a formula cell also emit the computed result, so searching for the NUMBER
                # finds it. Without this, "occurrences 670000000" reports zero for a figure that
                # is visible in the sheet, and the builder confirms a fix against a false negative.
                v = values.get((ws.title, co))
                if v is not None and v != (str(cell.value) if cell.value is not None else None):
                    chunks.append((f"{ws.title}!{co} (value)", v))
    props = wb.properties
    for field in ("creator", "lastModifiedBy", "title", "subject", "keywords", "description"):
        val = getattr(props, field, None)
        if val:
            chunks.append((f"metadata:{field}", str(val)))
    return chunks


def _pdf(path):
    chunks = []
    text_done = False
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                chunks.append((f"page{i}", page.extract_text() or ""))
        text_done = True
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        note(f"pdfplumber failed on {path}: {e}")
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        if not text_done:
            for i, page in enumerate(reader.pages, 1):
                chunks.append((f"page{i}", page.extract_text() or ""))
        meta = reader.metadata or {}
        for k, v in meta.items():
            if v:
                chunks.append((f"metadata:{str(k).lstrip('/')}", str(v)))
    except ImportError:
        if not text_done:
            note("no PDF library (pip install pdfplumber pypdf); skipping .pdf content")
    except Exception as e:  # noqa: BLE001
        note(f"pypdf failed on {path}: {e}")
    return chunks


def _docx(path):
    try:
        import docx
    except ImportError:
        note("python-docx not installed; skipping .docx content (pip install python-docx)")
        return []
    d = docx.Document(path)
    chunks = [("body", "\n".join(p.text for p in d.paragraphs))]
    for si, section in enumerate(d.sections, 1):
        for label, part in (("header", section.header), ("footer", section.footer)):
            txt = "\n".join(p.text for p in part.paragraphs)
            if txt.strip():
                chunks.append((f"{label}{si}", txt))
    for ti, table in enumerate(d.tables, 1):
        for ri, row in enumerate(table.rows, 1):
            for ci, cell in enumerate(row.cells, 1):
                if cell.text.strip():
                    chunks.append((f"table{ti}!r{ri}c{ci}", cell.text))
    cp = d.core_properties
    for field in ("author", "last_modified_by", "title", "subject", "keywords", "comments"):
        val = getattr(cp, field, None)
        if val:
            chunks.append((f"metadata:{field}", str(val)))
    return chunks


def _pptx(path):
    try:
        from pptx import Presentation
    except ImportError:
        note("python-pptx not installed; skipping .pptx content (pip install python-pptx)")
        return []
    prs = Presentation(path)
    chunks = []
    for si, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = "\n".join(p.text for p in shape.text_frame.paragraphs)
                if txt.strip():
                    chunks.append((f"slide{si}", txt))
            if shape.has_table:
                for ri, row in enumerate(shape.table.rows, 1):
                    for ci, cell in enumerate(row.cells, 1):
                        if cell.text.strip():
                            chunks.append((f"slide{si}!table!r{ri}c{ci}", cell.text))
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text
            if notes.strip():
                chunks.append((f"slide{si}!notes", notes))
    cp = prs.core_properties
    for field in ("author", "last_modified_by", "title", "subject", "keywords", "comments"):
        val = getattr(cp, field, None)
        if val:
            chunks.append((f"metadata:{field}", str(val)))
    return chunks


# ---------- file walking ----------

def iter_files(root):
    if os.path.isfile(root):
        yield root
        return
    if not os.path.isdir(root):
        note(f"path not found: {root}")
        sys.exit(2)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            f = os.path.join(dirpath, fn)
            if _common.is_qc_artifact(f):
                continue
            yield f


# ---------- occurrences ----------

def cmd_occurrences(value, root):
    needle = value.lower()
    hits = 0
    for path in iter_files(root):
        rel = os.path.relpath(path, root if os.path.isdir(root) else os.path.dirname(root) or ".")
        if needle in os.path.basename(path).lower():
            print(f"{rel}\tFILENAME\t{os.path.basename(path)}")
            hits += 1
        # Count each PLACE once. A formula cell emits both its formula and its computed value, and
        # a needle present in both counted twice, so the number the builder verifies against did not
        # match the number of places to fix.
        seen = set()
        for loc, text in extract_chunks(path):
            if needle in text.lower():
                base_loc = loc.replace(" (value)", "")
                snippet = text.strip().replace("\t", " ")
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                print(f"{rel}\t{loc}\t{snippet}")
                if (rel, base_loc) not in seen:
                    seen.add((rel, base_loc))
                    hits += 1
    print(f"\n{hits} occurrence(s) of {value!r}", file=sys.stderr)
    report_unread()
    return 0 if hits else 1


# ---------- tells ----------

def seq_run(s, minlen=4):
    """True if s contains an ascending run of consecutive letters or digits >= minlen."""
    s2 = s.upper()
    run = 1
    for i in range(1, len(s2)):
        if s2[i].isalnum() and s2[i - 1].isalnum() and ord(s2[i]) - ord(s2[i - 1]) == 1:
            run += 1
            if run >= minlen:
                return True
        else:
            run = 1
    return False


TELL_PATTERNS = [
    ("lorem ipsum", re.compile(r"lorem ipsum", re.I), "high"),
    ("placeholder name (John/Jane Doe/Smith)",
     re.compile(r"\b(john|jane)\s+(doe|smith)\b", re.I), "high"),
    ("test/dummy user", re.compile(r"\b(test|dummy|sample|example)\s+user\b", re.I), "med"),
    ("foo/bar/baz filler", re.compile(r"\b(foo|bar|baz|qux)\b", re.I), "med"),
    ("example.com/org/net", re.compile(r"\bexample\.(com|org|net)\b", re.I), "high"),
    ("test@ / @test / @example email",
     re.compile(r"(\btest@|@test\b|@example\b)", re.I), "high"),
    ("reserved 555 phone", re.compile(r"\b555[-.\s]?01\d\d\b|\(555\)\s?\d", re.I), "high"),
    ("repeated-digit phone (555-555-5555)",
     re.compile(r"\b(\d)\1{2}[-.\s]?(\d)\2{2}[-.\s]?(\d)\3{3}\b"), "med"),
    ("placeholder literal (TODO/FIXME/TBD/XXX/PLACEHOLDER)",
     re.compile(r"\b(TODO|FIXME|TBD|XXX|PLACEHOLDER|CHANGEME)\b"), "high"),
    ("template marker ({{..}}, [INSERT..], <placeholder>)",
     re.compile(r"\{\{.*?\}\}|\[INSERT[^\]]*\]|<placeholder>", re.I), "high"),
    ("generic company (Acme/Contoso/Widget Corp)",
     re.compile(r"\b(acme|contoso|widget\s+corp|initech)\b", re.I), "med"),
    ("tool-signature metadata (reportlab/python-docx/python-pptx)",
     re.compile(r"reportlab|python-docx|python-pptx|docx-template", re.I), "high"),
]


def scan_text_for_tells(text):
    found = []
    for label, rx, conf in TELL_PATTERNS:
        m = rx.search(text)
        if m:
            found.append((label, conf, m.group(0)))
    # sequential placeholder: check whitespace-delimited tokens of length >= 4
    for tok in re.findall(r"[A-Za-z0-9]{4,}", text):
        if seq_run(tok):
            found.append(("possible sequential placeholder", "med", tok))
            break
    return found


def cmd_tells(root):
    total = 0
    for path in iter_files(root):
        rel = os.path.relpath(path, root if os.path.isdir(root) else os.path.dirname(root) or ".")
        # filename itself
        for label, conf, ev in scan_text_for_tells(os.path.basename(path)):
            print(f"{rel}\tFILENAME\t[{conf}] {label}: {ev}")
            total += 1
        for loc, text in extract_chunks(path):
            for label, conf, ev in scan_text_for_tells(text):
                ev = ev if len(ev) <= 60 else ev[:57] + "..."
                print(f"{rel}\t{loc}\t[{conf}] {label}: {ev}")
                total += 1
    report_unread()
    print(f"\n{total} potential tell(s) found (review; some may be false positives)",
          file=sys.stderr)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("occurrences", help="find every occurrence of a value")
    o.add_argument("value")
    o.add_argument("path")
    t = sub.add_parser("tells", help="flag synthetic tells in a file/folder")
    t.add_argument("path")
    args = p.parse_args()
    if args.cmd == "occurrences":
        sys.exit(cmd_occurrences(args.value, args.path))
    sys.exit(cmd_tells(args.path))


if __name__ == "__main__":
    main()
