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
| Shared/CrimeLab/BAC_Keeler.pdf | p.3, analyst certification signature line [round2 t01: blank signature on document claiming to be executed] | Signed: [blank underscore rule] | → | Signed: /s/ Alan Whitford |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/CrimeLab/BAC_Keeler.pdf | p.3, technical reviewer concurrence signature line [round2 t01: blank signature on document claiming to be executed] | Signed: [blank underscore rule] | → | Signed: /s/ Loretta M. Ainsley |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/rejection_0218.pdf | p.1, certificate of mailing signature line [round2 t01: blank signature on document claiming to be executed] | [blank underscore rule] | → | /s/ Marcia P. Ainsworth |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/rejection_0218.pdf | p.2 and p.3, Risk & Claims Manager signature line (both rejection notices) [round2 t01: blank signature on document claiming to be executed] | [blank underscore rule] | → | /s/ Gordon Espinoza |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | p.3, AUTHORIZATION block, SCPERA signature [round2 t01: blank signature on document claiming to be issued] | [blank underscore rule] | → | /s/ Ellen J. Whitmore |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Risk/coverage_summary.pdf | p.3, AUTHORIZATION block, District countersignature [round2 t01: blank signature on document claiming to be issued] | [blank underscore rule] | → | /s/ Gordon Espinoza |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/conservatorship_term.pdf | p.10, Exhibit A physician capacity declaration signature [round2 t01 sweep: same blank-signature-on-executed-declaration pattern] | [blank underscore rule] | → | /s/ Helena Vasquez-Ortiz, MD |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/post_accident_testing_policy.docx | Approval and Signature section + Concurrence block [round2 t01 sweep: same blank-signature-on-issued-policy pattern] | [blank underscore rule] x3 | → | /s/ Harlan T. Odegaard | /s/ Marlene Okonkwo | /s/ Diane Farkas |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | APPROVED block, Director of Safety line [round2 t01 sweep: same blank-signature-on-issued-manual pattern; Director of Operations line left blank, no name for that title exists anywhere in the corpus] | [blank underscore rule] | → | /s/ Marlene Okonkwo |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.2, Printed result tape affixed to form? field [round2 t02b: attachment claimed affixed but not reproduced in this filesystem export; clarifies it is affixed to the original retained in the ACTD Compliance file] | Yes — Attachment A | → | Yes (orig.) -- Att. A |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Police/FST_supplement_2025-1018.pdf | p.4, section 11 heading [round2 t02c: attachments claimed but not reproduced in this filesystem export; clarifies they are retained in the RPD case file] | 11.  Attachments to This Supplement | → | 11.  Attachments to This Supplement (Retained in RPD Case File) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.3, section 5 heading [round2 t02d: Tabs 1-11 claimed enclosed but not reproduced in this filesystem export; clarifies they are retained in the firm file] | Enclosure Index (Tabs) | → | Enclosure Index (Tabs, retained in firm file) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/docket_entry.xlsx | Deadlines!B12 [round2 t03: matter name drift vs MatterHub calendar CSV] | Reyes/Bus DUI Collision | → | Reyes / Cho / Mowbray v. Alder Creek Transit District |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/docket_entry.xlsx | Deadlines!K12 notes [round2 t03: City is a separate property-damage claim (ACTD-2026-0117), not part of this 3-claimant matter] | Reyes, Cho, Mowbray, City | → | Reyes, Cho, Mowbray |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Litigation/production_tracker.csv | columns review_status, final_call [round2 t04: production_tracker.csv handed T9's discovery produce/withhold conclusions to the solver as a lookup table] | review_status and final_call populated for all 22 rows (e.g. Confirmed/Produce, Attorney-confirmed/Withhold-Privileged) | → | review_status and final_call blanked for all 22 rows; first_pass_tag left as the unreliable system tag the spec calls for |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | para 27, Incapacity ground under 911.6(b)(4) section [round2 t05: Gov. Code 911.6(b) actually has six grounds, (b)(1)-(b)(6), verified against the statute; the memo's own (b)(4) citation was already correct and untouched] | any of four enumerated grounds | → | any of six enumerated grounds |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Claims/medical_billing_ledger.csv | last row [round2 t07: trailing totals/summary row after the header-defined data records, prohibited by the CSV-formatting dimension] | TOTAL,ALL PROVIDERS (9),... (trailing summary row) | → | [row deleted] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_draft.docx | para 44 comment anchor [round2 t06: draft/redline fidelity sub-check failed with zero comments and zero tracked changes; round1 disputed this and the dispute did not hold, so fixing it directly this round with an in-voice procedural comment rather than fabricated tracked edits to the narrative] | no comments part, no tracked-change elements | → | added one supervisor review comment (M. Okonkwo, dated 10/20/2025) on the closing DRAFT line |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/owl_service_rules.docx | APPROVED block, Director of Operations line [round2 t01 sweep: expert-directed to name this role rather than leave it blank; no prior document named this officeholder, so Victor R. Salcedo is a new named individual, checked against the corpus for collisions] | [blank underscore rule] | → | /s/ Victor R. Salcedo |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_lien_EOB.pdf | p.3: table row 8, Care remains ongoing sentence, Tab 8 label [expert-directed cleanup, not an AutoQC finding. NOTE: text now reads correctly as one phrase when isolated, but still surfaces out of natural reading-order sequence in a raw linear text extraction of the page (visually confirmed correct; a content-stream-level artifact of PyMuPDF's append-only text reinsertion, present since round 1, not fully resolvable without direct content-stream surgery)] | Ashby [visual gap] Outpatient Physical Therapy (3 places, name detached from following text in the PDF text layer since round 1's Meridian->Ashby rename) | → | Ashby Outpatient Physical Therapy (3 places, redacted and reinserted as one unified text run each; visual gap eliminated) |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Dispatch/tran_text_thread.pdf | whole file, rebuilt [round3 t01: file materially diverged from A52's registered content/timing and, worse, defeated the off-book trap by having Tran correct himself in-thread] | 5-page, 32-message thread (10/18-10/24), different content, self-resolves the off-book trap when Tran checks the block sheet and retracts his suspicion | → | 1-page, 3-message thread matching the spec verbatim (10/18/2025 03:20-03:40 AM): repeats the off-book suspicion, agrees to stay quiet until sure, does not self-resolve |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.2, Printed result tape affixed to form? field [round3 t02: escalating from round2's rewording to full removal of the Attachment-letter reference, per expert direction] | Yes (orig.) -- Att. A | → | Yes |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Compliance/DOT_655_Keeler.pdf | p.4, Distribution list [round3 t02: these named attachments are not mounted as files anywhere in the world; removed rather than reworded since round2's rewording did not resolve the finding] | Attachment A / B / C bullets (3 items) in the Distribution list | → | [removed; Copy -- distribution items and Retention note retained] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | table1 r1c2, table1 r11c2, table3 r1c0 [round3 t02: pre-trip yard sheet and EMS run sheets are not mounted as files anywhere in the world; removed the dangling citations and pointed the passenger-table note to content within this same document instead] | Duty roster; pre-trip yard sheet | RPD TC-2025-1018 §IV; EMS run sheets | See APC/farebox export (A11) and on-scene EMS run sheets for... | → | Duty roster | RPD TC-2025-1018 §IV | See APC/farebox export (A11) for the passenger roster and the timeline above for injury dispositions and transport destinations. |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Safety/IR_2025-1018_final.docx | table0 r0, table1 r0, table2 r0, table3 r0 (10 runs) [round3 t04: dark navy fill with no color override left header text unreadable] | header cells (fill 1B2A4E) inherit Normal style color 333944 -- dark text on dark fill | → | header cells (fill 1B2A4E) explicit run color FFFFFF -- white text on dark fill |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Legal/Reyes/intake_memo.docx | table1 r0c0 'Role', r0c1 'Attorney/Staff' [round3 t04: dark navy fill with no color override left header text unreadable] | table1 r0 header cells (fill 141A2E) inherit Normal style color 4A5266 -- dark text on dark fill | → | table1 r0 header cells (fill 141A2E) explicit run color FFFFFF -- white text on dark fill |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| ACTD/Ops/RunSchedule_Owl512.xlsx | Authorized Owl Routes!F7:F12 [round3 t03: Status column had no distinctive color encoding, violating format-native status-rendering sub-check] | F7:F12 plain alternating white/beige fill (same as other columns) | → | F7:F12 alternating green shades (C6E8C6 / DDF0DD) distinct status-color encoding |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.2, Table of Contents [round3 t02: matching removal of the attachments section these entries point to] | Attachments / Attachment 1-5 table-of-contents entries | → | [removed] |

## manual edit

| File | Location | Old | → | New |
|---|---|---|---|---|
| Shared/Settlement/Reyes_life_care_plan.pdf | p.19 (formerly p.17 of 17), ATTACHMENTS section [round3 t02: escalating from round2's dispute (which was rejected) to removal, since these 5 named materials are not mounted as files anywhere in the world] | ATTACHMENTS heading + 5 numbered items, each (available on request) | → | [removed; End of report. retained] |
