# Error Taxonomy, diagnosis, decision rules, fix recipes

Read the section that matches your flag before applying the fix. Each type gives the **signature**
(how to recognize it), the **diagnosis** (what actually went wrong), **decision rules** (the
non-obvious calls), the **fix recipe**, and a **worked example** taken from a real Apex QC flag.

Contents:
- [A. Placeholder / synthetic tell](#a-placeholder--synthetic-tell)
- [B. Footing / internal arithmetic](#b-footing--internal-arithmetic)
- [C. Cross-artifact conflict (no disambiguator)](#c-cross-artifact-conflict-no-disambiguator)
- [D. Trap integrity](#d-trap-integrity)
- [E. Temporal / logical](#e-temporal--logical)
- [F. Realism / plausibility](#f-realism--plausibility)
- [G. Out-of-world / build-artifact leakage (systemic)](#g-out-of-world--build-artifact-leakage-systemic)

---

## A. Placeholder / synthetic tell

**Signature.** A value that a real system would randomize or vary is instead patterned or generic:
sequential alphabets/digits (`ABCD12`, `123456`, `AAA111`), `Lorem ipsum`, obvious names (`John
Doe`, `Jane Smith`, `Test User`, `Acme`), reserved-for-fiction numbers (`555-01xx` phones,
`example.com`, `test@test.com`), suspiciously round money everywhere, the *same* value repeated
where variety is natural (identical timestamps across many records, identical amounts), placeholder
literals (`TODO`, `FIXME`, `XXX`, `PLACEHOLDER`, `TBD`), or tool-signature metadata (PDF
Producer/Creator = `reportlab`, author = `python-docx`, default template names).

**Diagnosis.** The generator emitted filler where it should have emitted a realistic instance. The
file otherwise reads as genuine, so the placeholder is the one thread that unravels it, an agent
(or a human reviewer) can spot the synthetic origin and the eval is compromised.

**Decision rules.**
- Replace with something **realistic for that field's real-world format**, not just "less
  sequential." Know the format: an airline record locator (PNR) is 6 uppercase alphanumerics,
  randomized, usually avoiding easily-confused `0/O/1/I`: see `gen_realistic_values.py`. An order
  number, invoice number, and confirmation code each have their own shape.
- The replacement must be **collision-free**: it must not accidentally equal a real fact/trap value
  elsewhere in the world. Check your candidate with `scan_world.py occurrences <candidate>`.
- If the same placeholder legitimately appears in several places for the *same entity* (one
  booking's PNR on every page + filename + a confirmation email), replace it with the **same** new
  value everywhere so the entity stays internally consistent. If it's lazy reuse across *different*
  entities (every order shares one ID), give each entity its **own** distinct value.

**Fix recipe.**
1. `scan_world.py occurrences <placeholder> <world_dir>` → enumerate every location, incl.
   filenames, metadata, and inside binary artifacts.
2. Generate the realistic replacement(s) with `gen_realistic_values.py`, `--avoid`-ing existing
   values.
3. Edit each location with the right tool (text edit for CSV/EML/etc.; `openpyxl`/`python-docx` for
   office files; `pdf_replace.py` or regenerate for PDFs).
4. Rename the file if the value is in the filename, and update every cross-file mention of the old
   filename.
5. Verify: re-scan for the old value (expect zero hits) and for the new value (expect exactly the
   intended count), and confirm no tool-signature metadata remains if that was part of the flag.

**Worked example (real flag).**
> `rtw_sky_alliance_booking_pnr_abcd12.pdf` uses `ABCD12` as its PNR on every page and in the
> filename. A sequential-alphabet string is obvious placeholder filler; real record locators are
> randomized six-character alphanumerics. Fix by replacing `ABCD12` with a realistic randomized
> locator (e.g. `X7KQ2M`) everywhere it appears, including the filename.

Remediation: `gen_realistic_values.py --type pnr --n 1 --avoid ABCD12` → say `H4T9RM`. Replace on
every PDF page (via source regen if the generator exists, else
`pdf_replace.py input.pdf "ABCD12" "H4T9RM" -o output.pdf`),
in PDF metadata if present, rename the file to `rtw_sky_alliance_booking_pnr_h4t9rm.pdf`, and update
any email/manifest that references the old filename or PNR. Verify zero `ABCD12` hits world-wide and
that the new locator reads as genuine. **Do not** reuse the QC's example `X7KQ2M` verbatim, it may
appear in another world.

---

## B. Footing / internal arithmetic

**Signature.** Component rows don't sum to a stated total; a "total" or "grand total" row disagrees
with its own inputs; category subtotals don't add up to a hardcoded total; narrative notes assert a
figure the cells contradict. Very common in generated budget/finance spreadsheets where rows were
appended after the totals were written.

**Diagnosis.** A hardcoded total was never updated after inputs changed (e.g., two countries
appended to a sheet built for twenty), or subtotals were generated independently of their stated
total. The file claims a number its own data disproves, fatal when the sheet is designated the
"locked baseline" / source of truth.

**Decision rules, which side moves?**
- If the **total is a cited grounding fact** (e.g., `Personal Total = 5600` is FT052), the
  categories are wrong: re-foot the **components** to the total. Never change the canonical total.
- If the **components are the truth** (the per-row allocations are the real inputs and the total is
  just stale), re-foot the **total/grand-total** rows to the true sum.
- Watch for **downstream implications** the flag calls out: if re-footing reveals the real
  per-person figure blows a stated budget cap (e.g., allocations actually total $54,200 vs. each
  traveler's $50,000 cap, FT001), decide whether the *intent* was (a) an honest total that happens
  to exceed the cap, then just re-foot and let the overage stand as real, or (b) staying within
  the pool, then rebalance the per-country rows back down to the pool. The flag's phrasing usually
  signals which; when unclear, prefer re-footing to the true sum and surface the cap tension in your
  world thread in **#julius-world-threads** (tag the world-building team).
- Fix **every** dependent cell and note the flag names: total row, grand-total row, per-person
  column, and any narrative cells ("Days sum to 369", a mislabeled longest-stay), a footing fix
  that leaves a contradicting note is incomplete.

**Fix recipe.**
1. Dump the sheet (`extract-text file.xlsx` or `openpyxl`) and reproduce the arithmetic yourself so
   you know the true sums before editing.
2. Decide the canonical side (above).
3. Edit with `openpyxl`, **matching the sheet's convention**: if surrounding totals are hardcoded
   numbers, write the corrected number; if they're `=SUM()` formulas, write a formula and recalc per
   the `xlsx` skill. Update every dependent cell and narrative note.
4. `verify_xlsx.py <file.xlsx> --sheet "<name>" --range <range> --total <cell>` to confirm the total now equals
   the component sum, delta = 0.
5. Re-read to confirm notes and secondary totals (grand total, per-person) all reconcile.

**Worked example (real flag).**
> In `wanderlust_master_budget_v1.xlsx` the 'Per-Country Allocation' sheet lists 22 countries summing
> to $108,400 / 393 days, yet 'Total (allocated)' reads E27=$100,000 / C27=369 / F27=$50,000 and
> 'Grand total' reads E29=$100,000 / C29=373. England (#21) and Netherlands (#22) were appended
> without updating totals; notes A32 ('Days sum to 369') and A35 (India mislabeled longest stay)
> compound it. It's the locked baseline. Fix: update E27/C27/F27 and E29/C29 to $108,400 / 393 /
> $54,200 and $108,400 / 397, and correct A32/A35.

Remediation: components are canonical (they're the real per-country inputs), so re-foot the totals.
Set E27=108400, C27=393, F27=54200, E29=108400, C29=397 (matching the hardcoded style of the sheet),
fix A32 to "Days sum to 393" and A35 to the actual longest-stay country. If a companion flag notes
the per-person $54,200 exceeds the $50,000 cap (FT001) and the design intends the pool to hold,
instead rebalance the 22 rows down to $100,000/$50,000, but only if that's the stated intent;
otherwise the honest total stands. `verify_xlsx.py` to confirm E27 == SUM(country rows), then re-read
A32/A35.

---

## C. Cross-artifact conflict (no disambiguator)

**Signature.** The same real-world fact carries two different values in two files, and **nothing in
the world tells the agent which is right.** E.g., a rate appears as $899/pp in one email and $999/pp
in a storefront CSV for the same experience, with no note reconciling them.

**Diagnosis.** Independent generation of related artifacts drifted. Unlike a footing error (internal
to one file), this spans files, and unlike a *valid* trap, there's no in-world path to the truth, so
it silently points the agent at a wrong answer it couldn't have ruled out.

**Decision rules.** This is often really a **trap** flag in disguise, see
[D. Trap integrity](#d-trap-integrity) and `references/traps-and-facts.md`. The core call:
- **Accidental drift, no trap intended** → collapse it: pick the canonical value (prefer a cited FT
  value; else the more authoritative artifact, a receipt/confirmation usually outranks a storefront
  listing, but this is world-specific) and align the other file to it.
- **Intended trap** (the flag cites a "declared trap value") → do **not** collapse; instead give the
  agent a way to resolve it. Either add a minimal in-world reconciliation note, or restructure so the
  two values are legitimately about *different* things (base experience vs. upsell bundle → two
  distinct SKUs), leaving exactly one correct answer to the task's actual question.
- Beware **interacting traps**: if aligning this conflict would break the resolution logic of a
  *different* trap (e.g., two rate discrepancies that run opposite directions so no single
  "trust-the-receipt" heuristic solves both), you must fix them **together**: see the worked example.

**Fix recipe.**
1. `scan_world.py occurrences <value> <world_dir>` to find both (all) carriers of the fact and any
   related traps.
2. Determine intended-vs-accidental from the flag's language and the world spec/ledger.
3. Apply the alignment or the disambiguator, minimally.
4. Verify by stating the single correct answer and the derivation path an agent follows to reach it.

**Worked example (real flag).**
> The canonical heli-hike rate (FT037 = $899/pp → $1,798) appears only in Sara's confirmation email
> (gear 'included in the per-person rate'), while the declared trap value (FT058 = $999 → $1,998) is
> carried by products.csv order 2129 as a 'heli+gear' bundle, the same experience. No artifact
> reconciles the $100/pp difference, and it runs OPPOSITE to FT057 (there the email was higher), so
> no single 'trust the receipt / trust the storefront' heuristic resolves both. Fix: align the order
> to $899 (making the $999 bundle a distinct/optional catalog SKU) or add a reconciliation note
> distinguishing the base experience from the upsell bundle.

Remediation: FT058 is a *declared trap*, so preserve resolvability rather than deleting the tension.
Because FT057 runs the opposite direction, a heuristic-based agent can't win both, so make the two
about different things: turn order 2129's $999 line into a genuinely distinct **"heli+gear bundle"
SKU** (an upsell that legitimately costs $100 more) while the base FT037 heli-hike stays $899 with
gear included. Now the storefront and the receipt aren't in conflict; they describe two products, and
the task's question about the *base experience* resolves cleanly to $899. Alternatively, add a one-line
in-world note (invoice memo or product description) stating the bundle includes add-on gear beyond the
base rate. Verify: the agent can derive $899 for the base experience from Sara's confirmation, and the
$999 SKU no longer contradicts it. Coordinate with the FT057 fix so the pair is jointly consistent.

---

## D. Trap integrity

**Signature.** The flag references a **declared trap** and says it is unresolvable, points to a wrong
answer with no derivation, "has no in-world disambiguator," or that two traps interact so "no single
heuristic resolves both."

**Diagnosis.** A trap must satisfy an invariant: **exactly one correct answer, and that answer is
derivable from in-world evidence.** The generation broke it, either the evidence that would
disambiguate is missing, or another trap's logic collides with this one.

This type has its own dedicated treatment. **Read `references/traps-and-facts.md`** for the invariant,
the failure modes (unresolvable, wrong-anchor, colliding/opposite-direction, leaked-answer), and the
repair pattern for each. The fix always *restores the single-derivable-answer invariant*, it never
just removes the discrepancy (that deletes the eval signal). If a trap looks unsalvageable, remediate
to the best consistent state and flag it in your world thread in **#julius-world-threads** (tag the
world-building team) rather than quietly neutralizing it.

---

## E. Temporal / logical

**Signature.** Dates and times that don't cohere: an email that says "thanks for making the time
yesterday" but is dated the same day as the meeting; a timezone that contradicts where the person is
established to be; events out of chronological order; a follow-up timestamped before the thing it
follows.

**Diagnosis.** Generated dates/timezones weren't reconciled against the world's established timeline
and geography (itinerary, other emails, calendar). Individually minor, collectively a clear tell and
sometimes a solvability problem if a task depends on the sequence.

**Decision rules.**
- Anchor to the **established timeline**: whatever the itinerary, calendar, and prior thread fix as
  ground truth wins; move the off artifact to agree.
- Timezones must match the person's **established location on that date** (if the itinerary places
  Katie in Tokyo/Kyoto on Jan 20, her calls are GMT+9, not GMT+7).
- "Yesterday"/"tomorrow"/"last week" language must be consistent with the two dates involved, fix
  whichever is wrong (usually the date, occasionally the wording).
- Keep edits minimal and preserve the email/file's other headers and structure exactly.

**Fix recipe.**
1. Build the correct local timeline from the anchoring artifacts.
2. Identify the off value (date header, body reference, timezone).
3. Edit in place (for `.eml`, fix the `Date:` header *and* any body reference; preserve MIME/other
   headers).
4. Verify the artifact now agrees with the anchor and that relative-time language reads correctly.

**Worked example (real flag).**
> `email_marrowbone_postmeeting_followup.eml` is dated Tue, 20 Jan 2026 and says "Thanks for making
> the time yesterday," but the call was confirmed for Tuesday, January 20th, so the follow-up should
> be Jan 21, not the same day. It also says Katie dialed "from GMT+7" while the itinerary places her
> in Tokyo/Kyoto (GMT+9) on Jan 20. Fix: re-date the follow-up to 2026-01-21 and change GMT+7 to
> GMT+9.

Remediation: set the `.eml` `Date:` header to Wed, 21 Jan 2026 (keep a plausible clock time and the
correct offset), and change the body's "GMT+7" to "GMT+9". Leave every other header and the body text
untouched. Verify: "yesterday" now correctly points at the Jan 20 call, and the timezone matches the
itinerary's Jan 20 Kyoto location.

---

## F. Realism / plausibility

**Signature.** No single wrong value, but the artifact doesn't read like a real instance of its type:
an "airline confirmation" missing fields a real one always has, an invoice with an implausible layout,
prose in the wrong register, a CSV whose schema no real storefront export would use, uniform data with
no natural variation.

**Diagnosis.** The generator produced something structurally or tonally off for the artifact class.
Fidelity leak: a knowledgeable agent recognizes it isn't authentic.

**Decision rules.**
- Model the fix on a **real example of that artifact class**: what fields, sections, tone, and
  formatting does a genuine one have? Add/adjust to match.
- Change **only** what realism requires; do not disturb any fact or trap value. If adding a field
  requires a value, make it realistic *and* consistent with existing facts (don't invent a figure
  that contradicts the ledger).
- Introduce natural variation where uniformity is the tell (varied timestamps, amounts, phrasing),
  but never at the cost of a designed pattern a trap relies on.

**Fix recipe.**
1. Identify the specific unrealistic aspect from the flag.
2. Determine what a genuine artifact of that type looks like.
3. Edit to match, preserving all facts/traps and the existing conventions.
4. Verify against the "would a domain expert believe this is real?" bar, and re-scan for tells.

**Worked example (pattern).** A flag notes a booking confirmation lacks a fare-basis/ticket-number
block and carrier record that real e-tickets always include, making it read as synthetic. Remediation:
add the missing standard fields with realistic, internally-consistent values (a randomized ticket
number via `gen_realistic_values.py`, a fare basis consistent with the itinerary), matching the
formatting of the rest of the document, without altering the PNR, dates, or prices the ledger pins.

---

## G. Out-of-world / build-artifact leakage (systemic)

**Signature.** Builder-only codes or scaffolding surface in solver-visible content. The dominant case
is the spec's **A## artifact-registry IDs** leaking as cross-references inside world files,
`"CPO of record, see A27 for cert status"`, `"Crowd-manager assignment per A06 ratio policy"`,
`"Occupant loads mirror A26 verbatim"`, `"Authority: Reorganization Announcement A41"`. The A## codes
are the builder's index into the spec's Artifacts tab; they have **no in-world existence** and no
reader can resolve them, so they are pure out-of-world residue. (Also in this family: tool-signature
metadata like `/Producer=reportlab`, `author=python-docx`, and leftover build scaffolding.) AQC
reports this across several dimensions at once, No Broken Document References, In-World vs
Out-Of-World Separation, and No Out-of-World or Build Artifacts, so **de-dup it to one ticket** first
(Phase 0).

**Diagnosis.** The generator wrote the builder's cross-reference index into agent-visible prose
instead of the real in-world artifact name. Fidelity leak: a reader (or agent) sees a code that maps
to nothing in the world.

**This is the canonical systemic ticket** (Phase 1, CLEAN). Detection is systemic, one sweep finds every
occurrence, but the *replacement differs per code*, since each A## resolves to a different real
artifact. So the rule is: **one sweep + one consistent resolution rule + per-occurrence output**, not
one blind find-and-replace.

**Decision rules.**
- **Resolution rule (house standard): replace each `A##` with the human-readable name of the artifact
  it maps to in the spec's Artifacts tab.** `A27` → "the Safety Certification by Role Matrix"; `A06`
  → "the occupant-load / crowd-manager policy". Keep the surrounding sentence and any descriptive text
  intact, you are swapping the code for the name it should have had, not deleting the reference.
- **Only touch codes that resolve to the registry range** the spec defines (e.g. A01, A45). A string
  that merely *looks* like the pattern but is **not** in the registry, a real invoice line, a room or
  part code, a legitimate document number, is a potential **false positive**: do **not** auto-change
  it. Put it on a `REVIEW` list for the builder instead.
- **Be consistent across the whole corpus.** Do not strip some codes and rename others, mixed
  handling is itself a realism tell. One rule, applied everywhere.
- If a code has no entry in the Artifacts tab at all, it can't be resolved to a real artifact: flag it
  on the `REVIEW` list rather than inventing a referent.

**Fix recipe.**
1. Enumerate every occurrence across the corpus:
   `scan_world.py occurrences` for each registry code, or a pattern sweep for `A\d\d`: capture file
   + location for each hit.
2. Build a resolution map from the spec's Artifacts tab: `A## → real artifact name`.
3. For each hit: if the code is in the registry range **and** has an Artifacts-tab entry → replace
   with the mapped name, preserving surrounding text and the file's format (openpyxl/python-docx/text
   edit; `pdf_replace.py` or regenerate for PDFs). If not → add to the `REVIEW` list, unchanged.
4. Emit a **change manifest**: one row per change: `file | location | old code | → | new text`, plus
   a separate `REVIEW` block of pattern-matches left untouched. The builder skim-reads this to confirm
   nothing legitimate (an invoice, a real doc code) was rewritten and nothing real was missed.
5. Verify: `scan_world.py occurrences` for each raw code → expect **zero** solver-visible hits;
   `scan_world.py tells` → no tool-signature metadata remaining; spot-read a few edited sentences to
   confirm they read naturally.

**Worked example (real flag).**
> ~13 solver-reachable HR-world files cite policies/artifacts by the spec's internal A## IDs,
> `HRIS_Data_Dictionary_ID_Crosswalk.xlsx` says "System-of-record per Policy A09",
> `Zone_Staffing_Demand_Forecast.xlsx` says occupant loads "mirror A26 verbatim",
> `Current_Org_Chart_PostReorg.pdf` cites "Reorganization Announcement A41" and "Buyout close (A40)".
> These map onto the spec's Artifacts catalog (A09=System-of-Record Policy, A26=Occupant Load Plan,
> A40/A41=buyout/reorg) and have no in-world existence.

Remediation: one systemic sweep. Build the map from the Artifacts tab (A09 → "the System-of-Record
Policy", A26 → "the Zone Staffing Occupant Load Plan", A40 → "the buyout close notice", A41 → "the
Reorganization Announcement", etc.). Replace each in place, "System-of-record per Policy A09" → "per
the System-of-Record Policy"; "mirror A26 verbatim" → "mirror the Occupant Load Plan verbatim";
"Reorganization Announcement A41" → "the Reorganization Announcement". Leave column-D formula
references (`=D5`) and any real document numbers alone, those are the false positives that land on
the REVIEW list. Emit the change manifest, then confirm zero raw `A##` hits remain in solver-visible
text.
