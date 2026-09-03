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
