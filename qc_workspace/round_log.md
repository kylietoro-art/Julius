# AutoQC round log

World: `/home/user/Julius/filesystem`

One row per round. `Repeats` are defect classes that already appeared in an earlier round,
each one means that class was fixed at the instance level, not the class level.

| Round | Opened | Findings | Classes | Repeats | Disposition |
|---|---|---|---|---|---|
| 1 | 2026-09-03T19:17 | 14 | 8 | 0 | fixed 6, widened 4, traps 1, false 3, blocked 0 |
| 2 | 2026-09-10T16:12 | 6 | 4 | 3 | fixed 5, widened 0, traps 1, false 0, blocked 0 |
| 3 | 2026-09-10T17:13 | 6 | 3 | 3 | fixed 5, widened 0, traps 1, false 0, blocked 0 |
| 4 | 2026-09-10T18:02 | 7 | 5 | 5 | fixed 5, widened 0, traps 1, false 1, blocked 0 |
| 5 | 2026-09-10T19:32 | 5 | 3 | 2 | fixed 4, widened 0, traps 0, false 1, blocked 0 |
| 6 | 2026-09-10T21:34 | 7 | 4 | 4 | fixed 7, widened 0, traps 0, false 0, blocked 0 |
| 7 | 2026-09-10T22:07 | 10 | 7 | 6 | fixed 9, widened 2, traps 1, false 0, blocked 0 |
| 8 | 2026-09-11T15:46 | 6 | 4 | 4 | fixed 6, widened 0, traps 0, false 0, blocked 0 |
| 9 | 2026-09-11T16:27 | 6 | 5 | 4 | fixed 5, widened 1, traps 0, false 1, blocked 0 |
| 10 | 2026-09-11T17:04 | 8 | 5 | 5 | fixed 3, widened 0, traps 0, false 2, blocked 3 |
| 11 | 2026-09-11T17:58 | 6 | 5 | 5 | _open_ |
| 12 | 2026-09-11T19:50 | 7 | 4 | 4 | fixed 2, widened 0, traps 0, false 1, blocked 4 |
| 13 | 2026-09-11T20:13 | 10 | 4 | 3 | fixed 2, widened 0, traps 0, false 6, blocked 2 |
| 14 | 2026-09-11T20:30 | 11 | 6 | 6 | fixed 2, widened 0, traps 0, false 7, blocked 2 |
| 15 | 2026-09-11T20:57 | 14 | 8 | 8 | fixed 3, widened 0, traps 0, false 9, blocked 2 |

## Detail

### Round 1, 2026-09-03T19:17

- **Builder A## codes visible in world files**: 3 finding(s)
  - files named: onboard_video_still_log.pdf, ir_2025-1018_final.docx, production_tracker.csv
- **Uncategorised, read the finding text**: 3 finding(s)
  - files named: intake_memo.docx, matter_calendar_matterhub.csv, reyes_lien_eob.pdf, ir_2025-1018_draft.docx
- **Dates, chronology or timeline don't hold together**: 2 finding(s)
  - files named: keeler_personnel.docx, tran_text_thread.pdf
- **Tool fingerprints / build dates in file metadata**: 2 finding(s)
  - files named: adjuster_note.docx, reserve_memo.docx, avl_gps_track_2025-1018.csv, medical_billing_ledger.csv
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)
  - files named: claims_0118.pdf, employment_verification.pdf, reyes_wage_records.pdf, rfp_set.pdf
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)
  - files named: reyes_life_care_plan.pdf, reyes_wage_records.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 1 finding(s)
  - files named: owl_service_rules.docx, post_accident_testing_policy.docx

### Round 2, 2026-09-10T16:12

- **Solution or reasoning leaked into world files**: 2 finding(s)
  - files named: intake_memo.docx, ir_2025-1018_final.docx, reserve_memo.docx, scene_photos_2025-1018.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: claims_0118.pdf
- **Builder A## codes visible in world files**: 1 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx

### Round 3, 2026-09-10T17:13

- **Uncategorised, read the finding text**: 4 finding(s)  **(REPEAT)**
  - files named: coverage_summary.pdf, dot_655_keeler.pdf, ir_2025-1018_final.docx, production_tracker.csv, medical_billing_ledger.csv, ir_2025-1018_draft.docx
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
  - files named: bac_keeler.pdf, complaint_reyes_filed.pdf
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**

### Round 4, 2026-09-10T18:02

- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, medical_billing_ledger.csv, reyes_lien_eob.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, production_tracker.csv
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**
- **Real-world references, citations or jurisdiction facts are wrong**: 1 finding(s)  **(REPEAT)**
  - files named: maintenance_log_bus4177.csv

Note: Also verified via spec_check.py traps that this round's edits do not touch any of the registered Reyes capacity/incapacity traps (conservatorship termination date, HIPAA personal-signature date, recorded-statement date, retention-to-window-close gap, intake-memo delay rationale, treating-physician 'much of' hedge) -- all confirmed still intact and untouched. Noted for a future round, out of scope for round 4's findings: spec_check.py ties flagged 3 pre-existing misses (Cho/Mowbray passengers' suit-filing deadline not literally present in A39/A14; blood-draw collection time not in A50/chain_custody.pdf) unrelated to any file touched this round.

### Round 5, 2026-09-10T19:32

- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: claims_tracker.csv, coverage_summary.pdf, late_claim_app.pdf, matter_calendar_matterhub.csv, reyes_lien_eob.pdf, reyes_life_care_plan.pdf
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
  - files named: production_tracker.csv
- **A referenced document or value doesn't resolve**: 1 finding(s)

### Round 6, 2026-09-10T21:34

- **Builder A## codes visible in world files**: 3 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, production_tracker.csv, runschedule_owl512.xlsx
- **Uncategorised, read the finding text**: 2 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx, dispatch_log_2025-1018.csv
- **A referenced document or value doesn't resolve**: 1 finding(s)  **(REPEAT)**
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**
  - files named: dot_655_keeler.pdf

### Round 7, 2026-09-10T22:07

- **Same person/entity named, titled or ID'd differently across files**: 2 finding(s)  **(REPEAT)**
  - files named: ir_2025-1018_final.docx, production_tracker.csv, roster_2025-1018.csv, onboard_video_still_log.pdf, tc_2025-1018.pdf
- **Totals don't foot / calculations disagree with inputs**: 2 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx, reyes_life_care_plan.pdf
- **Tool fingerprints / build dates in file metadata**: 2 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx
- **Builder A## codes visible in world files**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: hold_demand_letter.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 1 finding(s)  **(REPEAT)**
  - files named: owl_service_rules.docx, post_accident_testing_policy.docx
- **File is corrupt, empty, unreadable or won't render**: 1 finding(s)
  - files named: bid_award_512owl.docx, intake_memo.docx, ir_2025-1018_draft.docx, ir_2025-1018_final.docx, owl_service_rules.docx, post_accident_testing_policy.docx

Note: Also verified as false positives (no action needed): 2 blast_radius footing flags on files with no real total-row structure (medical_billing_ledger.csv, reserve_ledger.csv), 2 spec_check tie misses that are formatting-only (rejection_0218.pdf states a 6-month rule not a literal date; chain_custody.pdf's time is split across table cells), leak_scan's T1-answer-value hits (bare 911.4/946.6 citations that are pre-established Reyes-track facts, not the task's actual computed conclusion), and inventory_check's 9 registered-artifact/unregistered-file pairs (App Data-type artifacts the spec registers by system description rather than literal filename, pre-dating this round).

### Round 8, 2026-09-11T15:46

- **Builder A## codes visible in world files**: 2 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: dot_655_keeler.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)  **(REPEAT)**

Note: Re-verified as false positives (unchanged from round 7, confirmed no new instances from this round's edits): 2 blast_radius footing flags on ledgers with no real total-row structure, 2 spec_check tie misses that are formatting-only, leak_scan's bare-citation and reconciliation-boilerplate hits, and inventory_check's 9 registered-artifact/unregistered-file pairs. Both this round's text-growth deltas (post_accident_testing_policy.docx +238, IR_2025-1018_final.docx +57) were verified character-for-character against the logged edits.

### Round 9, 2026-09-11T16:27

- **Solution or reasoning leaked into world files**: 2 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, reyes_lien_eob.pdf
- **Builder A## codes visible in world files**: 1 finding(s)  **(REPEAT)**
  - files named: ir_2025-1018_final.docx, onboard_video_still_log.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: ir_2025-1018_final.docx, runschedule_owl512.xlsx
- **Voice, tone, texture or document authenticity reads machine-made**: 1 finding(s)
  - files named: scene_photos_2025-1018.pdf
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**

Note: scene_photos_2025-1018.pdf (minor): could not fix. A51's spec calls for '~10-15 captioned photos' but the built file is a text-only 61-entry photo log with zero embedded images. I cannot fabricate photorealistic evidence photographs of a collision scene (outside Rule 1's bounds and outside what I should attempt), and cannot edit WORLD_SPEC.xlsx myself to accept a text-only log format. This needs a builder-side decision: either the pipeline supplies real photos, or the spec is revised. Re-verified as false positives (unchanged from rounds 7-8): 2 blast_radius footing flags on ledgers with no real total-row structure, 2 spec_check tie misses that are formatting-only, and leak_scan's bare-citation/reconciliation-boilerplate hits. This round's one text-growth delta (Dispatch_log_2025-1018.csv, the new timepoint-exception entry) was verified as the only file that grew and confirmed as a factual entry, not reconciling language, via leak_scan's own reconciling-language category.

### Round 10, 2026-09-11T17:04

- **Builder A## codes visible in world files**: 2 finding(s)  **(REPEAT)**
  - files named: ir_2025-1018_final.docx, onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Solution or reasoning leaked into world files**: 2 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, reyes_lien_eob.pdf, ir_2025-1018_final.docx
- **Dates, chronology or timeline don't hold together**: 2 finding(s)  **(REPEAT)**
  - files named: late_claim_app.pdf
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf
- **A referenced document or value doesn't resolve**: 1 finding(s)  **(REPEAT)**
  - files named: dispatch_log_2025-1018.csv, ir_2025-1018_final.docx, runschedule_owl512.xlsx

Note: Two claims in this round's findings were independently verified WRONG and were NOT applied: (1) Reyes_life_care_plan.pdf's four 'weighted annual average' figures, summed with the plan's other 10 category rows, total exactly $180,000 (the canonical annual cost), and the standard level-annuity PV formula on $180,000/2.5%/36yr computes to $4,240,125 (rounds to the canonical $4,240,000) -- changing these four figures to AutoQC's suggested lower values would break WORLD_SPEC's canonical values, repeating round 5's exact mistake. (2) late_claim_app.pdf's citation to Gov. Code 912.2 for deeming the claim presented 'as of the date of the order granting leave' is the CORRECT reading of the statute -- verified the literal statutory text via multiple independent legal-database sources ('the claim shall be deemed to have been presented to the board upon the day that leave to present the claim is granted'); AutoQC's finding has the rule backwards. No changes made to either.

CHRONIC escalation, 4th consecutive round with no resolution: the Trip 06 schedule-vs-collision finding (Intended Traps Are Fair) has now failed dispute (r7), a sentence-level fix (r8), and a factual log entry addition (r9). No canonical value in WORLD_SPEC covers this specific clock-time gap -- only route/block assignment is canonical for the off-book trap. Further attempts risk either fabricating an unauthorized-deviation explanation (a forbidden bridge note) or touching either the heavily cross-referenced 02:05 collision time or the uniform schedule template shared by three other trips. This needs a spec-level decision: either WORLD_SPEC declares an explicit resolution/reconciliation for this gap, or the grading criteria for this dimension needs adjustment. Recommend escalating to the world thread per Gate 9.

Also unresolved after repeated rounds (4 rounds for the MP4, 2 for the photos), both requiring fabrication I should not attempt: ACTD/Video needs an actual MP4 file (A53 spec format) and Shared/Police/scene_photos_2025-1018.pdf needs ~10-15 real embedded photographs (A51 spec) -- neither can be produced by text-editing, and I cannot edit WORLD_SPEC.xlsx myself to revise either artifact's format requirement. Both need a builder-side decision: supply real media, or revise the spec.

Re-verified as false positives (unchanged from prior rounds): 2 blast_radius footing flags, 2 spec_check tie misses, leak_scan's baseline bare-citation/reconciliation hits. No files gained text this round -- all edits were deletions, formatting removal, or same-length name swaps. Two claims in this round's findings were independently verified WRONG and were NOT applied: (1) Reyes_life_care_plan.pdf's four 'weighted annual average' figures, summed with the plan's other 10 category rows, total exactly $180,000 (the canonical annual cost), and the standard level-annuity PV formula on $180,000/2.5%/36yr computes to $4,240,125 (rounds to the canonical $4,240,000) -- changing these four figures to AutoQC's suggested lower values would break WORLD_SPEC's canonical values, repeating round 5's exact mistake. (2) late_claim_app.pdf's citation to Gov. Code 912.2 for deeming the claim presented 'as of the date of the order granting leave' is the CORRECT reading of the statute -- verified the literal statutory text via multiple independent legal-database sources ('the claim shall be deemed to have been presented to the board upon the day that leave to present the claim is granted'); AutoQC's finding has the rule backwards. No changes made to either.

BLOCKED, needs a spec-level/builder decision, not further file edits: (1) CHRONIC, 4th consecutive round with no resolution -- the Trip 06 schedule-vs-collision finding (Intended Traps Are Fair) has now failed dispute (r7), a sentence-level fix (r8), and a factual log entry addition (r9). No canonical value in WORLD_SPEC covers this specific clock-time gap -- only route/block assignment is canonical for the off-book trap. Further attempts risk either fabricating an unauthorized-deviation explanation (a forbidden bridge note) or touching either the heavily cross-referenced 02:05 collision time or the uniform schedule template shared by three other trips. Recommend escalating to the world thread per Gate 9. (2) 4th round on the MP4: ACTD/Video needs an actual MP4 file per A53's spec format -- cannot be produced by text-editing, and I cannot edit WORLD_SPEC.xlsx myself to revise the format requirement. (3) 2nd round on scene_photos: Shared/Police/scene_photos_2025-1018.pdf needs ~10-15 real embedded photographs per A51's spec -- same constraint. Both (2) and (3) need a builder-side decision: supply real media, or revise the spec.

Re-verified as false positives (unchanged from prior rounds): 2 blast_radius footing flags, 2 spec_check tie misses, leak_scan's baseline bare-citation/reconciliation hits. No files gained text this round -- all edits were deletions, formatting removal, or same-length name swaps.

### Round 11, 2026-09-11T17:58

- **Builder A## codes visible in world files**: 2 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, reyes_lien_eob.pdf
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: reserve_memo.docx

### Round 12, 2026-09-11T19:50

- **Builder A## codes visible in world files**: 4 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, runschedule_owl512.xlsx, onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, late_claim_app.pdf, reyes_lien_eob.pdf
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: bac_keeler.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: reserve_memo.docx

Note: Blocked on named parties: Trip 06 schedule-vs-collision gap and the life-care-plan/spec figure mismatch are both pending the domain lead's WORLD_SPEC.xlsx update (6-cell table sent r11); MP4 (A53) and scene photos (A51) are pending a builder decision on real media vs. spec-format revision.

### Round 13, 2026-09-11T20:13

- **Builder A## codes visible in world files**: 6 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Solution or reasoning leaked into world files**: 2 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, late_claim_app.pdf, reyes_lien_eob.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)
  - files named: news_collision.html, reserve_memo.docx

Note: Blocked on named parties, unchanged: MP4 (A53) and scene photos (A51) still need real media or a spec format revision from the builder side.

### Round 14, 2026-09-11T20:30

- **Builder A## codes visible in world files**: 6 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, late_claim_app.pdf, reyes_lien_eob.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
  - files named: adjuster_note.docx, ir_2025-1018_draft.docx
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)  **(REPEAT)**
  - files named: news_collision.html

Note: Blocked on named parties, unchanged: MP4 (A53) and scene photos (A51) still need real media or a spec format revision from the builder side.

### Round 15, 2026-09-11T20:57

- **Builder A## codes visible in world files**: 6 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, onboard_video_still_log.pdf, production_tracker.csv, scene_photos_2025-1018.pdf
- **Solution or reasoning leaked into world files**: 2 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, late_claim_app.pdf, reyes_lien_eob.pdf, reserve_memo.docx, runschedule_owl512.xlsx
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
  - files named: adjuster_note.docx, ir_2025-1018_draft.docx, reserve_ledger.csv, reserve_memo.docx
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**
  - files named: employment_verification.pdf, reyes_wage_records.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 1 finding(s)  **(REPEAT)**
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: bills_billed.pdf

Note: Blocked on named parties, unchanged: MP4 (A53) and scene photos (A51) still need real media or a spec format revision from the builder side.

