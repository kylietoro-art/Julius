# Round economics: how a world takes 7 rounds instead of 20

This file is the *why* behind the five rules in SKILL.md. Read it once. Then apply the rules.

## The arithmetic

One AutoQC round is slow. Call it a day of wall-clock time between upload and usable report, plus the
builder's attention on both ends. The defects in a world do not vary anywhere near enough to explain a
7-round world and a 22-round world sitting side by side. What varies is **how many defects each round
actually retires.**

Two builders, same world, same 40 real defects:

| | Builder A | Builder B |
|---|---|---|
| AutoQC round 1 names | 12 findings | 12 findings |
| What they fix | the 12 named instances | the 12 findings' **classes**, 31 files |
| Checks the blast radius | no | yes, re-foots 6 totals |
| Uploads when | 5 fixed, "rest next round" | all 31 done |
| Round 2 names | 11, seven of them repeats | 6, no repeats |
| Rounds to close | 20+ | 6 to 8 |

Builder A is not lazy or slow. Builder A is doing exactly what the report literally says. That is the
trap. **The report is a sample of the defects, written as if it were the list of them.**

## Where the rounds actually go

Five leaks, in order of how much they cost.

### 1. Instance-level fixing (the big one)

AutoQC names two PDFs with leftover `<td>` tags. There are nine PDFs with leftover `<td>` tags.
Fixing two means the other seven come back, and not all at once either, because the next round samples
differently. One class of defect can generate five separate rounds this way.

**The fix:** for every finding, write down the class before you write down the fix. "Raw HTML in
Invoice_Q3.pdf" is an instance. "This corpus prints raw markup in rendered documents" is the class.
Then sweep for the class: `pdf_markup_scan.py scan <world>`, `scan_world.py occurrences <string>
<world>`, or the relevant class fixer.

Class expansion is bounded and cheap. You already know the string or the pattern, so you are not
reading the corpus looking for surprises. That distinction is what keeps this from turning into
detection, which is `world-qc`'s job and costs real tokens.

**Rule of thumb: if a finding names one file, assume the class has more. Prove it doesn't.**

### 2. Fixes that break their neighbours

This one is invisible, which is why it survives so long. A corpus is a web of shared values, so
changing one is never local:

- the number you changed is a component of a total in the same file, and now the total doesn't foot
- the same number is stated in three other files, and now the tie is broken the other way
- the person you renamed appears in a filename, an email address, a header and a signature block
- the date you corrected is the base for a tenure calculation two files over

Every one of those comes back in the next round as a **new** finding, in a different category, about a
different file. It does not look like a consequence of your own edit, so nobody treats it as one. Ten
rounds later the world looks cursed.

**The fix:** `blast_radius.py all <world>`, before Phase 5 of every round where you changed more than
a handful of values. It reads the change manifest, checks whether every value you replaced is still
standing somewhere else, re-foots every file you edited, and lists every unedited file that carries a
value you changed.

### 3. Premature upload

Fixing five of eleven and uploading burns a whole round to learn six things you already knew. There is
no partial credit in AutoQC. The report comes back with the six you skipped plus whatever it samples
fresh, and it reads like a new problem.

**The fix:** the batch gate. Every finding lands in one of four states before upload: fixed,
class-expanded-and-fixed, declared trap, or confirmed false. A fifth state exists but must be named
out loud, **blocked on a specific person for a specific decision.** "We'll get it next round" is not a
state.

### 4. Fixing things that were never wrong

AutoQC raises findings the file doesn't support. Editing a correct file to satisfy one introduces a
real defect, which surfaces in a later round as something new.

**The fix, partly:** paste the findings into the Verification Bench
(`assets/verification_bench.html`) before any editing. It checks two mechanical things per finding:
whether the string AutoQC quoted actually appears in the file it names, and whether a stated page
count is right. A quote that isn't there is strong grounds to challenge the finding before spending
anything on it.

**Know the limit.** The bench does not check footing claims, date claims or consistency claims, so it
clears only one bar. For the rest, the check is `scan_world.py occurrences` on the value in dispute,
or opening the file and reading it. Anything you rule out goes in the "false" bucket with the written
reason, and the reason goes in the revision comment so the next reviewer doesn't re-litigate it.

### 5. One-shot "fix everything" prompting

Handing the whole report over at once produces edits nobody reviewed, several of which are wrong in
ways that only surface as fresh findings two rounds later. It feels like it saves a round. It costs
three.

**The fix:** one ticket, one restatement, one diff, one go. The class fixers in Phase 1 are the
exception because they're deterministic and show their change table first, and even those get approved
one script at a time.

## The triage buckets

Every finding, on arrival, goes in exactly one:

| Bucket | What it means | Where it goes |
|---|---|---|
| **Mechanical class** | A Phase 1 script owns the whole class | Phase 1, dry run then `--write` |
| **One-off judgment** | Needs a human decision about the world | Phase 3, one at a time |
| **Declared trap** | It's in the trap manifest, on purpose | Nowhere. Record why, move on. |
| **False finding** | The file itself doesn't support it | Nowhere. Record the evidence, move on. |

De-dup first: one defect surfacing under three AQC dimensions is **one** ticket, not three. A## leakage
alone typically shows up under *No Broken Document References*, *In-World vs Out-Of-World Separation*
and *No Out-of-World or Build Artifacts* simultaneously.

## REPLACE, don't ADD, and why it's about answer leakage

The instinct when two documents disagree is to add a line that reconciles them. Do not.

Every sentence added to fix a defect is a sentence the in-world author never wrote, and it almost
always exists to explain something. Explanation is exactly what a solver is supposed to derive.
Add enough of it and the corpus solves its own tasks:

- adding "(figures per the signed contract are authoritative)" next to a discrepancy hands the agent
  the authority ordering it was supposed to work out
- leaving the wrong number visible with the right one beside it turns a single-answer task into a
  reading-comprehension exercise
- a "(corrected)" or "(see also)" parenthetical is a builder's voice in a solver's document, which is
  also a realism tell

**Overwrite the wrong value with the right one.** `pdf_replace.py` does exactly this for PDFs, and it
is the default for a value swap for that reason.

**The exception, stated precisely:** repairing a trap that has lost its single-derivable-answer
invariant does require adding in-world evidence, such as a timestamp, a signature block, an authority
line, or a label that distinguishes two things that looked identical. The test is voice. **If the
in-world author would not plausibly have written that sentence in that document, it is leakage, not
evidence.** See `traps-and-facts.md`.

## Cross-round memory

`round_log.py` records each round's findings and reports which **classes came back**.

A repeat class is a specific, actionable diagnosis, not a nuisance. It means the previous round fixed
instances, not the class. When one shows up, do not just fix the newly-named files. Go wide on that
class immediately and exhaustively, because it has already cost you at least one round and will cost
more.

**Third appearance is different.** At that point the class is not a sweep that came up short, it is a
class that is being regenerated by something you haven't identified. Fixing instances a third time is
guaranteed to buy a fourth round. Stop and run the structural pass.

## The structural pass, in one page

Full protocol is SKILL.md, Phase 2S. The shape of it:

**Stop editing.** Nothing gets changed during the pass.

**Ask whether the sweeps finished.** `blast_radius.py stale <world>`. For every value these scripts
have ever replaced, is the old value still standing somewhere else? If yes, that is the answer and the
stale list is the fix list.

**Ask whether your fixes broke their neighbours.** `blast_radius.py touched <world>`. Re-foots every
file edited in any round, and lists every unedited file carrying a value you changed. Both are things
your own remediation did.

**Then fix at the level of the value, not the file.** This is the actual shift, and it is what
separates builders who get through a build from builders who don't:

1. Take the canonical value from the spec. Its *Source artifact* is the side that never moves.
2. List every artifact obligated to carry it, from ② *Must match* and ④ *Relates to*, plus everything
   `blast_radius` found carrying it.
3. Bring the whole set into line in one pass, in one direction, toward the canonical value.
4. Re-foot every file in the set, because step 3 moved components.
5. `spec_check.py ties <spec> <world>` to confirm the set agrees.

One value, one sweep, one verification. A class fixed this way does not come back, because there is
nothing left of it to come back.

**Then check the class as a whole.** Entity names, titles, IDs, departments and email patterns against
the master. Every total that includes a changed component. Every date derived from a changed date.
Every filename that embeds a changed value. Every declared trap still standing with one derivable
answer.

**Escalate only with specifics.** If the pass finds nothing, the cause is upstream of the files you can
edit, and the world lead needs four things: the class name, the rounds it appeared in, confirmation
that a blast-radius pass found no stale values and no broken footing, and the two questions only they
can answer. Is the corpus being regenerated over remediated files, and does the spec actually declare
the value the findings keep disputing.

## A world already past 15 rounds

Do not just keep grinding. The loop has a cause. Work through these in order:

1. **Run `blast_radius.py all <world>`.** Most stuck worlds stop here, because the answer is stale
   values from earlier partial sweeps, or footing your own fixes broke.
2. **Read the round log for repeat classes.** `round_log.py status <world>`. Anything appearing three
   or more times gets the structural pass, exhaustively, before anything else is touched.
3. **Run the bench's "Check the spec".** A spec whose artifacts don't resolve to real files, where two
   artifacts claim the same file, where a canonical value is its own corroborator, or where tasks cite
   evidence that doesn't exist, will generate findings faster than anyone can clear them. That is a
   stop-and-escalate to the world lead with the failing rows attached, not something to fix file by
   file. Note this is a diagnostic here. Gate A spec review is the `world-spec-qc` skill's job.
4. **Check whether files are being regenerated.** If a file you fixed comes back broken, compare it to
   its copy in `_qc_backup`. If it reverted, someone is re-running generation over the remediated
   corpus. That is a process problem and it needs escalating, not remediating.
5. **Count the traps.** If the spec declares no traps and AutoQC keeps flagging discrepancies, the
   skill cannot tell an intentional divergence from an error, and every round is a coin flip. The
   spec's trap columns need populating before remediation can converge.
6. **Only then keep remediating.** With the five rules on, hard.

## What good looks like

- Round 1 and 2: the mechanical classes (A## leakage, entity drift, metadata tells, raw markup) go to
  zero corpus-wide, not file by file.
- Round 3 to 5: judgment tickets and tie and footing work, one at a time, batched, with a blast-radius
  check before each upload.
- Round 6 to 8: single-digit findings, no repeats, close.
- Every round: full batch, no "next round" items, coverage map written, log closed.
