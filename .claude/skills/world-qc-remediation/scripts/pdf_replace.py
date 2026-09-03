#!/usr/bin/env python3
"""In-place PDF string replacement across all pages (redaction + reinsert).

PREFER regenerating from source when the world folder contains the generator/template that produced
the PDF (see references/file-formats.md), that yields perfect text and layout. Use this only when
you have just the PDF.

How it works: finds the target string on every page via PyMuPDF, erases each occurrence with a
redaction, and reinserts the replacement at the same baseline with a best-effort match of size and
color. Also replaces occurrences inside PDF metadata (Title/Author/etc.) by default.

CAVEATS (read these):
  * Exact embedded-font matching is not guaranteed; text is reinserted in a base font (Helvetica
    family, bold/oblique inferred from the original) that is visually close for typical business
    documents. For heavily-styled PDFs the glyphs may differ slightly.
  * A value split across kerning spans may not be found by the text search. The script prints the
    replacement count per page, CONFIRM it matches how many times you expected the value to appear.
  * Redaction fills the erased area white, which is correct on white backgrounds (typical). On a
    colored background a faint box may appear, use --render-check and inspect.
ALWAYS pass --render-check and actually look at the rendered page before accepting the result.

Requires: pip install pymupdf

Examples:
  python pdf_replace.py booking.pdf "ABCD12" "H4T9RM" -o booking_fixed.pdf --render-check check.png
  python pdf_replace.py booking.pdf "ABCD12" "H4T9RM" -o out.pdf --check-page 2
"""
import argparse
import re
import os
import sys
import tempfile

import _common
_common.setup_console()

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF required (pip install pymupdf)", file=sys.stderr)
    sys.exit(2)


def int_to_rgb(c):
    if c is None:
        return (0, 0, 0)
    return (((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0)


def base_font_for(name):
    n = (name or "").lower()
    bold = "bold" in n or "black" in n or "semibold" in n
    ital = "italic" in n or "oblique" in n
    if bold and ital:
        return "hebi"
    if bold:
        return "hebo"
    if ital:
        return "heit"
    return "helv"


def find_spans(page):
    """Return list of dicts: {text, bbox(Rect), size, color(int), origin, font}."""
    spans = []
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                spans.append({
                    "text": span.get("text", ""),
                    "bbox": fitz.Rect(span["bbox"]),
                    "size": span.get("size", 0) or 0,
                    "color": span.get("color", 0),
                    "origin": span.get("origin"),
                    "font": span.get("font", ""),
                })
    return spans


def replace_on_page(page, old, new):
    rects = page.search_for(old)
    # A wrapped match comes back as one rect per line fragment. Inserting `new` at each of them
    # writes the replacement two or three times and scrambles the paragraph. That is silent document
    # damage, so refuse it and point at the mode that handles it.
    if len(rects) > 1:
        ys = sorted({round(r.y0, 1) for r in rects})
        if len(ys) > 1:
            print("  REFUSED on this page: the match spans more than one line, and single-line mode "
                  "would write the replacement once per line.")
            print("  Re-run with --multiline.")
            return 0
    if not rects:
        return 0
    spans = find_spans(page)
    # For each found rect, find the best-matching span (overlap + contains old) for style/baseline.
    styles = []
    for r in rects:
        best = None
        best_overlap = 0.0
        for s in spans:
            inter = r & s["bbox"]
            area = inter.get_area() if not inter.is_empty else 0.0
            if area > best_overlap and old in s["text"]:
                best_overlap = area
                best = s
        if best is None:  # fall back to any overlapping span
            for s in spans:
                inter = r & s["bbox"]
                area = inter.get_area() if not inter.is_empty else 0.0
                if area > best_overlap:
                    best_overlap = area
                    best = s
        size = (best["size"] if best and best["size"] else r.height * 0.8) or 10
        color = int_to_rgb(best["color"] if best else 0)
        font = base_font_for(best["font"] if best else "")
        # x MUST come from the found substring rect: a span's origin.x is the LINE start, not the
        # substring position, so using it would drop the replacement at the far left and scramble the
        # text layer. Take baseline y from the span origin (constant across the line) when available.
        ox = r.x0
        oy = best["origin"][1] if (best and best.get("origin")) else (r.y1 - size * 0.2)
        styles.append((r, ox, oy, size, color, font))
    # Erase originals
    for r, *_ in styles:
        page.add_redact_annot(r, fill=(1, 1, 1))
    page.apply_redactions()
    # Reinsert replacements
    for r, ox, oy, size, color, font in styles:
        page.insert_text((ox, oy), new, fontsize=size, color=color, fontname=font)
    return len(rects)


def _norm_tokens(t):
    return [w for w in re.sub(r"\s+", " ", (t or "").strip()).split(" ") if w]


def _norm(t):
    return re.sub(r"\s+", " ", (t or "")).strip().lower()


def replace_multiline(page, old, new):
    """Replace text that wraps across lines.

    `page.search_for` matches within a single line, so any sentence that wraps is invisible to it.
    That is the gap that made a builder write their own redact-and-reflow tool mid-session, and it is
    the common case: the paragraph you need to change is usually the one long enough to wrap.

    Word boxes do span lines, so: tokenise the page into words, find the consecutive run that matches
    the search string ignoring whitespace, redact every line-box the run covers, then reflow the new
    text into the union rectangle.

    Returns the number of replacements made on this page.
    """
    want = _norm_tokens(old)
    if not want:
        return 0
    words = page.get_text("words")          # x0, y0, x1, y1, word, block, line, word_no
    if not words:
        return 0
    hits = 0
    i = 0
    while i + len(want) <= len(words):
        window = [w[4] for w in words[i:i + len(want)]]
        if [x.strip() for x in window] == want:
            run = words[i:i + len(want)]
            size = max(8.0, min(14.0, (run[0][3] - run[0][1]) * 0.82))
            # One rect per line the run touches, so a wrapped sentence is fully covered.
            bylines = {}
            for w in run:
                bylines.setdefault((w[5], w[6]), []).append(w)
            rects = []
            for _, ws in sorted(bylines.items()):
                r = fitz.Rect(min(x[0] for x in ws), min(x[1] for x in ws),
                              max(x[2] for x in ws), max(x[3] for x in ws))
                rects.append(r)
                page.add_redact_annot(r, fill=(1, 1, 1))
            page.apply_redactions()
            if new.strip():
                union = fitz.Rect(min(r.x0 for r in rects), min(r.y0 for r in rects),
                                  max(r.x1 for r in rects), max(r.y1 for r in rects))
                # A touch of headroom, because reflowed text rarely lands on the same line count.
                box = fitz.Rect(union.x0, union.y0 - 1, union.x1, union.y1 + size * 1.2)
                rc = page.insert_textbox(box, new, fontsize=size, fontname="helv", align=0)
                if rc < 0:
                    # Did not fit. Say so rather than silently clipping, which is how a builder lost
                    # a net-debt row to a bad page bound.
                    print(f"  WARNING: replacement did not fit the original area on this page "
                          f"(short by {abs(rc):.0f}pt). Text was removed but NOT reinserted. "
                          f"Shorten the replacement or edit this one by hand.")
            hits += 1
            words = page.get_text("words")   # geometry moved, re-read
            i = 0
            continue
        i += 1

    # Verify rather than trust. Reflowing text into a fixed rectangle can clip, overlap or drop a
    # line, and none of that raises. A builder lost a net-debt row to exactly this and only found it
    # by reading the page afterwards.
    if hits:
        after = _norm(page.get_text())
        if _norm(old) in after:
            print("  VERIFY FAILED: the original text is still on the page after the edit.")
            return -1
        if new.strip() and _norm(new) not in after:
            print("  VERIFY FAILED: the replacement text is not on the page after the edit. It was "
                  "probably clipped by the original area. Nothing was saved.")
            return -1
    return hits


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pdf")
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("-o", "--out", required=True, help="output PDF path")
    p.add_argument("--multiline", action="store_true",
                   help="match across line breaks and reflow. Single-line search cannot find a "
                        "sentence that wraps, and the paragraph you need to change is usually long "
                        "enough to wrap.")
    p.add_argument("--no-metadata", action="store_true",
                   help="do not replace occurrences inside PDF metadata")
    p.add_argument("--render-check", metavar="PNG",
                   help="render the check page to this PNG for visual verification")
    p.add_argument("--check-page", type=int, default=1,
                   help="1-based page to render for --render-check (default 1)")
    p.add_argument("--dpi", type=int, default=150, help="render DPI (default 150)")
    args = p.parse_args()

    if args.old == "":
        print("ERROR: 'old' must not be empty", file=sys.stderr)
        sys.exit(2)
    try:
        args.new.encode("cp1252")
    except UnicodeEncodeError as e:
        print(f"ERROR: replacement text has characters outside the base-14 font's WinAnsiEncoding ({e}). "
              "This script cannot embed a Unicode font, so inserting this text would silently render as "
              "missing/garbled glyphs. Use Latin-1/WinAnsi-safe replacement text, or regenerate the PDF "
              "from source instead.", file=sys.stderr)
        sys.exit(2)

    # --- input / output preconditions (fail with a plain one-liner, never a traceback) ---
    if not os.path.isfile(args.pdf):
        print(f"ERROR: input PDF not found: {args.pdf}", file=sys.stderr)
        sys.exit(2)
    out_dir = os.path.dirname(os.path.abspath(args.out)) or "."
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        print(f"ERROR: could not create output directory {out_dir}: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        doc = fitz.open(args.pdf)
    except Exception as e:  # noqa: BLE001, corrupt/unreadable PDF
        print(f"ERROR: could not open PDF {args.pdf}: {e}", file=sys.stderr)
        sys.exit(2)
    if doc.needs_pass:
        doc.close()
        print(f"ERROR: PDF is password-protected, cannot edit: {args.pdf}", file=sys.stderr)
        sys.exit(2)

    total = 0
    for i, page in enumerate(doc, 1):
        n = (replace_multiline(page, args.old, args.new) if args.multiline
             else replace_on_page(page, args.old, args.new))
        if n < 0:
            print("\nABORTED. The document was NOT written. Edit this passage by hand, or shorten "
                  "the replacement so it fits the space the original occupied.", file=sys.stderr)
            sys.exit(3)
        if n:
            print(f"page {i}: {n} replacement(s)")
        total += n

    if not args.no_metadata:
        meta = doc.metadata or {}
        changed = {}
        for k, v in meta.items():
            if isinstance(v, str) and args.old in v:
                changed[k] = v.replace(args.old, args.new)
        if changed:
            meta.update(changed)
            doc.set_metadata(meta)
            print(f"metadata: replaced in {', '.join(changed)}")

    print(f"TOTAL page replacements: {total}")

    # Save to a temp file, render-check the SAVED file, then atomically move into place, and only
    # THEN print "saved:". A failed render-check must NOT lose the edit or crash, and the temp file
    # is always cleaned up.
    out_abs = os.path.abspath(args.out)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".pdf", dir=out_dir)
        os.close(fd)
        doc.save(tmp_path, garbage=4, deflate=True)
        if args.render_check:
            chk = None
            try:
                chk = fitz.open(tmp_path)
                pg = chk[max(0, min(args.check_page - 1, chk.page_count - 1))]
                pg.get_pixmap(dpi=args.dpi).save(args.render_check)
                print(f"render check written: {args.render_check} (page {args.check_page}), INSPECT IT")
            except Exception as e:  # noqa: BLE001, a failed preview must not lose the edit
                print(f"WARNING: render check failed ({e}); the edit was still saved.", file=sys.stderr)
            finally:
                # MUST close before os.replace, or Windows blocks the move (temp file still open).
                if chk is not None:
                    try:
                        chk.close()
                    except Exception:  # noqa: BLE001
                        pass
        doc.close()
        os.replace(tmp_path, out_abs)
        tmp_path = None
        print(f"saved: {args.out}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        try:
            doc.close()
        except Exception:  # noqa: BLE001, already closed
            pass

    if total == 0:
        print("WARNING: zero replacements, the string may be split across kerning spans or absent. "
              "Inspect the PDF text layer and consider regenerating from source.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
