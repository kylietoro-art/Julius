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

## a_scrub

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | in-text code | A42 | → | the Junior Adjuster Liability Note |
| ACTD/Claims/reserve_ledger.csv | in-text code | A43 | → | the Senior Claims-Manager Reserve Memo |
| ACTD/HR/Keeler_personnel.docx | in-text code | A54 | → | the Keeler DMV Driving Record |
| ACTD/HR/Keeler_personnel.docx | in-text code | A05 | → | the DOT Post-Accident Test Record |
| ACTD/Litigation/production_tracker.csv | in-text code | A01 | → | the Police Traffic Collision Report |
| ACTD/Litigation/production_tracker.csv | in-text code | A08 | → | the Owl Route 512 Run Schedule |
| ACTD/Litigation/production_tracker.csv | in-text code | A02 | → | the ACTD Final Incident Report |
| ACTD/Litigation/production_tracker.csv | in-text code | A08 | → | the Owl Route 512 Run Schedule |
| ACTD/Litigation/production_tracker.csv | in-text code | A12 | → | the AVL / GPS Route Track |
| ACTD/Litigation/production_tracker.csv | in-text code | A55 | → | the Route 512 Owl Block Bid Award Notice |
| ACTD/Litigation/production_tracker.csv | in-text code | A11 | → | the APC / Farebox Ridership Log |
| ACTD/Litigation/production_tracker.csv | in-text code | A12 | → | the AVL / GPS Route Track |
| ACTD/Litigation/production_tracker.csv | in-text code | A42 | → | the Junior Adjuster Liability Note |
| ACTD/Litigation/production_tracker.csv | in-text code | A54 | → | the Keeler DMV Driving Record |
| ACTD/Litigation/production_tracker.csv | in-text code | A55 | → | the Route 512 Owl Block Bid Award Notice |
| ACTD/Safety/IR_2025-1018_final.docx | in-text code | A05 | → | the DOT Post-Accident Test Record |
| ACTD/Safety/IR_2025-1018_final.docx | in-text code | A05 | → | the DOT Post-Accident Test Record |
| Med/Reyes/bills_billed.pdf | in-text code | A41 | → | the Plaintiff Paralegal Docket Entry |
| Shared/CrimeLab/BAC_Keeler.pdf | in-text code | A50 | → | the Blood-Draw Chain-of-Custody |
| Shared/CrimeLab/BAC_Keeler.pdf | in-text code | A50 | → | the Blood-Draw Chain-of-Custody |

**Left for you to check (not changed):**
- ACTD/Claims/medical_billing_ledger.csv: A0431, not in the ④ registry, real invoice/room/part code? left unchanged
- ACTD/Claims/medical_billing_ledger.csv: A0436, not in the ④ registry, real invoice/room/part code? left unchanged
- ACTD/Claims/medical_billing_ledger.csv: A0225, not in the ④ registry, real invoice/room/part code? left unchanged
- ACTD/Claims/reserve_ledger.csv: A42, context already names "Junior Adjuster Liability Note", rewrite by hand (drop the adjacent descriptor, e.g. "…the Junior Adjuster Liability Note")
- ACTD/Claims/reserve_ledger.csv: A43, context already names "Senior Claims-Manager Reserve Memo", rewrite by hand (drop the adjacent descriptor, e.g. "…the Senior Claims-Manager Reserve Memo")
- ACTD/Litigation/production_tracker.csv: A02, context already names "ACTD Final Incident Report", rewrite by hand (drop the adjacent descriptor, e.g. "…the ACTD Final Incident Report")
- ACTD/Litigation/production_tracker.csv: A03, context already names "ACTD Draft On-Scene Incident Report", rewrite by hand (drop the adjacent descriptor, e.g. "…the ACTD Draft On-Scene Incident Report")
- ACTD/Litigation/production_tracker.csv: A04, context already names "Crime-Lab Blood BAC Report", rewrite by hand (drop the adjacent descriptor, e.g. "…the Crime-Lab Blood BAC Report")
- ACTD/Litigation/production_tracker.csv: A05, context already names "DOT Post-Accident Test Record", rewrite by hand (drop the adjacent descriptor, e.g. "…the DOT Post-Accident Test Record")
- ACTD/Litigation/production_tracker.csv: A09, context already names "Dispatch "Off-Book" Email", rewrite by hand (drop the adjacent descriptor, e.g. "…the Dispatch "Off-Book" Email")
- ACTD/Litigation/production_tracker.csv: A13, context already names "Dispatch Log", rewrite by hand (drop the adjacent descriptor, e.g. "…the Dispatch Log")
- ACTD/Litigation/production_tracker.csv: A19, context already names "Keeler Personnel / HR File", rewrite by hand (drop the adjacent descriptor, e.g. "…the Keeler Personnel / HR File")
- ACTD/Litigation/production_tracker.csv: A20, context already names "Keeler Duty Roster / Timekeeping", rewrite by hand (drop the adjacent descriptor, e.g. "…the Keeler Duty Roster / Timekeeping")
- ACTD/Litigation/production_tracker.csv: A42, context already names "Junior Adjuster Liability Note", rewrite by hand (drop the adjacent descriptor, e.g. "…the Junior Adjuster Liability Note")
- ACTD/Litigation/production_tracker.csv: A43, context already names "Senior Claims-Manager Reserve Memo", rewrite by hand (drop the adjacent descriptor, e.g. "…the Senior Claims-Manager Reserve Memo")
- ACTD/Litigation/production_tracker.csv: A46, context already names "Blau Witness Statement", rewrite by hand (drop the adjacent descriptor, e.g. "…the Blau Witness Statement")
- ACTD/Litigation/production_tracker.csv: A48, context already names "Excess Risk-Pool Coverage Summary", rewrite by hand (drop the adjacent descriptor, e.g. "…the Excess Risk-Pool Coverage Summary")
- ACTD/Litigation/production_tracker.csv: A49, context already names "Bus Maintenance / Inspection Log", rewrite by hand (drop the adjacent descriptor, e.g. "…the Bus Maintenance / Inspection Log")
- ACTD/Litigation/production_tracker.csv: A51, context already names "Recovered Parts / Scene Evidence Photo Log", rewrite by hand (drop the adjacent descriptor, e.g. "…the Recovered Parts / Scene Evidence Photo Log")
- ACTD/Litigation/production_tracker.csv: A53, context already names "Onboard Video / Camera System Footage", rewrite by hand (drop the adjacent descriptor, e.g. "…the Onboard Video / Camera System Footage")
- ACTD/Litigation/production_tracker.csv: A57, context already names "ACTD Post-Accident Drug & Alcohol Testing Policy", rewrite by hand (drop the adjacent descriptor, e.g. "…the ACTD Post-Accident Drug & Alcohol Testing Policy")
- ACTD/Safety/IR_2025-1018_final.docx: A11, context already names "APC / Farebox Ridership Log", rewrite by hand (drop the adjacent descriptor, e.g. "…the APC / Farebox Ridership Log")
- ACTD/Safety/IR_2025-1018_final.docx: A11, context already names "APC / Farebox Ridership Log", rewrite by hand (drop the adjacent descriptor, e.g. "…the APC / Farebox Ridership Log")
- Legal/Reyes/intake_memo.docx: A62, context already names "Halstead & Cruz Matter Calendar / Practice-Management System", rewrite by hand (drop the adjacent descriptor, e.g. "…the Halstead & Cruz Matter Calendar / Practice-Management System")
- Med/Reyes/admit_2025-1018.pdf: A2, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/admit_2025-1018.pdf: A2, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/admit_2025-1018.pdf: A2, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/admit_2025-1018.pdf: A2, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/bills_billed.pdf: A0431, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/bills_billed.pdf: A0436, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/bills_billed.pdf: A0398, not in the ④ registry, real invoice/room/part code? left unchanged
- Med/Reyes/bills_billed.pdf: A0225, not in the ④ registry, real invoice/room/part code? left unchanged
- Shared/City/property_claim_0202.pdf: A58, context already names "City of Rivergate Light-Standard Repair Invoice", rewrite by hand (drop the adjacent descriptor, e.g. "…the City of Rivergate Light-Standard Repair Invoice")
- Shared/Police/scene_photos_2025-1018.pdf: A01, context already names "Police Traffic Collision Report", rewrite by hand (drop the adjacent descriptor, e.g. "…the Police Traffic Collision Report")

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Executive Summary, course-and-scope sentence | The course-and-scope determination is therefore that Operator Keeler was operating his assigned Owl Route 512 block at the time of the collision, consistent with the official run schedule and AVL/GPS telemetry. | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Passenger disposition table | See APC/farebox export (A11) and on-scene EMS run sheets for the passenger roster, injury dispositions, and transport destinations. | → | See the APC/farebox export for the passenger roster and Rivergate Police Department Traffic Collision Report No. TC-2025-1018, Section III, for injury dispositions and transport destinations. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Timeline table, EMS triage row, Source column | RPD TC-2025-1018 §IV; EMS run sheets | → | RPD TC-2025-1018 §IV |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | Section 1, item (ii) | and course-and-scope determination, which places Operator Keeler within the scope of his employment on his assigned Owl Route 512 block at the time of the collision | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | Section 2, Liability Assessment | The Director of Safety's internal investigation finds -- and the Fall 2025 Sign run schedule, the AVL/GPS track from Bus #4177, the Division 3 duty roster, and Operator Keeler's bid award (Owl Sr. Board Line 12) uniformly confirm -- that Operator Keeler was on his assigned Route 512 block on the run of record at the time of the collision. A preliminary off-book characterization circulating in the early hours after the collision is not supported by the operational records and does not control. | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | Section 2, Liability Assessment | On these facts the District's respondeat superior exposure attaches under Gov. Code Section 815.2, and a course-and-scope defense is not viable. | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | Section 4, Basis and limitations | the 11/21/2025 within-scope determination, and | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 2, Course and scope paragraph | Respondeat superior looks solid. ... We anticipate the District will attempt to characterize the overnight run as off-book ... Under Gov. Code Section 815.2, vicarious liability against the District should attach. | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 5, Calendaring | MatterHub deadlines module (A62) | → | MatterHub deadlines module |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | doc_id column, all rows | doc_id column reused spec artifact IDs A01-A57 | → | doc_id column renumbered to PT-01 through PT-22 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | PT-07 notes | held pending completeness review with the ACTD Final Incident Report/the Owl Route 512 Run Schedule/the AVL / GPS Route Track/the Route 512 Owl Block Bid Award Notice | → | held pending completeness review with the Final Incident Report, the Owl Route 512 Run Schedule, the AVL/GPS Route Track, and the Route 512 Owl Block Bid Award Notice |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | RL-2025-0090 notes | opening note (A42) | → | the Junior Adjuster Liability Note |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | RL-2025-0110 notes | reserved separately per A43 | → | reserved separately per the Senior Claims-Manager Reserve Memo |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/City/property_claim_0202.pdf | page 3 | itemizing the $48,500.00 cost of repair (Artifact A58). | → | itemizing the $48,500.00 cost of repair. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/scene_photos_2025-1018.pdf | page 1 header table | Case Reference (RPD): TC-2025-1018 (Cross-ref: Matter A01) | → | Case Reference (RPD): TC-2025-1018 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/scene_photos_2025-1018.pdf | page 1 header table | Controlling Time of Incident: 02:05 a.m. | → | Time of Incident: 02:05 a.m. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | Section 4.3, Reporting of Results | A confirmed alcohol concentration of 0.02 g/210L or greater is a positive DOT alcohol test for purposes of 49 CFR Part 655. | → | A confirmed alcohol concentration of 0.04 g/210L or greater is a positive DOT alcohol test for purposes of 49 CFR Part 655. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Passengers/claims_0118.pdf | Notice and Signature section, both claim forms (Cho and Mowbray) | up to four years in state prison and/or a fine of up to $10,000 | → | imprisonment under Section 1170(h) and/or a fine of up to $10,000 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | core properties | creator: openpyxl | → | creator: R. Delcourt |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | 2 event rows | ACTD-IR-2025-1018-001 | → | ACTD-IR-2025-1018 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | row 8 | PT-07 notes field unquoted, 13 CSV fields | → | PT-07 notes field quoted, 10 CSV fields |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | PT-16 first_pass_tag | Produce (CCP Section 2017.210) | → | Produce |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | final row | TOTAL,ALL PROVIDERS (9),... aggregate row | → | (deleted) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Fleet/maintenance_log_bus4177.csv | new final row | (no 10/18/2025 entry) | → | WO-077311 post-collision inspection row added |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Vehicle paragraph, Section 4 | is reconciled to the Div. 3 pre-trip yard sheet, the fleet dispatch log, and the Fleet Maintenance daily assignment record | → | is reconciled to the Div. 3 duty roster and the fleet dispatch log |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Section 7, Course-and-Scope Determination | the Div. 3 pre-trip yard sheet, the fleet dispatch log, the daily block assignment sheet, and / reconciles to the Div. 3 pre-trip yard sheet, the fleet dispatch log, and the daily block assignment sheet | → | the Div. 3 duty roster, the fleet dispatch log, and / reconciles to the Div. 3 duty roster and the fleet dispatch log |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Timeline table row 1, Source column | Duty roster; pre-trip yard sheet | → | Duty roster |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | page 3, closing banner | SEE ATTACHED MEMORANDUM OF COVERAGE FORM | → | SEE MEMORANDUM OF COVERAGE FORM |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | page 3, authorization block | 2 blank signature lines | → | /s/ Ellen J. Whitmore ; /s/ Gordon Espinoza |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CrimeLab/BAC_Keeler.pdf | page 3, certification blocks | 2 blank Signed: lines | → | /s/ Alan Whitford ; /s/ Loretta M. Ainsley |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | page 10, jury demand signature | By: (blank) | → | By: /s/ Nora Halstead |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | page 12, proof of service | (blank signature) | → | /s/ Grace Chen |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Criminal/Plea_Keeler.pdf | page 6, judgment/certification/filed blocks | 3 blank signature/deputy lines | → | /s/ Marion T. Escamilla ; /s/ J. Ontiveros (x2) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/City/repair_invoice_0202.pdf | page 2, prepared-by/approved-by | 2 blank signature lines | → | /s/ Halden R. Voss ; /s/ Marguerite E. Sandoval |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/RFP_set.pdf | pages 12 and 14 | By: (blank) / (blank signature) | → | By: /s/ Nora Halstead ; /s/ Grace Chen |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_grant.pdf | page 5 | judge and deputy-clerk blanks | → | /s/ Beatrice N. Halloway ; By: /s/ R. Castellanos, Deputy Clerk |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_term.pdf | pages 7 and 10 | judge, deputy-clerk, and physician declaration blanks | → | /s/ Beatrice N. Halloway ; By: /s/ R. Castellanos, Deputy Clerk ; /s/ Helena Vasquez-Ortiz, MD |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/rejection_0218.pdf | pages 1-3 | 3 blank signature lines | → | /s/ Marcia P. Ainsworth ; /s/ Gordon Espinoza (x2) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | Approved section | 2 blank approval signatures | → | /s/ Patricia Kwan ; /s/ Marlene Okonkwo |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | signature block | (blank signature) | → | /s/ Gordon Espinoza |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | pages 2 and 4 | affixed to form? Yes -- Attachment A / Attachment B / Attachment C labels | → | Retained in file / Retained - labels (no physical-attachment claim) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | word/comments.xml | (no comments part) | → | supervisor-review comment added, anchored to DRAFT banner paragraph |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/matter_calendar_MatterHub.csv | row late_claim_45_day [T3 Gov Code 911.6(b)(5) finding: filing date pushed 05/15/2026->08/07/2026 so real-law (b)(5) partial-incapacity ground is genuinely considered and correctly foreclosed by its own 6-month tail (08/05/2026), preserving relief-materially-at-risk design] | late_claim_45_day deadline_date=06/29/2026; entered/modified=05/15/2026 | → | late_claim_45_day deadline_date=09/21/2026; entered/modified=08/07/2026 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/matter_calendar_MatterHub.csv | row 946.6_petition [cascades from late-claim filing date shift to 08/07/2026] | 946.6_petition deadline_date=12/29/2026; entered/modified=05/15/2026 | → | 946.6_petition deadline_date=03/21/2027; entered/modified=08/07/2026 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/matter_calendar_MatterHub.csv | new row inserted before late_claim_45_day [genuine acknowledgment of real Gov Code 911.6(b)(5) partial-incapacity ground per T3 finding; six-month tail runs from conservatorship-termination/capacity-restoration date 02/05/2026] | (row did not exist) | → | 911.6(b)(5)_tail deadline_date=08/05/2026, statutory_basis=Gov. Code Sec 911.6(b)(5) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/claims_tracker.csv | row ACTD-2026-0119 (Reyes), notes field [T3 Gov Code 911.6(b)(5) finding: cascades filing-date shift and records genuine acknowledgment that (b)(5) is real law and correctly foreclosed] | notes: ...filed 05/15/2026...45-day deemed-denial point 06/29/2026... | → | notes: ...filed 08/07/2026...911.6(b)(5) partial-incapacity ground addressed and unavailable, filed after its 08/05/2026 six-month tail...45-day deemed-denial point 09/21/2026... |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/late_claim_app.pdf | DATE FILED block p.1; Sec II presentation-timeliness bullets/paragraphs pp.5-6,8; declaration signature block and dated line p.9; proof of service p.10 [T3 Gov Code 911.6(b)(5) finding: filing date pushed past the (b)(5) six-month tail (08/05/2026) so that ground is genuinely considered and correctly ruled out, preserving relief-materially-at-risk design; court filing itself does not argue (b)(5) since it does not help the applicant] | May 15, 2026 (9 occurrences: pages 1,5,6,8,9x2,10 as printed) | → | August 7, 2026 (same 9 occurrences) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | para 27 (Incapacity ground under 911.6(b)(4)) [911.6(b) actually enumerates six grounds ((1) excusable neglect, (2)-(3) minor, (4)-(5) incapacity, (6) death), not four; numeric correction] | the Board is directed by Gov. Code Sec 911.6(b) to grant the application on any of four enumerated grounds | → | the Board is directed by Gov. Code Sec 911.6(b) to grant the application on any of six enumerated grounds |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | column inserted before 'payer'; one row per provider (RRTC-001, ACNRI-001, SKY-001, RAD-001, ANES-001, NSG-001, TSG-001, ASH-001, HBC-001) carries that provider's EOB-stated Patient Resp. total [Reyes_lien_EOB.pdf Exhibit A separately reports Patient Resp. ($3,200, all documented as paid) distinct from Contractual Adj./Write-off ($2,640,800); ledger's adjustments column was silently absorbing the paid patient-responsibility amount, contradicting the EOB's own notes that no provider has an outstanding patient-owed balance] | no patient_responsibility column; adjustments totaled $2,644,000 (silently included $3,200 patient-responsibility paid amount) | → | added patient_responsibility column (total $3,200, one representative row per provider per Reyes_lien_EOB.pdf provider totals); adjustments reduced to $2,640,800 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/HIPAA_auth.pdf | page 1 Section 3; page 3 Section 14 [form was signed and dated 02/10/2026 naming Halstead & Cruz as recipient, but the firm's own records (late_claim_app.pdf paragraph 10, life care plan) place retention at 03/05/2026 -- a pre-engagement/hindsight conflict. Retargeting the recipient to Reyes herself (self-request) is consistent with Section 6's existing purpose language ('at my own request') and avoids cascading the date into the other documents that narrate this milestone] | Section 3 (Recipient) and Section 14 (Form Return) both named: Halstead & Cruz LLP, Attn: Nora Halstead, Esq., 88 South Grand Avenue Suite 2400, Los Angeles CA 90071, (213) 555-0170 | → | Section 3 and Section 14 both changed to: Yolanda M. Reyes (self - records requested for personal use), 612 Poplar Street, Rivergate, CA 91766, (626) 555-0187 (her own address/phone already given in Section 1) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/TC_2025-1018.pdf | page 2, narrative field [world spec defines Alder Creek Transit District (ACTD) as the sole transit entity ('the District'); MTA is never introduced elsewhere -- unexplained second transit-org label, naming drift] | Standing at posted MTA/ACTD bus stop, east side of S. Main Street... | → | Standing at posted ACTD bus stop, east side of S. Main Street... |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/scene_photos_2025-1018.pdf | page 5, photo log row P-043 [same MTA/ACTD naming-drift fix as police report; em dash also flattened to plain hyphen to avoid base-14 font encoding substitution] | P-043 Description: Bus-stop platform (em dash) overview; shelter, posted MTA/ACTD bus-stop signage, concrete pad, and impact zone at south end of shelter where the bus came to rest. | → | P-043 Description: Bus-stop platform - overview; shelter, posted ACTD bus-stop signage, concrete pad, and impact zone at south end of shelter where the bus came to rest. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Fleet/maintenance_log_bus4177.csv | rows WO-072889, WO-074761, WO-077022 (description field) [49 CFR 396.25 is 'Qualifications of brake inspectors' (what a qualified inspector must know/do), not a source of lining-thickness/leak-down/slack-adjuster/pass-fail thresholds; those performance specs are governed by 49 CFR 393.47 (brake actuators, slack adjusters, linings/pads, drums/rotors) and Part 396 Appendix A (Minimum Periodic Inspection Standards)] | Air-brake inspection per 49 CFR 396.25: [lining thickness / leak-down / slack-adjuster / warning-test specs] | → | Air-brake inspection per 49 CFR Part 396 App. A / Sec 393.47: [same specs] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/claims_tracker.csv | rows ACTD-2026-0114, ACTD-2026-0115 [WORLD_SPEC canonical value "Passengers' suit-filing deadline" (Type=Fact, 08/18/2026, derived from A39's 02/18/2026 rejection mailing + Gov. Code 945.6(a)(1) six-month clock) declares Must-match=A14 (this claims tracker); A14's own spec description says its purpose is tracking a computed deadline field, but the field was blank -- flagged by spec_check.py ties. A39 (rejection_0218.pdf) correctly stays untouched: real Gov. Code 913 rejection notices recite the statutory six-month boilerplate rather than a pre-computed date, and the spec lists only A14 (not A39) as a match target, consistent with A39 supplying the inputs to derive from rather than the computed output] | Cho (ACTD-2026-0114) and Mowbray (ACTD-2026-0115) rows: suit_filing_deadline blank, deadline_basis='see rejection notice' | → | suit_filing_deadline=08/18/2026, deadline_basis='Gov. Code § 945.6(a)(1) - 6 mo. from rejection mailing' for both rows |

## manual edit + pdf_replace.py

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | pages 7-16 (0-idx 6-15): Personal Care Attendant Hours table, Annual Cost Summary table, para 28-30 (Total Undiscounted), Present Value Analysis paras 35-38, both sensitivity tables [AutoQC round-4 finding: life care plan miscomputes its own annual-cost table figures. Verified via WebSearch-independent arithmetic that AutoQC's proposed $173,650.82 could not be reproduced from the document's own line items even after finding and fixing the one genuine per-line error (attendant-care overhead); adopted the honestly-verified $177,843 total instead, which is the exact sum of all 13 category subtotals with zero padding needed once the overhead error is corrected] | Attendant-care payroll overhead stated $11,337 (not 11% of the $98,912 wage base, which is $10,880.32); category subtotals summed to $178,300 but a $1,700 unexplained 'rounding/geographic-pricing adjustment' padded the headline to exactly $180,000; downstream undiscounted ($6,480,000) and PV ($4,240,000 and full sensitivity table) all compounded from that padded figure | → | Fixed the payroll overhead to $10,880 (verified 11% of $98,912); removed the $1,700 padding (rounding adjustment now $0); attendant-care subtotal $109,792; verified all 12 other category subtotals foot correctly to their own line items (all correct, no changes); new total weighted annual average $177,843 (exact sum of all 13 corrected category subtotals, no padding needed); recomputed undiscounted ($6,402,348 = $177,843 x 36) and PV at 2.0/2.5/3.0% x 30/36/40-yr horizons throughout using the document's own stated formula and rounding convention |

## manual edit (python-docx)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | paragraph 28 (new), between the existing (b)(4) paragraph and the Internal Presentation Target heading [Round 4/5 finding: world omits Gov. Code 911.6(b)(5), a real, on-point statutory ground, which materially distorts the claim-presentation analysis. Verified via WebSearch this is real law (confirmed exact statutory text and the Harrison citation). Anchor date (06/18/2026) makes it mathematically impossible for any pre-anchor filing to be time-barred under (b)(5) given the fixed capacity-restoration facts, so the filing-date-shift approach tried in round 4 could never have worked; the causation argument (grounded in existing retention-timeline facts already in the world) is what actually preserves the world's 'relief materially at risk' design while being legally honest and complete. Placed in this internal, privileged case-strategy memo rather than the filed application (late_claim_app.pdf) since Reyes's own counsel would not voluntarily flag a weakness in her own alternative ground in a document filed to persuade the Board] | Paragraph 27 discusses only the (b)(4) incapacity ground; the memo never mentions the partial-incapacity ground under Gov. Code 911.6(b)(5), despite already noting the Board has six enumerated grounds available | → | Inserted a new paragraph after the (b)(4) discussion candidly addressing (b)(5): notes it is facially available and not time-barred, but explains the firm is not relying on it because the same causation gap that weakens the (b)(1) excusable-neglect argument (46 days of retained counsel remaining when the window closed) likely also defeats reliance on (b)(5), citing Harrison v. County of Del Norte (1985) 168 Cal.App.3d 1 |

## manual edit (python csv)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | all data rows, columns review_status and final_call [AutoQC P0 finding: production tracker supplies final discovery-disposition answers, violating No Solution Or Reasoning Leakage for T9. A17's own spec description says it carries system tags 'pending attorney review' and Trap Content explicitly calls it 'only a first-pass, uncorrected index' -- the pre-task state should show nothing as attorney-confirmed. T9's Expected Output requires the solver to correct A42's status themselves as part of the deliverable, which is impossible if the tracker already shows a confirmed final call. Preserves the A42/A43 (PT-13/PT-14) trap intact -- first_pass_tag still shows PT-13 tagged Withhold-Privileged on the strength of its face legend alone, which is what the solver must independently overturn via CCP 2018.030 analysis] | review_status/final_call showed Confirmed/Produce, Attorney-confirmed/Withhold-Privileged, or First-pass/Withhold-Privileged for all 22 rows except PT-07, presenting final attorney-confirmed production/privilege outcomes for every document including PT-13 (A42, the junior adjuster's note) and PT-14 (A43, the senior reserve memo) -- the exact privilege calls T9 requires the solver to independently derive | → | review_status='Pending attorney review', final_call='TBD' for all 22 rows, matching PT-07's existing pre-decision template. first_pass_tag, producer_initials, log_entry, and notes columns unchanged |

## manual edit (python csv)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/AVL_GPS_track_2025-1018.csv | rows timestamp_local 2025-10-18 02:05:00 through 02:05:12, column heading_deg [AutoQC finding: collision trip direction cannot be reconciled across files. The final incident report (A02, no trap of its own, controlling record) and dispatch log both describe Bus 4177 as northbound on S. Main Street at the collision point, having departed Poplar at 02:04 on Trip 06 (NB per the run schedule's own trip roster). A12 (AVL/GPS) is declared in the spec as carrying no trap of its own and existing specifically to corroborate A08/A02 course-and-scope, not contradict it. A heading of 181-188deg reads as south-southwest, contradicting the northbound narrative used everywhere else, and the incident report's own mechanism description (no swerve, no braking, continued straight) rules out a real ~180deg heading reversal in the 12 seconds before impact. Speed decelerating 24.6 to 0.0 mph over that window is consistent with a straight-line collision, not a turn] | heading_deg = 181,182,183,184,186,188 at the six 02:05:00-02:05:12 breadcrumbs (the collision window), reading as south-southwest | → | heading_deg = 0 at all six breadcrumbs, continuing the constant 0 (north) heading held for the preceding ~5 minutes of accelerating travel (02:00:00-02:04:48) |

## manual edit (openpyxl)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | sheet 'Route 512 Owl Block', cells J25, A34, B34, C34, D34, A35 [Same root cause as the AVL heading fix: this mislabeled 'SB reference' entry (which does not correspond to any real trip's actual schedule) is what the dispatch log's 02:06 entry echoed, and together they were the source AutoQC flagged as an unreconcilable direction/routing conflict. A08 (this schedule) is the canonical source for the course-and-scope fact and carries no trap of its own -- nothing in the trap manifest protects this entry, so it is a genuine, correctable defect] | Trip 06 roster row's S. Main/Third cell read '02:05 (SB timepoint pass) / 02:31'; a separate Key Timepoint block described a '06 (SB pass, mid-loop reference)' row at '10/18/2025 02:05' labeled 'Southbound reference pass at S. Main / Third', which does not match trip 05's own actual SB passage (01:31 per its own roster row) or trip 06's own NB designation | → | Trip 06 roster cell now reads '02:31' only. Key Timepoint block corrected to '06 (NB, primary reference)' / 'Northbound revenue pass at S. Main / Third' / '10/18/2025 02:31', with notes and the trailing timepoint-reference sentence rewritten to consistently describe the real northbound 02:31 passage |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | row timestamp 10/18/2025 02:06 [Same SB/NB mislabeling as the schedule workbook fix; the 02:05 time itself is correct (matches the real collision time and AVL breadcrumbs) and was left unchanged, only the incorrect southbound/02:05-timepoint characterization was corrected] | 02:06 radio_call entry parenthetical read '(SB reference timepoint 02:05)' | → | parenthetical now reads '(Trip 06 northbound, en route to the 02:31 timepoint)' |

## pdf_replace.py + manual edit (2 passages needed hand redaction due to reflow-fit and multiline ambiguity)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | pages 2-4 (0-idx 1-3): paragraphs 2 and 3, section 5 heading, closing enclosures line [AutoQC finding: EOB package declares but omits Exhibit A and Tabs 1-11. Verified Exhibit A itself is NOT actually missing -- the provider-level reconciliation table (billed/adjustment/paid/patient-resp by provider, with totals) is printed inline on pages 2-3 of this same letter, so that half of the finding was a false read of the document. Tabs 1-11 (individual raw EOB backup packets and lien correspondence) genuinely do not exist in the world and the letter's 'enclosed'/'Enclosures' language affirmatively claimed physical inclusion, unlike a realistic 'available on request' convention -- that part of the finding was real and is fixed here] | Letter affirmatively claimed 'corresponding EOBs at Tabs 1-9', DHCS's letter 'enclosed at Tab 10', BlueShield's confirmation 'enclosed at Tab 11', a '5. Enclosure Index (Tabs)' section, and a closing 'Enclosures (Exhibit A; Tabs 1-11)' line -- none of Tabs 1-11 exist anywhere in the mounted filesystem | → | Reworded all Tab enclosure claims to 'available on request'; renamed section 5 to 'Supporting Documentation Index (Available on Request)'; closing line now reads 'Enclosures (Exhibit A)' only |

## git restore from commit e8df618

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | entire document -- all pages carrying the annual/undiscounted/PV figures [SELF-CORRECTION. Round 6 AutoQC flagged that these figures now contradict WORLD_SPEC.xlsx's Canonical Values sheet, which explicitly declares $180,000/$6,480,000/$4,240,000 as A36's authoritative figures -- and $6,480,000 is marked Type=Trap (the undiscounted lure meant to test whether the solver correctly uses the PV instead). Checking git history confirmed round 1 (a prior session) had ALREADY correctly identified this exact footing issue, checked it against the spec, and fixed it by adjusting three line items (attendant overhead, contingency, rounding) to preserve the canonical $180,000 total -- precisely the values I mistakenly treated as bugs and 're-corrected' in round 5 without checking the spec first. Round 5's fix is now understood to have been the error, not the original figures. Lesson: always check WORLD_SPEC Canonical Values / spec_check.py ties BEFORE treating a source artifact's own arithmetic as authoritative over a stated canonical value] | Round 5 changed this file's annual/undiscounted/PV figures to $177,843/$6,402,348/$4,189,000 (a bottom-up arithmetic recalculation), without checking the WORLD_SPEC.xlsx Canonical Values sheet first | → | Reverted to the round-1 fixed state (git commit e8df618): $180,000 annual / $6,480,000 undiscounted / $4,240,000 PV throughout, including the attendant-care overhead ($11,337), contingency ($6,540), rounding adjustment ($1,700), and full sensitivity table, all restored to match |

## manual edit (PyMuPDF redaction)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | page 1 (ToC) and page 18 (closing Attachments list) [AutoQC re-flagged this in round 6 despite round 5's dispute -- confirms 'available on request' wording is not accepted as resolving a named-but-unresolvable supporting-document reference. None of these 5 items are needed by any task; removing the itemized list (rather than continuing to soften its wording) is the only Rule-1-compliant fix that doesn't fabricate 5 new files] | Table of Contents and closing page listed 5 numbered Attachments (both experts' CVs, documents-reviewed index, pricing sources, year-by-year PV schedule) as 'available on request' | → | Removed the Attachments section and its ToC entries entirely; report now ends with the Present Value Analysis, Dr. Frome's signature block, and 'End of report.' |

## manual edit (PyMuPDF redaction)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | pages 3-4 (0-idx 2-3) [Same reasoning as the life-care-plan fix -- round 5's 'available on request' rewording of the same content was re-flagged in round 6, confirming that wording alone doesn't resolve a named-but-unavailable reference. The narrative Exhibit A discussion and its reconciliation table remain untouched since that content is genuinely present in the letter] | Section 5 'Supporting Documentation Index (Available on Request)' itemized Tabs 1-11 by name | → | Removed the itemized Tab 1-11 index entirely (both the section on page 3 and its continuation on page 4); section 6 Reservation now follows directly |

## manual edit (PyMuPDF redaction) + pdf_replace.py (renumber)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/FST_supplement_2025-1018.pdf | page 4 (0-idx 3) [Same class as the life-care-plan and EOB attachment findings this round -- an itemized, named list of unmounted supporting materials. None of these 4 items are needed by any task (their substance -- the 0.11% PAS result, the calibration date -- is already stated inline in the supplement's own body)] | Section 11 'Attachments to This Supplement' itemized 4 items (field notebook pages, PAS log entry, PAS accuracy-check certificate, blood-draw chain-of-custody form) none of which are mounted; section 12 was Officer Certification | → | Removed section 11 (Attachments) entirely; renumbered Officer Certification from 12 to 11 to keep sequential section numbering |

## manual edit (PyMuPDF redaction)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | page 3 (0-idx 2), closing footer below the authorization signatures [Missed this on the round-5 dispute pass -- I had only checked the ITEM 11 Schedule of Forms and Endorsements table (a standard, neutral insurance-declarations convention I still believe is not a broken reference) and missed this separate footer line, which does affirmatively instruct the reader to go see a document that does not exist in the world. The ITEM 11 schedule table itself is left untouched] | Closing footer overlapped 'END OF DECLARATIONS -- SCPERA-MOC-100 (07/23) FOR GENERAL TERMS AND CONDITIONS' with a second text run reading 'SEE MEMORANDUM OF COVERAGE FORM' -- an explicit pointer to a governing MOC document not mounted anywhere in the world | → | Removed the 'SEE MEMORANDUM OF COVERAGE FORM' text run; footer now reads cleanly as 'END OF DECLARATIONS -- SCPERA-MOC-100 (07/23) FOR GENERAL TERMS AND CONDITIONS', a plain form-identification stamp with no reader-facing instruction to go find another document |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | rows PT-13 and PT-14, notes column [AutoQC P0 finding: production tracker's first_pass_tag column, together with the privilege rationale in notes, collapses T9's required CCP 2018.030 analysis. Round 5 already neutralized review_status/final_call; this round removes the two notes phrases that pre-package the actual legal reasoning (why A43 is privileged, and a hint that A42's tag might not be reliable) rather than leaving that inference for the solver to draw from A42/A43 themselves. first_pass_tag values are left as-is (still Withhold-Privileged for both A42 and A43, matching their identical face legends) since T9's own Expected Output requires the solver to correct an existing tag value as part of the deliverable, and A17's spec description defines it as a raw, pre-review system tag] | PT-13 notes said 'first-pass tag follows the legend on the face' (meta-commentary flagging the tag as face-value-only); PT-14 notes said 'Prepared at direction of counsel post-course-and-scope finding and post-BAC report' (restates the CCP 2018.030 privilege standard's own language as an established fact) | → | PT-13 notes now end at the legend description plus RFP numbers; PT-14 notes now open with 'Routed to General Counsel and outside defense counsel' (a plain administrative fact) plus RFP numbers |

## manual edit (PyMuPDF redaction) after WebSearch verification

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | page 3 (0-idx 2), STEP 7 DER RECEIPT block [Verified via WebSearch: 49 CFR 655.53 is titled 'Supervisor acting as collection site personnel' and governs a conflict-of-interest rule during sample collection, unrelated to a DER's completeness review of a finished test record. 655.71 (Retention of records) is the real, on-point Subpart H administrative-requirements authority for a DER receiving and filing a completed record] | Received by ACTD Office of Compliance & Safety Assurance and reviewed for completeness under 49 CFR § 655.53. | → | Received by ACTD Office of Compliance & Safety Assurance and reviewed for completeness under 49 CFR § 655.71. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | row timestamp 10/18/2025 02:06 [SELF-CORRECTION -- my own round-5 edit to this message introduced the internal comma without quoting the field, breaking the file's column count. AutoQC caught it this round] | 02:06 radio_call message field was unquoted, and the comma introduced by round 5's edit ('...northbound, en route...') split it into 7 fields against a 6-column header | → | Wrapped the complete message field in double quotes, matching the quoting convention already used by other multi-clause messages in this file (e.g., the 02:07 emergency_dispatch row) |

## manual edit (openpyxl)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | sheet 'Authorized Owl Routes', cells A7:A12 and F7:F12 [Two AutoQC findings: Format-Native Feature Fidelity (status field not visually distinct) and Text Legibility And Contrast (gold route numbers on beige rows measured ~2.9:1, confirmed by independent WCAG relative-luminance calculation matching AutoQC's reported ratio exactly). Applied the darker gold uniformly across all 6 rows (not just the 3 beige ones) to avoid two different shades of the same data column looking like an inconsistency] | Sheet 'Authorized Owl Routes': F7:F12 'Authorized' status cells carried the same alternating white/beige (00FFFFFF/00F5F2EB) fill as neighboring data cells with no conditional formatting; A7:A12 route numbers used gold font 00B8862B, which measures ~2.9:1 contrast against the beige striped rows (A8/A10/A12), below the 3:1 minimum for bold text | → | F7:F12 now carry a light-green fill 00C6EFCE (Excel's standard 'Good' status color) behind the existing dark-green bold font, giving Authorized a distinct at-a-glance encoding. A7:A12 route-number font darkened to 008A6420 (verified 4.79:1 against the beige fill and 5.35:1 against white, both clearing WCAG AA 4.5:1) |

## metadata_hygiene.py clean + manual XML patch (zipfile) as final step

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | workbook core properties (docProps/core.xml, docProps/app.xml) [SELF-CORRECTION. My own round-6 hand-save via openpyxl (for the status-color/contrast fix) reset this file's creator, and metadata_hygiene.py's clean pass -- discovered this round to actively blank creator/lastModifiedBy for xlsx rather than preserve or set them -- could not restore it either. Fixed by setting creator/lastModifiedBy directly in the XML as the final step after running hygiene clean, so nothing overwrites it afterward. Round 2 had this correctly set to R. Delcourt; that is the same value restored here] | Workbook core property creator='openpyxl' (a generic library fingerprint, not in-world provenance) | → | creator='R. Delcourt' and lastModifiedBy='R. Delcourt' (the workbook's own Manager of Scheduling, per its Assignment Sign-Off block: 'Approved by: R. Delcourt, Manager of Scheduling'), Application restored to 'Microsoft Excel', modified date restored to the in-world 2026-06-18 convention |

## pdf_replace.py (initial, corrupted) + manual redaction fix (PyMuPDF)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Video/onboard_video_still_log.pdf | page 5, still-frame entry 041 (timestamp 02:05:04.150, CAM-01) [First pdf_replace.py pass introduced the same font-mismatch and curly-apostrophe-as-middle-dot corruption seen earlier this session; fixed by redacting and redrawing the complete line as one clean Times-Roman unit] | Page 5 said 'Cho's torso strikes seatback ahead of him', conflicting with TC_2025-1018.pdf's listing of Occ-1 Devin Cho as sex F and other records' 'Ms. Cho' usage | → | 'ahead of her', matching Cho's established gender elsewhere in the world |

## pdf_replace.py + manual redaction fixes (two edits needed hand repair after pdf_replace.py introduced font/overlap corruption)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | pages 7, 8, 15, 16, 17 (0-idx 6,7,14,15,16) [AutoQC finding: sensitivity table miscomputes PVs against its own formula -- this has apparently been wrong since round 1 and was carried forward unnoticed when round 6 reverted the file to match the spec's canonical annual/undiscounted/PV figures (which only cover the single 36yr/2.5% adopted figure, not the sensitivity table). Separately caught during this fix: three more Attachment N references that round 6's removal of the Attachments section missed, since they're inline body-text mentions rather than part of the removed section itself] | Sensitivity table: 2.0%/36yr=$4,592,000, 2.0%/40yr=$4,929,000, 2.5%/30yr=$3,766,000, 2.5%/40yr=$4,517,000, 3.0%/36yr=$3,921,000, 3.0%/40yr=$4,153,000 -- all six wrong relative to the document's own stated formula PV=C*[(1-(1+r)^-n)/r]. Also three body-text references to Attachment 3/4/5 (documents-reviewed list, pricing sources, year-by-year PV schedule) left dangling after round 6 removed the Attachments section itself | → | Recomputed all six sensitivity cells from the stated formula (verified independently, matches AutoQC's proposed figures exactly): 2.0%/36yr=$4,588,000, 2.0%/40yr=$4,924,000, 2.5%/30yr=$3,767,000, 2.5%/40yr=$4,518,000, 3.0%/36yr=$3,930,000, 3.0%/40yr=$4,161,000. Removed the three dangling Attachment 3/4/5 references (documents-reviewed list mention, pricing-sources mention, and the sensitivity-table PV-schedule parenthetical) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | rows RL-2025-0087 and RL-2025-0104, reserve_amount column [AutoQC P0 finding: reserve ledger contradicted the canonical values (Initial reserve=$250,000 Type=Trap, Controlling reserve=$3,250,000 Type=Fact, both Must-match=A16/this ledger) and the internally authored adjuster_note.docx ('opening the file at an initial indemnity reserve of $250,000') and reserve_memo.docx ('raise... from the initial $250,000... to $3,250,000'). Not an intentional stale-vs-controlling variation -- both narrative sources and the spec agree on the same two figures the ledger was missing] | RL-2025-0087 (initial Reyes indemnity) = $190,000; RL-2025-0104 (controlling Reyes indemnity) = $3,150,000 | → | RL-2025-0087 = $250,000; RL-2025-0104 = $3,250,000 |

## manual edit (python-docx)

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | paragraph 64, Attachments and Referenced Records list [AutoQC finding: only roster_2025-1018.csv is mounted; no pre-trip yard sheet exists anywhere in the world] | Attachments list bullet: 'Div. 3 duty roster and pre-trip yard sheet, 10/17/2025.' | → | 'Div. 3 duty roster, 10/17/2025.' (pre-trip yard sheet claim removed) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | rows PT-06, PT-08, PT-09, PT-19 [AutoQC finding: production tracker references absent export and native-media deliverables. Distinct from the round-4 onboard-video dispute, which was about being asked to fabricate the actual missing MP4 file -- Rule 1 correctly barred that. This is the opposite direction: correcting the tracker's own false claim that a native MP4 already exists, which is a legitimate replace-not-add fix. The new PT-19 wording is also more consistent with T7's actual design (the onboard video sits on a short vendor retention loop that has not yet been formally preserved/retrieved, which is precisely the urgency T7's preservation-hold task is built around)] | PT-06/PT-08/PT-09 descriptions claimed a 'PDF export' or 'map export' alongside the native file (none mounted); PT-19 claimed '(native MP4)' and a native-MP4 Bates-equivalent entry in log_entry, though no MP4 exists anywhere in the world | → | PT-06/08/09 descriptions trimmed to the native format that actually exists (native XLSX / native CSV / native CSV respectively). PT-19 reworded to 'Onboard video incident still-frame log -- Bus #4177 (native clip retained by vendor, not yet retrieved)', and its native-MP4 log_entry claim removed |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/hold_demand_letter.pdf | page 2, section preceding item 1 list [round7 t03: causal-order hindsight, letter dated 3/20/2026 reported a 5/15/2026 filing as already complete] | a late-claim application on behalf of Ms. Reyes was filed with the Board on 05/15/2026 | → | Ms. Reyes's presentation window closes 04/20/2026, after which late-claim relief under Government Code § 911.4 will be required on her behalf |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/hold_demand_letter.pdf | page 1, closing sentence of second paragraph [round7 t03 sweep: same hindsight defect unflagged on page 1, present-tense claimed the late-claim application already pending before a 5/15/2026 filing date] | Reyes's late-claim application under Government Code § 911.4 is pending before the Board | → | Reyes's late-claim relief under Government Code § 911.4 will be sought once her claim window closes 04/20/2026 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | §3.2 Non-Fatal Accidents, paragraph + (a)-(d) list deleted [round7 t04: 49 CFR 655.44(a)(2) makes nonfatal testing mandatory unless discounted, not conditional on injury/damage/hazmat/immovable-object thresholds; document invented citation and hazmat/immovable-object prerequisites not in the real rule] | cannot be completely discounted as a contributing factor, if: (a) disabling damage...tow truck; or (b) injury...and citation; or (c) hazardous materials release; or (d) disabling damage to other vehicle or immovable object | → | cannot be completely discounted as a contributing factor to the accident. Discounting...documented in writing by the DER or Compliance Officer |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | Rule 506, second sentence [round7 t04: same 655.44 mischaracterization as post_accident_testing_policy.docx - removed false citation prerequisite, restored discount-based mandatory testing rule] | Testing is required upon any accident meeting the Part 655 threshold...citation...injury...or disabling damage...tow truck or other vehicle. | → | Under Part 655, a qualifying accident is an occurrence involving loss of human life, or injury+medical treatment away from scene, or disabling damage+tow-away. For a fatal accident the operator is tested without exception; for a non-fatal accident, tested unless completely discounted. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | tables 0-3, header rows [round7 t06: dark-navy fill + no run-level color override = invisible text against Normal style's dark default] | table header/label cells (10 cells across 4 tables) filled #1B2A4E with no explicit run color, inheriting Normal's dark #333944 | → | same cells given explicit white (FFFFFF) run-level font color |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | table 1 (distribution list), header row [round7 t06: same dark-fill/no-override defect as IR_2025-1018_final.docx] | 'Role'/'Attorney/Staff' header cells filled #141A2E with no explicit run color, inheriting Normal's dark #4A5266 | → | same cells given explicit white (FFFFFF) run-level font color |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | Step 2, Basis for on-site collection [round8 P1: wrong pinpoint for the 8-hour alcohol testing window; correct subsection verified via ecfr.gov search] | 49 CFR § 655.44(b)(1)(ii) | → | 49 CFR § 655.44(a)(2)(ii) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | Step 3, confirmation-required sentence [round8 P1: § 40.251(b) is the confirmation-test waiting-period rule (different BAT step), not the >=0.02 confirmation-required trigger, which is § 40.247; § 40.253 (procedures) already separately cited in the next sentence] | per 49 CFR § 40.251(b) and § 40.253 | → | per 49 CFR § 40.247 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | Step 3, Employee observation period label [round8 sweep of citation-accuracy class: § 40.241 governs first steps of a screening test (begin without undue delay), not a 15-minute pre-test observation period, which is not a real DOT rule for the screening step at all] | (15-minute pre-test, § 40.241(b)) | → | (15-minute pre-test) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | Step 6, BAT certification paragraph [round8 sweep of citation-accuracy class: BAT certifies performing both the screening test (governed by Subpart L) and the confirmation test (Subpart M), but only Subpart M was cited] | in accordance with 49 CFR Part 40, Subpart M, and Part 655 | → | in accordance with 49 CFR Part 40, Subparts L and M, and Part 655 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Criminal/Complaint_Keeler.pdf | page 3, Enhancement D (Multiple Victims, Veh. Code 23558) [round8 P1 finding #2: the real statute is disjunctive (bodily injury OR death), verified via research; scenario has 3 injured victims and no deaths, so the conjunctive 'and' misstates the enhancement's actual trigger] | proximately caused bodily injury and death to more than one victim | → | proximately caused bodily injury or death to more than one victim |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | §3.2 Non-Fatal Accidents, opening sentence [round8 P1 Major: round 7's fix over-corrected by removing the real 49 CFR 655.4 accident-qualifying thresholds along with the fabricated ones, making it say every nonfatal accident (even a fender-bender) requires testing. Restored the genuine injury+medical-treatment-away-from-scene / disabling-damage+tow-away gate, matching how owl_service_rules.docx already correctly states it, while keeping the discount-based mandatory-testing rule.] | Following an accident that does not involve loss of human life, ACTD shall conduct... | → | Following an accident that does not involve loss of human life, in which an individual suffers bodily injury and immediately receives medical treatment away from the scene, or in which one or more vehicles incurs disabling damage and is transported away from the scene by a tow truck or other vehicle, ACTD shall conduct... |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Section 10, Attachments and Referenced Records, DriveCam bullet [round8 P1: A53's spec format is MP4 clip export + still-frame log but only the still-frame log PDF is mounted; reworded to match production_tracker.csv's PT-19 framing from round 7 rather than fabricate the missing MP4] | DriveCam video (forward-facing and cabin-facing), Bus #4177, 10/18/2025 01:59-02:07 (preserved). | → | DriveCam still-frame log (forward-facing and cabin-facing), Bus #4177, 10/18/2025 01:59-02:07; native clip retained by vendor under litigation hold, not yet retrieved. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Dispatch/tran_text_thread.pdf | entire file, replaced to match spec [round8 P0: built file directly contradicted A52's registry entry, and worse, resolved both the T5 course-and-scope trap and the T7 preservation-target point in prose within the artifact itself, collapsing the intended synthesis. Replaced with content matching the spec's verbatim quoted dialogue and stated time window; no generator script existed so rebuilt the PDF by hand matching the original's iMessage-export visual style] | 5-page, 32-message thread spanning 10/18-10/24/2025 that self-corrects the off-book claim ('so not off-book after all... Marlene... had already reconciled it') | → | 1-page, 3-message exchange, 10/18/2025 3:20-3:40am, repeating the uncorrected off-book characterization per A52's spec entry |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/HR/Keeler_DMV_record.pdf | throughout: header dates page 1, periodic-report dates + reference number page 3 [round8 P0: A54 registered as DMV record current as of 10/2025 but built dates were 08/14/2025; shifted all related dates by the same 2 months so the record stays internally self-consistent] | Record Extract/Print Date 08/14/2025, prior periodic report 08/14/2024, next scheduled 08/14/2026, reference H6-CA-20250814-047831 | → | 10/14/2025, 10/14/2024, 10/14/2026, reference H6-CA-20251014-047831 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 4, Government Claims Act Posture [round8 P0 Major: this paragraph (added in an earlier round to acknowledge (b)(5) per a prior finding) performs the exact comparative (b)(4)/(b)(5)/(b)(1) causation analysis and reaches the exact at-risk conclusion that T3's Design Purpose requires the solver to work out independently. A31's spec role is narrow (recite accrual date, window date, and the weak internal delay rationale as trap evidence), not the full legal synthesis. Deleted per Rule 2 (remove give-aways by deletion, not hedging); verified no other file references the deleted citation or analysis.] | paragraph: 'Partial-incapacity ground under 911.6(b)(5)...The same causation gap that limits an excusable-neglect argument under (b)(1) likely limits reliance on (b)(5) here.' | → | [paragraph deleted] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | paragraph 27, AVL/GPS Track section [round8 P1 Major (partial fix, partial dispute): the report falsely asserted the 02:05 AVL position was temporally coincident with the schedule's published control-point TIME (02:31 per RunSchedule_Owl512.xlsx) -- an outright internal factual error, not just a cross-document gap. Changed the claim from temporal ('coincident with...timepoint') to spatial ('at...location'), which is true and removes the false statement without touching the schedule itself or adding reconciling commentary] | at 02:05, coincident with the published S. Main / Third control-point timepoint for the Trip 05/06 turnaround pair. | → | at 02:05, at the published S. Main / Third control-point location for the Trip 05/06 turnaround pair. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Video/onboard_video_still_log.pdf | cover page, Vendor System Metadata table [round9 P1: an exact byte size and a computed SHA-256 hash are proof-of-possession markers that only exist once a file has actually been downloaded/exported; this contradicted the world's established 'preserved at vendor, not yet retrieved' framing (production_tracker.csv PT-19, IR bullet fixed round 8) and made the missing MP4's absence more conspicuous per AutoQC's finding] | Native Clip Size: 3,412,884,116 bytes; Native Clip SHA-256: 5b5b52667953dc1379b324d48454644350bb458d62ab721cdf7c8b05b72c5f23 | → | Native Clip Size: Not yet retrieved from vendor; Native Clip SHA-256: Not yet computed - native clip not yet retrieved |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 4, Government Claims Act Posture [round9 P0 Major, still failing after round 8's fix: this paragraph selected/concluded that the (b)(4) incapacity ground is available given the client's facts and listed supporting materials being assembled for it -- this is not part of A31's spec description (which only calls for noting the accrual/window dates and the weak internal delay rationale) and performs theory-selection reasoning T3 requires the solver to do. Deleted per Rule 2; the internal-presentation-target paragraph (unchanged) already carries the spec-mandated weak-delay-reason trap content.] | paragraph: 'Incapacity ground under 911.6(b)(4)...Supporting materials in hand or in progress: (a)...(d) a treating-physician capacity letter...' | → | [paragraph deleted] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Route 512 Owl Block sheet, rows 32-35 (deleted; Assignment Sign-Off shifted up to fill the gap) [round9 P1 No Signposting of Load-Bearing Facts: this callout artificially foregrounded exactly the course-and-scope evidence relevant to the off-book trap by isolating and labeling it 'primary reference' outside the ordinary operational schedule, instead of leaving it embedded unremarkably in the roster like every other trip's timepoints] | separate 'Key Timepoint — S. Main / Third' section (rows 32-35) labeling Trip 06 'primary reference' and spelling out the 02:04/02:31 figures again | → | [section deleted -- fully redundant with the Trip 06 row already in the main trip roster] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Root-Cause Analysis section, paragraphs 35/38/40 [round9 P1 No Signposting of Load-Bearing Facts: these were the only Root-Cause subsections with visual emphasis on their dispositive content, breaking the section's own consistent bold-label-only pattern and telegraphing which facts the reader should weight] | para 35 entirely bold (label+body, incl. 0.14% BAC); para 38 'EFFECT' in caps; para 40 'preventable' bolded mid-sentence | → | para 35 body un-bolded (label only, matching paras 36-39's pattern); 'effect' lower-case; 'preventable' un-bolded |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 4 (window date) and Section 5 (internal target date) [round9 P1 No Signposting of Load-Bearing Facts: isolated bold on these two dates visually flagged exactly the deadline/target gap the task requires the solver to notice unaided] | 'Monday, 04/20/2026' and '05/01/2026' bolded mid-sentence, isolated from surrounding unbolded prose | → | both un-bolded to match surrounding text |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | row inserted between the 02:04 and 02:06 entries [round9 P1 Major, 3rd consecutive round on this finding (CHRONIC): owl_service_rules.docx Rule 404 requires the dispatch run log to record timepoint exceptions, and Rule 304 makes an unauthorized deviation a rules violation -- but no such entry existed anywhere, leaving the 02:05-vs-02:31 gap silently unresolved. Added one factual, format-matching checkpoint entry (not a reconciling/bridge sentence -- it documents the raw fact per Rule 404's own pre-existing logging category, explicitly notes no authorization is on file, and does not explain away or resolve the significance of the gap). RunSchedule_Owl512.xlsx's main roster and AVL_GPS_track_2025-1018.csv were not touched.] | [no entry -- gap between 02:04 Poplar departure and 02:06 silent-alarm entries] | → | 10/18/2025 02:05,checkpoint,...,Trip 06 NB timepoint S. Main/Third -- AVL position logged 02:05 vs. 02:31 board time; timepoint exception, no deviation authorization on file. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/City/repair_invoice_0202.pdf | Referenced Incident section [round9 minor: the actual police report's Local Report Number is TC-2025-1018 (used consistently elsewhere in the corpus); RPD Case No. 2025-1018-0037 does not match any real record and would misdirect a reader trying to retrieve the incorporated report] | RPD Case No. 2025-1018-0037 | → | Traffic Collision Report No. TC-2025-1018 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/City/property_claim_0202.pdf | paragraph 1, narrative of the incident [round9 minor: same wrong case-number reference as repair_invoice_0202.pdf, swept as the same defect class] | RPD Case No. 2025-1018-0037 | → | Traffic Collision Report No. TC-2025-1018 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Criminal/Complaint_Keeler.pdf | page 7, DA signature block [round10 P1: filing is dated 11/14/2025; Gascon lost re-election and left office 12/03/2024, Hochman was the actual sitting LA County DA throughout 2025 -- verified via web search] | GEORGE GASCÓN | → | NATHAN HOCHMAN |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | Section 7, Course-and-Scope Determination [round10 P1: missed in round 9's sweep of the same defect class; this paragraph names the exact records (schedule, AVL, roster, dispatch log) that establish course-and-scope and states they reconcile -- bolding it whole-cloth signposted the answer the same way paragraph 35 did before that fix] | paragraph 43 (Course-and-Scope Determination body) entirely bold | → | un-bolded |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | Section 5, Internal Presentation Target [round10 P0 Major, 3rd round on this file: this elaborate four-part justification for the filing delay is not part of A31's spec description (which only calls for stating accrual date, window date, and the bare delay election/target date -- already fully present in paragraphs 26 and 28) and reads as confident strategic reasoning that could itself supply the decisive procedural analysis. Deleted per Rule 2, keeping the spec-mandated bare statement of the delay election intact.] | paragraph: 'Rationale in support of this scheduling choice: (i)...(iv) a single, well-supported package presented under the 911.4 late-claim procedure is preferable...' | → | [paragraph deleted] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | line 33 (02:05 entry) [Builder decision: Trip 06 schedule-vs-collision gap (CHRONIC, r7-r10) needed a real in-world reason for the early arrival rather than a wording patch. Zero-boardings + no-deviation-call is the factual, contemporaneous-dispatch-voice explanation; ties to the already-established impairment/blackout mechanism in the final IR without touching the canonical collision time or the shared schedule template.] | timepoint exception, no deviation authorization on file | → | zero APC/farebox boardings or alightings logged at Alder Creek/Broadway or Downtown Loop on this leg; no deviation call received from Op 4417 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | paragraph 27 (AVL/GPS Track) [Same builder decision as the Dispatch_log fix: gives the controlling incident report its own documented, evidence-backed reason for the 26-minute gap between Trip 06's scheduled S. Main/Third timepoint and the AVL/collision time, consistent across both artifacts.] | departing the Poplar / Rivergate Plaza layover at 02:04 for Trip 06 northbound. The last valid AVL position log | → | departing the Poplar / Rivergate Plaza layover at 02:04 for Trip 06 northbound. The APC/farebox export for this leg records no boardings or alightings at the Alder Creek / Broadway or Downtown Loop / Civic Center timepoints, and Dispatch received no deviation call from Op 4417 on this leg (see dispatch log). The last valid AVL position log |

## manual edit (PyMuPDF redaction)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | page 2 (0-idx 1), section 2 [r11 t03 (No Reachable Shortcut to the Answer): A35's spec job is to STATE the controlling $196K/$142K figures that defeat A34's billed-charges trap (Includes trap: No) -- the figures, the reconciliation table, and the Howell/Corenbaum citations all stay. What's removed is the letter handing over the legal CONCLUSION itself (the bolded HOWELL-RECOVERABLE label and the 'is the measure...recoverable at trial' sentence), which did the agent's connecting-work for them. Same underlying paid-vs-billed point still appears, more muted, in Exhibit A's own notes ('See Howell, supra').] | (Howell-Recoverable) heading label + (HOWELL-RECOVERABLE) total-box label + 'Under Howell and its progeny, this figure — not the $2,840,000.00 chargemaster total — is the measure of Ms. Reyes's past medical special damages recoverable at trial.' | → | Heading and total-box label trimmed to 'Total Amounts Paid / Accepted' and '$196,000.00'; sentence changed to 'Under Howell and its progeny, amounts written off as contractual adjustments are not separately billable to any party.' |

## manual edit (PyMuPDF redaction, exact font-matched reinsert)

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | pages 6-7, 11, 13-15 (0-idx 7,8,12,14,15,16) [r11 t02 (Calculation & Fixture Accuracy), builder decision: fix properly, cascade the totals down rather than hold as disputed. Also fixed a pre-existing wrong-font (Helvetica) artifact from an earlier round's sensitivity-table edit on page 13, found while verifying this fix.] | PT $8,150, OT $4,845, Neuro $7,320, Psych $8,275 (weighted annual averages that don't mathematically follow from their own shown frequency/unit-cost schedules even under the most generous reading); attendant-care 11% loading stated as $11,337 when 11% of $98,912 is $10,880; dependent totals $180,000/yr, $6,480,000 undiscounted, $4,240,000 PV, and the full PV sensitivity table (9 values across 3 rates x 3 horizons) | → | PT $7,700, OT $2,458, Neuro $4,573, Psych $7,967 (recomputed from each category's own schedule, reading undated/conditional line items as running the full 36-yr horizon -- 3 of 4 reproduce AutoQC's r11 recomputation exactly); attendant-care loading corrected to $10,880 (11% of $98,912); annual total $173,651, undiscounted $6,251,436, PV $4,091,000, full sensitivity table recomputed at the same 2.5%/36yr methodology (discount rate and horizon unchanged) |
