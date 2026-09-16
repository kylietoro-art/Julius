# Case briefing — read this before triaging the next AutoQC round

Reyes v. Alder Creek Transit District. Bus #4177, Block 512-OWL, Route 512, operator
R. Keeler (badge 4417). Collision 10/18/2025 ~02:05 a.m. at S. Main St & Third Ave,
Rivergate. Plaintiffs: Yolanda Reyes (pedestrian, catastrophic TBI), Devin Cho and
Alicia Mowbray (passengers). Roadside PBT 0.11% (superseded); evidentiary blood BAC
0.14% (controlling).

This file is a narrative companion to `round_log.py rulings` and `change_manifest.md` —
read those too, they're the machine-checked record. This is the "why," organized by
finding so you don't re-derive it. Four rounds closed as of 2026-09-16, branch
`claude/zealous-heisenberg-f47m2p`, all pushed.

## Standing rulings (also in rulings.md — repeated here with context)

1. **Round 2**: Internal memos and filed advocacy documents may draw their own
   conclusions; that alone is not leakage. Only strip content that pre-computes
   another task's specific deliverable value, or that a non-lawyer author has no
   business asserting as settled law.
2. **Round 3**: Refines #1. A document's conclusion is protected only when the
   document is *allowed* to reach it (a memo, filed advocacy) — not when the
   document is the *neutral operational record* a specific task's failure mode
   turns on. Strip it from the latter even though #1 would otherwise protect it.
   (This is why IR_2025-1018_final.docx's course-and-scope language was cut in
   round 3 but reserve_memo.docx's was not — the incident report is Safety's
   operational record of what happened, which is exactly what T5's candor test
   needs the solver to independently reach; the reserve memo is Espinoza's own
   advocacy-adjacent business judgment, which a reserve memo is supposed to state.)

## Findings that will keep recurring — do not re-investigate, just re-dispute

AutoQC repeats these almost every round because disputes aren't entered into the
Studio UI until the very end (user's explicit workflow — see below). A repeat is
expected, not a sign the reasoning was wrong.

| Finding | Verified answer | Disposition |
|---|---|---|
| Reyes lien/EOB "double-counts" $3,200 patient responsibility | Exhibit A's 4 columns reconcile exactly: $2,640,800 adj + $196,000 paid + $3,200 patient-resp = $2,840,000 billed. Ledger's $2,644,000 is a coarser adjustments bucket that nets the same gap. | FALSE POSITIVE — disputed R1-4 |
| docket_entry.xlsx gives all claimants a uniform 10/18/2027 deadline | Same declared trap family as matter_calendar_MatterHub.csv — both export the wrong case-level date by design (T1's Design Purpose: the firm's own MatterHub system carries this error and T1's job is to correct it, in MatterHub, not in this exported CSV). | TRAP — never touch |
| "No Broken Document References" (DOT Attachments A-C, FST supplement's 4 related records, final incident report's unmounted ops sheets/DriveCam, lien's Tabs 1-11, native MP4/A53) | Real litigation/business records legitimately reference material retained in a physical/other-system location without every item being independently exported into this filesystem. Native MP4 is the same App-Data-companion-export pattern as every other "9 inventory mismatches" item (see below). | FALSE POSITIVE pattern — disputed R1-4. Exception: coverage_summary.pdf's "SEE ATTACHED MEMORANDUM" was a real false claim (nothing attached) — fixed R3. |
| Docuseal/Wiki.js state changes, A62 live practice-management corrections | App Data seeded through a separate pipeline this filesystem-only toolkit doesn't cover. | OUT OF SCOPE — disputed R2-4 |
| TCR.pdf (= Shared/Police/TC_2025-1018.pdf) is an uncompleted blank CHP 555 template | Read all 6 pages directly, twice (R3 and R4): fully populated (case ID, party/vehicle data, diagram narrative, impairment investigation, certification). Not blank, not 4 pages. | FALSE POSITIVE — disputed R3-4 |
| scene_photos_2025-1018.pdf / onboard_video_still_log.pdf "impersonate" photo/video evidence | Both match their own registry Name/Style exactly ("Photo Log" / "still-frame log") and each documents where the real photos/video are archived. An honest index, not impersonation. | FALSE POSITIVE — disputed R2-4 |
| LIFE CARE PLAN.pdf external citations (TreasuryDirect/NY DFS/CMS) return 404/505 | The actual mounted file is 19 pages. Cited pages (37, 40, 115-116) don't exist in a 19-page document — AutoQC is checking against a page count consistent with a 120+ page file that isn't the one mounted here. | FALSE POSITIVE — disputed R2-4 |
| EOB / life-care plan / wage records "supply the damages answer" (No Reachable Shortcut) | Checked directly against T4/T6's Design Purpose in the spec: A35 (EOB) stating $196K paid, A36 (life-care plan) stating its own $4,240,000 PV, A37 (wage records) stating its own $1,200,000 lost-earning-capacity opinion are each **exactly** the artifact the task is supposed to read and apply legal doctrine to (Howell/Corenbaum paid-not-billed; PV-not-undiscounted). None states the memo's actual synthesis (net of lien, comparative fault, combined total). A36's PV-vs-undiscounted gap is its *registered* trap, working as designed. | NOT LEAKAGE — disputed R4, new reasoning, should hold |
| Late-claim application argues for the relief it's applying for; reserve memo reaches a course-and-scope conclusion | Advocacy document / internal memo drawing its own conclusion — protected by standing ruling #1. | PROTECTED — disputed R2-4 |
| Production tracker's A42 (junior note) "first-pass" vs A43 (senior memo) "confirmed" privilege split | A17's registered trap, working as designed — T9's whole job is to independently correct A42's tag via CCP §2018.030, not defer to the tracker's own unreviewed status column. | TRAP — never touch |

## Tool false-positive patterns (don't re-investigate these either)

- **blast_radius.py "footing broke"**: `medical_billing_ledger.csv` row `TSG-002` and
  `reserve_ledger.csv` row `RL-2025-0107` get flagged every round. Both are ordinary
  line items (TSG-002 is literally a surgery named "Total splenectomy" — the word
  "Total" tripped the heuristic; RL-2025-0107 is a normal LAE ledger entry). The tool
  sums *every* row above as if hunting a subtotal, which misfires on flat
  transactional ledgers with no real total rows. Verified by hand twice (R3, R4).
- **blast_radius.py "dependency set"**: `nhalstead@halstead-cruz.com` (matches the
  already-correct trap file), `$6,540` (an unrelated passenger's PT paid amount,
  coincidental match), `Supervisor-Reviewed` (correctly appears elsewhere — the term
  is now used consistently), `the DOT Post-Accident Test Record` (correct
  cross-reference). All verified fine, not stale values.
- **leak_scan.py "task answer" hits for 911.4/946.6** in intake_memo.docx,
  matter_calendar_MatterHub.csv, hold_demand_letter.pdf, claims_tracker.csv: all are
  Reyes's own late-claim-track statute citations, which T1's *correct* memo is
  explicitly supposed to reference. None states the actual hidden answer (the
  passengers' 08/18/2026 deadline, or the A62 correction). Verified against T1's
  Design Purpose directly, R3 and R4.
- **leak_scan.py "reconciling language"** in IR_2025-1018_final.docx ("Vehicle-to-
  block assignment... is reconciled to the Div.") and RunSchedule's Notes sheet
  ("...reconciles to the operator bid award..."): pre-existing text never touched by
  any edit, coincidental digit matches with unrelated traps' registered numbers, not
  real trap defusal.
- **IR_2025-1018_final.docx filename contains "final"**: pre-existing, spec-registered
  filename (A02's Location field). Not a remediation artifact, not in scope to rename.

## The Trip 06 timing resolution (round 4 — read this in full if it recurs)

This one took real back-and-forth, so the reasoning matters if AutoQC raises it again
in a different shape.

**The tension**: RunSchedule_Owl512.xlsx's own timepoint columns (Fifth → Third →
Downtown Loop → Alder Creek/Broadway → Poplar/Rivergate Plaza) are corroborated
identically across all *other* 9 trips in the APC ridership log — e.g. Trip 04 NB
takes 27 minutes from Poplar to reach Third. But Trip 06 (the collision trip) reaches
Third only ~90 seconds after leaving Poplar per the APC log, video log, and dispatch
log alike — skipping the Alder Creek/Broadway and Downtown Loop scans entirely. Both
"02:05" (collision time) and "02:31" (Third's scheduled time) are independently
canonical: A01 and A02's own spec Description fields register 02:05 as *the*
collision time, not just narrative color from the video log.

**Why neither side can be changed**: moving 02:05 contradicts the spec's own
registered artifact descriptions. Moving 02:31 (or redesigning the route's stop
order) contradicts 9 other trips' worth of already-consistent APC data. Explaining
the gap (e.g. "the driver deviated from his route") isn't in T5's registered trap and
would be manufactured reconciling language — exactly what leak_scan is built to
catch — plus it risks quietly injecting a new fact that muddies T5's actual candor
test (was Keeler on his assigned route — not whether he took a shortcut mid-route).

**The fix** (user-directed, R4): state both numbers plainly, explain neither.
- `RunSchedule_Owl512.xlsx`, Trip 06 row, S. Main/Third cell: now reads
  `02:31 scheduled (actual: 02:05, per incident record)`.
- Removed the old "Key Timepoint — S. Main / Third" explanatory block (rows 32-35)
  that used to gloss this with "SB timepoint pass" / "headway anchor" jargon — once
  the cell is self-explanatory, the block was redundant *and* was itself confusing.
- `Dispatch_log_2025-1018.csv` line 33 (02:06 entry): removed the matching
  "(SB reference timepoint 02:05)" cross-reference for the same reason.
- Nothing else changed. If AutoQC flags "why does Trip 06 skip two stops" or similar
  in a future round, the answer is: that's now an intentionally unexplained fact for
  the task-solver to notice, not a defect to fix further.

Note for future rounds: when editing this sheet, **clear cell contents rather than
`ws.delete_rows()`** — openpyxl does not reliably shift merged-cell ranges on row
deletion; a first attempt at this exact fix corrupted the "Assignment Sign-Off" table
below it. Caught via diff before saving to the real file; not a live problem, just a
tooling gotcha worth remembering.

## Round-by-round fix history (brief — see change_manifest.md for the full ledger)

- **R1**: banned-name scrub (Meridian → Ashby), white-on-gray table headers in
  Keeler_personnel.docx, established the A53-native-MP4 App-Data precedent.
- **R2**: direction/curb fixes (southbound→northbound, west→east side across several
  files), $48,500 City demand date/notes fix, unfulfilled attachment/enclosure
  language reworded across 5 files, A09/A52 rewritten to match registry exactly,
  photo/still-log decision (leave as honest logs), de-signposted reserve_memo.docx
  and IR_2025-1018_final.docx (first pass).
- **R3**: comprehensive A## build-code scrub (CHRONIC — 3 rounds of instance-only
  patching before this), closed R2's signposting gaps (reserve_memo.docx para 31,
  IR_2025-1018_final.docx paras 40/43), full southbound sweep (Complaint_Reyes_filed
  + Blau addendum), docket_entry.xlsx trap-family investigation, coverage_summary.pdf
  false-attachment fix, incident-number suffix fix, RunSchedule contrast fix,
  medical_billing_ledger TOTAL-row removal, T5 course-and-scope reconsideration
  (the one place round 2's reserve-memo ruling was deliberately *not* extended).
- **R4**: LIFE CARE PLAN.pdf weighted-annual-cost arithmetic (4 categories
  recomputed by hand, rounding/geo-adjustment plug rebalanced to preserve the
  canonical $180,000/$6,480,000/$4,240,000), RunSchedule Status column color
  encoding, IR_2025-1018_draft.docx native Word comment (format-native markup, no
  text changed), Trip 06 schedule-vs-actual clarification (above).

## Workflow reminder

User enters disputes into the AutoQC/Studio UI in one batch at the very end, not
round-over-round — so repeat findings on already-disputed items are expected and
are not evidence the reasoning was wrong. Keep fixing what's genuinely new/valid
each round; keep disputing the rest with the reasoning above; flag anything with
the stakes/ambiguity of the §911.6 statute question or the Trip 06 timing question
before touching it unilaterally.

## Toolkit quick reference

All in `.claude/skills/world-qc-remediation/scripts/`, run from `/home/user/Julius`:
- `round_log.py start filesystem --round N --findings qc_workspace/roundN_findings.txt`
- `round_log.py rulings filesystem` — print standing rulings (read this first, every round)
- `blast_radius.py all filesystem` — Gate 6, run after every round's edits
- `inventory_check.py check WORLD_SPEC.xlsx filesystem --round N` — Gate 8
- `leak_scan.py filesystem --spec WORLD_SPEC.xlsx` — Gate 8
- `round_log.py close filesystem --round N --fixed X --expanded X --traps X --false X --blocked X --changed "..." --dispute "..."`
- `round_log.py summary filesystem` — RLS paste block
