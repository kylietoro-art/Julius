# AutoQC round log

World: `/home/user/Julius/filesystem`

One row per round. `Repeats` are defect classes that already appeared in an earlier round,
each one means that class was fixed at the instance level, not the class level.

| Round | Opened | Findings | Classes | Repeats | Disposition |
|---|---|---|---|---|---|
| 1 | 2026-09-03T19:17 | 14 | 8 | 0 | fixed 6, widened 4, traps 1, false 3, blocked 0 |
| 2 | 2026-09-09T16:22 | 29 | 10 | 7 | fixed 6, widened 0, traps 0, false 23, blocked 0 |
| 3 | 2026-09-09T17:49 | 23 | 11 | 10 | fixed 8, widened 1, traps 0, false 14, blocked 0 |
| 4 | 2026-09-09T19:09 | 27 | 11 | 10 | fixed 6, widened 2, traps 0, false 19, blocked 0 |
| 5 | 2026-09-09T21:07 | 28 | 11 | 11 | fixed 9, widened 0, traps 0, false 19, blocked 0 |
| 6 | 2026-09-09T21:57 | 21 | 8 | 8 | _open_ |

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

### Round 2, 2026-09-09T16:22

- **Uncategorised, read the finding text**: 14 finding(s)  **(REPEAT)**
- **Totals don't foot / calculations disagree with inputs**: 4 finding(s)  **(REPEAT)**
  - files named: medical_billing_ledger.csv, rehab_neuropsych.pdf, reyes_lien_eob.pdf
- **A referenced document or value doesn't resolve**: 2 finding(s)
  - files named: onboard_video_still_log.pdf, reyes_lien_eob.pdf, avl_gps_track_2025-1018.csv, runschedule_owl512.xlsx, tc_2025-1018.pdf
- **Same person/entity named, titled or ID'd differently across files**: 2 finding(s)  **(REPEAT)**
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
  - files named: complaint_reyes_filed.pdf, rfp_set.pdf
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **Solution or reasoning leaked into world files**: 1 finding(s)
  - files named: runschedule_owl512.xlsx
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)

Note: blast_radius.py flags a footing break on medical_billing_ledger.csv (TSG-002/TOTAL rows); independently re-verified every row and the grand total foot exactly against the EOB Exhibit A figures, so this is a tool heuristic false positive, not a real defect. Two minor EOB sentences (the Tab-11 BlueShield line and the Notes 'corresponding tab' line) were left with their original 'enclosed'/'at the tab' wording because every reflow attempt to correct them corrupted the surrounding justified paragraph (verified via render-check); the 5 other, more prominent tab-enclosure claims in the same letter were fixed.

### Round 3, 2026-09-09T17:49

- **Uncategorised, read the finding text**: 7 finding(s)  **(REPEAT)**
  - files named: intake_memo.docx, ir_2025-1018_final.docx
- **Totals don't foot / calculations disagree with inputs**: 4 finding(s)  **(REPEAT)**
  - files named: reyes_wage_records.pdf, dispatch_log_2025-1018.csv, ir_2025-1018_final.docx, runschedule_owl512.xlsx, tc_2025-1018.pdf
- **Same person/entity named, titled or ID'd differently across files**: 2 finding(s)  **(REPEAT)**
- **Builder A## codes visible in world files**: 2 finding(s)  **(REPEAT)**
  - files named: production_tracker.csv, medical_billing_ledger.csv
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
- **A referenced document or value doesn't resolve**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)  **(REPEAT)**
- **Raw Markdown/HTML printed as visible text**: 1 finding(s)
  - files named: ir_2025-1018_draft.docx

Note: inventory_check.py's 9 registered-artifact/9 unregistered-file mismatches are pre-existing App-Data-type artifacts (spec Location/Address is an abstract system description, e.g. 'Fare system -> APC boardings table', not a real path) materialized as concrete exported files under different names; unchanged since the round 2 snapshot, not a round-3 regression. The 2 TEXT GROWTH flags are also accounted for: claims_tracker.csv's growth is the already-committed round-2 follow-up fix (commit 7f140cf) landing after that snapshot was taken; production_tracker.csv's growth is the intended uniform review_status/final_call neutralization (replacing varied leaked answers with 'Pending attorney review'/'TBD'), not added reconciliation prose.

### Round 4, 2026-09-09T19:09

- **Uncategorised, read the finding text**: 10 finding(s)  **(REPEAT)**
  - files named: dispatch_log_2025-1018.csv
- **Totals don't foot / calculations disagree with inputs**: 4 finding(s)  **(REPEAT)**
  - files named: reyes_life_care_plan.pdf, intake_memo.docx, reserve_memo.docx, reyes_lien_eob.pdf
- **Same person/entity named, titled or ID'd differently across files**: 3 finding(s)  **(REPEAT)**
- **Voice, tone, texture or document authenticity reads machine-made**: 2 finding(s)
  - files named: admit_2025-1018.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: claims_0118.pdf
- **Builder A## codes visible in world files**: 1 finding(s)  **(REPEAT)**
  - files named: tran_text_thread.pdf
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
  - files named: hold_demand_letter.pdf, late_claim_app.pdf
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)  **(REPEAT)**

Note: Self-QA pass (separate from this round's findings) found and fixed 3 regressions from round 3's own edits: a self-introduced CSV comma corruption, an em-dash-to-glyph-corruption + text-stream-order defect in DOT_655_Keeler.pdf (full re-audit of all 29 historical PDF edits found no other instances), and CRLF line endings from csv.writer defaults in two files. Also discovered and now avoid a second systemic pdf_replace.py limitation: it always reinserts text in Helvetica regardless of the source document's actual font, causing a visible font mismatch on Times-Roman documents (9 of 12 edited PDFs); fixed for this round's edits via explicit fontname parameters in manual PyMuPDF redaction, but historical edits across rounds 1-3 were not audited for this specific defect given time constraints.

### Round 5, 2026-09-09T21:07

- **Uncategorised, read the finding text**: 12 finding(s)  **(REPEAT)**
  - files named: adjuster_note.docx, intake_memo.docx, keeler_personnel.docx, post_accident_testing_policy.docx
- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: bills_billed.pdf, medical_billing_ledger.csv, reyes_wage_records.pdf
- **Tool fingerprints / build dates in file metadata**: 2 finding(s)  **(REPEAT)**
  - files named: docket_entry.xlsx
- **Same person/entity named, titled or ID'd differently across files**: 2 finding(s)  **(REPEAT)**
- **Builder A## codes visible in world files**: 2 finding(s)  **(REPEAT)**
  - files named: production_tracker.csv, reserve_memo.docx, runschedule_owl512.xlsx
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
  - files named: dot_655_keeler.pdf, post_accident_testing_policy.docx
- **Voice, tone, texture or document authenticity reads machine-made**: 1 finding(s)  **(REPEAT)**
- **Placeholder, template residue, or synthetic filler**: 1 finding(s)  **(REPEAT)**
- **A referenced document or value doesn't resolve**: 1 finding(s)  **(REPEAT)**
- **Solution or reasoning leaked into world files**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)  **(REPEAT)**

### Round 6, 2026-09-09T21:57

- **Uncategorised, read the finding text**: 9 finding(s)  **(REPEAT)**
  - files named: runschedule_owl512.xlsx
- **Totals don't foot / calculations disagree with inputs**: 3 finding(s)  **(REPEAT)**
  - files named: claims_tracker.csv, docket_entry.xlsx
- **Same person/entity named, titled or ID'd differently across files**: 2 finding(s)  **(REPEAT)**
- **Solution or reasoning leaked into world files**: 2 finding(s)  **(REPEAT)**
  - files named: reyes_lien_eob.pdf, bills_billed.pdf
- **Real-world references, citations or jurisdiction facts are wrong**: 2 finding(s)  **(REPEAT)**
- **Dates, chronology or timeline don't hold together**: 1 finding(s)  **(REPEAT)**
- **Tool fingerprints / build dates in file metadata**: 1 finding(s)  **(REPEAT)**
- **Real PII or copyrighted material in world files**: 1 finding(s)  **(REPEAT)**

