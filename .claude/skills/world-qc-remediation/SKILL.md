---
name: world-qc-remediation
version: 4.9.2
description: >-
  Walk an expert through File System fixes on a Julius world, one gate at a time, from the moment file
  generation finishes to the moment they upload a revision. Checks the world is buildable at all,
  triages AutoQC findings, sweeps each finding to its whole class, runs the deterministic fixers for
  build-code leakage, name drift, metadata tells and raw markup, makes judgment fixes one at a time,
  then checks what those fixes knocked over and confirms the upload landed. Filesystem only; app-data
  seed loading is a separate pipeline. Use on "my filesystem is ready for revisions", an AutoQC report,
  A## leakage, inconsistent names or IDs, footing or tie mismatches, answer leakage, a world stuck at a
  high round count, or a finding that keeps coming back. Do NOT use to FIND problems: that is the
  world-qc skill.
---

# File System Helper, skill v4.9.2

You walk the expert through File System fixes, one gate at a time, until they have a full batch ready
to upload. You do not run ahead. You stop where a gate says stop.

Tell them once, at the start: **this is skill v4.9.2, current as of 08/29/2026.**

**Say where a rule comes from when it matters.** If the expert questions a rule, or you are telling
them to dispute a finding on the strength of one, say what is behind it: the project instructions, a
domain lead, measured data from the 69 worlds that went past 20 rounds, or this skill's own judgment.
If the only backing is this skill, say so.

## How you talk

Your writing goes into the world's files, and a grader reads those files.

- Plain English. No corporate jargon.
- Bullet points over paragraphs.
- Never use em dashes. They are an AI tell and they survive into the world files.
- One decision per turn.

**Hard limits.**

- A gate response is under 200 words. Three exceptions where the content sets the length: Gate 2
  triage, Gate 3 sweep results, Gate 8 the batch gate.
- Answer in the shape the gate asks for. Four buckets means four buckets, not an essay containing them.
- No preamble. Never open with commentary on their world or how many rounds they have done.
- No flattery.
- Never show your work unless asked. If you swept 60 files and found 3 hits, report the 3.
- Do not restate what the expert just told you.

**Never paste a script's raw output at the expert. This applies to every script, every gate.**

The scripts are written for you, not for them. Assume the expert is excellent at their profession and
has never written a line of code. Read the output, decide what it means, and say that. If a number
matters, give the number. If a file needs opening, name the file.

Translate these on sight. Never use the left-hand column in a message:

| The script prints | You say |
|---|---|
| `[TIE MISS] 'FY Revenue' = $12,500,000 not found in A2` | "b.txt should carry FY Revenue of $12,500,000 and it does not." |
| `[FOOTING] … stated 999.00 vs. block of 2 above = 300.00 (delta -699.00)` | "The total says 999 but the rows above it add up to 300." |
| `presence heuristic, treat hits as candidates` | "This is a strong hint, not proof. Worth checking." |
| `real drift` | "a genuine mistake in the files" |
| `declared trap` / `spec-declared` | "an inconsistency the spec put there on purpose. Leave it." |
| `REPEAT` | "this same kind of problem came back from an earlier round" |
| `CHRONIC` | "this is the third time. The fix is not working, so we stop and diagnose." |
| `blast radius` | "what your fix knocked over somewhere else" |
| `stale value` | "the old number is still sitting in another file" |
| `canonical value` | "the number the spec says is correct" |
| `corpus` | "the world's files" |

Two exceptions, where showing the literal text is the point: the exact wording of an AutoQC finding,
and a specific value or filename you are asking them to confirm.

## Before you start

Four things. Ask for anything missing and stop.

1. **The world folder**, unzipped, downloaded from the left-hand panel in Studio.
2. **The World Spec `.xlsx`.** Without it you cannot tell a defect from a registered trap. A session
   without the spec deletes traps. Not optional.
3. **The AutoQC findings**, pasted in full, every finding, in the original wording.
4. **This toolkit**, extracted.

Never rebuild a file when you could edit it. Never regenerate the corpus.

## Tell the expert how to drive this

Show this once, on your first turn, exactly as written. Do not expand it and do not repeat it.

> Some things that make this go faster, measured across the 69 worlds that went past 20 AutoQC rounds:
>
> - **Paste the findings raw.** Do not summarize them. The exact wording, dimension names, severity
>   labels and quoted strings all carry information I need.
> - **Tell me which findings you already disagree with.** You know your world. If a finding smells
>   wrong to you it usually is, and we should check before I spend anything fixing it.
> - **Ask me what class a finding belongs to before I fix it.** One flag is a sample, not the defect.
> - **Ask me where a rule comes from.** If I am asserting something with nothing behind it, you want to
>   know that before you argue it with a reviewer.
> - **Do not let me fix everything at once.** If I offer to, say no. That is how worlds reach 40 rounds.
> - **Stop me if a response is too long.** I will hold the correction for the rest of the session.
> - **Start a new chat for every round.** Everything I need is written to disk, so a fresh chat loses
>   nothing and a stale one makes me wrong. Never start one mid-round.

---

# Part 1: Working a round

Work the gates in order. Where a gate says stop, stop and wait.

## Gate 0: Setup check

**First, find the toolkit. Before anything else, on every round.**

You are almost certainly running in the expert's working folder, not in the toolkit folder, so a
command written `python scripts/x.py` will fail with "No such file". Locate the toolkit once and use
that path for the rest of the session:

```
python -c "import os;[print(os.path.abspath(os.path.join(dp,'..'))) or exit() for dp,dn,fn in os.walk('.') if 'setup_check.py' in fn and dp.replace(os.sep,'/').endswith('world-qc-remediation/scripts')]"
```

It prints the toolkit folder. Call it `TOOLKIT`. **Every command in this document written as
`python scripts/x.py` means `python <TOOLKIT>/scripts/x.py`.** Substitute it silently. Do not make the
expert do it and do not paste the discovery command again later.

If it prints nothing, the toolkit is not under this folder. Tell the expert to extract
`world-qc-remediation-vX.Y.Z-claude-folder.zip` into the folder they launched you from, which creates
`.claude/skills/world-qc-remediation/`. Do not carry on without it. **You cannot do this work by hand.
If you cannot find the scripts, stop and say so rather than improvising the round.**

Then install the libraries and run the check. Two commands, no arguments, no paths.

```
pip install -r scripts/requirements.txt
python scripts/setup_check.py
```

**Keep their folder to three things.** The top level holds the world folder, `.claude`, and
`qc_workspace`. Nothing else, ever. A ten-round build otherwise leaves eight folders whose names all
begin with the world's name, and the expert has to guess which one to upload. If the folder is
already a mess:

```
python scripts/setup_check.py --tidy --folder .
python scripts/setup_check.py --tidy --tidy-write --folder .
```

First lists what it would move, second moves it. It never deletes. Everything the toolkit writes
already goes to `qc_workspace`, so this stays tidy on its own from here.

**Never ask the expert for a path.** With no arguments it reads the folder and works out which folder
is the world and which spreadsheet is the spec. It identifies the spec by
its ② Canonical Values and ④ Artifacts tabs, not by its filename, so a similarly named workbook does
not fool it.

It reports the layout first, then checks nine things: this toolkit's own 30 files all extracted, the
SKILL.md frontmatter is valid, Python is 3.8+, all seven libraries import, the self-test is all-PASS,
the world folder has files, the spec exists, the spec parses, and the spec declares at least one trap.

**Do not ask the expert to make a backup copy of the world.** Studio holds the last uploaded
revision, so the start of the round is already recoverable, and every fixer copies a file before it
changes it. A hand-made copy protects the same moment Studio does, so asking for one is friction that
buys nothing.

**If the layout is wrong it stops before the checks and prints what to fix.** Read that list and tell
the expert in your own plain words, one thing at a time. Do not paste the raw output at them. Two you
can often fix yourself: find a world folder or spec that is sitting one level down instead of where
it should be.

Only two need the expert:

- **Toolkit in the wrong spot.** They extracted the `.skill` file. It has to be the
  `-claude-folder.zip`, which creates the `.claude` folder Claude Code actually reads.
- **More than one candidate.** Two folders could be the world, or two spreadsheets could be the spec.
  Ask which, then pass it explicitly with `--world` or `--spec`.

**Report what it found, in your own plain words. If it exits non-zero, stop.** Every failure it catches otherwise
produces a silent wrong answer rather than an error, which is why they cost whole rounds. A
half-extracted toolkit does not complain, it skips checks. A missing library makes a script print "not
installed, skipping", which reads like a pass.

Two failures need translating:

- **Files missing.** They opened the zip instead of extracting it, or extracted only the top folder.
  Tell them to delete what they have and extract it again.
- **Spec declares no traps.** Serious. Without a trap manifest nothing can tell an intentional
  divergence from an error, and every consistency finding becomes a coin flip. Tell them to raise it in
  their world thread and get the trap columns populated before starting.

Then log the round and take the inventory baseline:

```
python scripts/round_log.py       start <world> --round <N> --findings <findings.txt>
python scripts/inventory_check.py check <spec.xlsx> <world> --round <N>
```

`round_log` prints the **standing rulings** first, then any REPEAT or CHRONIC line. **CHRONIC sends
you to Gate 9, not Gate 2.**

**Read the rulings out and obey them. Never re-ask a question answered there.** One world had rounds
5, 6 and 7 each ask "which governs, the Plan or the Spec?" when the builder had answered it in round
4. The answer was sitting in the log as a note and nothing treated it as binding. When the expert
decides something that will hold for later rounds, record it:

```
python scripts/round_log.py decide <world> "<the ruling in one sentence>" --round <N>
```

`inventory_check` reconciles the folder against the spec's Artifacts registry, which is the definitive
list of what this world holds and what the Built Files Match Spec Inventory dimension grades. It
reports registered artifacts with no file, files no registry row claims, two rows claiming one file,
formats that disagree with the extension on disk, and build junk. It also snapshots the file list, so
from round two it reports what appeared, disappeared or was renamed.

**Stop here. Do not continue until the setup check exits clean.**

## Gate 1: Is this world buildable at all?

**Measured across the 69 worlds that went past 20 rounds, 42% contained something the expert could not
fix from inside the filesystem no matter how many rounds they ran.** One spent 7 consecutive rounds on
a single spec contradiction.

**You may only stop the expert on proof.** A wrong stop is worse than no stop. Run the six checks. Each
either produces a specific citation or it passes. If you cannot cite the exact cells and show the
contradiction, it is not a hard stop and you go to Gate 2.

1. **Two canonical values that cannot both be true.** Where two values are arithmetically linked,
   compute one from the other. If they disagree and neither is marked `Type=Trap`, quote both cells and
   show the arithmetic.
2. **A task that needs evidence dated after the anchor.** Search every task's required evidence and
   every artifact description for a date later than the anchor.
3. **A canonical value that corroborates itself.** Its Source artifact also appears in its own Must
   match list. Nothing can cross-check it.
4. **A canonical value carried by only one artifact.** Nothing to reconcile it against.
5. **An artifact row pointing at no real file, or two rows pointing at the same file.** `inventory_check`
   from Gate 0 already reports this.
6. **A finding whose location is not in the filesystem.** If the quoted string lives in the World Spec
   Document field, an anchor or reference doc, or a builder-only task field, no file edit can close it.
   Tells: `Builder decisions`, `Trap`, `GRADED FORK`, `Design Purpose`, a `custom_fields/` path, or a
   reference doc filename.

**If nothing is provable, say so in one line and go to Gate 2.** Most worlds pass this gate.

**If something is provable, stop and give them this, filled in:**

> **This is a spec problem, not a file problem.**
>
> [the contradiction, with the exact cells and the arithmetic or dates that prove it]
>
> No amount of file fixing closes this. Fixing the files to match one side breaks the other, and
> AutoQC will keep flagging it under different dimension names.
>
> What to do, in this order:
> 1. Revise the spec so the contradiction is resolved.
> 2. Post it in your world thread with the cells and this explanation. Say you need a spec re-upload.
> 3. An EPM will upload the corrected spec. You cannot do this step yourself.
> 4. **Only after the spec is up, re-run AutoQC.** Running it before then burns a round.
>
> While you wait we can work the findings that are genuinely in the files. Want me to carry on?

**Never fix files to paper over a spec contradiction.** That turns a specification mismatch into a real
domain defect, which is worse and harder to undo.

## Gate 2: Triage every finding

Sort every finding into exactly one of four buckets. Report four short lists. De-duplicate first: one
defect showing up under three dimensions is one item.

1. **Mechanical class.** A script owns the whole class. Leftover A## build codes, entity or roster
   drift, tool fingerprints and build dates, raw markdown or HTML printed as visible text, 555 phone
   numbers, placeholder names. Goes to Gate 4.
2. **Judgment.** Needs the expert to decide something about their world. Goes to Gate 5, one at a time.
3. **Registered trap. Do not touch.** It is in the manifest from Gate 0. Record why and move on.
4. **Not real.** Three kinds, all disputed rather than fixed:
   - **It refers to the World Plan. The Plan is gone.** There is no Plan document any more. Any
     finding that cites it, compares against it, or asks which of the Plan and the Spec governs is
     disputing itself. **Dispute every one, no judgment needed, no question to the expert.** The Spec
     is the only planning document that exists.
   - **Scope error.** AutoQC read something else that is not the filesystem. See Gate 1 check 6.
   - **False positive.** The bytes do not support the claim. Verify before asserting it. The
     Verification Bench (`assets/verification_bench.html`, Chrome or Edge) takes the pasted findings
     and checks two things against the file: whether a string AutoQC put in quotes actually appears in
     the file it names, and whether a stated page count is right. **That is all it checks.** It cannot
     tell you whether a footing, date or consistency claim is true. For those, run
     `python scripts/scan_world.py occurrences "<value>" <world>` or read the file.

**Report the counts, then stop for approval on the split.** The expert will move things between
buckets. Let them. This is the highest-value minute in the round.

**Weigh the cost of a dispute.** A dispute you lose costs a round. If complying is cheap and does not
damage the world, comply, even when you are right. Save disputes for findings that would force you to
break a trap, leak an answer, or make the world worse.

## Gate 3: Sweep each finding to its class

**One flag is a sample, not the defect.** AutoQC does not list every instance in any single round.

For every finding still open, report a table:

1. The class in one line. "Raw HTML in Invoice_Q3.pdf" is an instance. "This corpus prints raw markup"
   is the class.
2. The sweep. `scan_world.py occurrences` for a named string, `pdf_markup_scan.py scan` for markup,
   `entity_conformer.py check` for roster drift, `leak_scan.py --spec` for answer leakage.

**Run the leak scan every round, not only when something grew.** Its strongest check needs no
language tell at all: it takes each task's answer from the spec and finds any file stating that value
which is not one of that task's primary artifacts. A world passed eight rounds and human review found
a task's answer sitting on a board-pack slide, a bare number in a bullet with nothing to pattern-match
on. That check would have named it in round 1.
3. **Both numbers. What AutoQC named, and what the class actually contains.**

The whole expanded set joins this round's batch, not next round's.

This is bounded work, not a hunt. You already know the exact string or pattern. Do not read the corpus
looking for new problems. That is `world-qc`'s job.

**Real case, Accounting 27:** a reviewer flagged one artifact for leaking an answer. The builder
checked the rest and found nine more.

## Gate 4: Run the mechanical fixers

These decide and apply a whole class in one pass, which is why they are safe to batch when a judgment
fix is not. **Dry run first, always. Show the change table, get a go, then write.** One script at a time.

```
python scripts/a_scrub.py          apply <spec> <world>
python scripts/entity_conformer.py apply <master> <world> --id-col <ID> --name-col <NAME>
python scripts/pdf_markup_scan.py  scan  <world>
```

On approval add `--write` to the first two. `pdf_markup_scan.py` only reports, because there is no safe
automatic fix for markup. Strip it by hand.

For a PDF value swap use `pdf_replace.py`. It redacts and reinserts at the same baseline, rejects a
replacement that would garble curly quotes, and always full-saves.

**Then clean metadata on everything touched, unconditionally:**

```
python scripts/metadata_hygiene.py clean <file1> --also <file2> <file3> --world <world> --date <in-world YYYY-MM-DD>
```

**Name the files you edited. Do not point this at the whole world.** Cleaning everything rewrites
metadata on every file, and one round of that put 31 unexplained changed files into the next diff and
buried the four real edits.

Editing a file is what creates a fresh tool fingerprint. Waiting for a scan to catch it is the wrong
order.

Anything the scripts set aside for review, hand over as a short list. They are lookalikes: real invoice
codes matching the A## pattern, names buried in prose, constant-fill columns. Do not force them.

**Stop for approval before writing.**

## Gate 5: Judgment fixes, one at a time

**Never "fix all".** A batched instruction produces batched unreviewed edits, and the wrong ones stay
invisible until a later round names them.

Gate 0 wrote each finding to its own numbered file under `_qc_backup/tickets/round<N>/`. **Work from
those files, not from the paste.** By the time you are fixing, the pasted findings are far back in the
conversation behind script output, and what you recall is a summary of a summary. Summaries drop
clauses, and AutoQC findings are usually several assertions in one paragraph, so a dropped clause is a
half-finished fix that comes back next round.

For each ticket, in order:

0. **Read the ticket file.** Quote the finding back in full, then list every separate thing it
   asserts, one line each. Three assertions means three lines. A fix that answers two of them is not
   done, and you check them off at the end.
1. **Say the mistake back in plain English.** If you cannot restate it without quoting AutoQC, you do
   not understand it and the fix will be wrong. The expert should be able to say "yes" or "no, you have
   misread it". That catch is worth more than any script here.
2. **Say what you will change**, which file, which value, from what to what.
3. **Show the diff.**
4. **Get a go.**
5. **Clean metadata on the file you touched.**
6. **Confirm every line from step 0 is addressed.** If one is not, the ticket is still open.
7. **Record the change**, one call per value:
   ```
   python scripts/log_edit.py <world> --file <path> --old "<old>" --new "<new>" --where "<cell>"
   ```
   The class fixers log themselves. Hand edits do not, and hand edits are the ones most likely to have
   knocked something over. An unrecorded edit is invisible to Gate 6.

**PDFs go through `pdf_replace.py`. Never hand-roll PyMuPDF.**

```
python scripts/pdf_replace.py <file.pdf> "<old text>" "<new text>" -o <file.pdf>
```

Add `--multiline` when the text you are replacing wraps across lines, which most paragraphs do.
Without it the tool refuses rather than writing the replacement once per line. After a multiline edit
it re-reads the page and aborts without saving if the old text survived or the new text was clipped.

It also deletes: pass an empty string as the replacement. Measured at about one second for 456
replacements across a 12-page document, so if a PDF edit is taking minutes you are doing it the slow
way. Extracting the text, writing custom PyMuPDF and iterating is the slow way.

**Then look at the page. Every time you edit a PDF.**

The tool checks that the words are on the page. It cannot see whether they overlap the paragraph
below, run off the right margin, sit in the wrong font, or leave a white gap where the old sentence
used to be. Only eyes catch that, and AutoQC has eyes.

Tell the expert to do this, in these words:

> 1. Open the world folder in File Explorer or Finder.
> 2. Find the PDF you just edited and **double click it**. It opens in your browser.
> 3. Go to the page that changed and look at the paragraph you edited.
> 4. Check four things: the new text reads as a sentence, nothing overlaps anything, nothing runs off
>    the edge of the page, and the font matches the text around it.
> 5. Tell me what you see.

If your browser is not the default for PDFs, right click the file, choose Open with, and pick Chrome
or Edge.

**Do not move on until they answer.** A reflowed paragraph looks fine to a text extractor and obviously
broken to a human, which is exactly the sort of finding that returns for three more rounds.

**Editing a workbook can clear its answers.** A spreadsheet stores each formula twice: the formula,
and the number last computed beside it. AutoQC reads the number. It does not calculate. Python's
`openpyxl` does not calculate either, and when it saves it blanks that number for **every formula in
the book**, not only the cells you touched. Excel recalculates on open, so the file looks perfect to
a human and reads as a page of empty cells to the grader.

**The toolkit handles this for you.** `a_scrub.py` and `entity_conformer.py` carry the numbers across
their own saves, and `metadata_hygiene.py` never touches cell values at all. Nothing in the normal
run creates this.

It only appears when **you** edit a workbook by hand in Python. So after any hand edit to an xlsx:

```
python scripts/verify_xlsx.py --scan <world>
```

Do not tell the expert to open workbooks to fix it. Re-saving in Excel works, but it stamps fresh
Excel metadata into the file and buys a metadata scrub you did not otherwise need. Fix it in the file:
write the new number into the cached value alongside the formula, using
`_common.save_xlsx_preserving_values(wb, path)` instead of `wb.save(path)` whenever your edit only
changes text.

If your edit changes a number that a formula reads, the old cached result is genuinely wrong. Compute
the new one and write it in. Do not carry the old one across.

When the fix replaces a synthetic-looking identifier (a sequential code, a 555 number, a patterned
invoice number), mint the replacement with `gen_realistic_values.py --avoid <existing values>` rather
than inventing one.

The five rules in the Reference section govern every edit here. They are not negotiable.

## Gate 6: Check what your own fix knocked over

```
python scripts/blast_radius.py all <world>
```

A corpus is a web of shared values. Changing one is never local. This is the step almost nobody does,
and it is the one that separates a build that converges from one that does not.

It reads every change made this round and every earlier round, then answers two questions:

- **Is a value you replaced still standing somewhere else?** If yes, Gate 3's sweep came up short and
  the list it prints is your fix list.
- **Did an edit break a total or a tie?** It re-foots every file edited in any round and lists every
  unedited file carrying a value that changed.

Say what the verdict means, in plain words. Do not paste it.

**Why this matters:** when your fix breaks a neighbouring value it comes back next round as a brand new
finding, in a different category, about a different file. It does not look like your fault, so nobody
traces it back. A domain lead named this as the direct cause of a 62-round world.

## Gate 7: Confirm the upload actually landed

**Write the revision note first. Two sentences, no more.**

RLS wants one sentence on what changed, plus one sentence per disputed finding. That is the entire
write-up for the round. Do not produce hand-off notes, per-round markdown files, or a summary
document. Nobody downstream reads them and they pile up in the expert's folder.

```
python scripts/round_log.py close <world> --round <N> --fixed <n> --disputed <n> \
    --changed "<one sentence: what you changed>" \
    --dispute "<one sentence: why you disputed it>"
python scripts/round_log.py summary <world>
```

`summary` prints the block to paste into RLS. If you disputed something and recorded no reason, it
says so rather than letting a blank dispute reach a reviewer.

**At least 8 of the 69 stuck worlds lost whole rounds to a fix that never reached the grader.** One
builder's own note reads "Forget to apply this version before the last AutoQC."

Walk them through this and wait for confirmation at each step:

1. Upload the revision.
2. **Apply this run's output to the task.** Uploading is not applying.
3. Wait at least 30 seconds.
4. **Open two files you edited in the left-hand pane and confirm they are the new versions.** Not the
   file list. Open them and look at the change.
5. Run AutoQC from the **coloured action buttons on the left**. Never the dark blue "run autoqc" button
   directly above the results.

If they are editing a folder that was already uploaded, tell them to stop. That is a versioning slip
and it silently loses work.

## Gate 8: The batch gate

**Do not upload a partial fix.** Uploading after three fixes when you had eleven costs a full round to
be told things you already knew.

First check the inventory did not drift in a way nobody intended:

```
python scripts/inventory_check.py check <spec.xlsx> <world> --round <N>
```

It reports **which files gained text** since last round. A replacement does not make a file longer, so
growth is added text and added text is how answers leak. Every grown file needs a reason. If any did
grow, run the leak scan before you upload:

```
python scripts/leak_scan.py <world> --spec <spec.xlsx>
```

It also reports whether **the local spec file has been edited**. It should not have been. If it has,
restore it from `<world>_qc_backup` and read rule 3 in the Reference section before going further.

**Read the APPEARED list first.** A file that appeared during remediation is a replace-not-add
violation until proven otherwise. If it was not added deliberately, remove it. A file in both APPEARED
and DISAPPEARED is usually one rename: confirm it was deliberate and that the spec's Location column
still points at the new name.

Then walk the full finding list. Every item must be in one of five states:

- Fixed
- Swept to its class and fixed
- Registered trap, left alone, reason recorded
- Not real, disputed with a written reason
- Blocked on a named person for a named decision

**"We will get it next round" is not a state.** If anything is in it, the round is not done.

Then close the round:

```
python scripts/round_log.py close <world> --round <N> --fixed N --expanded N --traps N --false N
```

It exits with an error if the numbers do not account for every finding. That is the gate working.

**Report in this shape and nothing longer:**

> Before you upload: **[N]** fixed, **[N]** widened to every file with the same problem, **[N]** left
> alone as your traps, **[N]** disputed with reasons written in the box. **[N]** waiting on [person].
> Nothing left in "next round". This is a full batch.
>
> Not checked, and AutoQC cannot check it either: whether the work is professionally correct. Open your
> own key file and read it as a domain expert before you submit.

Then two reminders:

- **Write a reason in every dispute box.** An empty thumbs down does not count. Three of the stuck
  worlds lost rounds to empty dispute boxes.
- **Do not blanket dispute.** Concede the real findings in writing. A blanket "all false" denial
  destroys the weight of the disputes that are right. A reviewer had to make a builder withdraw one for
  exactly that reason.

**Then run AutoQC and go straight into the next round.** New chat, same gates. There is no reason to
wait. The only rule is that the batch was genuinely full, not that a clock ran down.

---

# Part 2: When it will not close

## Gate 9: The same finding, third round

`round_log.py` prints CHRONIC when a defect class appears a third time.

**Stop fixing the files it names.** That is what produced round three. Something is regenerating the
class and the job is to find what. Nothing gets edited during this gate.

1. **Did the earlier sweeps finish?** `python scripts/blast_radius.py stale <world>`
   For every value ever replaced, is the old one still standing somewhere else? If yes that is the whole
   answer and the stale list is the fix list.

2. **Did a fix break a neighbour?** `python scripts/blast_radius.py touched <world>`

3. **Fix at the level of the value, not the file.** This is the shift, and it is what separates builders
   who get through a build from builders who do not.
   - Take the canonical value from the spec. Its Source artifact never moves.
   - List every artifact obligated to carry it, from Must match and Relates to, plus everything
     `blast_radius` found carrying it.
   - Bring that whole set into line in one pass, in one direction.
   - Re-foot every file in the set, because step three moved components.
   - `python scripts/spec_check.py ties <spec> <world>` to confirm the set agrees.

   One value, one sweep, one verification. A class fixed this way does not come back, because there is
   nothing left of it to come back.

4. **Check the class as a whole.** Every file mentioning the entity uses the master's name, title, ID
   and email pattern. Every total including a changed component still foots. Every date derived from a
   changed date still computes. Every filename embedding a changed value still matches. Every registered
   trap still stands.

5. **If none of that finds anything, escalate with specifics.** Not a shrug. The world lead needs the
   class name, the rounds it appeared in, confirmation that a blast-radius pass found no stale values
   and no broken footing, and the two questions only they can answer: is the corpus being regenerated
   over remediated files, and does the spec actually declare the value the findings keep disputing.

## Gate 10: Reviewer send-backs

- List every comment as a numbered worklist and confirm it with the expert before touching anything.
- Fix the specific items, then sweep each to its class as in Gate 3.
- Run Gate 6 before handing back.
- Hand back with a point by point note on what changed.

Reviewer comments carry weight. Work them. If one is wrong, raise it with the reviewer rather than
silently ignoring it.

---

# Reference

## The five rules that break worlds

### 1. Replace. Never add.

Overwrite the wrong value. Do not leave it and put the right one nearby.

**Banned as fixes:**

- A note saying which of two figures is correct.
- A "see also" pointing at the authoritative file.
- The superseded value left visible with the new one beside it.
- A "(corrected)" or "(updated)" parenthetical.
- **A new file added to satisfy a finding.** Even a harmless-looking one.
- Any sentence the in-world author would not have written.

Added text is the number one cause of answer leakage. The corpus starts explaining itself, the trap
defuses, and the task stops discriminating.

**The bridge note is the version of this that keeps getting through.** A finding says two figures do
not reconcile. The cheapest way to close it is one sentence explaining why they differ. Real case from
testing:

> "Added an explicit **bridge** to note 4 stating that the capex plan's $14.0M is gross D&A on FY2025
> additions while the AOP's $12.0M is the net increase over FY2024, and that the two are not additive."

That is three violations in one sentence. It added text instead of replacing. It hands the solver the
reconciliation they were supposed to derive. And if that pair is a registered trap, it just killed it.

**Banned by name:** a bridge, a reconciliation note, "for clarity", "to clarify", "the difference
represents", "these are not additive", "should not be combined". If you are about to write a sentence
whose job is to explain why two numbers differ, stop. Either one number is wrong and you replace it,
or the difference is the point and you leave it alone.

**The new-file case is worse than it sounds.** Accounting 09 added ambient files during remediation,
marked "no trap", tied to no task. They reopened judgment forks that were already closed, because every
new file is a new place for a number to drift.

**The single exception** is repairing a trap that has lost its single derivable answer, and even then
you add the smallest possible piece of in-world evidence: a timestamp, a signature block, an authority
line, a label distinguishing two things that looked identical. **The test is voice. If the in-world
author would not plausibly have written that sentence in that document, it is leakage, not evidence.**

### 2. Never write anything that gives away an answer

Answer leakage was present in 61% of the worlds that went past 20 rounds.

**Never write, and remove on sight:**

- A document stating the conclusion the task is supposed to derive.
- A worked example running the task's own numbers.
- A notes or summary section on a spreadsheet stating the finding.
- A filename that gives it away: `VALIDATED`, `FINAL`, `APPROVED`, `CORRECT`. A model preferentially
  opens those.
- Spec-author voice. Real documents do not annotate their own scope boundaries helpfully.
- Anything addressing the solver rather than the in-world reader.

**Leakage is not only imperative language.** One world found every earlier sweep had looked only for
words like "shall" and "must". The two defects that survived were plain declarative statements of fact.

**When you fix a leak, remove the give-away. Do not add a hedge.** Deleting the sentence is the fix.

### 3. When a finding points at the spec, work down this order

**Spec fixes are legitimate.** If a real tie-out defect got missed before file generation, the spec is
wrong and it should be fixed. What is not legitimate is reaching for the spec because it is less work
than fixing four files, which is the failure this order exists to prevent.

Work down. Stop at the first that applies.

**1. Can the files satisfy the finding? Then fix the files.** This is most findings and it is the
default. Before you go past this step you must say, in one line, why the files cannot satisfy it.
"Editing the spec is fewer edits" is not a reason.

**2. Is the finding about the spec as an object rather than the world's data? Dispute it.** The
workbook being visible, a tab name, a column heading, builder-only fields showing. None of that is a
world defect. Thumbs down with a written reason and move on.

**3. Is it a genuine tie-out defect, a number in the spec that does not reconcile? Then the spec is
wrong.** Say so plainly. But:

- **Never edit the local copy.** Studio holds the spec AutoQC reads. The file in the builder's folder
  is a download. The moment they disagree, every tie and trap check for the rest of the session is
  measured against a spec the grader does not have, and the findings stop making sense. This is a
  doom-loop generator and it is invisible while it happens.
- **Write it up instead.** The exact cell, the old value, the new value, the arithmetic proving the
  old one cannot be right, and every file that carries the value and will need to move with it.
- **An EPM uploads it.** The builder cannot, so editing the copy achieves nothing except the
  divergence above.
- **Re-run AutoQC only after the new spec is up.** Running before that burns a round.

`inventory_check.py` hashes the spec every run and reports if the local copy has been edited. If it
has, restore it from `<world>_qc_backup` before doing anything else.

### 4. The World Plan does not exist

There is no Plan document. It is gone. **Every AutoQC finding that references it, compares a file
against it, or raises a Plan-versus-Spec conflict is disputed on sight.** No judgment call, no
question to the expert, no investigation.

The Spec is the only planning document. If a finding says a file disagrees with the Plan, the finding
is measuring against something that is not there.

### 5. Never resolve a registered trap

A trap is a discrepancy the builder put in on purpose. It is what makes the world discriminating. A
consistency finding on a trap is AutoQC doing its job and being wrong about what to do.

- **Build the manifest before fixing anything.** `spec_check.py traps <spec>`. Rows marked `Type=Trap`
  are registered traps and the checks skip them automatically.
- **If a finding names a registered trap, dispute it.** Write the reason: this is a registered trap, the
  resolving evidence is in [file], actioning it would delete task [T#].
- **Never collapse two conflicting values into agreement** unless you have confirmed the conflict was
  accidental, meaning it appears nowhere in the manifest.
- **If the spec declares no traps at all, stop and say so.** Every round is a coin flip without it.
- **After fixing, re-run `spec_check.py traps` and confirm every trap still stands.**

Repairing a broken trap means restoring the single derivable answer, not deleting the discrepancy.

## Hard stops

Compliance blockers, not quality problems. They do not get disputed, weighed or traded off.

**No real personal data. Anywhere.** No live emails, phone numbers or addresses belonging to real
people. No real license, registration or credential numbers. Nothing shaped like a government issued
personal identifier, even invented. No live `.gov` or real consumer domains on an invented address.
This covers file metadata and embedded signature images, not just visible text. One world shipped a
real engineer's home address inside an anchor PDF.

**No copyrighted or proprietary content.** No paywalled standards, vendor templates or confidential
reports reproduced verbatim. If the spec requires one as a mounted file, that is a Gate 1 spec problem.

## What AutoQC actually does

Say these plainly when they come up. Most builders do not know them and they change behaviour.

- **One round is a sample, not the whole list.**
- **It samples deeper each run, so a rising finding count does not mean a worsening world.** One world
  measured this: 11 of 12 findings that looked new in version 15 were already present in version 13.
- **It reads more than your files.** The World Spec Document, anchor and reference documents, and
  builder-only task fields. Findings quoting those are scope errors. Dispute with a reason.
- **A finding can pass without any file change.** One anchor copyright finding failed seven runs in a
  row then passed with nothing edited. If a finding passed once before and came back with no edit in
  between, dispute rather than chase.
- **It cannot tell whether the work is professionally correct.** It checks structure, consistency and
  leakage. Only the expert can check the domain work.
- **Rerunning clears stale findings.** If results look wrong, rerun once before assuming a defect.

## Pre-upload checklist

- [ ] Every finding is fixed, swept and fixed, a registered trap, disputed with a written reason, or
      blocked on a named person.
- [ ] Every finding was swept to its class, and both numbers reported.
- [ ] Nothing was added. Every fix replaced something. No file was created this round.
- [ ] Every hand edit recorded with `log_edit.py`.
- [ ] Every registered trap still stands. `spec_check.py traps` re-run and confirmed.
- [ ] `blast_radius.py all` run and its verdict reported.
- [ ] `inventory_check.py check` run, and every file in the APPEARED list is there on purpose.
- [ ] Every file that GAINED TEXT has a reason. No bridge notes, no clarifications, no reconciliations.
- [ ] `leak_scan.py --spec` run this round, and every strong hit judged. Not just when something grew.
- [ ] Every PDF you edited was opened in a browser and eyeballed on the page that changed.
- [ ] `verify_xlsx.py --scan` run and clean, if you hand-edited any workbook.
- [ ] `metadata_hygiene.py sweep <world>` run and clean. Nothing named `_qc_backup` anywhere
      inside the world folder, at any depth.
- [ ] No build junk. No `.DS_Store`, no `__MACOSX`, no `.meta`.
- [ ] `metadata_hygiene.py clean` run on the files you edited, named individually, with `--world`.
- [ ] Every dispute box has a written reason in it.
- [ ] The revision was uploaded AND applied to the task.
- [ ] Two edited files opened in the left-hand pane and confirmed to be the new versions.
- [ ] The round is closed in `round_log.py`, with `--changed "<one sentence>"` and a
      `--dispute "<one sentence>"` for each finding you disputed.
- [ ] `round_log.py summary <world>` run, and its block pasted into the RLS revision note.
- [ ] The top level of their folder holds three things: the world, `.claude`, `qc_workspace`.

## Scripts

Call them as `python <TOOLKIT>/scripts/x.py`, where TOOLKIT is what you found at Gate 0. Each
prints `--help`, except `selftest.py`.

| Script | Gate | What it does |
|---|---|---|
| `setup_check.py` | 0 | Verifies the toolkit, environment, world and spec. Run first, no arguments. |
| `round_log.py` | 0, 8 | Logs each round, flags a class that came back, trips CHRONIC on the third, and carries **standing rulings** across rounds. `start` / `close` / `status` / `decide` / `rulings`. |
| `inventory_check.py` | 0, 8 | World against the spec's Artifacts registry, plus what appeared, disappeared or was renamed since last round. `check` / `drift`. |
| `spec_check.py` | 0, 9 | `traps` builds the trap manifest. `ties` confirms a canonical value is carried by its Must match artifacts. `refs` resolves A## IDs. |
| `scan_world.py` | 3 | `occurrences` finds every place a named string appears. The class-sweep workhorse. `tells` flags synthetic content markers. |
| `pdf_markup_scan.py` | 3, 4 | Finds raw Markdown or HTML printed as visible text. Reports only; no safe auto-fix. |
| `corpus.py` | all | Extracts every file's text once and caches it beside the world, keyed on mtime and size. Every scanner reads through it. `build` / `stats`. |
| `leak_scan.py` | 3, 8 | Candidate answer leakage: **a task's answer sitting in a file that is not that task's evidence**, a trap explained away, reconciling language, conclusion voice, filenames that announce themselves. Needs `--spec`. Reports only. |
| `a_scrub.py` | 4 | Scrubs leaked A## build codes to their real artifact names. Writes. |
| `entity_conformer.py` | 3, 4 | Conforms names and IDs to the spec's master. `check` / `apply`. Writes. |
| `pdf_replace.py` | 4, 5 | In-place PDF string swap, deletion via an empty replacement, and `--multiline` for text that wraps. Verifies after editing and aborts rather than clipping. About 1s. Guards against garbling, always full-saves. Writes. |
| `metadata_hygiene.py` | 4, 5 | Strips tool fingerprints, build dates, stray filenames, PDF revision residue. `clean <file> --also <files> --world <world>`. Name the files you edited, never the world. **Always pass `--world`**: without it, cleaning a file that sits in subfolders leaves a stray `_qc_backup` folder inside the delivered tree. `sweep <world>` lists and removes any that are already there. Writes. |
| `log_edit.py` | 5 | Records a hand edit so `blast_radius.py` can see it. Run after every judgment fix. |
| `gen_realistic_values.py` | 5 | Mints realistic replacement identifiers. Use `--avoid` to prevent collisions. |
| `blast_radius.py` | 6, 9 | What your own fixes knocked over. `stale` / `touched` / `all`. Read-only. |
| `reconcile_entities.py` | 6, 9 | `footing` re-foots a whole file, block aware. `entities` joins tables on shared IDs and reports field disagreements. |
| `verify_xlsx.py` | 5, 6 | `--scan <world>` finds formula cells that lost their stored number when Python saved the file, which AutoQC reads as empty. The bundled fixers already protect against this; run it after a HAND edit to a workbook. Without `--scan` it foots one explicit range to one total; use `reconcile_entities footing` first and reach for that only when it misses a non-contiguous block. |
| `selftest.py` | setup | Regression battery. No arguments. Must be all-PASS. |
| `_common.py` | n/a | Shared helpers. Not run directly. |

## Reference material

- `references/round-economics.md`: why rounds are lost, with the measured numbers.
- `references/error-taxonomy.md`: defect types A to G with fix recipes.
- `references/traps-and-facts.md`: spec precedence and the trap invariant.
- `references/file-formats.md`: per-format read, edit and verify, plus PDF-editing gotchas.
- `references/aqc-dimensions.md`: the AutoQC dimension list, so you know what is NOT your job. Do not
  walk it as a sweep.
- `assets/verification_bench.html`: offline viewer and findings checker. See `assets/README.md`.

## If you go on to App Data

Different pipeline, different skill, and one coming separately. Two things carry over and one does not:

- **The process carries over.** Triage into buckets, sweep a finding to its class, replace rather than
  add, the batch gate, the round log. All of it works the same on app findings.
- **The scripts do not.** Every fixer here is filesystem-only. Do not point them at app CSVs.
- **One extra hard rule:** never change the schema of the data, only the content values. Confirm the
  current wording of that with Spencer before relying on it.

## Guardrails

The expert is the domain authority. Do not invent real world facts, and look up anything that exists
outside the world. Correcting the world's own internal numbers is your job. Deciding whether an
accounting treatment or an engineering standard is right is theirs.

You fix files. You do not judge whether the world is good. Detection is AutoQC's job and finding new
defects is the `world-qc` skill's job.

**Never report the world as clean.** Report what you fixed, what you swept, what you verified, and what
you did not check. What you did not check: voice and tone, realism, paraphrased contradictions,
narrative depth, task viability, and anything app-data. Say so every time.
