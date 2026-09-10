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
