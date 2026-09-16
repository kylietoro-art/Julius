# AutoQC round log

World: `/home/user/Julius/filesystem`

One row per round. `Repeats` are defect classes that already appeared in an earlier round,
each one means that class was fixed at the instance level, not the class level.

| Round | Opened | Findings | Classes | Repeats | Disposition |
|---|---|---|---|---|---|
| 1 | 2026-09-03T19:17 | 14 | 8 | 0 | fixed 6, widened 4, traps 1, false 3, blocked 0 |
| 2 | 2026-09-16T16:54 | 12 | 7 | 6 | fixed 4, widened 0, traps 0, false 8, blocked 0 |
| 3 | 2026-09-16T20:05 | 12 | 6 | 6 | fixed 7, widened 1, traps 3, false 4, blocked 0 |

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

### Round 2, 2026-09-16T16:54

- **Builder A## codes visible in world files**: 5 finding(s)  **(REPEAT)**
  - files named: ir_2025-1018_final.docx, production_tracker.csv, reserve_memo.docx
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, late_claim_app.pdf, plan.pdf
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)  **(REPEAT)**
  - files named: medical_billing_ledger.csv, reyes_lien_eob.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **File is corrupt, empty, unreadable or won't render**: 1 finding(s)
  - files named: 13.pdf, tcr.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, scene_photos_2025-1018.pdf

### Round 3, 2026-09-16T20:05

- **Builder A## codes visible in world files**: 5 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, production_tracker.csv, matter_calendar_matterhub.csv, ir_2025-1018_final.docx, reserve_memo.docx, runschedule_owl512.xlsx
- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: docket_entry.xlsx, medical_billing_ledger.csv, reyes_lien_eob.pdf, plan.pdf
- **Uncategorised, read the finding text**: 1 finding(s)  **(REPEAT)**
  - files named: tcr.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Same person/entity named, titled or ID'd differently across files**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: medical_billing_ledger.csv

Note: Gate 6 blast_radius: 0 stale values; 2 footing flags (medical_billing_ledger.csv TSG-002, reserve_ledger.csv RL-2025-0107) both verified as tool heuristic misfires on flat-list CSVs with no real total rows, not real breaks; 4 dependency-set hits all verified consistent or coincidental. Gate 8 inventory_check: 9/9 artifact-vs-filename mismatches are the same repeat App-Data-companion-export pattern as rounds 1-2; text growth in BAC_Keeler.pdf/Keeler_personnel.docx/production_tracker.csv fully accounted for by the A## scrub, reserve_ledger.csv by round 2/3 notes edits. Gate 8 leak_scan: 4 'task answer' hits (911.4/946.6 in intake_memo/matter_calendar/hold_demand_letter/claims_tracker) verified against T1's Design Purpose -- all are Reyes's own §911.4/§946.6 track citations, which the correct T1 memo is explicitly supposed to reference, not the actual hidden passenger-deadline (08/18/2026) or A62-correction answer; 4 trap-defusal hits are coincidental digit matches in unrelated operational sentences, not real reconciliation language.

