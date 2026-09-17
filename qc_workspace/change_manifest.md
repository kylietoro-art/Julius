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
| ACTD/Claims/reserve_memo.docx | table1 row5 [T10 round2: de-signpost, stamp handed T6's remediation-path first step for free] | Prior initial reserve — SUPERSEDED | → | Prior initial reserve — Briggs, 10/28/2025 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | para 14, para 30, table1 row5 [T10 round2: No Signposting of Load-Bearing Facts] | bold: $250,000 / $3,250,000 / supersedes (para 14); Controlling reserve label (para 30); Prior initial reserve — SUPERSEDED (table1 row5) | → | bold removed, text unchanged except table1 row5 label reworded |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 6 (subtitle) [T10 round2: self-authority label, not part of A02/A03 trap mechanism (verified against spec)] | Supervisor-Reviewed / Controlling Report of Record | → | Supervisor-Reviewed |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 47 (section 8 heading) [T10 round2: same as subtitle] | 8.  Report of Record; Relationship to Draft Report | → | 8.  Relationship to Draft Report |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 77 (certification) [T10 round2: drop self-certifying clause, rest of certification unchanged] | ...Scientific Services Bureau, that it reflects the controlling documentary record of this collision. | → | ...Scientific Services Bureau. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 35 [T10 round2: No Signposting of Load-Bearing Facts] | bold: alcohol-impairment root-cause sentence (para 35) | → | bold removed, text unchanged |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Passengers/claims_0118.pdf | pages 4, 6 [T05(a) round2: Coherence Flag Ratio, conflicted with A01/FST supplement/final incident report (all northbound, east curb)] | Southbound South Main Street (x2, Cho p.4 + Mowbray p.6); west side of South Main Street (x1, Cho p.4) | → | Northbound South Main Street (x2); east side of South Main Street (x1) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Press/news_collision.html | line 204 [T05(a) round2: same coherence conflict as claims_0118.pdf] | street-light standard on the west side of Main | → | street-light standard on the east side of Main |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | row 12 (RL-2025-0110) [T05(b) round2: Coherence Flag Ratio, demand wasn't received until 02/02/2026 (invoice dated 02/01/2026)] | RL-2025-0110 date_set=12/15/2025, notes referenced A43 | → | date_set=02/02/2026, notes reference A40/A58 (actual demand + invoice) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | table2 row 8 [T05(b) round2: 12/15/2025 memo can't state a figure not demanded until 02/02/2026] | City of Rivergate property claim ($48,500 demand) — RESERVED SEPARATELY | → | City of Rivergate property claim (anticipated; demand not yet received) — RESERVED SEPARATELY |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | row 6 (RL-2025-0104) [T05(c) round2: Coherence Flag Ratio, contradicts A43 (reserve_memo.docx) same-date statement that no LCP is on file yet] | Reset following C&S finding, lab BAC, LCP workup — see A43. | → | Reset following C&S finding, lab BAC, initial catastrophic-injury documentation — see A43. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/FST_supplement_2025-1018.pdf | section 11 heading + first bullet [T02 round2: No Broken Document References, attachments not mounted in filesystem] | 11. Attachments to This Supplement (photocopy) | → | 11. Related Records Referenced in This Supplement; dropped '(photocopy)' claim |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | page 4, distribution list [T02 round2: No Broken Document References, attachments not mounted in filesystem] | Attachment A/B/C — [claimed physically enclosed] | → | Attachment A/B/C (retained in ACTD Compliance file): [same content, custody clarified] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | pages 1, 2, 3 heading, 4 (6 locations) [T02 round2: No Broken Document References, Tabs 1-11 not mounted in filesystem] | 'enclosed'/'Enclosure Index'/'Enclosures (Exhibit A; Tabs 1-11)' claiming Tabs 1-11 physically included | → | 'on file'/'Reference Index'/'Enclosures (Exhibit A); Tabs 1-11 retained in claims file' -- only Exhibit A (actually part of this PDF) still called enclosed |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Dispatch/email_offbook.eml | whole file (A09) [T08 round2: Built Files Match Spec Inventory, built file didn't match registry's Purpose & Content / Author requirements] | To: dispatch-supervisors@actd.gov, Cc: mokonkwo@actd.gov, Subject: 'FYI — Keeler incident on Owl — off-book run?', ~250-word body | → | To: gespinoza@actd.gov, dfarkas@actd.gov (no Cc), Subject: 'Overnight incident - Route 512', 3-sentence body per registry |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Dispatch/tran_text_thread.pdf | whole file (A52) [T08 round2: Built Files Match Spec Inventory, built file didn't match registry's narrow personal-device exchange] | 5 pages, 2:47am-Oct 24, 32 messages | → | 1 page, 3:20-3:40am 10/18/2025, 3 messages per registry |

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
- ACTD/Claims/reserve_ledger.csv: A40, context already names "City of Rivergate Property-Damage Claim", rewrite by hand (drop the adjacent descriptor, e.g. "…the City of Rivergate Property-Damage Claim")
- ACTD/Claims/reserve_ledger.csv: A58, context already names "City of Rivergate Light-Standard Repair Invoice", rewrite by hand (drop the adjacent descriptor, e.g. "…the City of Rivergate Light-Standard Repair Invoice")
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
| ACTD/Litigation/production_tracker.csv | doc_id column, 16 rows [round3 CHRONIC: comprehensive A## class-level fix] | doc_id column: bare A02,A03,A04,A05,A09,A13,A19,A20,A42,A43,A46,A48,A49,A51,A53,A57 | → | doc_id column: registry descriptive names, matching the pattern a_scrub.py already applied to A01 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | row 12 notes [round3 CHRONIC: comprehensive A## class-level fix] | (see A40) ... (see A58) | → | removed, already named in-line |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | para 31 [round3 CHRONIC: comprehensive A## class-level fix] | MatterHub deadlines module (A62) to reflect | → | MatterHub deadlines module to reflect |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/scene_photos_2025-1018.pdf | page 1 header table [round3 CHRONIC: comprehensive A## class-level fix] | Case Reference (RPD): TC-2025-1018 (Cross-ref: Matter A01) | → | Case Reference (RPD): TC-2025-1018 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/City/property_claim_0202.pdf | page 3 [round3 CHRONIC: comprehensive A## class-level fix] | itemizing the $48,500.00 cost of repair (Artifact A58). | → | itemizing the $48,500.00 cost of repair. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 30, table3 r1c0 [round3 CHRONIC: comprehensive A## class-level fix] | see A11 (APC/farebox export) / See APC/farebox export (A11) | → | see the APC/farebox export / See the APC/farebox export |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | row 5 [round3 CHRONIC: comprehensive A## class-level fix] | opening note (A42) | → | opening note |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | para 31 [round3: missed this in round 2's T10 de-signposting pass (only did para 14 and 30)] | bold: $3,250,000 (para 31) | → | bold removed |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 40, para 43 [round3: missed in round 2's T10 pass, only checked paras the finding quoted verbatim rather than sweeping the whole doc] | bold: 'preventable' (para40); entire para43 (Section 7 body) bold | → | bold removed from both |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 13 [round3: same self-certification pattern as para 6/77, missed in round 2] | This Final Incident Report is the report of record issued following completion... | → | This Final Incident Report was issued following completion... |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | page 4, para 11 [round3: Coherence Flag Ratio, conflicts with controlling northbound sources (police report, final incident report, AVL/schedule)] | in the southbound direction on South Main Street | → | in the northbound direction on South Main Street |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Witness/blau_statement.pdf | page 3 [round3: Coherence Flag Ratio, original statement said southbound (conflicts with controlling sources); used the addendum's own established correction mechanism rather than silently editing a signed statement] | addendum ends at item 4; closing line 'Everything else... stands as written' | → | added item 5 (Direction of travel, corrects southbound to northbound per AVL/GPS); closing line now 'Except as corrected above...' |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | page 3, closing line [round3 T02: standard industry form referenced by number (Item 11 schedule), not claimed as physically attached to this declarations excerpt] | SEE ATTACHED MEMORANDUM OF COVERAGE FORM | → | SEE MEMORANDUM OF COVERAGE FORM |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | lines 37, 45 [round3: Consistent Naming, no trap/subsystem-number justification found in spec] | ACTD-IR-2025-1018-001 (x2) | → | ACTD-IR-2025-1018 (matches all other 10 references in corpus) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Authorized Owl Routes sheet, A7:A12 [round3: Text Legibility And Contrast, ~2.9:1 contrast on cream-fill rows A8/A10/A12] | Route # column: gold #B8862B font (all rows) | → | dark navy #0E1B2C font, matching column B's body-text color |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | last row [round3: CSV Formatted Correctly, every row after header must be a data record] | trailing TOTAL row (mixed schema, not a bill record) | → | removed; not a Must-match artifact for the billed/paid canonical values (that's A15), and the 82 line items independently foot to the same totals |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | para 13, para 42 [round3: distinguished from reserve_memo.docx (informal claims-manager assessment) -- this is the Director of Safety's OFFICIAL final report, with a section literally titled to match T5's task name and declaring a 'determination,' which a real safety report wouldn't naturally do. Kept all underlying facts (schedule/AVL/telemetry), removed only the legal-conclusion framing and task-name collision.] | 'The course-and-scope determination is therefore that...' sentence (para13); section 7 heading 'Course-and-Scope Determination' | → | sentence removed (redundant restatement using T5's own task-name vocabulary); heading renamed to 'Operator Assignment and Route Verification' |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | pages 8-9, Physical/Occupational Therapy, Neurocognitive Rehab, Psychotherapy tables [round4: Calculation & Fixture Accuracy, weighted annual averages didn't match the tables' own stated frequency/unit-cost/year-range inputs] | $8,150 (PT) / $4,845 (OT) / $7,320 (neurocognitive) / $8,275 (psychotherapy) | → | $7,700 / $2,458 / $4,573 / $7,967 -- each recomputed by hand from the row's own stated inputs |
| Shared/Settlement/Reyes_life_care_plan.pdf | page 13, Annual Cost Summary table [round4: same finding, cascading fix] | 4 category rows updated to match; Rounding/geographic-pricing adjustment $1,700 | → | Rounding/geographic-pricing adjustment $7,592 -- rebalanced so Total, weighted annual average still equals the spec's canonical $180,000 (and downstream $6,480,000 undiscounted / $4,240,000 PV, both unchanged) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Authorized Owl Routes sheet, F7:F12 [round4: Format-Native Feature Fidelity, Status column had no fill/badge encoding (only font color)] | white/cream fill behind existing dark-green "Authorized" text | → | light green #DCEFE0 fill added (5.32:1 contrast against the existing #2E6B3B text), giving the Status column an actual color-coded badge |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | para 13 ("Passengers aboard: approximately four...") [round4: Format-Native Feature Fidelity, a document presenting as DRAFT had no comments/tracked-changes markup] | no comment markup | → | added one native Word comment (author W. Tran) on "approximately four" reading "Confirm against APC/farebox pull before this goes anywhere -- don't want this to be the number that sticks." Text content unchanged; format-native markup only, verified via direct OOXML manipulation (well-formed XML confirmed on all 5 modified parts, full paragraph text diffed byte-identical to the original) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Trip 06 row, S. Main/Third column [round4b: Intended Traps Are Fair -- user-directed fix, not a route redesign. A01/A02 register 02:05 as the canonical collision time; APC log's other 9 trips corroborate the schedule's own ~27-33min stop order (Poplar->AlderCreek->DowntownLoop->Third->Fifth). Both numbers are independently canonical and can't be reconciled by moving either one -- so state both plainly, explain neither.] | 02:05 (SB timepoint pass) / 02:31 | → | 02:31 scheduled (actual: 02:05, per incident record) |
| ACTD/Ops/RunSchedule_Owl512.xlsx | rows 32-35, "Key Timepoint — S. Main / Third" explanatory block [round4b: same finding -- this block existed only to explain the confusing cell above; once the cell states both numbers plainly, the block is redundant, and its own wording ("headway anchor," "SB pass, mid-loop reference") was the same confusing jargon] | full block (header, 1-row table, trailing note) | → | removed (cell contents cleared, rows left blank; merged-range structure below re-verified intact) |
| ACTD/CAD/Dispatch_log_2025-1018.csv | line 33, 02:06 radio_call entry [round4b: same finding -- matching cross-reference to the same confusing schedule concept] | AVL last position vicinity S. Main at Third Ave (SB reference timepoint 02:05). | → | AVL last position vicinity S. Main at Third Ave. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Legal/Reyes/intake_memo.docx | para 27 (Government Claims Act Posture section) | to grant the application on any of four enumerated grounds. | → | to grant the application if one or more of the statute's enumerated grounds is established. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.9, attendant-care 11% loading (11% of $98,912 = $10,880.32) | $11,337 | → | $10,880 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.9 Subtotal attendant care; p.13 Personal care attendant hours row | $110,249 (attendant-care subtotal, p.9 and p.13) | → | $109,792 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.13 Annual Cost Summary, rebalanced to keep Total = $180,000 after the attendant-care fix | $7,592 (rounding/geo-pricing plug, p.13) | → | $8,049 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.16 Sensitivity Analysis; p.17 extended sensitivity table | $4,592,000 (PV @2.0%/36yr, p.16 and p.17) | → | $4,588,000 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.16 Sensitivity Analysis; p.17 extended sensitivity table | $3,921,000 (PV @3.0%/36yr, p.16 and p.17) | → | $3,930,000 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.17 extended sensitivity table | $4,929,000 (PV @2.0%/40yr, p.17) | → | $4,924,000 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Shared/Settlement/Reyes_life_care_plan.pdf | p.17 extended sensitivity table | $4,153,000 (PV @3.0%/40yr, p.17) | → | $4,161,000 |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/ACTD/Ops/roster_2025-1018.csv | whole-file column restructure | schema: badge_number,operator_name,division,block_assignment,sign_in_time,sign_out_time,actual_hours,timekeeping_flag | → | schema: employee_id,employee_name,shift_date,clock_in,assigned_run_id,clock_out,status (matches External Files Registry A20); kept Keeler's clock_out=10/18/2025 02:35 (corroborated by dispatch log line 41, IR_2025-1018_final.docx, and Complaint_Keeler.pdf's arrest time -- did NOT blank it per the registry's 'blank/incident-truncated' phrasing, since that would contradict 3 other files) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/ACTD/Safety/IR_2025-1018_draft.docx | heading, Section 2 | 2. Preliminary Data — placeholder fields | → | 2. Preliminary Data |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| filesystem/Legal/Reyes/intake_memo.docx | para 26, Six-month presentation window | Monday, 04/20/2026 (bold) | → | Monday, 04/20/2026 (not bold, matches surrounding body text) |
