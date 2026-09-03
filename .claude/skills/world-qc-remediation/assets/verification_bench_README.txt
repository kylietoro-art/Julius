VERIFICATION BENCH
Mechanical Engineering 32 [U.S.], WS-400 wire-shaping plier family
=========================================================================

WHAT IT IS

A single self-contained HTML page for checking a world build against its
spec. It makes no network requests, loads no libraries, and sends nothing
anywhere. Every file it reads stays on the machine it is opened on.


HOW TO RUN IT

Double-click "Verification Bench.html". It opens in the browser.

Chrome or Edge is required, the page uses the File System Access API to
read a folder you choose. Safari and Firefox do not support it.


WHAT IT ASKS FOR, IN ORDER

  1. The World Spec workbook (.xlsx).
     Read once and remembered, so you are not asked again next time.
     Either the full builder spec or the worker-facing copy will do:
     columns are matched by heading, not by position, so a spec with
     columns removed still traces correctly.

  2. The file system folder, the root of the built corpus, the folder
     that contains Engineering/, Quality/, Procedures/ and the rest.

  3. The reference anchors folder, if you want anchor tracing.
     Optional. Skip it and everything else still works.


WHAT IT DOES

  Open      Renders the file in the page. Workbooks show every sheet as a
            tab with the full cell grid; documents show headings, text and
            tables; decks show the text of each slide; PDFs show recovered
            text; images and HTML render directly. Nothing downloads.

  Trace     Draws the path from the spec to the artifact and back, which
            canonical values it must match, which tasks depend on it, which
            other artifacts it must agree with, and which anchor backs it.
            Every item is listed. Nothing is collapsed into "+N more".

  Paste     Takes AutoQC output pasted straight in, splits it into
  findings  per-file claims, and checks each one against the bytes. Files
            named by a finding are flagged, and the disputed strings are
            highlighted in red inside the file when you open it.

  Check     Audits the World Spec itself rather than the files: that every
  the spec  artifact is fully registered and resolves to a real file, that no
            two artifacts claim the same one, that every canonical value
            names a source that exists and is not its own corroborator, that
            every task names evidence that exists, and that nothing in the
            register is orphaned. Each check either passes or lists the exact
            rows that fail it. Needs the spec; the file-level checks are
            skipped if no folder is chosen.

  Log       An append-only record of the work. Every mark, note, file
            opened, trace drawn, findings paste, spec check and report is
            timestamped and kept, with the before and after value of
            anything that changed. Corrections append rather than overwrite,
            so a mark that went issue then ok shows both, in order. The log
            is stored per corpus folder and survives closing the browser.
            "Copy the log" puts the whole thing on the clipboard as plain
            text for pasting into a revision comment or a hand-off note.

  Marks     Looks right / Issue / Skip per file, with a note box. "Build
            report" turns the marks into a plain-text summary and copies
            it to the clipboard.


A NOTE ON PDFs

PDFs are drawn, not just read. The page executes the drawing's own vector
content, lines, arcs, hatching, dimensions, title block and all, and
renders each sheet as scalable graphics, so a drawing looks like a drawing
in both the hosted and the local copy. Multi-page documents show every page.

If a PDF turns out to be a scan, or uses features outside that subset, the
page falls back to showing the recovered text and says so.

Running locally, an "Open in the desktop application" button sits above each
document if you would rather see it in Acrobat or Preview.

If the browser saves the file rather than opening it, turn off "Ask where
to save each file" in the browser's download settings.
