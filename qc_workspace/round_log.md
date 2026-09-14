# AutoQC round log

World: `/home/user/Julius/filesystem`

One row per round. `Repeats` are defect classes that already appeared in an earlier round,
each one means that class was fixed at the instance level, not the class level.

| Round | Opened | Findings | Classes | Repeats | Disposition |
|---|---|---|---|---|---|
| 1 | 2026-09-03T19:17 | 14 | 8 | 0 | fixed 6, widened 4, traps 1, false 3, blocked 0 |
| 2 | 2026-09-14T16:16 | 14 | 7 | 5 | fixed 3, widened 0, traps 1, false 9, blocked 1 |
| 3 | 2026-09-14T17:17 | 14 | 6 | 6 | fixed 7, widened 0, traps 1, false 2, blocked 4 |

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

### Round 2, 2026-09-14T16:16

- **Builder A## codes visible in world files**: 7 finding(s)  **(REPEAT)**
  - files named: op_reports.pdf, reyes_life_care_plan.pdf, onboard_video_still_log.pdf, scene_photos_2025-1018.pdf
- **Uncategorised, read the finding text**: 2 finding(s)  **(REPEAT)**
  - files named: 13.pdf, tcr.pdf
- **Totals don't foot / calculations disagree with inputs**: 1 finding(s)  **(REPEAT)**
  - files named: late_claim_app.pdf, reyes_lien_eob.pdf, reyes_life_care_plan.pdf
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: docket_entry.xlsx
- **Solution or reasoning leaked into world files**: 1 finding(s)
  - files named: ir_2025-1018_final.docx, production_tracker.csv, reserve_memo.docx
- **File is corrupt, empty, unreadable or won't render**: 1 finding(s)

### Round 3, 2026-09-14T17:17

- **Builder A## codes visible in world files**: 5 finding(s)  **(REPEAT)**
  - files named: onboard_video_still_log.pdf, tran_text_thread.pdf, scene_photos_2025-1018.pdf, ir_2025-1018_final.docx, production_tracker.csv, reserve_memo.docx, runschedule_owl512.xlsx
- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, late_claim_app.pdf, reyes_lien_eob.pdf, hold_demand_letter.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: plan.pdf
- **Uncategorised, read the finding text**: 2 finding(s)  **(REPEAT)**
  - files named: 13.pdf, ir_2025-1018_draft.docx, tcr.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: medical_billing_ledger.csv

Note: Blocked-on-person items: A53 onboard video and A52 text-thread chronology are judgment calls put to the world owner rather than guessed at. Anomaly Detection Catch-All (Docuseal/Wiki.js) and A51/onboard-log photos remain blocked on the app-data pipeline and on image-generation capability respectively, same as round 2.

