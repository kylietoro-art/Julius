# File-Format Handling, read, edit in place, verify

These worlds mix plain-text and binary office artifacts. The governing rule for all of them:
**edit in place and preserve the file's existing conventions** (formatting, schema, headers, fonts,
number/date formats). A remediation that reformats the artifact trades one synthetic tell for
another. Change only what the flag requires.

For office formats, the public `docx`, `pdf`, and `xlsx` skills carry the full tooling detail; this
file covers what's specific to QC remediation.

Contents: [Occurrence hunting](#occurrence-hunting-do-this-first) · [CSV/TSV](#csv--tsv) ·
[EML](#eml-email) · [TXT/MD/JSON/HTML](#txt--md--json--html) · [XLSX](#xlsx) · [DOCX](#docx) ·
[PDF](#pdf) · [Filenames & metadata](#filenames--metadata)

---

## Occurrence hunting (do this first)

Before editing, find **every** place the offending value/reference lives. Plain `grep -r` misses
values inside `.xlsx`/`.pdf`/`.docx` (they're zip/binary) and misses metadata. Use:

```bash
python scripts/scan_world.py occurrences "<value>" /path/to/world_dir
```

It extracts text from office/PDF files, reads their metadata, checks filenames, and reports each
hit with file + location. Run it again after editing to confirm zero stale hits.

---

## CSV / TSV

Direct text edit, but exactness matters because a storefront/export CSV's schema is part of its
realism.

- Read with `pandas` for analysis, but for a **surgical value change** prefer editing the raw text so
  you don't perturb quoting, column order, line endings, or unquoted numeric formatting that pandas
  round-trips can alter.
- Preserve the exact delimiter, header row, quote style, and column order. Do not reorder columns or
  add/drop a trailing newline.
- If a value appears in multiple rows for the same entity, change all; if the fix is per-row, target
  the specific `order`/`id` the flag names.

## EML (email)

An `.eml` is RFC-822 text: headers, a blank line, then the (possibly MIME-multipart) body.

- Fix the specific header (`Date:`, `From:`, `Subject:`) and/or body text the flag names; leave all
  other headers and the MIME structure intact.
- For a date fix, correct the `Date:` header **and** any in-body relative reference ("yesterday").
  Keep the offset consistent with the person's established timezone on that date (see taxonomy E).
- Preserve `Message-ID`, `In-Reply-To`, `References`, boundaries, and encoding exactly, these make
  the thread read as real and sometimes anchor other artifacts.
- Parse/serialize with Python's `email` module if the body is multipart; for a simple header/date
  change, a targeted text edit is safest.

## TXT / MD / JSON / HTML

Direct text edit.
- **JSON**: keep it valid; preserve key order and indentation style. Prefer a targeted string edit
  over `json.load`→`json.dump` when you only need to change one value, to avoid reflowing the whole
  file.
- **HTML/MD**: change only the flagged content; preserve structure and formatting.

## XLSX

Use `openpyxl` to edit in place so formatting survives (`pandas.to_excel` discards it). See the
`xlsx` skill for full mechanics. QC-specific points:

- **Inspect first:** use the `xlsx` skill's text-extraction tooling for a fast dump (illustrated here
  as `extract-text file.xlsx | head -100`: that command comes from the `xlsx` skill, it is not a
  script in this skill), or load with `openpyxl` to
  see cell-by-cell (use `data_only=True` in a *separate* read to see computed values, never save a
  workbook opened `data_only=True`, it discards formulas).
- **Match the sheet's convention.** These generated budgets typically **hardcode** totals. If the
  flag prescribes a specific number and surrounding totals are hardcoded, write the number. If the
  sheet's other totals are `=SUM()` formulas, write a formula and recalc via the separate `xlsx`
  skill's own recalc tooling (needs LibreOffice). That recalc script lives in the `xlsx` skill, **not**
  in this skill's `scripts/` directory, there is no `recalc.py` here, so don't try to run one from
  this skill's `scripts/`.
  Don't introduce a lone `=SUM()` into a sheet of hardcoded numbers (or vice-versa), the
  inconsistency is itself a tell.
- **Fix every dependent cell + narrative note.** Total row, grand-total row, per-person column, and
  any text note stating a figure ("Days sum to 369", a header saying "Twenty target countries"). A
  footing fix that leaves a contradicting note or stale header is incomplete.
- **Verify footing** with the exact figures:
  ```bash
  python scripts/verify_xlsx.py file.xlsx --sheet "Per-Country Allocation" --total E27 --range E7:E28
  ```
  Expect delta = 0. Re-check secondary totals and per-person cells too.
- Preserve number formats, fonts, fills, column widths, and merged cells on any cell you touch.

## DOCX

Use `python-docx` in place (see the `docx` skill). Preserve styles, headers/footers, and tables.
- Text often lives split across multiple runs within a paragraph; a naive run-by-run replace can miss
  a value that straddles runs. Check paragraph text as a whole, and when replacing, rebuild the run(s)
  carefully or use the docx skill's find-and-replace guidance.
- Check **headers, footers, and text boxes** for the value too, not just body paragraphs.
- Check document **metadata** (`core_properties`: author, last-modified-by, title) for tells.

## PDF

Hardest format. Decide the approach up front:

> **RLS cannot regenerate an individual file, so every PDF fix happens here in Claude Code.** That
> makes PDF-metadata hygiene mandatory: any PDF you rebuild or write with a Python toolchain will
> carry a `reportlab` / `python` fingerprint in `/Producer` and `/Creator` (and sometimes the flagged
> value in `/Title` or `/Author`). A fresh tool signature is itself a Type-A/G synthetic tell that AQC
> will flag. After **any** PDF edit or rebuild: clear/normalize `/Producer`, `/Creator`, `/Author`,
> `/Title` (and any custom keys), then run `scan_world.py tells <file>` to confirm no signature or
> flagged value survives in the metadata.

> **Never leave a PDF on `doc.saveIncr()`: always end on a full rewrite.** If you edit a PDF with
> raw PyMuPDF (redact-and-reinsert, a multi-page rebuild) via `page.add_redact_annot()` /
> `insert_text()` / `insert_textbox()` and call `doc.saveIncr()` to persist each step, every call
> appends a new revision onto the file instead of replacing it, including any discarded or
> silently-failed intermediate attempt (see the gotcha below). Normal viewers only render the latest
> revision, so this is invisible until someone inspects the raw bytes (`grep -c '%%EOF' file.pdf`: 1
> is clean, >1 means stacked editing history), at which point it reads as a bigger tell than any
> single metadata field. Fix: finish every PDF-editing session with either (a) a full rewrite,
> `doc.save(path, garbage=4, deflate=True)` (what `pdf_replace.py` already does for you): or (b) run
> `python scripts/metadata_hygiene.py clean <file> --app "..." --date YYYY-MM-DD`, which rewrites via
> pypdf and collapses any revision history as a side effect. `metadata_hygiene.py scan` now flags
> multi-revision files on its own, so this surfaces even if you forget, but don't rely on that;
> treat "collapse to one revision" as a required last step, not a scan-triggered cleanup.

> **Base-14 fonts (Times-Roman, Helvetica, etc.) silently mangle "smart" typography.** Inserting text
> with a curly quote (`“ ” ‘ ’`) or an em/en dash (`— –`) via `insert_text`/`insert_textbox` in a
> base-14 font renders the wrong glyph (a stray `?`, a middle dot, or similar): no error, and it's
> easy to miss on a quick visual check. Sanitize to ASCII first (straight quotes, `--` for an em
> dash) before inserting, or reuse the document's own embedded font (extract via
> `doc.extract_font(xref)` and pass `fontfile=`: note this can itself fail silently on a *subset*
> embedded font that lacks the glyphs/cmap for your new text, so verify output either way).
> `pdf_replace.py` already guards this (it hard-errors up front if the replacement isn't
> cp1252-encodable): a bespoke rebuild script does not, so add the same check or sanitize.

> **`insert_textbox` can render *nothing* if the box is too tight.** It returns "spare" space
> (`rect_height - text_height`); when spare comes back at or near zero, even a small negative value
> like `-0.2`: this PyMuPDF version can silently draw no text at all rather than clipping the
> overflow, with no exception raised. Always size the box with comfortable slack, check the returned
> spare is clearly positive, and, the check that actually catches it, re-extract the page's text
> afterward and confirm the new string is really there before moving on. Don't trust "it didn't
> error" as a correctness signal.

> **A redaction rect can eat more than you intend.** `apply_redactions()` clears every text span that
> *intersects* the rect, not just spans fully inside it, a rect that starts even a fraction of a
> point into a neighboring glyph (a checkbox `[✓]`, a preceding character) can wipe it too. Keep
> redaction rects safely clear of anything adjacent you want to keep, and re-render (or re-extract)
> the surrounding area afterward to confirm nothing else vanished.


**1. Regenerate from source (preferred, if it exists).** These PDFs are generated; if the world
folder (or an adjacent build/assets dir) contains the generator script or template that produced it
(`reportlab` code, an HTML template + renderer, a `.md`→PDF source), fix the value **there** and
re-run it. This yields a clean PDF with correct text, layout, and metadata. Search for it:
```bash
python scripts/scan_world.py occurrences "<value>" /path/to/world_dir   # finds source that emits it
grep -rl "<filename-stem>" /path/to/world_dir                            # finds a builder referencing it
```

**2. In-place token replacement (when you only have the PDF).** Use the helper:
```bash
python scripts/pdf_replace.py input.pdf "ABCD12" "H4T9RM" -o output.pdf --render-check page1.png
```
It finds the string on every page (via PyMuPDF), redacts the original span, and reinserts the
replacement with a best-effort match of size and color. **Caveats:** exact embedded-font matching
isn't guaranteed (it falls back to a base font that's visually close for typical business docs);
values split across kerning spans can be missed, the script reports how many replacements it made
per page so you can confirm the count matches expectations. **Always** `--render-check` a page and
look at it to confirm the result reads cleanly.

**3. Full rebuild (last resort).** Only for simple PDFs where 1 and 2 fail, extract layout and
rebuild with `reportlab` (or raw PyMuPDF page-by-page), accepting some visual drift. Match
fonts/margins as closely as possible. This is the scenario most exposed to the font-encoding and
`insert_textbox`-silent-failure gotchas above, measure, insert, then re-extract and verify text is
actually present before moving to the next page, and don't leave the file on `saveIncr()`.

After any PDF edit or Claude-Code rebuild: **clear the metadata** (`/Producer`, `/Creator`,
`/Author`, `/Title`, custom keys) of any tool signature, stray original filename, or flagged value,
set them to neutral, in-world-plausible values or strip them, **and** confirm the file is back to a
single revision (no leftover `saveIncr()` history). `python scripts/metadata_hygiene.py clean <file>
--app "..." --date YYYY-MM-DD` does both in one step; `metadata_hygiene.py scan` and `scan_world.py
tells <file>` both confirm nothing survives. A PDF that reads perfectly but announces `reportlab` in
its Producer field, or carries three stacked revisions from your editing session, is still a failed
remediation.

## Filenames & metadata

Two places remediations routinely miss:

- **Filenames.** If the offending value is in the filename (a PNR, an order id), rename the file
  (`git mv` / `os.rename`) to the corrected value, and update **every** cross-file reference to the
  old name, an email that attaches or names it, a manifest, an index, a README.
  `scan_world.py occurrences "<old-filename>"` finds these.
- **Metadata.** Office and PDF files carry authorship/tool metadata that can leak synthetic origin
  (`python-docx`, `reportlab`, default template names) or can literally contain the flagged value.
  Check and clean it whenever the flag is about a placeholder or realism. `scan_world.py tells
  <file>` surfaces common metadata tells.
