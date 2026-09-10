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

