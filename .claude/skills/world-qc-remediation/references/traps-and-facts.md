# Source of truth, grounding facts, and traps, the invariant behind every judgment call

## Source of truth: spec > any built artifact

Almost every non-mechanical remediation decision reduces to two questions: *which value is
canonical?* and *does this trap still resolve?* This file defines both precisely.

Canonical truth has a strict precedence order. When two things disagree, the higher one wins and the
lower one is what you fix:

1. **The spec** (top). Its **Canonical Values**, its **Artifacts registry** (the A## index), and its
   **declared-trap list** are the world's ground truth. A cited canonical value is immovable, when
   any artifact contradicts it, the *artifact* is wrong. In "LIGHT" worlds the Canonical Values tab
   may say it is "not a fact ledger"; it is still canonical for the values it *does* state, and the
   declared-trap list still decides which divergences are intended.
2. **Any built artifact** (bottom). Everything else, every document and spreadsheet in the corpus.
   When a conflict isn't settled by the spec, resolve by authority ordering (a signed
   contract/receipt outranks a draft/storefront listing; world-specific) or by internal derivation
   (components foot to their own total; a ledger sums to its own entries). If nothing resolves it,
   surface it to the builder, don't guess.

Legacy note: older Apex worlds cited grounding facts by code (`FT001`, `FT037`, `FT052`) in a fact
ledger. Treat any such code as a **spec Canonical Value**: same rule, same precedence. Newer AQC
worlds use the spec's Canonical Values + Artifacts registry instead of an FT ledger.

### The load-bearing rule

- **A canonical value is immovable.** When any artifact contradicts a spec value, the
  *artifact* is the defect. Fix the artifact to the canonical value; never edit the canonical value
  to match a stray artifact.
- **Consistency is corpus-wide.** A tasker can pull from any file, so an accidental drift in a file
  no current task reads is still a real defect. Do not scope consistency to "only the values a task
  touches", the target is complete internal consistency across the whole corpus, *except* for
  spec-declared traps.
- When a flag says the categories don't foot to a canonical total, the *categories* are the defect,
  re-foot the components to the total. Changing the canonical total would corrupt the ground truth the
  eval depends on.

## Traps

A **trap** is an intentional inconsistency, ambiguity, or lure placed so that a flawed agent takes the
bait and a competent one navigates it. Traps are what make the eval *discriminating*. A "declared
trap value" (e.g. `FT058`) is a value the designer deliberately put in tension with the truth.

### The invariant every valid trap must satisfy

> **Single derivable answer:** the task the trap bears on has **exactly one correct answer**, and that
> answer is **derivable from evidence present in the world**: via a rule, an authority ordering, a
> reconciling note, a timestamp, a distinguishing label, or similar.

If either half fails, it isn't a trap, it's noise that penalizes the agent for something it could not
have known. QC flags exist largely to catch traps that have lost this invariant.

The corollary that most remediations turn on: **repairing a broken trap means restoring the invariant,
not deleting the discrepancy.** Collapsing every conflict to a single agreed value would make the
world consistent but would also delete the evaluation signal the trap was there to provide. Only
collapse when the discrepancy was *accidental* (no trap intended). When a trap is intended, add the
missing disambiguator or restructure so one answer becomes derivable.

## Trap failure modes and how to repair each

### 1. Unresolvable (missing disambiguator)
Two conflicting values, no in-world way to tell which is right. *Repair:* add the smallest piece of
in-world evidence that makes the correct value derivable, a reconciliation note ("bundle includes
add-on gear beyond the base rate"), an explicit authority ("figures per the signed contract supersede
the draft"), a timestamp showing which is current, or a distinguishing label that reveals the two
values describe different things.

### 2. Wrong anchor (points at a wrong answer as if correct)
The trap's "correct" side is actually the wrong value, or the derivation leads to the lure. *Repair:*
re-point so the derivable answer is the true one; the lure must be the *dis*preferred branch, not the
one the evidence supports.

### 3. Colliding / opposite-direction traps
Two traps that a single heuristic can't jointly solve, e.g., discrepancy #1 makes the receipt higher
than the storefront and discrepancy #2 makes it lower, so neither "trust the receipt" nor "trust the
storefront" resolves both. This is the subtlest failure: each trap looks fine alone but together they
guarantee a wrong answer under any consistent rule. *Repair:* fix them **as a pair**. Options:
give each its own *distinct* in-world disambiguator (so the agent resolves each on evidence, not a
blanket heuristic), or restructure one so the values describe genuinely different things (base vs.
bundle SKU), removing the false symmetry. Never fix one in isolation and call the flag closed, verify
the *set* of related traps is jointly solvable.

### 4. Leaked answer (trap defused)
The world accidentally states the resolution outright, so there's no bait left (or, conversely, the
lure is so obviously fake no agent would take it). *Repair:* restore a realistic tension, remove the
give-away, or make the lure plausible again, while keeping one derivable answer.

## The intended-vs-accidental test

The single most important classification when a fix offers options:

- **Intended trap**: the flag cites a "declared trap value" / an FT trap code, or the world spec
  places a trap at this location. → **Preserve the trap.** Choose the option that leaves exactly one
  derivable answer (usually: add the minimal disambiguator or split into distinct entities). Do not
  collapse.
- **Accidental drift**: no trap referenced; this is just two artifacts that disagree because they
  were generated independently. → **Collapse it.** Align the non-canonical value to the canonical one
  so no ambiguity remains.

If you cannot determine which (no spec/ledger available), **do not guess silently.** Post both
options with the tradeoff in your world thread in **#julius-world-threads** (tag the world-building
team), and default to *preserving the declared trap by adding the smallest
in-world disambiguator*, because a QC that names a "declared trap value" implies the designer wanted
a trap there, and deleting it would remove an evaluation signal.

## Verifying a trap fix

State it explicitly in your remediation report:
1. **The single correct answer** to the task the trap bears on.
2. **The derivation path**: the exact in-world evidence and reasoning an agent follows to reach it.
3. **Joint consistency**: for colliding traps, confirm the whole related set resolves under
   evidence-based reasoning, not a heuristic that only works for one.

If you can't write (1) and (2) cleanly after your fix, the invariant isn't restored yet.

## Reading truth and traps from the spec (v4.x "All Apps")

The precedence above maps directly onto the spec tabs, so `spec_check.py` can enforce it mechanically:

- **Canonical value + its immovable source** = ② Canonical Values *Value* + *Source artifact (ID)*.
- **A declared tie** = ② *Must match (IDs)*, the artifacts obligated to carry that value. `ties`
  checks each; the *Source artifact* is the side that never moves.
- **The trap manifest** = ④ *Trap Content* + ③ *Trap: What Misleads / How Agent Fails / Remediation
  Path* + ② *Note*. Any value or artifact named here is an **intended** divergence; `ties` auto-skips
  trap-bearing artifacts, so the guard is enforced, not remembered.
- **Referential integrity** = ④ IDs / *Relates to* + REF · Schema Library *Depends on* / *Lookup key*.

The intended-vs-accidental test becomes concrete: **in the manifest → intended (preserve); breaks a
② tie and not in the manifest → accidental (fix toward the Source artifact); neither → surface, do
not collapse.** If the spec declares no traps, the skill cannot distinguish trap from error, stop
and have the builder populate the trap columns first.
