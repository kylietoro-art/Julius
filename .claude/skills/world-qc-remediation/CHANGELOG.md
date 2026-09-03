# Changelog, world-qc-remediation

## [4.9.2] - 2026-08-30

**Spreadsheets were not being read at all.** Reported from the field as "it doesn't process
spreadsheets, it logs a silent note and treats them as empty, which makes the scan results look
clean." Correct on every point. Three causes:

- **A regression I introduced in 4.6.0.** Reading cached values meant touching `.coordinate` on
  every cell, but openpyxl's read-only mode returns `EmptyCell` for blanks and `EmptyCell` has no
  `.coordinate`. It raised on the first blank cell in the sheet, the caller swallowed it, and EVERY
  workbook came back as zero chunks. Any world whose spreadsheets have a gap anywhere, so all of
  them.
- **`.xlsm` was never supported.** Macro-enabled workbooks are ordinary xlsx underneath and are
  common in finance worlds. They fell through to "unknown binary type" and returned nothing.
- **Unreadable files were indistinguishable from empty ones.** `.xls`, `.doc`, `.ppt` and friends
  returned `[]` with a stderr note that scrolls past, and the summary still printed "0 occurrences".

Fixed, plus the structural problem behind it: a file that could not be opened is now collected and
reported under a banner at the end of every scan, naming each file and why. A zero is only a clean
result for the files that actually opened, and nothing in the old output said which those were.

5 regression tests, including a workbook with its content deliberately below a run of blank cells.


All notable changes to this skill. Versioning is semantic-ish: MINOR for additive workflow/tooling
that keeps single-flag remediation working unchanged, MAJOR for breaking changes to how a flag is
consumed.

## [4.3.0] - 2026-08-29

Everything here comes from the FP&A 24 test run and Bryan's review of it. The world passed eight
rounds and human review still found a task's answer sitting in plain sight.

### Added

- **`leak_scan.py` task-answer check.** Takes each task's expected answer from the spec's ③ Tasks tab
  and finds any file stating that value which is not one of that task's primary artifacts. This is the
  one that catches Bryan's finding: `$670.0M` on slide 22 of the board pack, T1's answer, in a file
  the agent opens first. It is a bare number in a bullet with no reconciling language, no conclusion
  voice and no filename tell, so every language-based check I built missed it. **The spec knows the
  answer and knows which artifacts carry the derivation, so the question is not "does this sentence
  look like leakage" but "is this answer somewhere it has no business being".** Reproduced as a
  regression test.
- **`corpus.py` (NEW).** Extracts every file once and caches it beside the world, keyed on path, mtime
  and size, so an edit can never leave a stale entry. Every scanner reads through it. Built because a
  builder wrote their own extractor and their own JSON cache twice in one session and a leak scan
  still timed out. When people route around a tool, the tool is the problem.
- **Standing rulings.** `round_log.py decide <world> "<ruling>"` writes to `_qc_backup/rulings.md`,
  and every later `start` prints them before triage. Rounds 5, 6 and 7 of FP&A 24 each re-asked "which
  governs, the Plan or the Spec?" after the builder answered it in round 4. The answer was in the log
  as a note and nothing treated it as binding. Decisions now survive the new-chat rule like everything
  else on disk.
- **`pdf_replace.py --multiline`.** Matches across line breaks and reflows, for the wrapped paragraph
  case that single-line search cannot see at all. This is the gap that made a builder write their own
  redact-and-reflow tool mid-session.

### Fixed

- **`metadata_hygiene.py` wrote its backups INSIDE the world.** It joined `_qc_backup` onto the target
  path instead of calling `_common.default_backup_dir` like every other script. So `clean <world>` put
  copies of world files into the world, where they get zipped and uploaded as corpus content. That is
  a filesystem-leakage defect AutoQC grades, caused by the tool meant to prevent tells.
- **`metadata_hygiene.py clean` now takes the files you edited**, via `--also`, and warns when pointed
  at a directory. Cleaning a whole world rewrote metadata on 31 files in one round and buried the four
  real edits in the next diff. Gate 4 told people to clean what they touched while the command shown
  cleaned everything, so the doc and the command contradicted each other and the command won.
- **`pdf_replace.py` duplicated text on a wrapped match.** `search_for` returns one rect per line
  fragment and the code inserted the full replacement at each, so a two-line match got the replacement
  written twice and the paragraph scrambled. It now refuses and points at `--multiline`.
- **`pdf_replace.py --multiline` verifies and aborts rather than clipping.** After editing it re-reads
  the page and requires the old text gone and the new text present. If the replacement did not fit it
  writes nothing and says so. A builder lost a net-debt row to a bad page bound and only found it by
  reading the page.

### Changed

- **The World Plan is gone, and that is now a hard rule.** Reference rule 4 and Gate 2 bucket 4: any
  finding that cites the Plan, compares a file against it, or raises a Plan-versus-Spec conflict is
  disputed on sight. No judgment, no question to the expert. The Spec is the only planning document.
- Gate 3 says run the leak scan every round, not only when a file grew.
- `selftest.py` F22, 6 new checks covering the task-answer leak, the rulings carry-forward and the
  backup location. Battery is 86 PASS / 0 FAIL.

### Still open

- The reading order after a multiline PDF reflow is not always the visual order. Content is correct
  and nothing is duplicated or lost, but a reflowed paragraph should be eyeballed.
- `xlsx` recalculation still needs LibreOffice or Excel. openpyxl clears cached formula values and the
  toolkit has no answer for that beyond raw XML patching.

## [4.2.0] - 2026-08-28

Answer leakage. The toolkit had a rule against writing it and nothing that found it, while leakage was
present in 61% of the worlds that went past 20 rounds. Found by Danielle testing the skill.

### Added

- **`leak_scan.py` (NEW).** Candidate answer leakage, in four categories, strongest first:
  - **Trap possibly defused.** Both sides of a declared trap in one sentence, plus reconciling
    language. Uses the spec's own trap values, so a hit means a file is explaining away a designed
    discrepancy. Two tiers: with explaining language is near-certain, bare co-occurrence is listed
    separately and quietly because a real document can put two figures side by side legitimately.
  - **Reconciling language.** Two different figures in one sentence plus wording whose job is to
    explain the gap. This is the bridge-note shape.
  - **Conclusion voice.** A document announcing an answer rather than recording a fact.
  - **Filenames that announce themselves.** FINAL, VALIDATED, APPROVED, ANSWER.
  Reports only, never fixes, and says on every run that a hit is a candidate and not a verdict.
- **Text-growth tracking in `inventory_check.py`.** Snapshots extracted text length per file, not byte
  size, because docx and xlsx are zips whose size moves on a re-save with no content change. A
  replacement does not make a file longer, so growth is added text, and added text is how answers
  leak. Files that gained 40+ characters are listed with the delta and pointed at `leak_scan.py`.
  **This makes replace-not-add measurable rather than aspirational.**
- **The bridge note is named in Rule 1**, with the real example from testing and the banned phrases:
  bridge, reconciliation note, for clarity, to clarify, the difference represents, not additive,
  should not be combined.

### Fixed

- **Gate 5 never mentioned PDFs**, so on a judgment fix in a PDF the model had no instruction and
  hand-rolled PyMuPDF: extract, write custom code, verify, iterate. Measured `pdf_replace.py` at 1.1s
  for 456 replacements across 12 pages, and 0.9s to delete a sentence via an empty replacement. Gate 5
  now says use it, including for deletion, and never hand-roll. `pdf_replace.py` moved to gates 4 and 5
  in the script table.
- Two bugs in `leak_scan.py` caught while testing it, both of which silently disabled the strongest
  check: it hand-rolled a header read that asked `find_header` for only two columns, so it never saw
  Type or Note and returned an empty trap list; and `canonical_rows` does not map the Note column
  either, which is where a trap's second figure usually lives.
- `selftest.py` F21, 9 new checks including the clean-control case that must land in the weak tier
  rather than the strong one. Battery is 80 PASS / 0 FAIL.

## [4.1.0] - 2026-08-27

Three fixes from builder feedback: the model reaching for the spec instead of the files, half-read
findings producing half-finished fixes, and a merge bug found while testing the second.

### Added

- **The spec decision order, Reference rule 3.** The earlier draft of this was wrong. Spec fixes are
  legitimate: if a real tie-out defect got missed before file generation, the spec IS wrong and it
  should be fixed. The failure is reaching for it because it is less work than editing four files.
  So it is an order, not a prohibition. Can the files satisfy it? Fix the files, and say why not
  before going further. Is it about the spec as an object, the workbook being visible, a tab name?
  Dispute it. Is it a genuine number that does not reconcile? The spec is wrong, write up the exact
  change and hand it to an EPM.
- **Never edit the local spec copy, with the reason stated.** Studio holds the spec AutoQC reads; the
  builder's file is a download. Edit the copy and it silently diverges, so every tie and trap check
  for the rest of the session is measured against a spec the grader does not have. The builder cannot
  upload it anyway, so editing achieves nothing except the divergence. `inventory_check.py` now hashes
  the spec each run and reports if the local copy has been edited, with restore instructions.
- **Findings are written to per-ticket files.** `round_log.py start` writes each finding to
  `_qc_backup/tickets/round<N>/tNN.txt`. Gate 5 reads the ticket immediately before fixing it rather
  than working from the paste, which by then is far back in the conversation behind script output.
  Each ticket carries the finding verbatim and instructs the fixer to enumerate every separate
  assertion in it, one line each, and to check them off before closing. AutoQC findings are usually
  several assertions in one paragraph, and a summary drops clauses.
- **Gate 5 gains a step 0 (read the ticket) and a step 6 (confirm every assertion is addressed).**
- **A short App Data pointer.** The process carries over, the scripts do not, they are filesystem-only.
  One extra rule about not changing schemas, flagged for confirmation. A separate app skill is coming.

### Fixed

- **`split_findings` merged findings when a round had only two of them.** The bullet-mode threshold
  was three, so two bullets fell through to paragraph mode and became one block: one ticket containing
  two findings, and a reported count of 1. Late rounds are exactly where counts are small, so the
  merge hit precisely when the count mattered most. Threshold is now two. Found by testing the ticket
  writer, not by reading the code.
- `selftest.py` F20, 10 new checks covering the split at one, two and paragraph-style findings, one
  ticket file per finding with no bleed between them, and the spec-edit detector across baseline,
  unchanged and edited. Battery is 71 PASS / 0 FAIL.

## [4.0.1] - 2026-08-27

### Fixed

Two bugs in `setup_check.py`, both reported from the field, both producing a false "do not start work"
stop. Both were in code written the same day. A gate that stops people who have done nothing wrong is
worse than no gate, because the next thing they learn is to ignore it.

- **The trap count was substring-matched.** `"0 declared" in out` matches 10, 20, 50, 100 and every
  other count ending in zero. A spec with 50 registered traps was told it had none and to stop and
  raise it in the world thread. Now parses the integer with `re.search(r"(\d+)\s+declared", out)`.
- **The file manifest trusted `os.path.exists` alone.** On Windows a packaged-app install can redirect
  that path, so stat reports False on a file that is present and readable, and the whole toolkit read
  as missing. `present()` now falls back to directory enumeration, then to opening the file, because
  those take different code paths and see through the redirect. Case-insensitive on the enumeration,
  since Windows is. The folder check uses the same tolerance.
- `selftest.py` F19, 8 new checks: the count parsed correctly at 0, 10, 20, 50, 100 and 130, the
  substring form gone from the source, and `present()` verified against a monkeypatched
  `os.path.exists` that returns False on everything, confirming it finds a real file and still refuses
  a missing one. Battery is 61 PASS / 0 FAIL.

## [4.0.0] - 2026-08-27

The consolidation. Three documents described the same workflow to overlapping audiences: this
SKILL.md at 6,720 words, a separate FileSystem_Helper_Skill at 5,463, and a Loom script at 2,671. The
same rules appeared in all three, so keeping them in sync was manual and they would have drifted.

MAJOR because the structure changed. Phases became Gates and the two documents became one.

### Changed

- **SKILL.md is now the gated walkthrough**, in the same shape as the World Spec Builder skill: How
  you talk, Before you start, a drive-this block, eleven gates, then Reference. The helper's structure
  won because it was more complete: it had the buildability stop and the upload-confirmation gate that
  the phase list never had. This file's script precision was kept.
- **12,183 words across two documents became 5,131 in one.** Nothing was dropped that a builder needs.
  What went: a five-rules section that restated the gates, a fourteen-item core principles list that
  restated them again, a glossary of terms defined in context, three Engine sections whose content
  moved into the gates and the script table, and a coverage-map contract that duplicated Gate 8.
- `FileSystem_Helper_Skill_v1.0.md` and the Loom script are retired. This file replaces both.
- Script reference is now one table mapping each script to the gate it belongs to, so nothing sits in
  the package unwired.

### Fixed

- `gen_realistic_values.py` was in the package but referenced by no phase, so it was never run.
  Placeholder and synthetic-tell defects were present in 41% of the stuck worlds. Now called at Gate 5
  when a fix replaces a patterned identifier, with `--avoid` to prevent collisions.
- `verify_xlsx.py` overlapped `reconcile_entities footing` with no stated precedence, so both the
  model and the builder had to guess. The table now says use `footing` first and reach for
  `verify_xlsx` only when a non-contiguous block defeats it.

## [3.3.1] - 2026-08-27

### Fixed

- **Frontmatter description exceeded the 1024 character limit** at 1293, so the skill failed to load.
  Cut to 787 with every trigger phrase kept: AutoQC report, A## leakage, inconsistent names or IDs,
  placeholder and metadata tells, footing and tie mismatches, a world stuck at a high round count, a
  finding that keeps coming back, and "fix this world". The detail that came out of the description
  was already in the body, where it belongs.

## [3.3.0] - 2026-08-27

### Added

- **`log_edit.py` (NEW).** Records a change made by hand into `change_manifest.md`, in the same row
  format the automated fixers write, so `blast_radius.py` reads a hand edit and a scripted edit
  identically.
  - **This closes a hole that made `blast_radius.py` far less useful than 3.0 claimed.** Only
    `a_scrub.py` and `entity_conformer.py` ever wrote to the manifest. Every edit made during a Phase 3
    judgment fix was invisible to the blast-radius pass. That is backwards: the class fixers are the
    safe changes, one rule applied everywhere at once. The hand edits are the dangerous ones, and they
    were the ones nothing recorded.
  - Verified end to end: log a hand edit changing 398100 to 412500 in one file, and `blast_radius all`
    now reports the old value still standing in a second file it was never told about. Before this,
    that returned nothing.
  - Refuses a no-op where old equals new. Warns rather than refuses when the path does not resolve,
    because the edit may have been the rename, and refusing would push the model into skipping the log.
- Phase 3 now ends with a `log_edit.py` call per value changed.
- `selftest.py` F18, 5 new checks. Battery is 53 PASS / 0 FAIL.

## [3.2.1] - 2026-08-27

### Fixed

- **`setup_check.py` passed the backup check when there was no backup.** It accepted the tool's own
  `<world>_qc_backup` folder as evidence of one. That folder is created automatically the first time
  any script writes, and it only holds copies of files a fixer happened to touch, so from round two
  onward the check passed forever while protecting almost nothing. Caught by a negative test: deleting
  the real backup still returned PASS. The tool's folder is now excluded by name, a candidate must
  either carry the world's name or say backup/copy/original, and it must hold at least half as many
  files as the world, so an empty folder named BACKUP no longer counts.

## [3.2.0] - 2026-08-27

### Added

- **`inventory_check.py` (NEW).** Nothing in the toolkit checked the world's files against the spec's
  ④ Artifacts registry, which is the definitive list of what the world holds and what the "Built Files
  Match Spec Inventory" dimension grades. It now does, and it also tracks drift, because the inventory
  is only fixed at the first AutoQC run and moves during remediation.
  - `check <spec> <world>` reports registered artifacts with no matching file, files no registry row
    claims, two rows resolving to the same file, formats that disagree with the extension on disk, and
    build junk (`.DS_Store`, `__MACOSX`, `.meta`). Reuses `spec_check`'s `artifact_index` and
    `resolve_path`, so matching behaves the same as the tie checks.
  - Every run snapshots the file list to `_qc_backup/inventory/` and reports what **appeared,
    disappeared or was renamed** since the previous snapshot. A file in both lists is usually one
    rename, and the report says so.
  - **A file that appeared during remediation is called out as the thing to look hardest at**, with
    the reason: it is a replace-not-add violation, and one world's ambient "no trap" additions
    reopened judgment forks that were already closed.
  - Junk folders are deliberately not pruned from the walk. They have to be visible to be reported,
    and a grader walking the tree sees them too.
- Added to Phase 0 and to the Phase 4 verify block. Added to `setup_check.py`'s manifest.
- `selftest.py` F17, 9 new checks: missing artifact, format mismatch, unregistered file, junk inside a
  junk folder, baseline snapshot, drift on a file that appeared, drift on a file that disappeared, a
  rename clearing its own format mismatch, and the `drift` subcommand running without a spec. Battery
  is 48 PASS / 0 FAIL.

## [3.1.0] - 2026-08-27

Setup hardening, from a measured root-cause analysis of the 69 worlds that have run 20 or more File
System AutoQC rounds (17% of every world that reached the stage; the worst has run 133).

### Added

- **`setup_check.py` (NEW).** Run before anything else. Verifies the toolkit's full 26-file manifest
  extracted, Python is 3.8+, all seven libraries import, the self-test is all-PASS, and, given
  `--spec` and `--world`, that the world folder has files, the spec parses, the spec declares at
  least one trap, and a backup of the world exists. Exits non-zero on any failure.
  - The point is that **none of these failures announce themselves.** A half-extracted zip does not
    error, it silently skips checks. A missing library makes a checker print "not installed,
    skipping", which reads like a pass. A session without the spec cannot tell a defect from a
    registered trap, so it deletes traps. Each one costs at least one AutoQC round.
  - The file manifest is maintained in the script. Adding a file to the skill means adding it there,
    otherwise a builder with a partial extract passes the check.
- Prerequisites and Phase 0 now lead with `setup_check.py`.

### Companion

- **`FileSystem_Helper_Skill_v1.0.md` (NEW, ships separately).** A builder-facing gated walkthrough in
  the same shape as the World Spec Builder skill: eleven gates from setup to upload, a "how to drive
  this" block, and hard stops. It drives this toolkit. This package stays the engine; the helper is
  the conversation. Its Gate 1 is new and has no equivalent here: a buildability check that can stop
  a builder before they start, on six provable spec contradictions, because 42% of the stuck worlds
  contained something no file edit could ever fix.

## [3.0.0] - 2026-08-25

The round-count release. 2.2 made the fixers correct. It did not make the *process* converge, and
worlds were still hitting 20+ AutoQC rounds. The cause was never defect volume. It was three habits:
fixing the instances AutoQC named instead of the classes they belong to, re-uploading before the batch
was finished, and never checking whether one fix knocked over something next to it. 3.0 puts the
operating doctrine into the skill instead of leaving it in Slack, and adds the two read-only tools
that make the failure visible.

MAJOR because the workflow contract changed: the phase list is different, there is a gate before
upload, and a round that isn't fully dispositioned now fails rather than proceeding.

### Added, the five rules (SKILL.md)

- **Rule 1: one flag is a sample, not the defect. Fix the class.** AutoQC is not comprehensive in a
  single round. Every finding now requires the class written down before the fix, and the class swept
  corpus-wide. Framed explicitly against the "don't detect" principle: class expansion is bounded
  because you're looking for a *named* string or pattern, while detection is open-ended and belongs to
  `world-qc`. This is the biggest single lever on round count.
- **Rule 2 (NEW): every fix has a blast radius. Check it before you close the round.** A changed
  number is usually a component of a total in its own file, is usually stated in other files too, and
  a renamed person appears in filenames, headers, email addresses and signature blocks. All of that
  surfaces next round as a *new* finding in a different category, which is why nobody traces it back
  to their own edit. This was the missing half of the whack-a-mole problem: 2.2 could stop a class
  recurring but had nothing to say about a fix causing the next class.
- **Rule 3: batch the round. Never re-upload a partial fix.** Every finding must reach one of four
  states before upload (fixed, class-expanded-and-fixed, declared trap, confirmed false) with one
  named exception, blocked on a specific person for a specific decision. "Next round" is not a state.
  Enforced by `round_log.py close`, which exits non-zero on a partial batch.
- **Rule 4: REPLACE, don't ADD.** Overwrite a wrong value; never leave it and append the right one, a
  reconciling note, a "see also", or a "(corrected)". Added text is the primary cause of answer
  leakage and defuses traps. The trap-repair exception is stated precisely, with a voice test: if the
  in-world author wouldn't plausibly have written that sentence, it's leakage, not evidence.
- **Rule 5: one fix at a time. Never "fix all".** Batched instructions produce batched unreviewed
  edits whose errors surface two rounds later. Each ticket gets a plain-English restatement of the
  mistake before the fix. If you can't restate it without quoting AutoQC, you don't understand it yet.

### Added, Phase 2S and the structural pass

- **`blast_radius.py` (NEW, read-only).** The structural pass. Reads `change_manifest.md`, which every
  writer in this skill appends to, so it holds every change across every round, and answers the two
  questions a chronic class always turns on:
  - **`stale`**: for every value ever replaced, is the OLD value still standing somewhere else in the
    corpus? If yes, the class was fixed file by file, that is the whole diagnosis, and the stale list
    is the fix list.
  - **`touched`**: re-foots every file edited in any round, and lists every unedited file carrying a
    value that changed. Both are self-inflicted defect sources.
  - **`all`**: both, ending in a plain verdict across four situations (stale values, broken footing,
    loose dependencies, nothing structural) each with its own next step.
  - Footing detection parses the count out of `reconcile_entities`' summary line rather than grepping
    for the word "mismatch", because the clean-run summary reads "0 footing mismatch(es)" and a naive
    grep turns every clean file into a false alarm.
- **SKILL.md Phase 2S (NEW)**, the protocol the CHRONIC signal now triggers. Stop editing, run
  `stale`, run `touched`, then **fix at the level of the value rather than the file**: take the
  canonical value, list every artifact obligated to carry it plus everything `blast_radius` found
  carrying it, bring the whole set into line in one pass in one direction, re-foot, then `ties` to
  confirm. One value, one sweep, one verification. Followed by a five-question cross-file consistency
  check covering entities, totals, derived dates, filenames and traps.
- **Escalation now carries specifics.** If the pass finds nothing structural the cause is upstream, and
  the escalation must include the class name, the rounds it appeared in, confirmation that a
  blast-radius pass found nothing, and the two questions only a lead can answer: is the corpus being
  regenerated over remediated files, and does the spec declare the value the findings keep disputing.
  The 2.2-era advice to "go look at the generator or the spec" was useless to a builder who has access
  to neither.

### Added, cross-round memory

- **`round_log.py` (NEW).** Records each round's findings, buckets them into 13 defect classes, and
  reports which classes **came back**. A repeat class is a diagnosis: last round fixed instances, not
  the class. A third appearance trips CHRONIC, which now stops the builder and hands them the Phase 2S
  commands rather than a suggestion to look somewhere they can't reach. `start` / `close` / `status`.
  Reads the AutoQC report text only, never touches the world's files, zero token cost. The log lives
  in the sibling `_qc_backup` folder so re-zipping the world can't ship it.
  - The classifier strips AutoQC's dimension prefix before bucketing. Otherwise a metadata finding
    filed under "No Out-of-World or Build Artifacts" classified as A## leakage.
  - Filename capture disallows spaces in the stem. Allowing them made the match swallow the preceding
    words of the sentence ("in leave_ledger.csv"), which broke round-to-round comparison.
  - Report header lines before the first bullet are dropped rather than counted as a finding.
  - A long run with no repeats past round 12 now prompts a blast-radius pass anyway, because a fix that
    breaks a neighbouring value shows up as a NEW class rather than a repeat, so a clean-looking run
    can still be self-inflicted.
- **`references/round-economics.md` (NEW).** The why: the two-builder arithmetic, the five places
  rounds actually leak, the triage buckets, why replace-not-add is an answer-leakage rule, the
  structural pass in one page, and a six-step checklist for a world already past 15 rounds.

### Added, the Verification Bench, bundled

- **`assets/verification_bench.html` (NEW).** Self-contained offline HTML bench, shipped inside the
  skill so installing the skill distributes it. Wired into Phase 0 as the **false-finding filter**
  (paste AutoQC output, each per-file claim checked against the actual bytes) and re-used in Phase 4
  to confirm fixed findings no longer match. Its **Trace** view is documented as the fastest way to
  scope a blast radius by hand.
- **Scope stated explicitly.** The bench covers both the spec and the files, and it is a viewer, not a
  QC skill. SKILL.md and `assets/README.md` both carry a table separating it from `world-spec-qc`
  (Gate A spec review), `world-qc` (corpus detection) and this skill (corpus fixing). Its spec
  self-check is a **diagnostic** here, answering "is the cause upstream of the files I can edit", not
  a re-run of spec QC.
- Also `assets/README.md` and the original `verification_bench_README.txt`.

### Changed, phases

- Was 5 phases (0 setup through 4 hand-off). Now 7, with the new gates:
  - **Phase 0** gains the bench pre-flight, the round log, and a mandatory **four-way triage** of every
    finding (mechanical class, one-off judgment, declared trap, false finding).
  - **Phase 2 (NEW)**: class expansion. State each open finding's class, sweep the corpus for it,
    report "AutoQC named 2, the class has 9". The expanded set joins the batch.
  - **Phase 2S (NEW)**: the structural pass, which runs *instead of* more fixing on a third-round class.
  - **Phase 3**: the old Phase 2, restated around Rule 5 (restate the mistake, show the diff, one go).
  - **Phase 4** adds `blast_radius.py all` and a bench re-check of the original findings.
  - **Phase 5 (NEW)**: the batch gate and round close, before hand-off.
- Core principles list reordered and extended to 14. Round count is now principle 1, the five rules sit
  above the 2.2 mechanics, and "verify only what you touched" became "verify what you touched, and
  what you touched touches".
- `pdf_markup_scan.py` and `scan_world.py occurrences` are now documented as the Rule 1 class-expansion
  workhorses rather than incidental utilities. No code change to either.
- Coverage map gains three required lines: **Widened** (what AutoQC named versus what the class
  contained), **Blast radius** (what your fixes touched downstream), and **Round** (which round, which
  classes repeated).
- Builder-facing wording gains Phase 0 (triage), Phase 2 (class expansion), Phase 2S (structural pass),
  Phase 4 (blast radius) and Phase 5 (batch gate) scripts, all in plain words.
- Em dashes removed throughout the skill's prose, per house style.

### Added, tests

- `selftest.py` F15, 8 checks on `round_log.py`: header-line rejection, dimension-prefix stripping,
  filename capture precision, repeat detection, first-time-class non-repeat, batch gate blocking a
  partial round (non-zero exit), batch gate passing a full round, and log written beside the world
  rather than inside it.
- `selftest.py` F16, 5 checks on `blast_radius.py`: manifest parsing, a stale sibling detected, a
  clean sweep reporting no stale values, no false footing alarm on a clean file, and the verdict
  escalating correctly when nothing structural is found.

### Unchanged

No behavior change to `a_scrub.py`, `entity_conformer.py`, `metadata_hygiene.py`, `pdf_replace.py`,
`spec_check.py`, `reconcile_entities.py`, `verify_xlsx.py`, `scan_world.py` or `gen_realistic_values.py`.
A single-flag remediation runs exactly as it did in 2.2.

## [2.2.0], 2026-07-21

The apply-path release. Through 2.1 the skill sold itself on "scripts do the work", but only
`metadata_hygiene clean` actually wrote files; the A## scrub had **no script at all**, and
`entity_conformer`/`pdf_markup_scan` only detected, leaving the model to hand-edit every file. That is
where the token cost and the hand-editing mistakes (the 2.1 Law-world garbling) came from. 2.2 makes
the deterministic classes actually self-applying, and fixes a batch of correctness bugs a review found,
several of which caused silent false "all-clear" results on real (non-UTF-8, Windows) files.

### Added, the CLEAN apply path (scripts now decide AND apply)
- **`a_scrub.py` (NEW)**: the A## build-artifact scrub finally has a script. Builds the A##→name map
  from ④ Artifacts (same reader `spec_check` uses), enumerates every leaked code across
  csv/xlsx/txt/md/html/docx (PDFs routed through `pdf_replace.py`), and swaps each **only where it reads
  cleanly**. Codes not in the registry (real invoice/room codes) and swaps that would double an adjacent
  word (`per Policy A09`) are left on a REVIEW list with a suggested rewrite, never auto-mangled.
  Dry-run by default; `--write` backs up every file and records the change log.
- **`entity_conformer.py apply`**: new subcommand. Fixes the fully-determined whole-cell cases in place
  (a cell that is exactly the wrong name for its row's ID; a wrong ID-shaped token), toward the master.
  Detection and apply share one rule function, so they can never drift. Judgment cases (name buried in
  prose, constant-fill) are flagged, not changed. Dry-run by default; `--write` backs up + logs.
- **`metadata_hygiene.py clean` now takes a directory** and cleans every Office/PDF file under it, so
  "clean everything you touched" is one command.
- **`change_manifest.md` + `comments.txt`** are now actually written into the world folder by the
  writers (2.1 promised `comments.txt` to the builder but nothing ever created it). Backups go to a
  sibling `_qc_backup` folder *outside* the world, so they're never re-scanned or re-zipped in.
- **`scripts/requirements.txt` (NEW)**: the full dependency set, with `pip install -r`. SKILL.md now
  has a Prerequisites section (install, find-the-spec, back-up-first) and a plain-English glossary.
- **`_common.py` (NEW)**: shared encoding-safe reads, backups, change-log, and the `_qc_backup`
  exclusion, imported by every script.

### Fixed, silent false "all-clear" bugs (from a full code review)
- **cp1252 blindness (BLOCKER).** `scan_world occurrences`, `spec_check` (ties/extract), and
  `reconcile_entities` all read text as UTF-8 with `errors=ignore/replace`, so an accented value in a
  cp1252 CSV/TXT (the norm in this domain) read as *absent*, a false "0 stale hits" / false `TIE MISS`.
  All now decode utf-8→cp1252→latin-1 via `_common.read_text`.
- **`metadata_hygiene clean` could damage files.** It stamped **`Application=Microsoft Excel` onto every
  file type** (a Word doc claiming Excel is a louder tell than the one removed), now sets the correct
  native app per format. PDF clean dropped bookmarks/outline and truncated the file in place with no
  backup, now clones the full catalog and writes atomically via a temp file. The `shutil.move` outside
  the try left an orphan `.tmp` and a raw traceback when a file was open in Excel/read-only, now a
  plain message, no orphan. `clean` without `--date` now warns loudly instead of silently leaving the
  build date.
- **`metadata_hygiene scan` silently reported "0 leaking"** when pypdf was missing or a PDF was
  encrypted/corrupt, now prints a NOTE and an "unchecked" count.
- **`pdf_replace.py`** printed `saved:` before saving and lost the edit (and orphaned a temp) if
  `--render-check` failed; added no error handling for missing/corrupt/encrypted input. Now saves →
  render-checks safely → replaces → reports, with plain-English errors and non-zero exit on no-op.
- **`entity_conformer` false positives:** the `CONSTANT FILL` flag fired on legitimate single-entity
  tables (a 12-week timesheet); the `NAME MISSING` flag fired on every ID-only reference row (ledgers,
  crosswalks). Constant-fill now requires a multi-ID table with one ID dominating; the ID-only-row flag
  was removed (that's not a defect). The real "46 mess" is still caught by constant-fill + wrong-name.
- **`reconcile_entities footing`** foot-checked non-additive columns (year, rate, qty, id): pure noise
  that buried real misses; now skips them and constant-valued blocks.
- **`spec_check ties/refs`** didn't validate `world_dir`; a typo'd path produced a report full of fake
  `[FILE NOT FOUND]` problems, now exits with a clear message. `verify_xlsx --range B:B` (whole column)
  crashed, now a clear error.

### Fixed, docs & packaging
- **Removed the double-nested `.claude/.claude`** (the skill wasn't discoverable) and renamed the folder
  to `world-qc-remediation` to match the frontmatter `name`.
- **Removed `present_files`** (not a real tool): the change table is written to `change_manifest.md` and
  printed inline. Removed the dangling `[CONFIRM: …]` legend (no such markers remain).
- **SKILL.md rewritten**: runnable literal commands per phase, honest Engine-1 labeling (WRITES vs
  DETECT), glossary, prerequisites, an error-handling rule (a "skipping" note voids the check), and an
  explicit "do NOT use to detect / for app-data" line in the description. Redundancy trimmed.
- **References:** removed all personal names (escalate via your world thread in #julius-world-threads),
  fixed stale "Step N" → "Phase N", neutralized `aqc-dimensions.md`'s "walk the list" sweep into a
  reference-only note, dropped the obsolete "anchor" precedence tier (now spec > any built artifact),
  fixed the `verify_xlsx`/`recalc.py` invocations.
- **Shipping hygiene:** dropped `__pycache__/` and `spec_check.py.orig_backup` (the latter is itself the
  "build scaffolding in the filesystem" defect this skill lectures about). `selftest.py` expanded to 24
  known-answer cases covering the apply path, cp1252 recall, and the new false-positive fixes.

## [2.1.0], 2026-07-15

Driven by a live Law-world run: a bespoke raw-PyMuPDF redact/insert pass (used because `pdf_replace.py`
wasn't listed in SKILL.md's script table and so never got reached for) left three PDFs with silently
garbled em-dashes/curly-quotes, one PDF with a checkbox glyph wiped by redaction bleed, and four PDFs
carrying 2-3 stacked `saveIncr()` revisions each (visible only by inspecting raw `%%EOF` counts),
caught after the fact by a byte-size question, not by the skill itself. Closes that loop.

### Added
- **`metadata_hygiene.py` now detects two more tells:** a stray Title/Subject field carrying an
  original working filename (e.g. a Google Docs export leaving `Foo_Revised.docx` in `/Title`), and,
  for PDFs, more than one `%%EOF` in the file, meaning it carries incremental-save (`saveIncr()`)
  revision history rather than being a single clean revision. `clean` already fixes both as a side
  effect of its full pypdf rewrite; it now reports the before→after revision count when it collapses
  one.
- **`pdf_replace.py` and `verify_xlsx.py` added to SKILL.md's script list**: both existed and were
  fully functional but were missing from the table, so they weren't being reached for. `pdf_replace.py`
  in particular already guards the two mistakes below (rejects a non-cp1252 replacement instead of
  mangling it; always ends on a full non-incremental save), it's now called out as the default for a
  simple in-place PDF string swap, before hand-rolling anything.
- **`references/file-formats.md` PDF section: four new gotcha call-outs** for anyone hand-rolling a
  PyMuPDF edit (multi-paragraph rewrite, page rebuild) that `pdf_replace.py` doesn't cover: (1) never
  leave a PDF on `saveIncr()`: always end on a full rewrite or run `metadata_hygiene.py clean`; (2)
  base-14 fonts (Times-Roman, Helvetica) silently render the wrong glyph for curly quotes/em-dashes
  with no error, sanitize to ASCII or verify the embedded-font-reuse path actually renders; (3)
  `insert_textbox` can render nothing at all when the box is too tight (spare at/near zero), with no
  exception, always verify positive spare *and* re-extract the text afterward to confirm it's really
  there; (4) a redaction rect that starts even a fraction of a point into a neighboring glyph (a
  checkbox, an adjacent character) can wipe it too, keep rects clear of anything adjacent you want to
  keep.

### Changed
- **`clean` is now unconditional**, not scan-triggered: run it on every file you edit, every time,
  principle 6 and the Phase 1/3 wording updated accordingly. The whole point is that editing a file is
  what *creates* these tells (a fresh fingerprint, revision-history residue); waiting for `scan` to
  flag it after the fact is the wrong order of operations.

## [2.0.0], 2026-07-14

Major reframe. The skill is now a **fixer, not a detector**: AutoQC (free, server-side) finds defects;
this skill fixes them deterministically, one class at a time, and verifies only what it touched.
Scope narrowed to the **filesystem** (documents + spreadsheets); app-data loading is a separate
pipeline. Driven by two live test runs, one where the checks cried wolf (65 false positives) and one
where "clean" was reported but AutoQC found five real defects.

### Added, CLEAN engine (deterministic class-level fixers)
- **`entity_conformer.py`**: domain-agnostic name/ID conformer. Point it at the spec's canonical
  master (employees, vendors, parties, accounts, SKUs) with `--id-col`/`--name-col`; flags any ID
  carrying the wrong name, name carrying the wrong ID, or ID constant-filled across rows (the
  "1000s of names" mess, the vendor-crosswalk "46").
- **`metadata_hygiene.py`**: `scan` for tool fingerprints (openpyxl/reportlab/python-docx) and
  build/today dates; `clean` strips them via direct docProps rewrite (no re-save, so it doesn't
  re-stamp). Fixes the openpyxl-leak miss and prevents the skill causing it.
- **`pdf_markup_scan.py`**: flags PDFs/docs printing raw Markdown/HTML as visible text (`##`, `**`,
  `<td>`, `|---|`), the unrendered-source defect from Slack.

### Fixed, the false positives (from the noisy live run)
- `spec_check.py ties` now: skips `Type=Trap` canonical rows; matches `95.0`==`95`; matches datetime
  cells against written dates across formats; reads `.pptx`.
- `spec_check.py refs` is **filesystem-only**: app-data foreign-key/orphan checks are off unless
  `SPEC_CHECK_APPDATA=1`.
- `reconcile_entities.py footing` is **block-aware**: sums only the contiguous block above each
  total, so stacked sub-tables in one column no longer false-positive.

### Changed, contract & framing
- **Never reports "clean."** Output is a **coverage map**: fixed / verified / not-checked (AutoQC's
  job, voice, realism, paraphrased facts, app-data).
- **Verify only what you touched**: scoped, not a broad detection sweep (that duplicates world-qc and
  burns tokens).
- SKILL.md rewritten around AutoQC-detects → CLEAN → scoped-verify → coverage-map, filesystem-only,
  builder-gated phases.
- `selftest.py` expanded to 15 known-answer cases covering every new/fixed behavior.

### Removed / out of scope
- App-data referential integrity, app-table reconciliation, and cross-file temporal joins (DocuSeal
  etc.), those belong to the app-load pipeline, not filesystem remediation.

## [1.5.2], 2026-07-13

### Changed
- **Final report (Step 9) rewritten in plain language.** The end-of-run log is now written for the
  builder (a domain expert, not a coder): short sentences, concrete before→after numbers, no internal
  defect letters (A, G) or jargon like "systemic"/"footing". Replaces the previous dense
  ticket-closing format.

## [1.5.1], 2026-07-13

Bug-fix release from a Layer-1 adversarial stress test of `spec_check.py`. The battery caught two real
bugs, both now fixed and regression-guarded.

### Fixed
- **Numeric substring false-match:** the tie check matched values as plain substrings, so headcount
  `327` "matched" a cell containing `3270` and a real drift was **missed**. Now numbers match on digit
  boundaries (and commas are ignored, so `$43.2M` still reconciles to `43,200,000`).
- **Trap declared only in ③ Tasks was flagged:** a trap declared solely in the ③ *Trap* columns
  wasn't in the tie-check skip-set, so it could be reported as a fixable drift, the exact
  trap-deletion risk. The skip-set now honors ③ traps (from the trap description, not the Remediation
  Path, which names the correct artifacts).

### Added
- `scripts/selftest.py`: the known-answer battery (7 fixtures) as a shippable, zero-token regression
  test. Run after any script change; must be all-PASS.
- "Testing it cheaply" note: run the deterministic scripts against real worlds for free; only the
  adversarial lens costs tokens.

## [1.5.0], 2026-07-13

Adds a plain-language guidance layer so a non-technical domain expert can run the whole thing without
knowing any code. The skill now prints simple, click-by-click instructions at setup, at every
checkpoint, and for the manual steps it can't do itself (eyeballing key files, uploading to RLS).

### Added
- **Builder-facing guidance section**: verbatim plain-English scripts to print at setup (make a
  folder, add the spec, open Claude Code, run the skill) and at each Phase 0 to 4 checkpoint (what
  happened, what to check, "reply go"). Written for zero technical knowledge.
- **Phase 5 hand-off text**: the steps the builder does by hand, eyeball the domain's key files
  (roster for HR, GL+TB for Accounting, etc.) and the RLS upload sequence (upload revision → comment →
  submit → apply revision → Submit for AutoQC).
- The skill writes **comments.txt** (every change + one-line why) into the world folder so the builder
  can copy-paste change comments into RLS.

### Note
- Two spots are marked `[CONFIRM: …]`: the exact "open Claude Code" button and the exact RLS button
  labels, for you to verify against the live tools before this goes to builders.

## [1.4.0], 2026-07-13

Final structural change: the skill now runs in **builder-controlled, checkpointed phases** instead of
one unattended pass, so the builder always knows what changed and why (no more firing it off and
returning 2.5 hours later to a silently rewritten world). No new detection logic, this sequences the
existing machinery into gated phases with explicit STOP points.

### Added
- **Gated-phase run mode (default):**
  - Phase 0, Setup & plan: trap manifest + de-duped tickets, no edits yet -> CHECKPOINT.
  - Phase 1, Remove A## builder-code leakage -> CHECKPOINT (review change manifest before apply).
  - Phase 2, Resolve AQC tickets one at a time -> CHECKPOINT per ticket.
  - Phase 3, Broad re-check (the catch-what-AQC-missed pass) -> CHECKPOINT.
  - Phase 4, Resolve re-check findings one at a time, then targeted re-verify -> CHECKPOINT (upload-ready).
  - Every checkpoint reports what the phase did / found / changed and waits for go-ahead.
- **"Balancing token cost against catching what AQC missed"** note resolving the tension: cheap
  deterministic checks run broad over the whole corpus every re-check; the expensive adversarial sweep
  runs broad once (Phase 3) then scoped to changed files (Phase 4). States the honest residual.

### Changed
- Description now advertises checkpointed phases rather than a single pass.

## [1.3.0], 2026-07-13

Makes the skill genuinely domain-agnostic and hardens trap preservation, by reading what a world must
satisfy from its **spec** instead of hardcoding any domain. Driven by domain-lead feedback (Accounting
8 ties, FP&A 16, HR 6, Law figure list, S&M "connectedness over reconciliation"), none of which is
baked into the skill; it all rides in via the spec tabs. Token-negative: all new checks are
deterministic, diff-only Python that move detection off the adversarial lens.

### Added
- **`scripts/spec_check.py`**: spec-driven, domain-agnostic engine with three subcommands:
  - `traps` builds the **trap manifest** from ④ *Trap Content* + ③ trap columns + ② *Note*.
  - `ties` checks every ② Canonical Value is carried by its *Must match* artifacts, **auto-skipping
    trap-bearing artifacts** so declared divergences are never flagged as fixes.
  - `refs` checks referential integrity: unresolved ④ IDs + orphaned app-data foreign keys from
    REF · Schema Library *Depends on* (the HR/FP&A/S&M "not connected / parent key not exported" class).
- **Trap-manifest guard** section: build the manifest before any fix; flag-not-fix; classify each
  mismatch (manifest → preserve, undeclared-and-breaks-a-tie → drift, ambiguous → surface); stop and
  ask if the spec declares no traps; re-verify traps survive after fixing. Includes the Accounting
  discriminator (a real trap nets back so the higher tie still holds).
- SKILL.md "what the engine reads from the spec" mapping (②/③/④/REF tabs) and a matching section in
  `references/traps-and-facts.md`.

### Changed
- Source-of-truth + trap logic now anchored to concrete spec tabs, so the intended-vs-accidental call
  is mechanical, not remembered. Core principle 3 references the manifest guard.
- Step 8 now runs `spec_check.py ties` and `refs` alongside `reconcile_entities.py`.

### Design guarantees (the three constraints)
- **Token-neutral/negative:** new checks are deterministic scripts emitting diff-only output; they
  shift detection off the expensive adversarial lens.
- **Domain-agnostic:** zero domain logic in the skill; ties/traps/keys are read from the spec, so one
  download serves Accounting, FP&A, HR, Law, S&M, Personal alike.
- **Traps preserved:** the manifest is a hard guardrail; `ties` structurally skips trap-bearers, and
  the guard forbids collapsing any divergence the spec hasn't cleared as accidental.

### Note
- Trap preservation is only as strong as the spec's declared traps. If builders leave ③/④ trap
  columns empty, the skill defaults to "don't collapse, ask." The durable fix is upstream in the spec.

## [1.2.0], 2026-07-13

Token/cost optimization after a real run burned a plan (logged ~1.5M subagent tokens + 221M
cache-read: subagent-heavy verification, each agent above 150K context, on a premium model). The
Phase-1 remediation loop was already lean; this release attacks the verification/subagent layer. No
change to *what* gets fixed, only to how much context and model spend it costs.

### Added
- **Cost & context discipline section** (applies throughout): cost ≈ (tool calls) × (context per
  call) × (model rate); do detection in scripts and surface only diffs; targeted reads of the flagged
  region only; verify with scripts not re-reads; one batch per session with a context reset between
  batches; persist the de-duped ticket list to a file instead of re-pasting the AQC report.
- **Core principle 8, "cheapest correct path"**: thoroughness must not mean holding the whole world
  in context.

### Changed
- **Step 8 subagent cost rules**: the headline change. Explicit **model split**: mechanical lenses
  (extraction, inventory, deterministic checks) → **Haiku 4.5**; adversarial/judgment lenses (narrative
  contradictions, visual PDF artifacts, answer-set pollution) → **Sonnet 5**; **never a
  premium/creative model (e.g. Fable) for this work.** Rationale baked in: Haiku's 200K context ceiling
  and reasoning gap make it unsafe for adversarial lenses, but ideal (and Anthropic's intended
  sub-agent model) for mechanical ones. Plus: **scope each subagent to only its files** (~7x cheaper
  per call, keeps mechanical lenses under 200K), **cap spawn count** (one agent per lens over a scoped
  set, not one per file), and **targeted re-checks** (re-run only the lenses that found majors, against
  only changed files, not a fresh exhaustive sweep).
- **Step 2 / Step 7** reinforced for targeted reads and script-based verification instead of whole-file
  reads.

### Notes
- Preserves the adversarial verification signal (it caught 20 majors deterministic checks can't see),
  the goal is to make that signal cheap via model tier + context scoping + targeted re-runs, not to
  drop it.
- Model tiers reflect July 2026 availability (Haiku 4.5 = 200K context, $1/$5; Sonnet 5 = frontier
  reasoning, 1M context). Revisit if the model lineup changes.

## [1.1.0], 2026-07-11

Adapts the skill from a single-flag remediation tool into a full **AQC-report → whole-world**
remediation pass runnable in Claude Code against the unzipped filesystem, while keeping the original
single-flag path intact. Motivation: cut file-revision time and reduce the number of RLS AQC rounds.

### Added
- **Inputs & setup section** with two operating modes: **Mode A** (a hand-verified anchor file the
  builder declares canonical for a named slice) and **Mode B** (spec + files only, the default).
  Establishes explicit source-of-truth precedence: **spec > anchor > artifact.**
- **Step 1 rewritten to parse a full AQC report** and de-duplicate its many dimension findings into
  root-cause tickets (a single defect that surfaces in 3 to 4 dimensions becomes one ticket). Includes a
  mandatory **coverage check** (every non-pass finding maps to ≥1 ticket) and keeps **all severities,
  minors included**; passes are set aside for the Step 8 re-check.
- **Step 4, triage systemic vs. surgical**, with the decision test ("one rule correct everywhere
  without re-deciding?") and the systemic-sweep + **change-manifest** requirement.
- **Defect Type G, out-of-world / build-artifact leakage** in the taxonomy: the systemic recipe for
  **A## artifact-registry codes** leaking into solver-visible files. House rule: replace each A## with
  the human-readable artifact name from the spec's Artifacts tab; only touch codes in the registry
  range; list pattern-matches that don't resolve (real invoices, doc codes) on a REVIEW list instead
  of auto-changing them; emit a change manifest for builder skim.
- **Step 8, final light AQC-category self-check**: walks the current AQC dimensions over the revised
  corpus before upload (checking passes too, to catch regressions and AQC misses), framed as a debug
  pass to reduce RLS rounds.
- `references/aqc-dimensions.md`: the current AQC dimension checklist, encoded verbatim from the
  latest HR-world AQC run (P0/P1 markers).
- `scripts/reconcile_entities.py`: deterministic, diff-only reconciliation of tabular app-data: joins
  records on shared IDs to flag same-entity field mismatches across files, and foots labeled totals,
  exhaustively (catches the "50-of-84-rows" class an LLM pass samples). Runs in the final check.

### Changed
- **Re-anchored the "grounding fact" model to the spec.** FT0xx fact-ledger framing is now treated as
  legacy; canonical truth comes from the spec's Canonical Values + Artifacts registry + declared-trap
  list, with an optional anchor file. Handles "LIGHT / no fact ledger" worlds.
- **Consistency reframed as corpus-wide, not task-scoped**: because taskers pull from any file, an
  accidental drift in a file no current task reads is still a live defect. Complete internal
  consistency *except spec-declared traps*.
- **PDF handling**: made explicit that RLS cannot regenerate individual files, so PDF rebuilds happen
  in Claude Code, with mandatory metadata hygiene (strip `/Producer` `/Creator` `/Author` `/Title`
  tool signatures, then run `scan_world.py tells`) so a rebuild doesn't create a fresh synthetic tell.
- Report format (Step 9) now covers multi-ticket runs, the de-dup collapse, strategy per ticket, and
  the final-check verdict.
- Description/frontmatter updated to advertise the AQC-report path and add a `version` field.

### Notes / known limits
- The Step 8 light check only sees what the AQC categories + `reconcile_entities.py` look for;
  prose-level drift across narrative docx/pdf that no dimension checks can still slip through. It
  reduces RLS AQC rounds, it does not replace them.
- `aqc-dimensions.md` is a snapshot of the HR-world run. If AQC's category set changes, update that
  file, it is the single source for the check.

## [1.0.0], 2026-07-05

Initial skill. Single QC flag → single file surgical remediation loop (parse → scan → classify
A, F → decide → apply → verify → report), with `scan_world.py`, `gen_realistic_values.py`,
`verify_xlsx.py`, `pdf_replace.py`, and the error-taxonomy / traps-and-facts / file-formats references.
