# Change manifest

Every automated change to this world, newest tool last. Skim it to confirm nothing legitimate was rewritten.

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | provider column, 12 rows [banned Tier-A name Meridian] | Meridian Outpatient Physical Therapy | → | Ashby Outpatient Physical Therapy |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | bill_id column, 11 rows [banned Tier-A name Meridian] | MER-0xx bill_id prefix | → | ASH-0xx bill_id prefix |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | lines 1-15 and trailing notes [CSV header not on row 1 / non-data rows in row stream] | 8 leading metadata comment lines + trailing Reconciliation Notes block | → | removed; row 1 is now the real header, TOTAL row is last data row |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Med/Reyes/bills_billed.pdf | p.1 table, p.10 heading and field [banned Tier-A name Meridian] | Meridian Outpatient Physical Therapy | → | Ashby Outpatient Physical Therapy |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.3, 3 occurrences [banned Tier-A name Meridian] | Meridian | → | Ashby |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.1 caption block [matter number inconsistent across 3 files, canonicalized to MatterHub's HC-2026-0087] | Our File No.: HC-2026-0037 | → | Our File No.: HC-2026-0087 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Witness/blau_statement.pdf | p.1, 2 occurrences [banned Tier-A name Meridian] | Meridian Grill / the Meridian | → | Palisade Grill / the Palisade |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Passengers/claims_0118.pdf | p.3 and p.6 [email typo inconsistent with 6 other files using the hyphenated domain] | nhalstead@halsteadcruz.com | → | nhalstead@halstead-cruz.com |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Video/onboard_video_still_log.pdf | p.1 Native Clip SHA-256 row [synthetic sequential-pattern hash, not a real digest] | 8c6f0e0d2f7a4b9a54e0a9e2d3b1c72f6c1a9a2b3c5d7e9f01234567890abcdef | → | 5b5b52667953dc1379b324d48454644350bb458d62ab721cdf7c8b05b72c5f23 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Video/onboard_video_still_log.pdf | p.6 signature block [unfilled bracket placeholder] | /s/ [Vendor Custodian of Record] | → | /s/ Marcus T. Whitfield |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | A12 row date_range [overstated produced window vs native AVL file end (02:05:12) and final incident report] | 10/17/2025 22:15 – 10/18/2025 02:20 | → | 10/17/2025 22:15 – 10/18/2025 02:05 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | A53 row date_range [same stale 02:20 value, same fix] | 10/17/2025 22:15 – 10/18/2025 02:20 | → | 10/17/2025 22:15 – 10/18/2025 02:05 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | lines 1-7 [CSV header not on row 1] | 6 leading metadata comment lines | → | removed; row 1 is now the real header |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/matter_calendar_MatterHub.csv | answer_due row [law firm's own deadline tracker should calendar the answer date at service, not leave it null] | answer_due blank, entered_by/entered_date/last_modified blank | → | answer_due=06/22/2026, entered_by=gchen@halstead-cruz.com, entered_date/last_modified=05/22/2026 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/matter_calendar_MatterHub.csv | lines 1-8 [CSV header not on row 1] | 8 leading metadata comment lines | → | removed; row 1 is now the real header |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | matter file caption [matter number inconsistent across 3 files, canonicalized to MatterHub's HC-2026-0087] | H&C Matter No. 2026-0117 | → | H&C Matter No. HC-2026-0087 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Route 512 Owl Block!L29 (Trip 10, Alder Creek/Broadway) [time out of chronological order for a northbound trip] | 04:57 (recovery) | → | 04:46 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Criminal/criminal_docket.csv | lines 1-10 [CSV header not on row 1] | 9 leading caption lines + blank | → | removed; row 1 is now the real header |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Fleet/maintenance_log_bus4177.csv | lines 1-9 and trailing [CSV header not on row 1 / trailing non-data rows] | 8 leading metadata comment lines + blank + 2 trailing comment lines | → | removed; row 1 is now the real header, last real work order is last row |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/AVL_GPS_track_2025-1018.csv | lines 1-14 [CSV header not on row 1; stated record count also didn't match actual 227 data rows] | 14 leading metadata comment lines, incl. false Record count: 214 rows (header + 213 data rows) | → | removed; row 1 is now the real header (actual data has 227 rows) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/roster_2025-1018.csv | lines 1-12 [CSV header not on row 1] | 11 leading metadata comment lines + blank | → | removed; row 1 is now the real header |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | §3.2(b) [misstated the real 49 CFR 655.4 rule it cites, inconsistent with owl_service_rules.docx Rule 506; confirmed no task depends on this specific distinction] | (b) The accident results in an injury requiring immediate medical treatment away from the scene; or | → | (b) The accident results in an injury requiring immediate medical treatment away from the scene, and the covered employee received a citation under state or local law for a moving traffic violation arising from the accident; or |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | body, course-and-scope paragraph [stated T5's legal conclusion outright instead of the operational facts the agent is meant to synthesize] | The course-and-scope determination is therefore that Operator Keeler was acting within scope of his employment at the time of the collision. | → | The course-and-scope determination is therefore that Operator Keeler was operating his assigned Owl Route 512 block at the time of the collision, consistent with the official run schedule and AVL/GPS telemetry. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | A43 row, notes column [spelled out T9's CCP 2018.030 legal analysis rather than leaving it to the agent; A42's tag (the actual T9 trap) and A43's Attorney-confirmed/Withhold-Privileged status both left untouched as accurate] | CCP § 2018.030 attorney work-product / attorney-directed material; responsive to RFP 31, RFP 32, and RFP 33 | → | responsive to RFP 31, RFP 32, and RFP 33 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.9 Personal Care Attendant Hours detail table [Annual Cost Summary categories summed to 190,000 against a stated 180,000 total that matches the spec's canonical PV chain; line items needed to come down by 10,000, split across 3 categories per expert direction] | Payroll taxes/overhead loading $14,837 (blended 15% loading) | → | $11,337 (blended 11% loading) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.9 and p.11, Personal care attendant hours subtotal (2 places) [reflects the payroll-loading reduction above] | $113,749 | → | $110,249 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.12 Contingency for Complications detail table [part of the 10,000 line-item correction, split across 3 categories] | Reserve for unforeseen therapies and specialty consults $9,540 | → | $6,540 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.12 and p.11, Contingency for complications subtotal (2 places) [reflects the unforeseen-therapies reduction above] | $14,843 | → | $11,843 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.11 Annual Cost Summary, Rounding / geographic-pricing adjustment [part of the 10,000 line-item correction, split across 3 categories] | $5,200 | → | $1,700 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_wage_records.pdf | p.10 PV Worksheet, Household-services capacity loss, Undiscounted Loss [PV worksheet's 4 components summed to 1,100,000 against a stated (and spec-matching) 1,200,000 total] | $362,410 | → | $500,130 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_wage_records.pdf | p.10 PV Worksheet, Household-services capacity loss, PV @ 2.5% [closes the 100,000 footing gap; this is the only worksheet component with no shown sub-breakdown] | $263,180 | → | $363,180 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_wage_records.pdf | p.2, TAB A employer verification letter [conflicted with the corroborated details on employment_verification.pdf and this same file's own p.7 (TAB D): address, title, email domain, and phone all drifted on this one page] | 2245 Harborview Boulevard / SHRM-CP, Human Resources Manager, Southern California Region / mtorres@coastlinehg.com / (562) 555-0164 | → | 2740 Harbor Boulevard, Suite 210 / HR Manager / mtorres@coastlinehomegoods.com / (562) 555-0185 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/adjuster_note.docx | header table, File / Claim No. row [document dated 10/28/2025 cited 2026-prefixed claim numbers for claims not presented until 2026; also contradicted the document's own Section 2, which lists Gov Code 910 presentations as not yet in file] | Individual claim nos.: Reyes ACTD-2026-0119 | Cho ACTD-2026-0114 | Mowbray ACTD-2026-0115 | City ACTD-2026-0117 | → | Individual claim nos. not yet assigned; no Gov. Code § 910 claims presented as of this writing. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | header, CLAIM FILE line [document dated 12/15/2025 cited 2026-prefixed claim numbers for claims not presented until 2026 (Cho/Mowbray 01/16/2026, City 02/02/2026)] | Per-claimant claim nos.: Reyes ACTD-2026-0119 (pedestrian); Cho ACTD-2026-0114 (passenger); Mowbray ACTD-2026-0115 (passenger); City of Rivergate ACTD-2026-0117 (property) | → | Per-claimant Gov. Code § 910 claims not yet presented as of this writing. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/HR/Keeler_personnel.docx | table header rows, 18 runs across 4 tables [white text on light gray D9D9D9 fill was effectively unreadable] | white (FFFFFF) header text on D9D9D9 fill, 4 tables (Date/Event, Item/Status, Cycle/Rating/Notes, Test type/History) | → | black (000000) header text, same fill, same labels |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | p.10 jury demand signature block | By: __________________________________ (blank) | → | By: /s/ Nora Halstead |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | p.12 proof of service signature | __________________________________ (blank) | → | /s/ Grace Chen |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/RFP_set.pdf | p.12 attorney signature block | By: ______________________________ (blank) | → | By: /s/ Nora Halstead |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/RFP_set.pdf | p.14 proof of service signature | ______________________________ (blank) | → | /s/ Grace Chen |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | row TOTAL, adjustments column | 2644000 (TOTAL adjustments) | → | 2640800 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | row TOTAL, balance column | 0 (TOTAL balance) | → | 3200 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | ACNRI-001,002,003,004,006,007,008 service_date | 2025-12-22 to 2026-04-28 | → | 2025-12-22 to 2026-04-06 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | ACNRI-005 service_date | 2026-02-03 to 2026-04-15 | → | 2026-02-03 to 2026-04-06 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | ACNRI-001 description | (127 days) | → | (105 days) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.1 opening paragraph | Copies of each underlying EOB, remittance advice, and the DHCS lien notice are enclosed at the tabs indicated. | → | ...are produced separately. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.2 section 2 | the schedule attached hereto as Exhibit A, with corresponding EOBs at Tabs 1-9. | → | ...as Exhibit A. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.2 section 3 | DHCS's countersigned reduction letter is enclosed at Tab 10. | → | ...is produced separately. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.3 section 5 heading | 5.  Enclosure Index (Tabs) | → | 5.  Materials Index (Tabs) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.4 signature block | Enclosures (Exhibit A; Tabs 1-11) | → | Enclosures (Exhibit A) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | A53 row, log_entry/description/notes columns | REYES-000369–000377 + native MP4 (REYES-NATIVE-0004) | → | REYES-000369–000377 (native MP4 held by vendor, not yet produced) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/AVL_GPS_track_2025-1018.csv | rows 02:01:00-02:05:12, lat and heading_deg columns | latitude decreasing 34.08498->34.07852, heading 0 then 181-188 (southbound-consistent) | → | latitude increasing 34.08498->34.09144 (mirrored), heading 0 then 1-8 (northbound-consistent) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Trip 06 row, S. Main/Third column (J25) | 02:05 (SB timepoint pass) / 02:31 | → | 02:31 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | rows 32-35 | Key Timepoint - S. Main / Third (Downtown Rivergate) callout table (rows 32-35) | → | (removed, blanked) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/employment_verification.pdf | p.1 table + paragraph, p.3 rate history table | Date of hire 06/2018; since June 2018; 06/2018 (hire) | → | 04/2019; since April 2019; 04/2019 (hire) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/reyes_recorded_statement.pdf | p.3 dialogue | A little over three years. I started in the summer of 2022. | → | A little over six years. I started in the spring of 2019. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | para 9 | sixth week of outpatient rehabilitation...transitioned to outpatient status in early February 2026 | → | eleventh week of inpatient rehabilitation...discharge to outpatient status anticipated in early April 2026 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | para 19 (Injuries) | transitioned to outpatient rehab in early February | → | remains an inpatient there as of this memo, with discharge to outpatient care anticipated in early April |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/claims_tracker.csv | rows 2-3, suit_filing_deadline + deadline_basis columns | suit_filing_deadline blank, deadline_basis 'see rejection notice' (Cho + Mowbray rows) | → | 08/18/2026, reject+6mo (Gov. Code § 945.6) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | row 20 (A53) | A53 description field with unquoted comma causing 11-field row | → | properly quoted description field, 10 fields |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | all data rows | review_status=Confirmed/First-pass/Attorney-confirmed, final_call=Produce/Withhold-Privileged, log_entry=PL-LOG-001/PL-LOG-002 for A42/A43 | → | review_status=Pending attorney review, final_call=TBD (all 22 rows); log_entry='—' for A42/A43 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | last row | TOTAL,ALL PROVIDERS (9),... aggregate row | → | (row removed) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.2 Step 4 table | Yes — Attachment A (tape affixed to form) | → | No — Attachment A (retained in Compliance safe) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.4 Distribution list | Attachment A/B/C listed as distributed with this copy | → | Attachment A/B/C labeled (Compliance safe), shortened descriptions |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | Rule 102 | the general ACTD Operator Rulebook or Standard Bus Operator Bulletin ... the general Rulebook remains in force | → | the District's other operating policies ... those other policies remain in force |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | Rule 104 | operator hours-of-service limits set forth in the current ACTD collective bargaining agreement | → | operator hours-of-service limits established under the District's fatigue-management program (Rule 206) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_wage_records.pdf | Tab E, Section 7 PV worksheet | Acute/rehab $27,180/$27,020; Years1-5 $215,970/$198,610; Total $1,194,450/$868,410; Rounding +$2,500 | → | Acute/rehab $26,892/$26,892; Years1-5 $215,948/$200,593; Total $1,194,140/$870,265; Rounding +$4,645 (final $1,200,000 unchanged, matches spec canonical value sourced from this artifact) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 13 and para 27 (AVL/GPS Track section) [t17 CHRONIC: false claim that AVL coincides with published schedule timepoint when schedule (Trip 06 J25=02:31) contradicts actual/AVL 02:05] | AVL/GPS telemetry ... at the published S. Main/Third timepoint ... The last valid AVL position log ... at 02:05, coincident with the published S. Main/Third control-point timepoint | → | running ahead of the published timepoint ... at 02:05, approximately 26 minutes ahead of the published S. Main/Third control-point timepoint (02:31) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Timeline table, rows for PD/EMS arrival [t17 CHRONIC: arrival times must match cited source TC-2025-1018 (PD arrived 0212 per narrative; Medic 11 first EMS unit at 0210)] | Table 1 row: PD first on scene 02:11; EMS on scene 02:15 | → | PD first on scene 02:12; EMS on scene 02:10 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | 02:06 radio_call row [t17 CHRONIC: leftover wrong-direction (SB) label on a NB trip (Trip 06), same defect class round 2 fixed in the schedule cell but missed here] | AVL last position vicinity S. Main at Third Ave (SB reference timepoint 02:05). | → | AVL last position vicinity S. Main at Third Ave at 02:05, ahead of Trip 06's NB schedule. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | closing status line (last paragraph) [t21/Finding: draft lacks any visible review markup (comments=[], zero w:ins/w:del) despite being labeled DRAFT/SUBJECT TO SUPERVISOR REVIEW] | (no comments; no w:ins/w:del; zero tracked-change or review markup in the package) | → | Added one Word comment (author: Marlene Okonkwo, Director of Safety, dated 2025-10-18) anchored to the closing 'DRAFT -- pending Safety-Director review' line, acknowledging receipt and instructing to hold the draft's placeholder figures pending confirmation |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Table0 row0, Table1 row0, Table2 row0, Table3 row0 [t22: dark-on-dark header text, Text Legibility And Contrast — Major] | Header rows (Table0 r0 'Incident No.:'; Table1 r0 'Time/Event/Source'; Table2 r0 'Name'; Table3 r0 'Passenger/Status/Disposition') on 1B2A4E dark fill with no explicit run color, inheriting Normal style's dark 333944 font | → | Same header rows given explicit white (FFFFFF) run-level font color |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Table1 row0 [t22: dark-on-dark header text, Text Legibility And Contrast — Major] | Table1 row0 ('Role','Attorney/Staff') on 141A2E dark fill with no explicit run color, inheriting Normal style's dark 4A5266 font | → | Same header row given explicit white (FFFFFF) run-level font color |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.2 Step 4 table, 'Printed result tape affixed to form?' [self-QA: found via direct PDF rendering that the round-3 fix had two defects -- an em-dash rendered as a stray middle-dot, and the replacement text was appended to the end of the page's content stream separately from its own continuation lines] | No — Attachment A (retained in Compliance safe) [round-3 version: em-dash corrupted to a middle-dot glyph by pdf_replace.py's base-14 font, AND the replacement text was split from its own trailing continuation lines in the underlying content stream] | → | No - Attachment A (retained in Compliance safe; two-copy EBT thermal printout, screening plus confirmation, sequential numbers 002417 and 002418, device serial ASIV-XL-73142-KN) [full 3-line cell value replaced as one unit via --multiline, plain ASCII hyphen instead of em-dash] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.4 Distribution list, 3 bullets [self-QA: same em-dash glyph corruption as the p.2 fix] | Attachment A/B/C (Compliance safe) descriptions [round-3 version: em-dashes corrupted to middle-dot glyphs] | → | Attachment A/B/C (Compliance safe) - descriptions, using a plain ASCII hyphen; each bullet's text redone as one full-line unit (bullet character itself left untouched/original since inserting a replacement bullet glyph via the fallback font corrupts it too) |
