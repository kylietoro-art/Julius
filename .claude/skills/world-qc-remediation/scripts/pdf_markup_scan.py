#!/usr/bin/env python3
"""Flag documents that print RAW MARKDOWN/HTML as visible text, a Markdown/HTML source that was
converted to PDF (or docx) without rendering, so tokens like '## Heading', '**bold**', '<td>',
'|---|' show up literally. Common file-gen defect (AQC: Vendor_Approvals_2025.pdf).

Detection only (fixing means re-rendering from the source or stripping the markup). Diff-only output:
file, which markup, sample line.

  scan <dir|file>    Scan PDFs (and .docx/.txt/.md/.html if you point at them) for literal markup.

Deps: pdfplumber or pypdf for PDFs; python-docx for docx (optional; skipped with a note if missing).
"""
import argparse, os, re, sys, glob

import _common
_common.setup_console()

PATTERNS = [
    ("md-heading",  re.compile(r"^\s{0,3}#{1,6}\s+\S")),
    ("md-bold",     re.compile(r"(?<!\d)\*\*[^\s*\d]|[^\s*\d]\*\*(?!\d)|(?<!\w)__(?!\w*__\b)\S(?:[^_]*?\S)?__(?!\w)")),
    ("md-table-sep",re.compile(r"\|\s*:?-{3,}:?\s*\|")),
    ("md-link",     re.compile(r"\[[^\]]+\]\([^)]+\)")),
    ("md-checkbox", re.compile(r"^\s*[-*]\s*\[[ xX]\]")),
    ("code-fence",  re.compile(r"```|~~~")),
    ("html-tag",    re.compile(r"</?(?:table|thead|tbody|tr|td|th|div|span|p|br|ul|ol|li|h[1-6]|b|i|strong|em|a|img)\b[^>]*>", re.I)),
    ("html-entity", re.compile(r"&(?:nbsp|amp|lt|gt|quot|#\d+);")),
]

def extract(path):
    ext = path.lower().rsplit(".",1)[-1] if "." in path else ""
    if ext == "pdf":
        try:
            import pdfplumber
        except ImportError:
            pdfplumber = None
        if pdfplumber:
            try:
                with pdfplumber.open(path) as pdf:
                    return "\n".join((pg.extract_text() or "") for pg in pdf.pages)
            except Exception:
                pass
        try:
            import pypdf
        except ImportError:
            pypdf = None
        if pypdf:
            try:
                return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(path).pages)
            except Exception:
                pass
        if not pdfplumber and not pypdf:
            print(f"NOTE: {path}: skipped, no PDF library installed (pip install pdfplumber or pypdf)", file=sys.stderr)
        return None
    if ext == "docx":
        try:
            import docx
        except ImportError:
            print(f"NOTE: {path}: skipped, python-docx not installed (pip install python-docx)", file=sys.stderr)
            return None
        try:
            return "\n".join(p.text for p in docx.Document(path).paragraphs)
        except Exception:
            return None
    if ext in ("txt","md","html","htm"):
        try: return _common.read_text(path)
        except Exception: return None
    return None

def scan_path(path):
    if not os.path.exists(path):
        print(f"ERROR: path not found: {path}", file=sys.stderr)
        sys.exit(1)
    files = [path] if os.path.isfile(path) else [
        f for f in glob.glob(os.path.join(path,"**","*"), recursive=True)
        if os.path.isfile(f) and f.lower().rsplit(".",1)[-1] in ("pdf","docx","txt","md","html","htm")
        and not _common.is_qc_artifact(f)
    ]
    flagged = 0
    skipped = 0
    for f in sorted(files):
        txt = extract(f)
        if txt is None:
            skipped += 1
            continue
        hits = {}
        for line in txt.splitlines():
            for name, pat in PATTERNS:
                if pat.search(line):
                    hits.setdefault(name, line.strip()[:80])
        # ignore .md/.txt source files themselves, markup is expected there
        ext = f.lower().rsplit(".",1)[-1]
        if hits and ext not in ("md","txt","html","htm"):
            flagged += 1
            base = os.path.relpath(f, path if os.path.isdir(path) else os.path.dirname(f))
            print(f"[MARKUP] {base}: {', '.join(sorted(hits))}")
            for name, sample in list(hits.items())[:3]:
                print(f"         {name}: {sample!r}")
    tail = f" ({skipped} file(s) skipped, see NOTE above)" if skipped else ""
    print(f"\n--- {flagged} file(s) printing raw markup{tail}. Fix by re-rendering from source or stripping markup. ---")
    return flagged

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("scan"); sc.add_argument("path")
    a = ap.parse_args()
    scan_path(a.path)

if __name__ == "__main__":
    main()
