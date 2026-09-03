# AQC dimension checklist (Phase 4 pre-upload reference)

**Reference only, this is what AutoQC (AQC) checks, so you know what is NOT your job to detect.**
Detection is AQC's job; this skill fixes flags AQC (or a human) already raised. **Do not walk this
list as a sweep** over the corpus, that would be a full detection pass, which this skill must not do.
Use it during the **Phase 4 pre-upload reference** step only to understand which dimension a given flag
belongs to and to sanity-check that a fix you already made didn't obviously regress a neighboring
dimension.

> **Provenance.** Derived verbatim from the latest HR-world AQC run. AQC's category set evolves and
> some dimensions are world-type-specific (e.g. *U.S. Regional Requirements*). If AQC's categories
> change, update this file, it is the single place the check is defined. `[P0]` = binary/blocking,
> `[P1]` = graded.

This is a **debug pass to reduce RLS AQC rounds, not a replacement for AQC.** It only sees what these
categories (plus `reconcile_entities.py`) look for; prose-level drift no dimension checks can still
slip through.

## World Foundations
- `[P0] Supports Independent Tasks`: world is broad/deep enough for many independent tasks, not one repeated template.
- `[P0] Evidence Surface Completeness And Format Diversity`: rich, format-diverse artifacts; every scenario domain has supporting files; all cited primary artifacts present.
- `[P0] Built Files Match Spec Inventory`: the spec's Artifacts registry reconciles exactly to the built files; no phantoms, formats match, state markers agree.

## World Realism
- `[P1] No Synthetic Markers Template Residue Or Placeholder Data`: no placeholder/template residue, TODO/scaffolding, AI disclaimers, or generic filler in rendered content.
- `[P1] Voice Tone And Formatting Match Authors And Document Types`: realistic variation by author/function/doc-type, not one flattened machine style.
- `[P1] Document Authenticity Texture And Markings`: domain-appropriate letterhead, permit/form numbers, watermarks, version stamps, signature blocks.
- `[P1] Traceability And Cohesion`: one coherent reconstructable scenario; systems share a consistent spine; load-bearing numbers reconcile; seeded divergences are intended.
- `[P1] Solver Navigation And Traceability`: discoverable via realistic folders, self-describing names, consistent IDs, crosswalks; navigable without blind search.
- `[P1] Visual / Non-Text Data Has Text Companion`: every content-bearing visual has extractable text; no uncaptioned content-bearing images.

## Cross-Artifact Consistency
- `[P0] Personnel Names Titles Roles And Identifiers Are Consistent`: same person carries the same name/title/role/dept/ID across all systems and files (except spec-declared traps).
- `[P0] Numerical Values Constraints And Structured Data Are Consistent`: structured calculations agree; totals foot; constraints hold across files.
- `[P1] No Broken Document References`: every referenced document resolves; no unresolvable cross-references (incl. leaked A## codes).
- `[P1] Calculation & Fixture Accuracy`: computed figures agree with their inputs; totals foot to line items; no stale-base derivations.
- `[P1] Domain Reconciliation Ties`: domain reconciliations compute correctly (e.g. leave balance = allocation − approved leave) across the ledger, exhaustively.
- `[P1] Timeline And Dates Are Coherent`: all dates/timing fit one coherent timeline; recomputed tenure/age/expiry math checks out.
- `[P1] World Temporal Anchoring`: every agent-reachable file's own date is at/before the spec anchor; later dates are legitimate forward references.
- `[P1] Document Chronology Is Causally Consistent`: no post-event knowledge appears early; past events completed, future events prospective.
- `[P1] Consistent Naming And Defined Terms`: entities and defined terms named consistently across all files.

## Leakage And Separation
- `[P1] In-World vs Out-Of-World Separation And Metadata Cleanliness`: no builder/spec residue in worker-visible content; hidden/metadata channels clean.
- `[P0] No Out-of-World or Build Artifacts`: no spec artifact-index IDs (A##), build scaffolding, or tool signatures in solver-reachable files. **(Primary home of the A## leakage ticket, see error-taxonomy Type G.)**
- `[P0] No Solution Or Reasoning Leakage`: no answer-key language, "correct answer"/"trap"/task-ID tags, or reasoning chains in worker files.
- `[P1] No Environment / Filesystem Leakage`: no grading scripts, answer keys, hidden/dot files, caches, logs, or env files in the built FS.
- `[P1] No Signposting of Load-Bearing Facts`: formatting/naming/ordering doesn't telegraph answers; answer-bearing cells not singled out.

## Factual Integrity
- `[P1] Trap Presence in Built Files`: traps are present as designed (or a NEUTRAL "no ledger" world, per spec).
- `[P1] No Synthetic Substitutes For Real-World Facts`: real-world references are plausible and correctly attributed, not fabricated substitutes.
- `[P1] External Citations Resolve To Real Content`: high-value external citations resolve to real statutes/standards and match the claims.
- `[P0] U.S. Regional Requirements`: jurisdictional/institutional/standards references accurate and internally consistent (world-type-specific).
- `[P1] No Real PII or Copyrighted Material`: no real individuals' private data; reserved fictional phone/email/SSN patterns; no reproduced copyrighted content as in-world material.
- `[P1] Intended Traps Are Fair`: every deliberate trap is planted, paired with an authoritative counterpart + governing policy, and resolvable to one answer.

## Aggregate Risk And Coverage
- `[P0] File Integrity Defect Rate`: no structurally broken, empty, corrupted, or unusable files; everything parses/renders.
- `[P0] Coherence Flag Ratio`: confirmed cross-file inconsistencies effectively absent; every divergence is a registered trap or explicitly reconciled.
- `[P0] Realism Flag Ratio`: no confirmed realism failures after a marker scan + representative rendering.
- `[P0] Anomaly Detection Catch-All`: no material anomaly outside the named dimensions (do not double-count issues already owned by another dimension).
