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
| Med/Reyes/op_reports.pdf | whole document (was 13pp/5 reports, now 6pp/3 reports) [round2 finding: A22 operative-report compilation does not match registry content] | Five-report compilation: 10/18 exploratory laparotomy/splenectomy, 10/18 external fixators, 10/22 washout/irrigation, 10/25 definitive pelvic+bilateral-LE ORIF, 11/05 tracheostomy+PEG -- no brain surgery of any kind, contradicting the TBI narrative in reserve_memo.docx and the life-care plan | → | Three-report compilation matching the A22 registry exactly: 10/18 decompressive hemicraniectomy + evacuation of acute SDH + ICP monitor (Neurosurgery), 10/21 pelvic ring ORIF, 11/03 bilateral tibia/fibula ORIF (Orthopedic Trauma Surgery), each with an anesthesia record documenting GA and post-op depressed consciousness |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/docket_entry.xlsx | docProps/core.xml (created/modified) [round2: World Timeline Holds Together — docket_entry.xlsx core properties post-anchor] | created=modified=2026-09-14 (real build/checkout date, post-anchor) | → | created=modified=2026-03-06T09:42:00Z, creator/lastModifiedBy=Grace Chen, Paralegal (matches the sheet's own stated Export date/time and Prepared by fields) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | section 2 heading [round2: No Synthetic Markers/Placeholder Data — draft incident report exposes a placeholder-fields heading] | 2. Preliminary Data — placeholder fields | → | 2. Preliminary Data — unconfirmed, pending verification |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/adjuster_note.docx | body + table1 r2c1/r5c1 [round2: No Synthetic Markers/Placeholder Data — active reserve materials retain placeholder labels] | 'The pedestrian placeholder is expressly...'; 'Pedestrian (Reyes) — placeholder pending medical workup'; 'Allocated expense placeholder' | → | 'The pedestrian figure above is expressly a book-opening estimate...'; 'Pedestrian (Reyes) — opening estimate pending medical workup'; 'Allocated expense reserve' |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | body + table0 r2c1/r5c1 [round2: No Synthetic Markers/Placeholder Data — active reserve materials retain placeholder labels] | '...are placeholders based on preliminary treating-team indications...'; 'Pedestrian (Reyes) placeholder'; 'Allocated expense placeholder' | → | '...are working estimates based on preliminary treating-team indications...'; 'Pedestrian (Reyes) — opening estimate'; 'Allocated expense reserve' |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_ledger.csv | rows RL-2025-0090, RL-2025-0108, RL-2025-0109 (notes column) [round2: No Synthetic Markers/Placeholder Data — active reserve materials retain placeholder labels] | 'Allocated expense placeholder booked with opening note...'; 'LAE placeholder — passenger track defense costs.' (x2) | → | 'Allocated expense estimate booked with opening note...'; 'Estimated LAE — passenger track defense costs.' (x2) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/docket_entry.xlsx | docProps/core.xml (creator/lastModifiedBy) [self-correction: keep the fix minimal, matches inventory_check's text-growth flag] | creator=lastModifiedBy=Grace Chen, Paralegal (over-fix, added info beyond the flagged finding) | → | creator=lastModifiedBy=blank (reverted to original; only created/modified date is the actual fix) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | pages 8-9 (category tables), p.13 (Annual Cost Summary), p.16-17 (sensitivity tables) [round3: Calculation & Fixture Accuracy -- weighted annual category figures and PV sensitivity tables don't follow their displayed inputs] | PT $8,150 (should be $7,700); OT $4,845 (should be $2,458); Neurocog $7,320 (should be $4,573); Psychotherapy $8,275 (should be $7,967); rounding/geo adj $1,700; sensitivity cells 2.0%/36yr $4,592,000, 2.0%/40yr $4,929,000, 2.5%/30yr $3,766,000, 2.5%/40yr $4,517,000, 3.0%/36yr $3,921,000, 3.0%/40yr $4,153,000 -- none of these matched the stated line-item inputs or the level-annuity formula | → | PT $7,700; OT $2,458; Neurocog $4,573; Psychotherapy $7,967 (all recomputed as weighted annual averages from the plan's own displayed frequency/unit-cost line items); rounding/geo adj raised to $7,592 so the summary still foots to the canonical $180,000; sensitivity cells recomputed from PV=C*(1-(1+r)^-n)/r and corrected to $4,588,000 / $4,924,000 / $3,767,000 / $4,518,000 / $3,930,000 / $4,161,000; the adopted 2.5%/36yr cell ($4,240,000) was already correct and untouched |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | docProps/core.xml (creator) [round3: In-World vs Out-Of-World Separation -- openpyxl creator leak] | creator=openpyxl (tool fingerprint) | → | creator=blank |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | 'Authorized Owl Routes'!A7:A12 font color [round3: Text Legibility And Contrast -- route-number gold text fails contrast] | gold 00B8862B on white/cream fills (~3.2:1 contrast) | → | dark navy 000E1B2C (matches column B text), same fills |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/hold_demand_letter.pdf | p.1 closing sentence of opening paragraph; p.2 mid-paragraph clause [round3: World Timeline Holds Together -- March preservation letter contains May hindsight] | Reyes's late-claim application under Government Code § 911.4 is pending before the Board. (p.1) / ...a late-claim application on behalf of Ms. Reyes was filed with the Board on 05/15/2026. (p.2) | → | Reyes's late-claim application under Government Code § 911.4 has not yet been filed. (p.1) / ...a late-claim application on behalf of Ms. Reyes remains unfiled. (p.2) -- both corrected so a 03/20/2026 letter no longer describes the 05/15/2026 filing as already complete |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | row 83 (final row) [round3: CSV Formatted Correctly -- trailing aggregate row is not a per-record data row] | TOTAL,ALL PROVIDERS (9),... aggregate row summing billed/paid/adjustments | → | row removed; canonical $2,840,000/$196,000/$2,644,000 totals remain independently stated in Reyes_lien_EOB.pdf (A35) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | 2 Word comments anchored to the off-book flag and the passenger-count flag [round3 (repeat from round1): Format-Native Feature Fidelity sub-check (d) -- draft has no visible review machinery] | no comments/tracked-changes in a document labeled DRAFT -- SUBJECT TO SUPERVISOR REVIEW | → | added 2 real Word comments from Marlene Okonkwo (Director of Safety, already an established character) asking to confirm the off-book characterization against A08/A12 and to pull APC before finalizing -- consistent with the review the final report actually reflects |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | § 3.2 Non-Fatal Accidents (replaced the (a)-(d) list) [round3: Real-World Facts, Institutions and Jurisdiction Stated Correctly -- ACTD policy misstates FTA nonfatal post-accident testing rule] | conditioned nonfatal testing on disabling damage OR (injury + citation for a moving violation) OR hazmat release OR immovable-object damage -- an FMCSA/49 CFR 382.303-style, citation-gated standard that does not apply to FTA-regulated transit operators and can wrongly suppress testing | → | As soon as practicable following a nonfatal accident involving a revenue service vehicle, test the operator unless performance can be completely discounted as a contributing factor -- the actual 49 CFR 655.44(a)(2) standard (verified against the current regulation), with no citation/damage/hazmat gating |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | Rule 506, second sentence [round3: Real-World Facts, Institutions and Jurisdiction Stated Correctly -- swept to the class since this file shared the same regulatory error] | same citation-gated / disabling-damage-gated FMCSA-style nonfatal testing description as the compliance policy (round1 aligned the policy to match this file, but this file was itself wrong against real 49 CFR 655.44) | → | Testing is required upon any accident meeting the Part 655 threshold: loss of human life, or any other accident where the operator's performance cannot be completely discounted, per District determination -- matches the corrected policy and the actual regulation |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.9 attendant-care loading/subtotal, p.13 summary + rounding line [round4: Calculation & Fixture Accuracy -- attendant-care 11% loading didn't match its own stated base] | 11% loading shown as $11,337 (actually 11.46% of $98,912); subtotal $110,249; rounding adj $7,592 | → | loading corrected to $10,880 (exactly 11% of $98,912); subtotal $109,792; rounding adj increased to $8,049 to keep the $180,000 total |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Route 512 Owl Block!J25/K25/L25/I25/N26; Authorized Owl Routes!F7:F12; docProps [round4: Numerical Values Constraints (schedule/AVL conflict), Format-Native Feature Fidelity (status color), In-World vs Out-Of-World Separation (app.xml)] | Trip 06 NB reached S.Main/Third at 02:31 per schedule while AVL/APC/dispatch/final-report all show 02:05; Status column had no color encoding; docProps/app.xml said Openpyxl 3.1.5 | → | Trip 06 timepoints compressed so S.Main/Third reads 02:05, matching corroborating records (downstream layover note adjusted accordingly); Authorized status cells given a green fill; app.xml Application set to Microsoft Excel |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx, ACTD/HR/Keeler_personnel.docx, ACTD/Ops/bid_award_512OWL.docx, ACTD/Claims/reserve_memo.docx, ACTD/Claims/adjuster_note.docx | subtitle/TOC/body gold text runs (31 total) [round4: Text Legibility And Contrast -- swept beyond the 3 named files to 2 more with the same near-threshold color] | gold B8893B/B8862E/B87333/B5651D/A86A2D on white, 3.1-4.4:1 contrast | → | dark bronze 6B4A17 on white, 8.0:1 contrast |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx, ACTD/Ops/owl_service_rules.docx | signature lines (3 + 2) [round4: No Synthetic Markers/Placeholder Data -- unresolved signature fields in finalized policy documents] | blank underscore lines despite 'Approved and issued'/'APPROVED' | → | /s/ Name typed-signature indicators, matching this world's established convention (e.g. IR_2025-1018_final.docx) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Video/onboard_video_still_log.pdf | Preservation Statement paragraph, p.1 [round4 (4th occurrence): No Broken Document References -- A53 native footage; judgment call, native MP4 file itself still not mounted] | clip perpetually described as vendor-held only, in tension with production_tracker.csv showing A53 already Bates-stamped/Produce/Confirmed | → | added that the clip was retrieved from the vendor 12/10/2025 and copied to ACTD's own evidence locker, resolving the tension with the production tracker without fabricating an actual video file |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/AVL_GPS_track_2025-1018.csv | odometer_mi column, all 226 data rows [round5: Numerical Values Constraints -- Bus 4177 odometer conflicts with its recent maintenance record] | 187,342.6 - 187,442.x (39,139.6 mi jump from the 10/10/2025 maintenance log reading of 148,203 in 7 days) | → | 149,203.0 - 149,228.2 (offset -38,139.6, preserves the realistic incremental pattern, consistent with ~1,000 mi over 7 days from the maintenance log baseline) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx, ACTD/Ops/owl_service_rules.docx | sec 3.2/Rule 506 (qualifying-accident threshold); sec 4.3 (0.02 vs 0.04 positive-test label) [round5: Real-World Facts -- policy still misstated 49 CFR Part 655] | round-3 fix tested every nonfatal accident (missing the real 655.4 qualifying-accident threshold); 0.02+ was called a positive DOT test outright, contradicting the document's own sec 7.3 | → | restored the real qualifying threshold (bodily injury+immediate treatment away from scene, OR disabling damage requiring tow-away) before the discount test applies; 4.3 now matches 7.3: 0.04+ is positive, 0.02-0.039 is temporary removal only |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx, ACTD/Safety/IR_2025-1018_final.docx | table header cells (dark navy fill, 2 + 10 runs) [round5: Text Legibility And Contrast -- header cells washed out against their local fill] | no explicit run color on dark-navy header cells; rendered in the default/inherited color, washing out against the fill | → | explicit white (FFFFFF) run color on all header cells sharing the dark-navy fill |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | sec 7.4 Return-to-Duty Process [round6: Real-World Facts -- policy imposed SAP return-to-duty on the 0.02-0.039 temporary-removal category] | SAP/Subpart O process applied to anyone removed under sec 7.3, which covers both the 0.04+/positive category AND the 0.02-0.039 temporary-removal category | → | SAP/Subpart O scoped to only the sec 655.61/655.62 category (positive/0.04+/refusal); added the distinct, lighter sec 655.35/655.48 return path for 0.02-0.039 (retest below 0.02, no SAP) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/reserve_memo.docx | Section 1 (Summary/Recommended Action) [round7: Numerical Values -- controlling reserve misclassified between memo and reserve ledger] [the $3.25M figure mixes $3,150,000 indemnity and $100,000 expense; calling the blended total an indemnity reserve contradicted the memo's own allocation table] | memo called the full $3,250,000 total the 'controlling indemnity reserve' twice, even though its own Section 4 table allocates $100,000 of that total to loss-adjustment expense (matching reserve_ledger.csv's separate indemnity/expense line items) | → | removed the word 'indemnity' from both references so the memo calls it 'the reserve' / 'the controlling reserve' consistently with its own table heading and with reserve_ledger.csv's indemnity+expense split |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | page 2, Total Amounts Paid/Accepted paragraph [round7: Numerical Values/Calculation Accuracy -- ledger vs EOB treatment of $3,200 patient responsibility] [internal contradiction within the same document; the canonical $196,000 Howell-recoverable figure and the Exhibit A table/ledger tie were both already correct, only the page-2 narrative sentence was wrong] | the $196,000 Paid/Accepted total was described as inclusive of Medi-Cal, BlueShield, and de minimis patient out-of-pocket copay/coinsurance, contradicting Exhibit A's own table, which treats Patient Resp. $3,200 as a separate, additional column from Paid/Accepted $196,000 | → | removed the patient-copay clause from the inclusive list so the narrative matches Exhibit A's table and the medical_billing_ledger.csv tie: $196,000 Paid/Accepted is third-party payer remittances only, with $3,200 patient responsibility tracked and paid separately |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/reyes_recorded_statement.pdf | entire file [round7: Built Files Match Spec Inventory -- A29 wrong source/custodian and contrary account] [registry Prepared By/Source is 'Y. Reyes; copy retained in claimant's file,' not an ACTD-certified transcript distributed to defense counsel; the built file's custodian, distribution, and substantive account all diverged from spec] | 7-page ACTD-prepared 'Certified Transcript,' interview conducted and certified by ACTD's own claims manager, distributed to ACTD General Counsel and outside defense counsel; Reyes has zero memory from checking her phone at the stop through waking at the hospital (no mention of the bus at all) | → | rebuilt as a 2-page claimant's personal excerpted copy per the registry (A29): same underlying interview event (Espinoza, 02/18/2026, ACTD file GE-2026-0218-01, pro se, telephonic) but framed and retained as Reyes's own file copy, containing the three registry-specified Q&A excerpts verbatim, including her recalling the bus drift and pole strike as her last clear memory before waking at the hospital |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Discovery/RFP_set.pdf | p12 attorney signature block, p14 proof-of-service signature [round8: Placeholder/Template Residue -- blank signature lines on a served discovery document] [a served RFP with proof of service is a completed, executed document; bare underscores read as an unfinished template] | blank underscore signature lines for Nora Halstead and Grace Chen | → | filled with /s/ Name per the world's established executed-signature convention |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | p10 attorney signature block [round8: Placeholder/Template Residue] [the complaint is stamped ENDORSED -- FILED; a filed pleading is executed] | blank underscore signature line for Nora Halstead | → | filled with /s/ Nora Halstead |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CrimeLab/BAC_Keeler.pdf | p3 analyst and technical-reviewer certification signatures [round8: Placeholder/Template Residue] [the report is dated, distributed, and relied on throughout the world as an established, executed lab report] | blank underscore signature lines for Alan Whitford and Loretta M. Ainsley on a sworn penalty-of-perjury certificate | → | filled with /s/ Name for both |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/rejection_0218.pdf | p1 certificate of mailing, p2/p3 rejection-notice signatures [round8: Placeholder/Template Residue] [notices were actually mailed 02/18/2026 per the claims tracker and criminal docket; this is a completed, sent document] | blank underscore signature lines for Marcia P. Ainsworth and Gordon Espinoza (x2) | → | filled with /s/ Name for all three |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | p3 AUTHORIZATION block, both countersignature lines [round8: Placeholder/Template Residue] [the declarations page is dated (06/24 and 06/27/2025) and referenced elsewhere as the District's active coverage] | blank underscore signature lines for Ellen J. Whitmore and Gordon Espinoza | → | filled with /s/ Name for both |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_grant.pdf | p5 judge's signature and clerk certification [round8: Placeholder/Template Residue] [this is an entered court order relied on elsewhere in the world as an established fact] | blank underscore signature lines for Hon. Beatrice N. Halloway and the deputy clerk | → | filled with /s/ Beatrice N. Halloway and /s/ R. Castellanos, Deputy Clerk |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_term.pdf | p7 judge's signature and clerk certification [round8: Placeholder/Template Residue] [this is an entered court order relied on elsewhere in the world as an established fact] | blank underscore signature lines for Hon. Beatrice N. Halloway and the deputy clerk | → | filled with /s/ Beatrice N. Halloway and /s/ R. Castellanos, Deputy Clerk (same clerk's office as the companion grant order) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Criminal/Plea_Keeler.pdf | p6 judge's signature and deputy clerk certifications (x2) [round8: Placeholder/Template Residue] [this is a FILED abstract of judgment relied on elsewhere in the world (criminal_docket.csv) as an established, entered fact] | blank underscore signature lines for Hon. Marion T. Escamilla and J. Ontiveros (x2) | → | filled with /s/ Name for all three |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/CAD/Dispatch_log_2025-1018.csv | rows 37 and 45, incident number references [round8: Consistent Naming -- unreconciled ACTD incident-file number] [same incident, three records, two different ID formats with no cross-reference explaining the discrepancy; standardized to the majority (2 of 3 records already used no-suffix) form] | ACTD-IR-2025-1018-001 (with a -001 suffix) | → | ACTD-IR-2025-1018 (no suffix), matching the identifier used in IR_2025-1018_final.docx and onboard_video_still_log.pdf |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | para 37, present-value calculation detail [round8: Calculation Accuracy -- stated unrounded PV $45.19 below the formula's true result] [the rounded-to-nearest-thousand canonical figure ($4,240,000, para 38) is unaffected either way and was not touched; only the displayed intermediate arithmetic was wrong] | annuity factor truncated to 23.556 (3dp), giving PV = $180,000 x 23.556 = $4,240,080, which is $45.19 below the true full-precision result ($4,240,125.19) for r=0.025, n=36 | → | factor shown to 5dp (23.55625), giving PV = $180,000 x 23.55625 = $4,240,125, matching the formula's true result to the nearest dollar |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CivilCase/Complaint_Reyes_filed.pdf | p12 proof-of-service signature [round9: Placeholder/Template Residue -- unsigned proof of service] [the declaration says it was executed 05/22/2026; a sworn, dated proof of service on a filed complaint is a completed document] | blank underscore signature line for Grace Chen | → | filled with /s/ Grace Chen |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_term.pdf | p10, Exhibit A physician declaration signature [round9: Placeholder/Template Residue -- unsigned physician declaration] [the declaration says it was executed 02/03/2026; a sworn capacity declaration attached as an exhibit to an entered order is a completed document] | blank underscore signature line for Dr. Helena Vasquez-Ortiz | → | filled with /s/ Helena Vasquez-Ortiz, MD |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/employment_verification.pdf | letterhead, Date of hire, prose, and Wage Summary Schedule tables A/B [round9: Numerical Values -- payroll facts conflict with Reyes_wage_records.pdf Tab A/B] [two employer verification letters existed for the same person/company/period with materially different hire date, address, and wage history; the current $23.50/hour, 34 hrs/week, ~$41,500 annualized figures (which the registry and the vocational assessment both key off) already matched and were untouched] | hire date 06/2018, employer address 2740 Harbor Boulevard Suite 210, 2023-2025 rate history $21.00 (01/2023)/$22.25 (01/2024)/$23.50 (01/2025), and annual gross wages $41,182.15 (2023)/$41,614.30 (2024)/$32,748.90 (2025) | → | hire date 04/2019, employer address 2245 Harborview Boulevard, rate history $22.75 (03/2023)/$23.50 (03/2024, no further 2025 change), and annual gross wages $40,687.42 (2023)/$41,528.19 (2024)/$32,610.85 (2025), all matching Reyes_wage_records.pdf's Tab A verification letter, W-2 summaries, and paystub samples exactly |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | adjustments column, all 81 rows [round9: Calculation Accuracy -- $3,200 patient responsibility folded into adjustments, recurring finding since round 6] [disputed as a granularity difference (not a real error) for 3 consecutive rounds (6, 7, 8) with exact arithmetic proof each time, but AutoQC kept re-flagging it; splitting the column removes the ambiguity for good without changing any canonical total (billed $2,840,000, paid $196,000 both unchanged) or fabricating precision beyond what the EOB itself provides] | single 'adjustments' column totaling $2,644,000, bundling contractual write-offs and patient-paid copay together | → | split into 'contractual_adjustment' ($2,640,800 total) and 'patient_responsibility' ($3,200 total) columns, matching Reyes_lien_EOB.pdf Exhibit A's two-column breakdown exactly; the $3,200 is allocated by provider (one representative row per provider, matching the EOB's own per-provider totals: RRTC $1,800, ACNRI $400, SKY $300, RAD $200, ANES $100, NSG $100, TSG $50, ASH $200, HBC $50) since neither source gives bill-line-level patient-responsibility detail |
