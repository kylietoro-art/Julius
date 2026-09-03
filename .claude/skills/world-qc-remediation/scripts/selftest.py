#!/usr/bin/env python3
"""Layer-1 adversarial battery for spec_check.py. Builds tiny known-answer fixtures, runs the
script as a black box, asserts expected behavior. Weighted toward trap preservation."""
import atexit, openpyxl, os, shutil, subprocess, sys, tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SPEC_CHECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec_check.py")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
def run_script(name, *args):
    import subprocess as _sp, sys as _s
    # WQC_IN_SELFTEST stops setup_check from launching this same self-test, which would recurse
    # forever and look to the user like a hang rather than an error.
    _env = dict(os.environ, WQC_IN_SELFTEST="1")
    r=_sp.run([_s.executable, os.path.join(SCRIPTS,name), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    return r.stdout + r.stderr

results=[]
def check(name, cond, detail=""):
    results.append((name, cond, detail))
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   [{detail}]" if detail and not cond else ""))

def run(cmd, *args):
    r=subprocess.run([sys.executable, SPEC_CHECK, cmd, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout + r.stderr

def build_spec(path, canon_rows, task_trap=None, art_rows=None):
    """canon_rows: list of [name,value,src,must,note]; art_rows: list of [ID,trapcontent,relates,loc]"""
    wb=openpyxl.Workbook()
    cv=wb.active; cv.title="② Canonical Values"
    cv.append(["Thin value layer (NOT a fact ledger)"])
    cv.append(["Value name","Type","Value","Source artifact (ID)","Must match (IDs)","Note"])
    for r in canon_rows: cv.append([r[0],"",r[1],r[2],r[3],r[4]])
    t=wb.create_sheet("③ Tasks")
    t.append(["Task #","Task Name","Workflow Type","Primary Artifacts","Design Purpose","Expected Output","Trap: What Misleads","Trap: How Agent Fails","Trap: Remediation Path"])
    if task_trap: t.append(task_trap)
    a=wb.create_sheet("④ Artifacts")
    a.append(["registry narrative"])
    a.append(["ID","Type","Name","Format / App","Location / Address","Label","Prepared By","Description","Relates to (IDs)","Trap Content","Tasks","Reference Doc"])
    for ar in (art_rows or []):
        a.append([ar[0],"File",ar[0]+" file","TXT",ar[3],"Key","x","d",ar[2],ar[1],"",""])
    s=wb.create_sheet("REF · Schema Library")
    s.append(["Schema Library REFERENCE"])
    s.append(["App","Group","Artifact","Grain","Required schema fields","Content","References / ties","Default required","Depends on","Core / Supp","Lookup key","Active","Rank"])
    s.append(["ERPNext","Master","Company.csv","company","company","root","","Always","—","Core","x",1,1])
    s.append(["ERPNext","Master","Employee.csv","employee","employee,company","staff","Company","Always","Company","Core","x",1,2])
    wb.save(path)

def W(d, rel, content):
    p=os.path.join(d,rel); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(content); 

base=tempfile.mkdtemp()
atexit.register(lambda: shutil.rmtree(base, ignore_errors=True))

# ---- F1: numeric substring (327 must NOT match 3270) ----
d=os.path.join(base,"f1"); w=os.path.join(d,"world"); os.makedirs(w)
build_spec(os.path.join(d,"spec.xlsx"),
  [["Period-end headcount","327","A20","A21",""]],
  art_rows=[["A20","None.","","/hc.txt"],["A21","None.","","/roster.txt"]])
W(w,"hc.txt","headcount as of date: 327 employees")
W(w,"roster.txt","units sold 3270; roster of names only, no headcount figure")
out=run("ties", os.path.join(d,"spec.xlsx"), w)
print("\n[F1 numeric-substring] 327 vs 3270")
check("F1 flags A21 as a real tie miss (327 not truly present)", "TIE MISS" in out and "A21" in out, out.replace(chr(10)," ")[:200])

# ---- F2: trap declared ONLY in ③ Tasks (must NOT be flagged) ----
d=os.path.join(base,"f2"); w=os.path.join(d,"world"); os.makedirs(w)
build_spec(os.path.join(d,"spec.xlsx"),
  [["FY revenue","$43.2M","A07","A03, A12",""]],
  task_trap=["T1","Reconcile","P0","A03, A07, A12","audited governs","memo","Board deck A03 shows $43.8M","copies 43.8M","read A07"],
  art_rows=[["A07","None.","","/audited.txt"],["A03","None.","","/deck.txt"],["A12","None.","","/gl.txt"]])
W(w,"audited.txt","audited revenue $43.2M"); W(w,"deck.txt","slide: $43.8M flash"); W(w,"gl.txt","revenue 43.2")
out=run("ties", os.path.join(d,"spec.xlsx"), w)
print("\n[F2 ③-only trap] A03 declared trap only in Tasks tab")
check("F2 does NOT flag A03 (it's a declared trap)", "tie issue(s)" in out and ("A03" not in out or "TIE MISS" not in out), "A03 wrongly flagged: "+out.replace(chr(10)," ")[:200])
check("F2 still ties A07/A12 clean (no false miss)", "tie issue(s)" in out and "A07" not in out and "A12" not in out, out.replace(chr(10)," ")[:160])

# ---- F3: ④-only trap (control, should already pass) ----
d=os.path.join(base,"f3"); w=os.path.join(d,"world"); os.makedirs(w)
build_spec(os.path.join(d,"spec.xlsx"),
  [["FY revenue","$43.2M","A07","A03, A12",""]],
  art_rows=[["A07","None.","","/audited.txt"],["A03","Stale $43.8M flash never refreshed","","/deck.txt"],["A12","None.","","/gl.txt"]])
W(w,"audited.txt","audited $43.2M"); W(w,"deck.txt","$43.8M"); W(w,"gl.txt","43.2")
out=run("ties", os.path.join(d,"spec.xlsx"), w)
print("\n[F3 ④-only trap] control")
check("F3 does NOT flag A03", "tie issue(s)" in out and ("A03" not in out or "TIE MISS" not in out), out.replace(chr(10)," ")[:160])

# ---- F4: value formats ($43.2M vs 43,200,000) must MATCH (no false miss) ----
d=os.path.join(base,"f4"); w=os.path.join(d,"world"); os.makedirs(w)
build_spec(os.path.join(d,"spec.xlsx"),
  [["FY revenue","$43.2M","A07","A12",""]],
  art_rows=[["A07","None.","","/a.txt"],["A12","None.","","/b.txt"]])
W(w,"a.txt","revenue $43.2M"); W(w,"b.txt","total revenue 43,200,000 for the year")
out=run("ties", os.path.join(d,"spec.xlsx"), w)
print("\n[F4 value formats] 43,200,000 should satisfy $43.2M")
check("F4 no false tie miss on 43,200,000", "tie issue(s)" in out and "TIE MISS" not in out, out.replace(chr(10)," ")[:160])

# ---- F5: NO traps declared (guard should see empty manifest) ----
d=os.path.join(base,"f5")
build_spec(os.path.join(d if os.path.exists(d) else os.makedirs(d) or d,"spec.xlsx"),
  [["FY revenue","$43.2M","A07","A03",""]],
  art_rows=[["A07","None.","","/a.txt"],["A03","None.","","/b.txt"]])
out=run("traps", os.path.join(d,"spec.xlsx"))
print("\n[F5 no declared traps] manifest empty -> guard must warn")
check("F5 reports zero traps + warns", ("0 declared" in out) and ("none found" in out.lower()), out.replace(chr(10)," ")[:200])

# ---- F6: real drift IS flagged (control) ----
d=os.path.join(base,"f6"); w=os.path.join(d,"world"); os.makedirs(w)
build_spec(os.path.join(d,"spec.xlsx"),
  [["Cash balance","$500,000","A30","A31",""]],
  art_rows=[["A30","None.","","/a.txt"],["A31","None.","","/b.txt"]])
W(w,"a.txt","cash $500,000"); W(w,"b.txt","cash on hand $480,000 (wrong)")
out=run("ties", os.path.join(d,"spec.xlsx"), w)
print("\n[F6 real drift] control")
check("F6 flags the drift (A31 missing $500,000)", "TIE MISS" in out and "A31" in out, out.replace(chr(10)," ")[:160])


# ---- F7: Type=Trap row must NOT be tie-flagged ----
d=os.path.join(base,"f7"); w=os.path.join(d,"world"); os.makedirs(w)
sp=os.path.join(d,"spec.xlsx")
import openpyxl as _ox
wb=_ox.Workbook(); cv=wb.active; cv.title="② Canonical Values"
cv.append(["hdr"]); cv.append(["Value name","Type","Value","Source artifact (ID)","Must match (IDs)","Note"])
cv.append(["Stale ARR","Trap","$43.8M","A03","A12",""])
cv.append(["Headcount","Grounding","95.0","A20","A21",""])
a=wb.create_sheet("④ Artifacts"); a.append(["n"])
a.append(["ID","Type","Name","Format / App","Location / Address","Label","Prepared By","Description","Relates to (IDs)","Trap Content","Tasks","Reference Doc"])
for aid,loc in [("A03","/d.txt"),("A12","/g.txt"),("A20","/h.txt"),("A21","/r.txt")]:
    a.append([aid,"File",aid,"TXT",loc,"K","x","d","","None.","",""])
wb.save(sp)
W(w,"d.txt","$43.8M"); W(w,"g.txt","43.2"); W(w,"h.txt","95 employees"); W(w,"r.txt","names, 950 rows")
out=run("ties", sp, w)
print("\n[F7 Type=Trap skip + 95.0==95]")
check("F7 skips the Type=Trap row (A03/A12 not flagged)", "tie issue(s)" in out and "A03" not in out and "A12" not in out, out.replace(chr(10)," ")[:160])
check("F7 flags real drift; 95.0 not in '950'", "TIE MISS" in out and "A21" in out, out.replace(chr(10)," ")[:160])

# ---- F8: block-aware footing (stacked tables clean; broken block flagged) ----
d=os.path.join(base,"f8"); os.makedirs(d)
open(os.path.join(d,"stack.csv"),"w").write("s,amt\nA1,100\nA2,200\nA TOTAL,300\nB1,50\nB2,75\nB TOTAL,125\n")
open(os.path.join(d,"broke.csv"),"w").write("s,amt\nA1,100\nA2,200\nA TOTAL,999\n")
o1=run_script("reconcile_entities.py","footing",os.path.join(d,"stack.csv"))
o2=run_script("reconcile_entities.py","footing",os.path.join(d,"broke.csv"))
print("\n[F8 block-aware footing]")
check("F8 stacked sub-tables = 0 false positives", "0 footing mismatch" in o1, o1.replace(chr(10)," ")[:120])
check("F8 genuinely broken block = flagged", "FOOTING" in o2 and "999" in o2, o2.replace(chr(10)," ")[:120])

# ---- F9: entity conformer, WRONG NAME defect + constant-fill "46" mess; NO false positive on a
#          legitimate ID-only reference row ----
d=os.path.join(base,"f9"); w=os.path.join(d,"world"); os.makedirs(w)
open(os.path.join(d,"master.csv"),"w").write("employee_id,name\nHR-EMP-00046,Peridot Chandra\nHR-EMP-00045,Ada Lovelace\n")
# (1) a row that stamps HR-EMP-00046 but names a DIFFERENT canonical employee -> WRONG NAME
open(os.path.join(w,"roster.csv"),"w").write("employee_id,name\nHR-EMP-00046,Ada Lovelace\n")
# (2) a legitimate ID-only crosswalk (single vendor -> employee) -> must NOT be flagged
open(os.path.join(w,"vendors.csv"),"w").write("vendor,erpnext_employee_id\nPiedmont Catering LLC,HR-EMP-00046\n")
# (3) the real "46" mess: the same ID constant-filled across a many-vendor crosswalk that also
#     carries other IDs -> CONSTANT FILL
rows="".join(f"Vendor {i},HR-EMP-00046\n" for i in range(11))
open(os.path.join(w,"crosswalk.csv"),"w").write("vendor,erpnext_employee_id\n"+rows+"Vendor Z,HR-EMP-00045\n")
o=run_script("entity_conformer.py","check",os.path.join(d,"master.csv"),w,"--id-col","employee_id","--name-col","name")
print("\n[F9 entity conformer]")
check("F9 flags WRONG NAME (ID stamped with another entity's name)", "WRONG NAME" in o and "roster.csv" in o, o.replace(chr(10)," ")[:140])
check("F9 flags the constant-fill '46' mess", "CONSTANT FILL" in o and "crosswalk.csv" in o, o.replace(chr(10)," ")[:140])
check("F9 does NOT false-positive on a legit ID-only crosswalk row", "vendors.csv" not in o, o.replace(chr(10)," ")[:140])

# ---- F10: metadata hygiene scan flags openpyxl fingerprint, clean removes it ----
d=os.path.join(base,"f10"); os.makedirs(d)
mx=os.path.join(d,"s.xlsx"); _wb=_ox.Workbook(); _wb.active["A1"]="x"; _wb.save(mx)
o_scan=run_script("metadata_hygiene.py","scan",mx)
run_script("metadata_hygiene.py","clean",mx,"--app","Microsoft Excel","--date","2025-09-15",
           "--world",os.path.dirname(mx))
o_after=run_script("metadata_hygiene.py","scan",mx)
print("\n[F10 metadata hygiene]")
check("F10 scan flags openpyxl fingerprint", "openpyxl" in o_scan.lower(), o_scan.replace(chr(10)," ")[:120])
check("F10 clean removes it", "0 file(s) leaking" in o_after, o_after.replace(chr(10)," ")[:120])

# ---- F11: markup-in-doc scan flags literal markdown/html ----
d=os.path.join(base,"f11"); os.makedirs(d)
try:
    import docx as _dx
    doc=_dx.Document(); doc.add_paragraph("## Heading printed literally"); doc.add_paragraph("<td>cell</td>"); doc.save(os.path.join(d,"vend.docx"))
    o=run_script("pdf_markup_scan.py","scan",d)
    print("\n[F11 markup scan]")
    check("F11 flags literal markdown/html in a doc", "MARKUP" in o and "vend.docx" in o, o.replace(chr(10)," ")[:140])
except Exception as _e:
    print("\n[F11 markup scan] SKIPPED (python-docx missing)")

# ---- F12: entity_conformer apply, dry run doesn't write; --write fixes; idempotent ----
d=os.path.join(base,"f12"); w=os.path.join(d,"world"); os.makedirs(w)
open(os.path.join(d,"master.csv"),"w",encoding="utf-8").write("id,name\nHR-EMP-00046,Peridot Chandra\nHR-EMP-00047,Marcus Vale\n")
rp=os.path.join(w,"roster.csv")
open(rp,"w",encoding="utf-8").write("id,name\nHR-EMP-00046,Marcus Vale\n")   # wrong name for the ID
o_dry=run_script("entity_conformer.py","apply",os.path.join(d,"master.csv"),w,"--id-col","id","--name-col","name")
after_dry=open(rp,encoding="utf-8").read()
o_wr=run_script("entity_conformer.py","apply",os.path.join(d,"master.csv"),w,"--id-col","id","--name-col","name","--write")
after_wr=open(rp,encoding="utf-8").read()
o_re=run_script("entity_conformer.py","check",os.path.join(d,"master.csv"),w,"--id-col","id","--name-col","name")
print("\n[F12 entity_conformer apply]")
check("F12 dry run does not modify the file", "Marcus Vale" in after_dry and "Peridot" not in after_dry, o_dry.replace(chr(10)," ")[:120])
check("F12 --write fixes the wrong name", "Peridot Chandra" in after_wr, after_wr.replace(chr(10)," ")[:120])
check("F12 fix is idempotent (re-check clean)", "0 entity issue" in o_re, o_re.replace(chr(10)," ")[:120])

# ---- F13: a_scrub, clean swap applied; doubled-context flagged; non-registry code left alone ----
d=os.path.join(base,"f13"); w=os.path.join(d,"world"); os.makedirs(w)
_sp=_ox.Workbook(); _a=_sp.active; _a.title="④ Artifacts"
_a.append(["ID","Type","Name","Location / Address","Trap Content"])
_a.append(["A26","plan","Occupant Load Plan","/x.pdf",""])
_a.append(["A09","policy","System-of-Record Policy","/y.pdf",""])
_sp.save(os.path.join(d,"spec.xlsx"))
open(os.path.join(w,"dict.csv"),"w",encoding="utf-8").write("f,note\na,cross-ref A26 here\nb,per Policy A09\nc,invoice A77 is real\n")
o=run_script("a_scrub.py","scan",os.path.join(d,"spec.xlsx"),w)
print("\n[F13 a_scrub]")
check("F13 auto-fixes a clean swap (A26)", "A26 ->" in o and "Occupant Load Plan" in o, o.replace(chr(10)," ")[:140])
check("F13 flags doubled-context code for review (A09/Policy)", "A09" in o and "rewrite by hand" in o, o.replace(chr(10)," ")[:140])
check("F13 leaves a non-registry code alone (A77)", "A77" in o and "④ registry" in o, o.replace(chr(10)," ")[:140])

# ---- F14: cp1252 recall, scan_world finds an accented value in a non-UTF-8 file ----
d=os.path.join(base,"f14"); os.makedirs(d)
with open(os.path.join(d,"vendor.csv"),"wb") as fh: fh.write("vendor,city\nCafé Noir,Zürich\n".encode("cp1252"))
o=run_script("scan_world.py","occurrences","Café",d)
print("\n[F14 cp1252 recall]")
check("F14 scan_world finds an accented value in a cp1252 file", "vendor.csv" in o and "1 occurrence" in o.lower() or "occurrence(s) of 'Caf" in o, o.replace(chr(10)," ")[:140])

# ---- F15: round_log, class bucketing, repeat detection, and the batch gate ----
d=os.path.join(base,"f15"); w=os.path.join(d,"World"); os.makedirs(w)
open(os.path.join(w,"x.txt"),"w").write("x")
r1=os.path.join(d,"r1.txt"); r2=os.path.join(d,"r2.txt")
open(r1,"w",encoding="utf-8").write(
  "AutoQC Report - Round 1 header line that is not a finding\n"
  "- [P0] No Out-of-World or Build Artifacts: Crosswalk.xlsx says \"per Policy A09\", a spec index code.\n"
  "- [P1] In-World vs Out-Of-World Separation And Metadata Cleanliness: 6 files carry a Producer of reportlab.\n"
  "- [P1] Calculation & Fixture Accuracy: Budget_Rollup.xlsx column D does not sum to the stated total.\n")
open(r2,"w",encoding="utf-8").write(
  "- [P1] Calculation & Fixture Accuracy: Regional_Rollup.xlsx does not sum to the stated total.\n"
  "- [P1] Timeline And Dates Are Coherent: Offer_Letter.docx is dated after the anchor date.\n"
  "- [P1] No Real PII or Copyrighted Material: Contacts.csv uses a non-reserved phone pattern.\n")
o1=run_script("round_log.py","start",w,"--round","1","--findings",r1)
o2=run_script("round_log.py","start",w,"--round","2","--findings",r2)
import subprocess as _sp2
def _gate(*a):
    r=_sp2.run([sys.executable, os.path.join(SCRIPTS,"round_log.py"), *a],
               capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout + r.stderr
rc_short,o_short=_gate("close",w,"--round","2","--fixed","1")
rc_full,o_full=_gate("close",w,"--round","2","--fixed","2","--traps","1")
print("\n[F15 round_log]")
check("F15 drops the report header, counts 3 findings", "3 findings" in o1, o1.replace(chr(10)," ")[:140])
check("F15 metadata finding is NOT filed as A## leakage (dimension prefix stripped)",
      "Tool fingerprints" in o1, o1.replace(chr(10)," ")[:200])
check("F15 filename capture does not swallow preceding words",
      "budget_rollup.xlsx" in o1 and "in budget_rollup.xlsx" not in o1, o1.replace(chr(10)," ")[:200])
check("F15 flags the repeat class in round 2", "REPEAT" in o2 and "foot" in o2, o2.replace(chr(10)," ")[:200])
check("F15 does not flag a first-time class as a repeat", "Dates, chronology" in o2, o2.replace(chr(10)," ")[:200])
check("F15 batch gate blocks a partial round (non-zero exit)",
      rc_short==1 and "NOT DONE" in o_short, o_short.replace(chr(10)," ")[:160])
check("F15 batch gate passes a full round (zero exit)",
      rc_full==0 and "Upload it" in o_full, o_full.replace(chr(10)," ")[:160])
check("F15 writes the log beside the world, never inside it",
      os.path.exists(os.path.join(d,"qc_workspace","round_log.md"))
      and not os.path.exists(os.path.join(w,"round_log.md")), "")

# ---- F16: blast_radius, the structural pass ----
# Fixture: entity_conformer fixed roster.csv but left the same wrong name standing in
# leave_ledger.csv (the classic instance-level fix), and a changed number is echoed in a memo.
d=os.path.join(base,"f16"); w=os.path.join(d,"World"); os.makedirs(os.path.join(w,"HR"))
os.makedirs(os.path.join(w,"Finance"))
bk=os.path.join(d,"qc_workspace"); os.makedirs(bk)
open(os.path.join(w,"HR","roster.csv"),"w",encoding="utf-8").write("id,name\nE-1044,Marta Reyes\n")
open(os.path.join(w,"HR","leave_ledger.csv"),"w",encoding="utf-8").write("id,name,days\nE-1044,Marta Reyas,4\n")
open(os.path.join(w,"Finance","rollup.csv"),"w",encoding="utf-8").write("region,amount\nNorth,412500\n")
open(os.path.join(w,"Finance","memo.txt"),"w",encoding="utf-8").write("North came in at 412500 per the rollup.\n")
open(os.path.join(bk,"change_manifest.md"),"w",encoding="utf-8").write(
  "# Change manifest\n\n## entity_conformer.py\n\n"
  "| File | Location | Old | → | New |\n|---|---|---|---|---|\n"
  "| roster.csv | row2 | Marta Reyas | → | Marta Reyes |\n\n"
  "## a_scrub.py\n\n"
  "| File | Location | Old | → | New |\n|---|---|---|---|---|\n"
  "| rollup.csv | B2 | 398100 | → | 412500 |\n")
o_stale=run_script("blast_radius.py","all",w)
print("\n[F16 blast_radius]")
check("F16 parses the change manifest across multiple tools",
      "2 file(s) edited across all rounds" in o_stale, o_stale.replace(chr(10)," ")[:180])
check("F16 catches the stale sibling the sweep missed",
      "Marta Reyas" in o_stale and "leave_ledger.csv" in o_stale, o_stale.replace(chr(10)," ")[:200])
check("F16 no false footing alarm on a clean edited file",
      "every edited spreadsheet still foots" in o_stale, o_stale.replace(chr(10)," ")[:200])
check("F16 lists the unedited file carrying a changed value",
      "memo.txt" in o_stale, o_stale.replace(chr(10)," ")[:200])
check("F16 verdict names the incomplete sweep as the cause",
      "sweeps were incomplete" in o_stale, o_stale.replace(chr(10)," ")[-260:])
# Now finish the sweep: the stale hit is gone, so the verdict must escalate to the tie explanation.
open(os.path.join(w,"HR","leave_ledger.csv"),"w",encoding="utf-8").write("id,name,days\nE-1044,Marta Reyes,4\n")
o_clean=run_script("blast_radius.py","all",w)
check("F16 clean sweep reports no stale values",
      "None of them are still present" in o_clean, o_clean.replace(chr(10)," ")[:200])
check("F16 verdict moves on to the tie once the sweep is complete",
      "sweeps were complete" in o_clean, o_clean.replace(chr(10)," ")[-260:])

# ---- F17: inventory_check, world vs spec registry, plus drift between rounds ----
d=os.path.join(base,"f17"); w=os.path.join(d,"World"); os.makedirs(os.path.join(w,"Fin"))
os.makedirs(os.path.join(w,"__MACOSX"))
_sp=_ox.Workbook(); _a=_sp.active; _a.title="④ Artifacts"
_a.append(["narrative"])
_a.append(["ID","Type","Name","Format / App","Location / Address","Relates to (IDs)","Trap Content"])
_a.append(["A01","File","rollup.csv","CSV","/Fin/rollup.csv","",""])
_a.append(["A02","File","deck.pptx","PPTX","/Fin/deck.pptx","",""])     # never generated
_a.append(["A03","File","policy.docx","DOCX","/Fin/policy.docx","",""]) # on disk as .pdf
_sp.save(os.path.join(d,"spec.xlsx"))
open(os.path.join(w,"Fin","rollup.csv"),"w").write("region,amount\nNorth,412500\n")
open(os.path.join(w,"Fin","policy.pdf"),"w").write("policy\n")
open(os.path.join(w,"Fin","extra.txt"),"w").write("unregistered\n")
open(os.path.join(w,"__MACOSX","j"),"w").write("x\n")
o1=run_script("inventory_check.py","check",os.path.join(d,"spec.xlsx"),w,"--round","1")
print("\n[F17 inventory_check]")
check("F17 flags a registered artifact with no file", "A02" in o1 and "resolves to a real file" in o1, o1.replace(chr(10)," ")[:200])
check("F17 flags a format mismatch against the file on disk",
      "spec says .docx, file is .pdf" in o1, o1.replace(chr(10)," ")[:200])
check("F17 flags a file no spec row claims", "extra.txt" in o1, o1.replace(chr(10)," ")[:200])
check("F17 sees junk inside a junk folder rather than pruning it",
      "__MACOSX/j" in o1.replace("\\","/"), o1.replace(chr(10)," ")[:200])
check("F17 first run reports no drift and writes a baseline",
      "This is the baseline" in o1, o1.replace(chr(10)," ")[:200])
# round 2: a rename and an added file, the replace-not-add violation
os.rename(os.path.join(w,"Fin","policy.pdf"), os.path.join(w,"Fin","policy.docx"))
open(os.path.join(w,"Fin","RECONCILIATION_NOTE.txt"),"w").write("the 412500 figure governs\n")
o2=run_script("inventory_check.py","check",os.path.join(d,"spec.xlsx"),w,"--round","2")
check("F17 drift catches a file that appeared", "RECONCILIATION_NOTE.txt" in o2 and "APPEARED" in o2, o2.replace(chr(10)," ")[:220])
check("F17 drift catches a file that disappeared", "policy.pdf" in o2 and "DISAPPEARED" in o2, o2.replace(chr(10)," ")[:220])
check("F17 the rename clears the format mismatch", "spec says .docx, file is .pdf" not in o2, o2.replace(chr(10)," ")[:220])
o3=run_script("inventory_check.py","drift",w)
check("F17 drift subcommand runs without a spec", "DRIFT SINCE" in o3, o3.replace(chr(10)," ")[:200])

# ---- F18: log_edit, a hand edit must reach the manifest and be seen by blast_radius ----
d=os.path.join(base,"f18"); w=os.path.join(d,"World"); os.makedirs(os.path.join(w,"Fin"))
os.makedirs(os.path.join(w,"HR"))
open(os.path.join(w,"Fin","rollup.csv"),"w").write("region,amount\nNorth,412500\n")
open(os.path.join(w,"HR","memo.txt"),"w").write("The North region closed at 398100 for the quarter.\n")
o_log=run_script("log_edit.py",w,"--file","Fin/rollup.csv","--old","398100","--new","412500",
                 "--where","row 2","--why","AQC r3")
o_br=run_script("blast_radius.py","all",w)
o_same=run_script("log_edit.py",w,"--file","Fin/rollup.csv","--old","5","--new","5")
print("\n[F18 log_edit]")
check("F18 records a hand edit", "Recorded" in o_log, o_log.replace(chr(10)," ")[:160])
check("F18 the hand edit reaches the change manifest",
      os.path.exists(os.path.join(d,"qc_workspace","change_manifest.md")), "")
check("F18 blast_radius sees a hand edit it did not make itself",
      "398100" in o_br and "memo.txt" in o_br, o_br.replace(chr(10)," ")[:220])
check("F18 verdict treats it as an incomplete sweep",
      "sweeps were incomplete" in o_br, o_br.replace(chr(10)," ")[-200:])
check("F18 refuses a no-op edit", "old and new are the same" in o_same, o_same.replace(chr(10)," ")[:160])

# ---- F19: setup_check, two false "do not start work" stops reported from the field ----
import importlib.util as _ilu, re as _re
_spec=_ilu.spec_from_file_location("sc", os.path.join(SCRIPTS,"setup_check.py"))
_sc=_ilu.module_from_spec(_spec); _spec.loader.exec_module(_sc)
print("\n[F19 setup_check false stops]")

# 1. trap count parsed as a number, not a substring. "0 declared" matched 10/20/50/100.
def _zero(n):
    out=f"{n} declared trap(s) found"
    m=_re.search(r"(\d+)\s+declared", out)
    return int(m.group(1))==0
check("F19 a spec with 50 traps does not read as zero", not _zero(50), "")
check("F19 nor 10, 20, 100 or 130",
      not any(_zero(n) for n in (10,20,100,130)), "")
check("F19 a spec with 0 traps still reads as zero", _zero(0), "")
check("F19 setup_check parses the count rather than substring matching",
      '"0 declared" in out' not in open(os.path.join(SCRIPTS,"setup_check.py"),encoding="utf-8").read(), "")

# 2. presence survives a stat that lies, which is what a Windows packaged-app path redirect does.
d=os.path.join(base,"f19"); os.makedirs(d)
open(os.path.join(d,"real.txt"),"w").write("x")
check("F19 present() finds a file that is there", _sc.present(d,"real.txt"), "")
check("F19 present() does not invent one that is not", not _sc.present(d,"ghost.txt"), "")
_orig=os.path.exists
try:
    os.path.exists=lambda p: False          # simulate the redirect: stat lies about everything
    check("F19 present() sees through a stat that returns False on a real file",
          _sc.present(d,"real.txt"), "os.path.exists was the only check")
    check("F19 and still says no when the file really is absent",
          not _sc.present(d,"ghost.txt"), "")
finally:
    os.path.exists=_orig

# ---- F20: findings split into per-ticket files, and the spec-edit detector ----
d=os.path.join(base,"f20"); w=os.path.join(d,"World"); os.makedirs(w)
open(os.path.join(w,"a.txt"),"w").write("x")
_sp2=_ox.Workbook(); _a2=_sp2.active; _a2.title="④ Artifacts"
_a2.append(["n"]); _a2.append(["ID","Type","Name","Format / App","Location / Address","Relates to (IDs)","Trap Content"])
_a2.append(["A01","File","a.txt","TXT","/a.txt","","planted stale figure"])
_spec2=os.path.join(d,"spec.xlsx"); _sp2.save(_spec2)
# two bullets only: this merged into one block before the threshold was lowered from 3 to 2
_f=os.path.join(d,"f.txt")
open(_f,"w",encoding="utf-8").write(
 '- [P1] Calculation: Q3.xlsx column D does not sum to D42.\n'
 '- [P0] Build Artifacts: Crosswalk.xlsx says "per Policy A09".\n')
o=run_script("round_log.py","start",w,"--round","1","--findings",_f)
tdir=os.path.join(d,"qc_workspace","tickets","round001")
print("\n[F20 tickets + spec-edit detector]")
check("F20 two bullets are two findings, not one merged block", "2 findings" in o, o.replace(chr(10)," ")[:160])
check("F20 one ticket file per finding",
      sorted(os.listdir(tdir))==["t01.txt","t02.txt"] if os.path.isdir(tdir) else False,
      str(os.listdir(tdir)) if os.path.isdir(tdir) else "no ticket dir")
_t1=open(os.path.join(tdir,"t01.txt"),encoding="utf-8").read()
check("F20 the ticket carries the finding verbatim", "does not sum to D42" in _t1, _t1[:160])
check("F20 and does not carry the other finding too", "Policy A09" not in _t1, _t1[:200])
check("F20 the ticket tells the fixer to enumerate every assertion",
      "one line each" in _t1, _t1[:200])
# single finding must not be split
_f1=os.path.join(d,"one.txt")
open(_f1,"w",encoding="utf-8").write('- [P0] Crosswalk.xlsx says "per Policy A09".\n')
shutil.rmtree(os.path.join(d,"qc_workspace"), ignore_errors=True)
o1=run_script("round_log.py","start",w,"--round","1","--findings",_f1)
check("F20 a single finding stays one finding", "1 findings" in o1, o1.replace(chr(10)," ")[:160])

# spec-edit detector: baseline, then edit the spec, then it must say so
shutil.rmtree(os.path.join(d,"qc_workspace"), ignore_errors=True)
oa=run_script("inventory_check.py","check",_spec2,w,"--round","1")
check("F20 first run records the spec hash", "Recorded" in oa, oa.replace(chr(10)," ")[:200])
ob=run_script("inventory_check.py","check",_spec2,w,"--round","2")
check("F20 an untouched spec reports unchanged", "Unchanged since the last snapshot" in ob, ob.replace(chr(10)," ")[:200])
_wb2=_ox.load_workbook(_spec2); _wb2["④ Artifacts"]["C3"]="edited by hand"; _wb2.save(_spec2)
oc=run_script("inventory_check.py","check",_spec2,w,"--round","3")
check("F20 an edited local spec is caught", "HAS BEEN EDITED" in oc, oc.replace(chr(10)," ")[:240])
check("F20 and it explains why that breaks the session",
      "the grader does not have" in oc, oc.replace(chr(10)," ")[:300])

# ---- F21: leak_scan + text-growth, against the real bridge-note case from testing ----
d=os.path.join(base,"f21"); w=os.path.join(d,"World","Fin"); os.makedirs(w)
_wr=os.path.join(d,"World")
open(os.path.join(w,"note4.txt"),"w",encoding="utf-8").write(
 "Note 4. Depreciation and amortisation.\n"
 "The capex plan's $14.0M is gross D&A on FY2025 additions while the AOP's $12.0M is the net "
 "increase over FY2024, and the two are not additive.\n")
# clean control: both figures, no explaining language, must NOT be a strong hit
open(os.path.join(w,"board_pack.txt"),"w",encoding="utf-8").write(
 "Q3 revenue was $14.0M against a plan of $12.0M.\nHeadcount closed at 412.\n")
open(os.path.join(w,"FINAL_summary.txt"),"w",encoding="utf-8").write("Close pack. Agreed to ledger.\n")
_s21=_ox.Workbook(); _c=_s21.active; _c.title="② Canonical Values"
_c.append(["hdr"]); _c.append(["Value name","Type","Value","Source artifact (ID)","Must match (IDs)","Note"])
_c.append(["D&A gross vs net","Trap","$14.0M","A12","","AOP states $12.0M net; not additive"])
_a21=_s21.create_sheet("④ Artifacts"); _a21.append(["n"])
_a21.append(["ID","Type","Name","Format / App","Location / Address","Relates to (IDs)","Trap Content"])
_a21.append(["A12","File","note4.txt","TXT","/Fin/note4.txt","","gross vs net D&A"])
_sp21=os.path.join(d,"spec.xlsx"); _s21.save(_sp21)

o=run_script("leak_scan.py",_wr,"--spec",_sp21)
print("\n[F21 leak_scan + growth]")
check("F21 catches the bridge note as reconciling language",
      "RECONCILING LANGUAGE" in o and "not additive" in o, o.replace(chr(10)," ")[:220])
check("F21 flags it as a defused trap, the strong tier",
      "TRAP POSSIBLY DEFUSED" in o and "note4.txt" in o, o.replace(chr(10)," ")[:260])
check("F21 puts the clean board pack in the WEAK tier, not the strong one",
      "no explaining language" in o and "board_pack.txt" in o.split("no explaining language")[1],
      o.replace(chr(10)," ")[:400])
check("F21 flags a FINAL filename", "FINAL_summary.txt" in o, o.replace(chr(10)," ")[-300:])
check("F21 says plainly it is not a verdict", "None of these is a verdict" in o, o.replace(chr(10)," ")[-200:])
o_nospec=run_script("leak_scan.py",_wr)
check("F21 without --spec it says the trap check is off",
      "trap-defusal check is OFF" in o_nospec, o_nospec.replace(chr(10)," ")[:200])

# text growth: baseline, add the bridge sentence, must be measured
d2=os.path.join(base,"f21b"); w2=os.path.join(d2,"World","Fin"); os.makedirs(w2)
open(os.path.join(w2,"note4.txt"),"w",encoding="utf-8").write("Note 4. D&A.\nMonthly per policy.\n")
run_script("inventory_check.py","check",_sp21,os.path.join(d2,"World"),"--round","1")
open(os.path.join(w2,"note4.txt"),"w",encoding="utf-8").write(
 "Note 4. D&A.\nMonthly per policy.\nThe capex plan's $14.0M is gross while the AOP's $12.0M is "
 "net, and the two are not additive.\n")
og=run_script("inventory_check.py","check",_sp21,os.path.join(d2,"World"),"--round","2")
check("F21 text growth is measured, not byte size", "gained text since the last round" in og,
      og.replace(chr(10)," ")[:240])
check("F21 growth report points at leak_scan", "leak_scan.py" in og, og.replace(chr(10)," ")[:300])
og2=run_script("inventory_check.py","check",_sp21,os.path.join(d2,"World"),"--round","3")
check("F21 no growth reported when nothing changed",
      "No file gained meaningful text" in og2, og2.replace(chr(10)," ")[:240])

# ---- F22: the FP&A 24 findings. Task-answer leak, rulings, backup location, PDF safety ----
d=os.path.join(base,"f22"); w=os.path.join(d,"World","fin"); os.makedirs(w)
_wr=os.path.join(d,"World")
# Bryan's case: T1's answer on a board slide, a bare number with no linguistic tell at all
open(os.path.join(w,"board_pack.txt"),"w",encoding="utf-8").write(
 "Slide 22. Deferred revenue of $385.0M reflects billings against the committed base of $670.0M.\n")
open(os.path.join(w,"credit_agreement.txt"),"w",encoding="utf-8").write(
 "Consolidated Recurring Revenue means $670.0M as of the test date.\n")
_s22=_ox.Workbook(); _t=_s22.active; _t.title="③ Tasks"
_t.append(["h"]); _t.append(["Task #","Task Name","Primary Artifacts","Expected Output","Design Purpose"])
_t.append(["T1","Lender ARR","A07","Identify $670.0M as the lender reportable figure","definition hunt"])
_a=_s22.create_sheet("④ Artifacts"); _a.append(["n"])
_a.append(["ID","Type","Name","Format / App","Location / Address","Relates to (IDs)","Trap Content"])
_a.append(["A07","File","credit_agreement.txt","TXT","/fin/credit_agreement.txt","",""])
_a.append(["A33","File","board_pack.txt","TXT","/fin/board_pack.txt","",""])
_c=_s22.create_sheet("② Canonical Values"); _c.append(["h"])
_c.append(["Value name","Type","Value","Source artifact (ID)","Must match (IDs)","Note"])
_sp22=os.path.join(d,"spec.xlsx"); _s22.save(_sp22)

o=run_script("leak_scan.py",_wr,"--spec",_sp22)
print("\n[F22 FP&A 24 regressions]")
check("F22 finds a task answer sitting outside that task's evidence",
      "A TASK ANSWER IS SITTING WHERE IT SHOULD NOT BE" in o and "board_pack.txt" in o,
      o.replace(chr(10)," ")[:260])
check("F22 names the task and the value", "T1" in o and "$670.0M" in o, o.replace(chr(10)," ")[:260])
check("F22 does NOT flag the file the answer is meant to come from",
      "credit_agreement.txt" not in o.split("TRAP")[0], o.replace(chr(10)," ")[:300])

# standing rulings survive a fresh round
run_script("round_log.py","decide",_wr,"The World Plan is gone; dispute every finding citing it.","--round","4")
_f22=os.path.join(d,"f.txt")
open(_f22,"w",encoding="utf-8").write("- [P1] one about A09.\n- [P1] two about footing.\n")
orl=run_script("round_log.py","start",_wr,"--round","5","--findings",_f22)
check("F22 a ruling is printed on every later round",
      "STANDING RULINGS" in orl and "World Plan is gone" in orl, orl.replace(chr(10)," ")[:260])

# metadata backup must land beside the world, never inside it
d2=os.path.join(base,"f22b"); w2=os.path.join(d2,"World"); os.makedirs(w2)
_mx=_ox.Workbook(); _mx.active["A1"]="x"; _mx.save(os.path.join(w2,"a.xlsx"))
run_script("metadata_hygiene.py","clean",os.path.join(w2,"a.xlsx"),"--date","2025-07-17",
           "--world",w2)
inside=[r for r,_,_ in os.walk(w2) if "qc_workspace" in r or "_qc_backup" in r]
check("F22 metadata backups are never written inside the world", not inside, str(inside))
check("F22 and they are written beside it",
      os.path.isdir(os.path.join(d2,"qc_workspace")), os.listdir(d2))

# corpus cache lives outside the world too

# --- F23: formula cells that lost their cached value ------------------------------------------
# openpyxl writes <f>SUM(A1:A2)</f><v></v>. The formula survives, the number does not, and AutoQC
# reads the number. The negative case matters most: a formula that DOES carry its value must not
# be flagged, or the scan cries wolf on every healthy workbook in the world.
d23 = os.path.join(base, "f23"); os.makedirs(d23)
_b = _ox.Workbook(); _bs = _b.active
_bs["A1"] = 1200; _bs["A2"] = 3400; _bs["A3"] = "=SUM(A1:A2)"
_b.save(os.path.join(d23, "broken.xlsx"))

_n = _ox.Workbook(); _ns = _n.active
_ns["A1"] = 1200; _ns["A2"] = 3400; _ns["A3"] = 4600          # no formulas at all
_n.save(os.path.join(d23, "no_formulas.xlsx"))

# what Excel would have written: formula AND cached value
import zipfile as _zf
_src = os.path.join(d23, "broken.xlsx"); _dst = os.path.join(d23, "cached.xlsx")
_z = _zf.ZipFile(_src); _items = {n: _z.read(n) for n in _z.namelist()}; _z.close()
for _k in list(_items):
    if _k.startswith("xl/worksheets/"):
        _items[_k] = _items[_k].decode().replace(
            "<f>SUM(A1:A2)</f><v></v>", "<f>SUM(A1:A2)</f><v>4600</v>").encode()
with _zf.ZipFile(_dst, "w", _zf.ZIP_DEFLATED) as _o:
    for _k, _v in _items.items():
        _o.writestr(_k, _v)

o23 = run_script("verify_xlsx.py", "--scan", d23)
check("F23 flags a formula cell openpyxl stripped the value from",
      "broken.xlsx" in o23 and "A3" in o23, o23.replace(chr(10), " ")[:200])
check("F23 does NOT flag a formula that carries its cached value",
      "cached.xlsx" not in o23, o23.replace(chr(10), " ")[:200])
check("F23 does NOT flag a workbook with no formulas",
      "no_formulas.xlsx" not in o23, o23.replace(chr(10), " ")[:200])

d23b = os.path.join(base, "f23b"); os.makedirs(d23b)
_n2 = _ox.Workbook(); _n2.active["A1"] = 1; _n2.save(os.path.join(d23b, "plain.xlsx"))
o23b = run_script("verify_xlsx.py", "--scan", d23b)
check("F23 a clean folder reports none, and does not demand --sheet/--range",
      "None." in o23b and "required" not in o23b, o23b.replace(chr(10), " ")[:200])

# --- F24: the fixers must not blank a workbook's answers -----------------------------------------
# a_scrub and entity_conformer only swap TEXT, but a plain openpyxl save blanks the cached result
# of every formula in the book. AutoQC reads cached results, so before this was fixed, one name
# conform quietly emptied every computed cell in the workbook and came back as a wall of findings.
import re as _re24
import zipfile as _z24
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as _c24

d24 = os.path.join(base, "f24"); w24 = os.path.join(d24, "World"); os.makedirs(w24)


def _book_with_values(dest):
    """A workbook whose formulas carry their computed results, as Excel would write it."""
    wb = _ox.Workbook(); ws = wb.active; ws.title = "Budget"
    ws["A1"] = 1200; ws["A2"] = 3400; ws["A3"] = "=SUM(A1:A2)"
    ws["B1"] = 0.15; ws["B3"] = "=A3*B1"
    ws["C1"] = '=IF(A3>1000,"OVER","UNDER")'          # a TEXT result, carries t="str"
    ws["D1"] = "See A09 attached"
    ws2 = wb.create_sheet("Detail"); ws2["A1"] = 50; ws2["A2"] = "=A1*2"
    stage = dest + ".stage"
    wb.save(stage)
    z = _z24.ZipFile(stage); items = {n: z.read(n) for n in z.namelist()}; z.close()
    rep = {"<f>SUM(A1:A2)</f><v></v>": "<f>SUM(A1:A2)</f><v>4600</v>",
           "<f>A3*B1</f><v></v>": "<f>A3*B1</f><v>690</v>",
           '<f>IF(A3&gt;1000,"OVER","UNDER")</f><v></v>':
               '<f>IF(A3&gt;1000,"OVER","UNDER")</f><v>OVER</v>',
           "<f>A1*2</f><v></v>": "<f>A1*2</f><v>100</v>"}
    for k in list(items):
        if k.startswith("xl/worksheets/"):
            s = items[k].decode()
            for a, b in rep.items():
                s = s.replace(a, b)
            items[k] = s.replace('<c r="C1"><f>IF', '<c r="C1" t="str"><f>IF').encode()
    with _z24.ZipFile(dest, "w", _z24.ZIP_DEFLATED) as o:
        for k, v in items.items():
            o.writestr(k, v)
    os.remove(stage)


def _vals(p):
    wb = _ox.load_workbook(p, data_only=True)
    return (wb["Budget"]["A3"].value, wb["Budget"]["B3"].value,
            wb["Budget"]["C1"].value, wb["Detail"]["A2"].value)


_book_with_values(os.path.join(w24, "budget.xlsx"))
check("F24 baseline: the test book really does carry its values",
      _vals(os.path.join(w24, "budget.xlsx")) == (4600, 690, "OVER", 100),
      str(_vals(os.path.join(w24, "budget.xlsx"))))

_sp24 = os.path.join(d24, "spec.xlsx")
_s = _ox.Workbook(); _sh = _s.active; _sh.title = "④ Artifacts"
_sh.append(["ID", "File Name", "Format"]); _sh.append(["A09", "Board Pack", "docx"])
_s.save(_sp24)

o24 = run_script("a_scrub.py", "apply", _sp24, w24, "--write")
_after = _vals(os.path.join(w24, "budget.xlsx"))
check("F24 a_scrub still makes the text fix",
      "Board Pack" in str(_ox.load_workbook(os.path.join(w24, "budget.xlsx"))["Budget"]["D1"].value),
      o24.replace(chr(10), " ")[:160])
check("F24 a_scrub does NOT blank the cached values (2 sheets, incl. a text result)",
      _after == (4600, 690, "OVER", 100), f"got {_after}, expected (4600, 690, 'OVER', 100)")
_f24 = _ox.load_workbook(os.path.join(w24, "budget.xlsx"))
check("F24 and the formulas are still formulas",
      _f24["Budget"]["A3"].value == "=SUM(A1:A2)" and _f24["Detail"]["A2"].value == "=A1*2",
      str(_f24["Budget"]["A3"].value))
o24b = run_script("verify_xlsx.py", "--scan", w24)
check("F24 the scan agrees the book is clean after a_scrub", "None." in o24b,
      o24b.replace(chr(10), " ")[:200])

# entity_conformer takes the same save path
d24c = os.path.join(base, "f24c"); w24c = os.path.join(d24c, "World"); os.makedirs(w24c)
_bk = os.path.join(w24c, "budget.xlsx"); _book_with_values(_bk)
_wb = _ox.load_workbook(_bk); _wb["Budget"]["D1"] = "changed"
_n = _c24.save_xlsx_preserving_values(_wb, _bk)
check("F24 the shared save helper carries every cached value across", _n == 4, f"carried {_n}, expected 4")
check("F24 entity_conformer's save path keeps the values",
      _vals(_bk) == (4600, 690, "OVER", 100), str(_vals(_bk)))

# Attribute ORDER must not matter. openpyxl writes Target before Id; Excel writes Id before
# Target. An ordered pattern passes on whichever file you happened to test and silently
# returns nothing on the other, which is how this shipped broken the first time.
_z = _z24.ZipFile(_bk); _it = {n: _z.read(n) for n in _z.namelist()}; _z.close()
_rels = _it["xl/_rels/workbook.xml.rels"].decode()
_swapped = _re24.sub(r'<Relationship Type="([^"]*)" Target="([^"]*)" Id="([^"]*)"/>',
                  r'<Relationship Id="\3" Type="\1" Target="\2"/>', _rels)
check("F24 test setup: the two attribute orders really are different", _swapped != _rels,
      _rels[:160])
_it["xl/_rels/workbook.xml.rels"] = _swapped.encode()
_bk2 = os.path.join(w24c, "excel_order.xlsx")
with _z24.ZipFile(_bk2, "w", _z24.ZIP_DEFLATED) as _o:
    for _k, _v in _it.items():
        _o.writestr(_k, _v)
check("F24 sheet lookup works with Id before Target (Excel's order)",
      set(_c24._xl_sheet_files(_c24._xl_read(_bk2))) == {"Budget", "Detail"},
      str(_c24._xl_sheet_files(_c24._xl_read(_bk2))))
check("F24 and with Target before Id (openpyxl's order)",
      set(_c24._xl_sheet_files(_c24._xl_read(_bk))) == {"Budget", "Detail"},
      str(_c24._xl_sheet_files(_c24._xl_read(_bk))))

# --- F25: a descriptive prefix must not cost the finding its class ------------------------------
# The dimension-prefix strip exists so "Metadata and Fingerprints: ..." is not classified by its
# dimension name (see F15). But the same strip ate "Footing:", which IS the content, dropping the
# finding into Uncategorised. Uncategorised findings never match each other, so REPEAT and CHRONIC
# went blind on the single most common defect class in the project.
d25 = os.path.join(base, "f25"); w25 = os.path.join(d25, "World"); os.makedirs(w25)
open(os.path.join(w25, "a.txt"), "w").write("x")
_r = os.path.join(d25, "r.txt")
open(_r, "w", encoding="utf-8").write(
    "- [P1] Footing: the Q3 summary total does not equal the sum of its components.\n")
o25 = run_script("round_log.py", "start", w25, "--round", "1", "--findings", _r)
check("F25 'Footing:' still classifies as a footing defect, not Uncategorised",
      "foot" in o25.lower() and "Uncategorised" not in o25, o25.replace(chr(10), " ")[:220])

# and it must still repeat-match a later round worded differently
_r2 = os.path.join(d25, "r2.txt")
open(_r2, "w", encoding="utf-8").write(
    "- [P1] The FY total in forecast.xlsx does not foot to the quarterly detail.\n")
run_script("round_log.py", "close", w25, "--round", "1", "--fixed", "1", "--disputed", "0")
o25b = run_script("round_log.py", "start", w25, "--round", "2", "--findings", _r2)
check("F25 and it matches the same class next round, so REPEAT fires",
      "REPEAT" in o25b, o25b.replace(chr(10), " ")[:220])


# --- F26: the folder auto-discovery ---------------------------------------------------------------
# Experts should never type a path. Each one they type is a chance to type the wrong one and lose a
# round. These are the layouts they actually arrive with.
import shutil as _sh26

def _mkspec26(path):
    wb = _ox.Workbook(); cv = wb.active; cv.title = "② Canonical Values"
    cv.append(["h"]); cv.append(["Value name", "Type", "Value", "Source artifact (ID)",
                                 "Must match (IDs)", "Note"])
    cv.append(["ARR", "Trap", "x", "A03", "A12", ""])
    a = wb.create_sheet("④ Artifacts"); a.append(["n"])
    a.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
              "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
    a.append(["A03", "File", "memo", "TXT", "/m.txt", "K", "x", "d", "", "stale", "", ""])
    wb.save(path)


def _folder26(name, world=True, spec=True, backup=True, decoy=False, second_world=False):
    d = os.path.join(base, name); os.makedirs(d)
    # the toolkit, at the path Claude Code loads from
    tk = os.path.join(d, ".claude", "skills", "world-qc-remediation", "scripts")
    os.makedirs(tk); open(os.path.join(tk, "setup_check.py"), "w").write("#")
    if world:
        w = os.path.join(d, "CrucibleWorld"); os.makedirs(w)
        open(os.path.join(w, "memo.txt"), "w").write("x")
        if backup:
            _sh26.copytree(w, os.path.join(d, "CrucibleWorld_backup"))
    if second_world:
        w2 = os.path.join(d, "OtherWorld"); os.makedirs(w2)
        open(os.path.join(w2, "b.txt"), "w").write("y")
    if spec:
        _mkspec26(os.path.join(d, "World_Spec.xlsx"))
    if decoy:
        wb = _ox.Workbook(); wb.active["A1"] = "budget"; wb.save(os.path.join(d, "Q3_Budget.xlsx"))
    return d


_ok = _folder26("f26_ok")
o26 = run_script("setup_check.py", "--folder", _ok)
check("F26 a correct folder resolves the world and the spec with no arguments",
      "CrucibleWorld" in o26 and "World_Spec.xlsx" in o26 and "WHAT TO FIX" not in o26,
      o26.replace(chr(10), " ")[:240])

# the .skill was extracted instead of the claude-folder zip, so the skill never loads
_ws = os.path.join(base, "f26_wrongspot"); os.makedirs(_ws)
_tk = os.path.join(_ws, "world-qc-remediation", "scripts"); os.makedirs(_tk)
open(os.path.join(_tk, "setup_check.py"), "w").write("#")
_w = os.path.join(_ws, "W"); os.makedirs(_w); open(os.path.join(_w, "a.txt"), "w").write("x")
_sh26.copytree(_w, os.path.join(_ws, "W_backup")); _mkspec26(os.path.join(_ws, "spec.xlsx"))
o26b = run_script("setup_check.py", "--folder", _ws)
check("F26 catches the toolkit being somewhere Claude Code will not load it",
      "WRONG SPOT" in o26b and "claude-folder" in o26b, o26b.replace(chr(10), " ")[:240])

# a spreadsheet that is not the spec must not be mistaken for one
_ns = _folder26("f26_nospec", spec=False, decoy=True)
o26c = run_script("setup_check.py", "--folder", _ns)
check("F26 does not mistake an ordinary workbook for the spec",
      "MISSING   The World Spec" in o26c and "Q3_Budget.xlsx" in o26c,
      o26c.replace(chr(10), " ")[:240])

_nb = _folder26("f26_nobackup", backup=False)
o26d = run_script("setup_check.py", "--folder", _nb)
# A hand-made copy of the world is no longer required: Studio holds the last uploaded revision and
# every fixer copies a file before changing it. Its absence must be a note, never a blocker.
check("F26 a missing world copy is a note, not something that stops the round",
      "NOTE" in o26d and "MISSING   A backup" not in o26d and "WHAT TO FIX" not in o26d,
      o26d.replace(chr(10), " ")[:240])

_tw = _folder26("f26_twoworlds", second_world=True)
o26e = run_script("setup_check.py", "--folder", _tw)
check("F26 asks rather than guessing when two folders could be the world",
      "ASK" in o26e and "OtherWorld" in o26e, o26e.replace(chr(10), " ")[:240])

check("F26 a broken layout stops before the checks, it does not half-run",
      "SETUP CHECK" not in o26b, o26b.replace(chr(10), " ")[:200])


# --- F27: the debugging-run fixes ------------------------------------------------------------------
# Every one of these was a confirmed bug found by auditing the toolkit against the conditions real
# folders have. They are locked here because each was invisible in normal use: the tool reported
# success while doing the wrong thing.
import csv as _csv27, io as _io27
sys.path.insert(0, SCRIPTS)
import _common as _c27

# (a) encoding round-trip. Reading cp1252 and saving utf-8 mojibakes every accented name in Excel.
d27 = os.path.join(base, "f27"); os.makedirs(d27)
_enc = {"cp1252.csv": ("Name,Vendor\r\nMarcus,Caf\u00e9 M\u00fcller\r\n", "cp1252"),
        "utf16.csv":  ("Name,Vendor\r\nMarcus,Caf\u00e9 M\u00fcller\r\n", "utf-16"),
        "bom.csv":    ("Name,Vendor\nMarcus,Caf\u00e9\n", "utf-8-sig")}
for fn, (txt, enc) in _enc.items():
    fp = os.path.join(d27, fn)
    open(fp, "wb").write(txt.encode(enc))
    orig = open(fp, "rb").read()
    _c27.write_text(fp, _c27.read_text(fp).replace("Marcus", "Dana"))
    now = open(fp, "rb").read()
    check(f"F27 {fn} keeps its encoding and its accents through an edit",
          _c27.sniff_encoding(now)[0] == _c27.sniff_encoding(orig)[0]
          and "Caf\u00e9" in _c27.read_text(fp) and "Dana" in _c27.read_text(fp),
          f"{_c27.sniff_encoding(orig)} -> {_c27.sniff_encoding(now)}")

# (b) a formula must not be restored with a stale result after the edit invalidates it
import zipfile as _z27
def _book27(dest):
    wb = _ox.Workbook(); ws = wb.active
    ws["B2"] = "Marcus Ellery"; ws["C2"] = 10
    ws["E1"] = '=COUNTIF(B2:B2,"Marcus Ellery")'
    ws["E2"] = "=C2*2"
    stage = dest + ".s"; wb.save(stage)
    z = _z27.ZipFile(stage); it = {n: z.read(n) for n in z.namelist()}; z.close()
    for k in list(it):
        if k.startswith("xl/worksheets/"):
            t = it[k].decode()
            t = t.replace('<f>COUNTIF(B2:B2,"Marcus Ellery")</f><v></v>',
                          '<f>COUNTIF(B2:B2,"Marcus Ellery")</f><v>1</v>')
            t = t.replace("<f>C2*2</f><v></v>", "<f>C2*2</f><v>20</v>")
            it[k] = t.encode()
    with _z27.ZipFile(dest, "w", _z27.ZIP_DEFLATED) as o:
        for k, v in it.items():
            o.writestr(k, v)
    os.remove(stage)

_bk27 = os.path.join(d27, "book.xlsx"); _book27(_bk27)
_w27 = _ox.load_workbook(_bk27)
_old = _w27.active["B2"].value
_w27.active["B2"] = "Dana Whitfield"
_c27.save_xlsx_preserving_values(_w27, _bk27, changed=[("Sheet", "B2", _old)])
_v27 = _ox.load_workbook(_bk27, data_only=True).active
check("F27 a COUNTIF on the changed name does NOT keep its stale result",
      _v27["E1"].value is None, f"E1={_v27['E1'].value!r}, expected blank")
check("F27 an unrelated formula DOES keep its result",
      _v27["E2"].value == 20, f"E2={_v27['E2'].value!r}, expected 20")

# (c) a_scrub must not rewrite A## inside a formula, and must back up BEFORE writing
d27b = os.path.join(base, "f27b"); w27b = os.path.join(d27b, "W"); os.makedirs(w27b)
_wb = _ox.Workbook(); _ws = _wb.active
_ws["A26"] = 52; _ws["B1"] = "=SUM(A26:A27)"; _ws["C1"] = "loads mirror A26 verbatim"
_wb.save(os.path.join(w27b, "s.xlsx"))
open(os.path.join(w27b, "n.txt"), "w").write("governed by A09 in all cases.")
_sp = _ox.Workbook(); _sh = _sp.active; _sh.title = "④ Artifacts"
_sh.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
            "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
_sh.append(["A26", "File", "Occupant Load Table", "xlsx", "/x", "K", "x", "d", "", "", "", ""])
_sh.append(["A09", "File", "System-of-Record Policy", "docx", "/y", "K", "x", "d", "", "", "", ""])
_spp = os.path.join(d27b, "spec.xlsx"); _sp.save(_spp)
run_script("a_scrub.py", "apply", _spp, w27b, "--write")
check("F27 a_scrub leaves A26 alone inside a formula",
      _ox.load_workbook(os.path.join(w27b, "s.xlsx")).active["B1"].value == "=SUM(A26:A27)",
      str(_ox.load_workbook(os.path.join(w27b, "s.xlsx")).active["B1"].value))
_bkp = os.path.join(d27b, "qc_workspace", "backups", "n.txt")
check("F27 a_scrub's backup is the ORIGINAL, not the file it just edited",
      os.path.exists(_bkp) and "A09" in open(_bkp).read()
      and "A09" not in open(os.path.join(w27b, "n.txt")).read(),
      (open(_bkp).read() if os.path.exists(_bkp) else "no backup"))

# (d) the spec must never be scrubbed as if it were a world file
d27c = os.path.join(base, "f27c"); w27c = os.path.join(d27c, "W"); os.makedirs(w27c)
_sp2 = os.path.join(w27c, "World_Spec.xlsx"); _sp.save(_sp2)
open(os.path.join(w27c, "n.txt"), "w").write("governed by A09.")
run_script("a_scrub.py", "apply", _sp2, w27c, "--write")
check("F27 the spec's own ID column survives a scrub of the folder it lives in",
      _ox.load_workbook(_sp2)["④ Artifacts"]["A2"].value == "A26",
      str(_ox.load_workbook(_sp2)["④ Artifacts"]["A2"].value))

# (e) CSV structure: multi-line fields, TSV tabs, duplicate headers
d27d = os.path.join(base, "f27d"); w27d = os.path.join(d27d, "W"); os.makedirs(w27d)
open(os.path.join(w27d, "r.csv"), "wb").write(
    b'EmpID,Name,Notes\r\nHR-1,Marcus Ellery,"Line one\r\nLine two, with comma"\r\n')
open(os.path.join(w27d, "r.tsv"), "wb").write(b"EmpID\tName\nHR-1\tMarcus Ellery\n")
open(os.path.join(w27d, "d.csv"), "wb").write(
    b"EmpID,Name,Approver,Name\r\nHR-1,Marcus Ellery,Ops,Kim Doe\r\n")
_m = _ox.Workbook(); _mw = _m.active
_mw.append(["EmpID", "Name"]); _mw.append(["HR-1", "Dana Whitfield"]); _mw.append(["HR-2", "Marcus Ellery"])
_mp = os.path.join(d27d, "m.xlsx"); _m.save(_mp)
run_script("entity_conformer.py", "apply", _mp, w27d, "--id-col", "EmpID", "--name-col", "Name", "--write")
_rows = list(_csv27.reader(_io27.StringIO(open(os.path.join(w27d, "r.csv"), newline="").read(), newline="")))
check("F27 a multi-line quoted CSV field survives the edit intact",
      len(_rows) == 2 and "Line two, with comma" in _rows[1][2] and "\n" in _rows[1][2],
      repr(open(os.path.join(w27d, "r.csv"), "rb").read()))
check("F27 CRLF is not doubled on write",
      b"\r\r\n" not in open(os.path.join(w27d, "r.csv"), "rb").read(),
      repr(open(os.path.join(w27d, "r.csv"), "rb").read()[:80]))
check("F27 a .tsv is parsed with tabs, so its mismatch is actually found",
      "Dana Whitfield" in open(os.path.join(w27d, "r.tsv")).read(),
      open(os.path.join(w27d, "r.tsv")).read())
_d = list(_csv27.reader(_io27.StringIO(open(os.path.join(w27d, "d.csv"), newline="").read(), newline="")))
check("F27 a duplicate header writes to the column it checked, not another one",
      _d[1][1] == "Dana Whitfield" and _d[1][3] == "Kim Doe", str(_d))

# (f) spec_check: A1-style IDs, and a value must not match inside a decimal
import spec_check as _sc27
check("F27 A1 and A1000 are recognised as artifact IDs",
      bool(_sc27.ID_RE.fullmatch("A1")) and bool(_sc27.ID_RE.fullmatch("A1000")),
      "ID_RE still requires 2-3 digits")
check("F27 '327' is not 'found' inside '0.327'",
      not _sc27.value_present("327", "ratio 0.327") and _sc27.value_present("327", "headcount 327"),
      "decimal boundary")

# (g) leak_scan must say so when a spec check silently did nothing
d27e = os.path.join(base, "f27e"); w27e = os.path.join(d27e, "W"); os.makedirs(w27e)
open(os.path.join(w27e, "a.txt"), "w").write("nothing here")
_bs = _ox.Workbook(); _c = _bs.active; _c.title = "② Canonical Values"
_c.append(["h"]); _c.append(["Value name", "Type", "Value"])          # Note column missing
_c.append(["ARR", "Trap", "$43.8M"])
_t = _bs.create_sheet("③ Tasks"); _t.append(["Task #", "Deliverable"])  # Expected Output missing
_a = _bs.create_sheet("④ Artifacts"); _a.append(["n"])
_a.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
           "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
_bsp = os.path.join(d27e, "spec.xlsx"); _bs.save(_bsp)
o27 = run_script("leak_scan.py", w27e, "--spec", _bsp)
check("F27 leak_scan warns loudly when its spec-driven checks became no-ops",
      o27.count("WARNING") >= 2 and "did NOTHING" in o27, o27.replace(chr(10), " ")[:240])

# (h) leak_scan value matching
import leak_scan as _ls27
check("F27 a bare year is not treated as a task answer", _ls27._is_year("2025"),
      "every file mentions the fiscal year")
check("F27 '670.0' does not match inside '1,670.05'",
      not _ls27._num_present("670.0", "ap aging 1,670.05 outstanding")
      and _ls27._num_present("670.0", "net debt of 670.0"), "whole-value match")

# (i) corpus cache must notice a same-length edit inside one second
d27f = os.path.join(base, "f27f"); os.makedirs(d27f)
_cf = os.path.join(d27f, "x.txt"); open(_cf, "w").write("Acme Corp owes 670")
import corpus as _cp27
_s1 = _cp27.signature(_cf) if hasattr(_cp27, "signature") else None
open(_cf, "w").write("Apex Corp owes 670")          # same length, same second
_s2 = _cp27.signature(_cf) if hasattr(_cp27, "signature") else None
if _s1 is not None:
    check("F27 the corpus cache notices a same-length edit within one second", _s1 != _s2,
          f"{_s1} == {_s2}")


# --- F28: second debugging pass -------------------------------------------------------------------
# Confirmed bugs from auditing the code written in the first pass, plus the scripts that had never
# been audited at all.
import _common as _c28

# (a) THE REGRESSION THE FIRST PASS INTRODUCED. Preserving line endings by handing open() a newline=
# argument also translated the "\r\n" that read_text had already decoded, giving "\r\r\n": a blank
# record between every row of every CRLF file, compounding on each pass.
d28 = os.path.join(base, "f28"); os.makedirs(d28)
for fn, raw in (("crlf.csv", b"a,b\r\nc,d\r\n"), ("lf.csv", b"a,b\nc,d\n")):
    fp = os.path.join(d28, fn)
    open(fp, "wb").write(raw)
    _c28.write_text(fp, _c28.read_text(fp).replace("c", "z"))
    out = open(fp, "rb").read()
    check(f"F28 {fn} line endings are neither doubled nor changed",
          b"\r\r" not in out and out == raw.replace(b"c", b"z"), repr(out))

# (b) formula dependency: no false negative on a cross-sheet range, no false positive from
# pairing two unrelated ranges
S28 = "Summary"
for f, ch, exp, why in [
        ("=SUM(A1:A5)+SUM(C1:C5)", {(S28, 2, 3)}, False, "B3 is in neither range"),
        ("=SUM(Jan!B2:B6)", {("Jan", 2, 4)}, True, "inside a cross-sheet range"),
        ("=SUM(Jan!B2:B6)", {(S28, 2, 4)}, False, "same coord on the wrong sheet"),
        ('=IF(B2>0,"Order A123 shipped","")', {(S28, 1, 123)}, False, "only inside a string literal")]:
    check(f"F28 formula dependency: {why}",
          _c28._formula_touches(f, S28, ch, set()) is exp, f)

# (c) blast_radius stale detection
import blast_radius as _br28
check("F28 a widened number is still caught elsewhere (1000 alongside 10000)",
      _br28._stale_in("cost 1000 and total 10000", "1000", "10000"), "old-in-new no longer voids all hits")
check("F28 but not when it only occurs inside the replacement",
      not _br28._stale_in("total 10000 only", "1000", "10000"), "false positive")
check("F28 stale search does not match 327 inside 3270 or 0.327",
      not _br28._stale_in("price 3270 and ratio 0.327", "327", "415")
      and _br28._stale_in("headcount 327", "327", "415"), "boundary")

# (d) reconcile_entities footing and key detection
import reconcile_entities as _re28
d28b = os.path.join(base, "f28b"); os.makedirs(d28b)
def _w28(n, t):
    p = os.path.join(d28b, n); open(p, "w", newline="").write(t); return p
_cases = [("identical.csv", "Item,Amount\nRent Jan,500\nRent Feb,500\nTotal,1200\n", 1,
           "equal components still get footed"),
          ("blank.csv", "Item,Amount\nAlpha,100\n,\nGamma,200\nDelta,300\nTotal,600\n", 0,
           "a blank spacer row is not a block boundary"),
          ("subtotal.csv", "Item,Amount\nA,10\nB,20\nSubtotal,30\nC,40\nD,50\nTotal,120\n", 0,
           "a grand total may legitimately span a subtotal"),
          ("subtotal_bad.csv", "Item,Amount\nA,10\nB,20\nSubtotal,30\nC,40\nD,50\nTotal,150\n", 1,
           "but a genuinely wrong grand total is still caught")]
for fn, body, want, why in _cases:
    o = run_script("reconcile_entities.py", "footing", _w28(fn, body))
    m = _re24.search(r"(\d+) footing mismatch", o)
    got = int(m.group(1)) if m else -1
    check(f"F28 {why}", got == want, f"{fn}: got {got}, want {want}")

check("F28 a spaced header like 'Employee ID' is recognised as a key column",
      bool(_re28.ID_HINT.search("Employee ID")) and bool(_re28.ID_HINT.search("Invoice Number"))
      and bool(_re28.ID_HINT.search("Vendor Code")), "ID_HINT still needs an underscore")

# (e) round_log classification must not match inside longer words
import round_log as _rl28
for text, notclass, why in [
        ("The invoice INV-1001 appears twice in the ledger and totals differ.", "realism_voice",
         "'voice' must not match inside 'invoice'"),
        ("The workbook could not be validated by the reader.", "temporal",
         "'date' must not match inside 'validated'"),
        ("Consolidated statement is missing a footnote reference.", "math_footing",
         "'foot' must not match inside 'footnote'")]:
    check(f"F28 {why}", _rl28.classify(text)[0] != notclass, f"got {_rl28.classify(text)[0]}")

# (f) inventory_check must pick its baseline by time, not by filename sort
import json as _j28
d28c = os.path.join(base, "f28c"); w28c = os.path.join(d28c, "W"); os.makedirs(w28c)
open(os.path.join(w28c, "a.txt"), "w").write("x")
import inventory_check as _ic28, time as _t28
_sd = _ic28.snap_dir(w28c); os.makedirs(_sd, exist_ok=True)
_older = os.path.join(_sd, "round004-20260820-100000.json")
_newer = os.path.join(_sd, "20260829-100000.json")
open(_older, "w").write(_j28.dumps({"files": {"a.txt": 1}}))
_t28.sleep(0.02)
open(_newer, "w").write(_j28.dumps({"files": {"a.txt": 1, "b.txt": 1}}))
_picked = _ic28.previous_snapshot(w28c)
check("F28 the newest snapshot is the baseline, whatever it is called",
      _picked and _picked[0] == "20260829-100000.json", str(_picked[0] if _picked else None))


# --- F29: key-column naming, and a whole-corpus integration run -----------------------------------
import reconcile_entities as _re29
for h in ("Employee ID", "Invoice Number", "Vendor Code", "emp_id", "ID", "Account No."):
    check(f"F29 {h!r} is recognised as a key column", bool(_re29.ID_HINT.search(h)), h)
for h in ("Number of Units", "Notes", "Income", "Codename", "Number of Days"):
    check(f"F29 {h!r} is NOT treated as a key column", not _re29.ID_HINT.search(h), h)

# The integration test. Everything above checks one function on a two-row fixture. This runs the
# real fixers over a realistic mixed corpus (three encodings, CRLF, a multi-line quoted field, a
# TSV, workbooks with live formulas and cached values, a docx, nested folders) and then asks the
# only question that finally matters: is every file still intact and still correct?
import zipfile as _z29, csv as _csv29, io as _io29
d29 = os.path.join(base, "f29"); w29 = os.path.join(d29, "W")
for sub in ("finance", "hr", "ops", "legal"):
    os.makedirs(os.path.join(w29, sub))

open(os.path.join(w29, "hr", "roster.csv"), "wb").write(
    'Employee ID,Full Name,Notes\r\nHR-001,Marcus Ellery,"Joined 2021\r\nMoved 2023"\r\n'
    'HR-002,Caf\u00e9 Dupont,none\r\n'.encode("cp1252"))
open(os.path.join(w29, "ops", "vendors.tsv"), "w", newline="").write(
    "Vendor Code\tName\tSpend\nV-01\tAcme\t12500\n")
open(os.path.join(w29, "ops", "notes.txt"), "w", newline="").write(
    "Escalation is governed by A09.\r\nSee A26 for occupancy.\r\n")

def _book29(path, rows, total):
    wb = _ox.Workbook(); ws = wb.active; ws.title = "Sheet"
    ws["A1"] = "Item"; ws["B1"] = "Amount"
    for i, (n, v) in enumerate(rows, start=2):
        ws[f"A{i}"] = n; ws[f"B{i}"] = v
    r = len(rows) + 2
    ws[f"A{r}"] = "Total"; ws[f"B{r}"] = f"=SUM(B2:B{r-1})"
    stage = path + ".s"; wb.save(stage)
    z = _z29.ZipFile(stage); it = {n: z.read(n) for n in z.namelist()}; z.close()
    for k in list(it):
        if k.startswith("xl/worksheets/"):
            it[k] = it[k].decode().replace(f"<f>SUM(B2:B{r-1})</f><v></v>",
                                           f"<f>SUM(B2:B{r-1})</f><v>{total}</v>").encode()
    with _z29.ZipFile(path, "w", _z29.ZIP_DEFLATED) as o:
        for k, v in it.items():
            o.writestr(k, v)
    os.remove(stage)

_book29(os.path.join(w29, "finance", "q3.xlsx"), [("Rent", 500), ("Rent", 500), ("Fees", 250)], 1250)

_sp29 = _ox.Workbook(); _cv = _sp29.active; _cv.title = "② Canonical Values"
_cv.append(["h"]); _cv.append(["Value name", "Type", "Value", "Source artifact (ID)",
                               "Must match (IDs)", "Note"])
_cv.append(["ARR", "Trap", "$43.8M", "A09", "A09", "vs $43.2M audited"])
_ar = _sp29.create_sheet("④ Artifacts"); _ar.append(["n"])
_ar.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
            "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
_ar.append(["A09", "File", "System of Record Policy", "txt", "/ops/notes.txt", "K", "x", "d",
            "", "", "", ""])
_spec29 = os.path.join(d29, "spec.xlsx"); _sp29.save(_spec29)

run_script("a_scrub.py", "apply", _spec29, w29, "--write")

_r29 = open(os.path.join(w29, "hr", "roster.csv"), "rb").read()
check("F29 integration: a cp1252 file keeps its encoding and its accents",
      b"\xe9" in _r29 and b"\xc3\xa9" not in _r29, repr(_r29[:60]))
check("F29 integration: CRLF is not doubled anywhere",
      b"\r\r" not in _r29, repr(_r29[:60]))
_rows29 = list(_csv29.reader(_io29.StringIO(_c27.read_text(os.path.join(w29, "hr", "roster.csv")),
                                            newline="")))
check("F29 integration: the multi-line quoted field is still one field",
      len(_rows29) == 3 and "Moved 2023" in _rows29[1][2], str(len(_rows29)))
_q3 = os.path.join(w29, "finance", "q3.xlsx")
check("F29 integration: a workbook total keeps its cached value",
      _ox.load_workbook(_q3, data_only=True).active["B5"].value == 1250,
      str(_ox.load_workbook(_q3, data_only=True).active["B5"].value))
check("F29 integration: and its formula",
      str(_ox.load_workbook(_q3).active["B5"].value).startswith("=SUM"), "formula lost")
try:
    _z29.ZipFile(_q3).testzip()
    check("F29 integration: the workbook is still a valid archive", True)
except Exception as _e:  # noqa: BLE001
    check("F29 integration: the workbook is still a valid archive", False, str(_e))
check("F29 integration: the leaked code was actually fixed",
      "A09" not in open(os.path.join(w29, "ops", "notes.txt")).read(), "not scrubbed")
check("F29 integration: nothing was written inside the world",
      not os.path.isdir(os.path.join(w29, "qc_workspace")), "qc_backup inside the world")
check("F29 integration: backups mirror the folder structure",
      os.path.exists(os.path.join(d29, "qc_workspace", "backups", "ops", "notes.txt")), "flattened")
check("F29 integration: the backup holds the ORIGINAL, not the edited file",
      "A09" in open(os.path.join(d29, "qc_workspace", "backups", "ops", "notes.txt")).read(), "backup is post-edit")


# --- F30: the case an expert hit on a real world --------------------------------------------------
# Reported from the field: a workbook full of ordinary cross-sheet references like
# ='Ranked Segments'!A2 produced 4,275 false "leaked artifact ID" hits, and applying the fixer would
# have rewritten those formulas. Locked here at realistic scale.
d30 = os.path.join(base, "f30"); w30 = os.path.join(d30, "W"); os.makedirs(w30)
_wb30 = _ox.Workbook(); _s1 = _wb30.active; _s1.title = "Ranked Segments"
for _i in range(1, 400):
    _s1.cell(row=_i, column=1, value=f"Segment {_i}")
_s2 = _wb30.create_sheet("Plan")
for _i in range(1, 400):
    _s2.cell(row=_i, column=1, value=f"='Ranked Segments'!A{_i}")
    _s2.cell(row=_i, column=2, value=f"=SUM(A1:A{_i})")
_s2["D1"] = "Prepared per A26 guidance"          # the one REAL leak, in prose
_wb30.save(os.path.join(w30, "horizon_capital_plan_FY2027.xlsx"))

_sp30 = _ox.Workbook(); _sh30 = _sp30.active; _sh30.title = "④ Artifacts"
_sh30.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
              "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
_sh30.append(["A26", "File", "Occupant Load Table", "xlsx", "/x", "K", "x", "d", "", "", "", ""])
_spec30 = os.path.join(d30, "spec.xlsx"); _sp30.save(_spec30)

o30 = run_script("a_scrub.py", "apply", _spec30, w30, "--write")
_p30 = _ox.load_workbook(os.path.join(w30, "horizon_capital_plan_FY2027.xlsx"))["Plan"]
check("F30 798 cross-sheet references produce no false artifact-ID hits",
      "Fixed 1 A## occurrence" in o30, o30.replace(chr(10), " ")[-200:])
check("F30 every cross-sheet formula survives untouched",
      _p30["A5"].value == "='Ranked Segments'!A5" and _p30["B300"].value == "=SUM(A1:A300)",
      f"{_p30['A5'].value!r} / {_p30['B300'].value!r}")
check("F30 and the one real leak in prose is still fixed",
      "Occupant Load Table" in str(_p30["D1"].value), str(_p30["D1"].value))

import leak_scan as _ls30
check("F30 a fiscal year like 2027 is not reported as a leaked task answer",
      _ls30._is_year("2027"), "bare year")
check("F30 but a real money answer still matches, whatever its case",
      _ls30._num_present("$670.0M", "net debt of $670.0M at year end"), "case sensitivity")


# --- F31: formula safety, end to end --------------------------------------------------------------
# Formulas have been the single most damaging area in this toolkit's history: rewritten formula text,
# blanked cached values, and stale cached values restored after the edit invalidated them. This holds
# all three shut at once, plus the parts an openpyxl round trip is known to drop.
import zipfile as _z31
from openpyxl.chart import BarChart as _Bar31, Reference as _Ref31
from openpyxl.worksheet.datavalidation import DataValidation as _DV31
from openpyxl.workbook.defined_name import DefinedName as _DN31

d31 = os.path.join(base, "f31"); w31 = os.path.join(d31, "W"); os.makedirs(w31)
_wb31 = _ox.Workbook(); _ws31 = _wb31.active; _ws31.title = "Data"
_ws31["A1"] = "Item"; _ws31["B1"] = "Amount"
for _i, (_n, _v) in enumerate([("Alpha", 100), ("Beta", 200), ("Gamma", 300)], start=2):
    _ws31[f"A{_i}"] = _n; _ws31[f"B{_i}"] = _v
_ws31["B5"] = "=SUM(B2:B4)"
_ws31["C1"] = "Prepared per A26 guidance"          # the real leak, in prose
_ws31["C2"] = '=IF(B5>0,"see A26","")'             # a code inside a quoted string
_ws31["C3"] = "='Ranked Segments'!A2"              # a cross-sheet reference
_ws31["E1"] = "Note referencing A26 here"          # prose a formula reads
_ws31["E2"] = "=E1"
_s2_31 = _wb31.create_sheet("Ranked Segments"); _s2_31["A2"] = "Segment Two"
_ch31 = _Bar31()
_ch31.add_data(_Ref31(_ws31, min_col=2, min_row=1, max_row=4), titles_from_data=True)
_ws31.add_chart(_ch31, "G2")
_ws31.add_data_validation(_DV31(type="list", formula1='"Yes,No"', sqref="D2:D4"))
_wb31.defined_names.add(_DN31("TotalRange", attr_text="Data!$B$2:$B$4"))
_ws31.freeze_panes = "B2"
_stage31 = os.path.join(d31, "stage.xlsx"); _wb31.save(_stage31)
_z = _z31.ZipFile(_stage31); _it31 = {n: _z.read(n) for n in _z.namelist()}; _z.close()
for _k in list(_it31):
    if _k.startswith("xl/worksheets/sheet1"):
        _t = _it31[_k].decode()
        _t = _t.replace("<f>SUM(B2:B4)</f><v></v>", "<f>SUM(B2:B4)</f><v>600</v>")
        _t = _t.replace("<f>E1</f><v></v>", "<f>E1</f><v>Note referencing A26 here</v>")
        _t = _t.replace('<c r="E2"><f>E1', '<c r="E2" t="str"><f>E1')
        _it31[_k] = _t.encode()
_bk31 = os.path.join(w31, "model.xlsx")
with _z31.ZipFile(_bk31, "w", _z31.ZIP_DEFLATED) as _o:
    for _k, _v in _it31.items():
        _o.writestr(_k, _v)

_sp31 = _ox.Workbook(); _sh31 = _sp31.active; _sh31.title = "④ Artifacts"
_sh31.append(["ID", "Type", "Name", "Format / App", "Location / Address", "Label", "Prepared By",
              "Description", "Relates to (IDs)", "Trap Content", "Tasks", "Reference Doc"])
_sh31.append(["A26", "File", "Occupant Load Table", "xlsx", "/x", "K", "x", "d", "", "", "", ""])
_spec31 = os.path.join(d31, "spec.xlsx"); _sp31.save(_spec31)

run_script("a_scrub.py", "apply", _spec31, w31, "--write")
_f31 = _ox.load_workbook(_bk31)["Data"]
_v31 = _ox.load_workbook(_bk31, data_only=True)["Data"]
_names31 = _z31.ZipFile(_bk31).namelist()

check("F31 a plain formula is never rewritten", _f31["B5"].value == "=SUM(B2:B4)", repr(_f31["B5"].value))
check("F31 a cross-sheet reference is never rewritten",
      _f31["C3"].value == "='Ranked Segments'!A2", repr(_f31["C3"].value))
check("F31 a code inside a quoted string in a formula is never rewritten",
      _f31["C2"].value == '=IF(B5>0,"see A26","")', repr(_f31["C2"].value))
check("F31 but the real leak in prose IS fixed",
      "Occupant Load Table" in str(_f31["C1"].value), repr(_f31["C1"].value))
check("F31 an untouched formula keeps its cached value", _v31["B5"].value == 600, repr(_v31["B5"].value))
check("F31 a formula reading a cell we changed has its stale value DROPPED",
      _v31["E2"].value is None, repr(_v31["E2"].value))
check("F31 charts survive the write", any("chart" in x for x in _names31), str(_names31))
check("F31 data validation survives", len(_f31.data_validations.dataValidation) > 0)
check("F31 defined names survive", "TotalRange" in _ox.load_workbook(_bk31).defined_names)
check("F31 freeze panes survive", _f31.freeze_panes == "B2", str(_f31.freeze_panes))
check("F31 the other sheet is intact",
      _ox.load_workbook(_bk31)["Ranked Segments"]["A2"].value == "Segment Two")

run_script("a_scrub.py", "apply", _spec31, w31, "--write")     # second pass
_f31b = _ox.load_workbook(_bk31)["Data"]
check("F31 a second pass changes nothing further",
      _f31b["B5"].value == "=SUM(B2:B4)" and _f31b["C2"].value == '=IF(B5>0,"see A26","")',
      "not idempotent")


# --- F32: backups must never land inside the delivered world, at any depth ------------------------
# Reported by a builder who found ten stray _qc_backup folders inside a world they were about to
# deliver. This has been wrong twice: first backups went INSIDE the target folder, then BESIDE it,
# which is still inside the delivered tree whenever the file sits in subfolders. It also made
# inventory_check report false "unregistered file" errors.
import shutil as _sh32
d32 = os.path.join(base, "f32")
_deep = os.path.join(d32, "filesystem", "deliver", "budgets"); os.makedirs(_deep)
_bk = os.path.join(_deep, "q3.xlsx")
_w = _ox.Workbook(); _w.active["A1"] = "x"; _w.save(_bk)
_world32 = os.path.join(d32, "filesystem")

run_script("metadata_hygiene.py", "clean", _bk, "--world", _world32, "--date", "2025-07-17")
_inside = [r for r, dn, _ in os.walk(_world32) for x in dn if x.endswith("_qc_backup") or x == "qc_workspace"]
check("F32 --world keeps backups out of the delivered tree", not _inside, str(_inside))
check("F32 and puts them beside the world root",
      os.path.isdir(os.path.join(os.path.dirname(_world32), "qc_workspace")), os.listdir(d32))

# with no --world but a world-level backup already present, it must find that one
_bk2 = os.path.join(_deep, "q4.xlsx"); _w.save(_bk2)
run_script("metadata_hygiene.py", "clean", _bk2, "--date", "2025-07-17")
_inside2 = [r for r, dn, _ in os.walk(_world32) for x in dn if x.endswith("_qc_backup") or x == "qc_workspace"]
check("F32 without --world it finds the existing world-level backup, not a nested spot",
      not _inside2, str(_inside2))

# with nothing to infer from it must refuse rather than guess
d32b = os.path.join(base, "f32b")
_deep2 = os.path.join(d32b, "filesystem", "deliver", "budgets"); os.makedirs(_deep2)
_bk3 = os.path.join(_deep2, "q3.xlsx"); _w.save(_bk3)
o32 = run_script("metadata_hygiene.py", "clean", _bk3, "--date", "2025-07-17")
_inside3 = [r for r, dn, _ in os.walk(os.path.join(d32b, "filesystem"))
            for x in dn if x.endswith("_qc_backup") or x == "qc_workspace"]
check("F32 with nothing to infer from it refuses rather than guessing",
      "--world" in o32 and not _inside3, o32.replace(chr(10), " ")[:200])

# sweep clears an existing mess without touching world content
d32c = os.path.join(base, "f32c"); _w32c = os.path.join(d32c, "filesystem", "deliver")
for _sub in ("budgets", "legal"):
    os.makedirs(os.path.join(_w32c, _sub))
    os.makedirs(os.path.join(_w32c, _sub + "_qc_backup"))
    open(os.path.join(_w32c, _sub + "_qc_backup", "old.xlsx"), "w").write("copy")
    open(os.path.join(_w32c, _sub, "real.txt"), "w").write("world content")
    open(os.path.join(_w32c, _sub, ".DS_Store"), "wb").write(b"\0")
_root32c = os.path.join(d32c, "filesystem")
o32b = run_script("metadata_hygiene.py", "sweep", _root32c)
check("F32 sweep lists strays without removing anything by default",
      "Nothing removed" in o32b and os.path.isdir(os.path.join(_w32c, "budgets_qc_backup")),
      o32b.replace(chr(10), " ")[:200])
run_script("metadata_hygiene.py", "sweep", _root32c, "--write")
_left = [r for r, dn, _ in os.walk(_root32c) for x in dn if x.endswith("_qc_backup") or x == "qc_workspace"]
check("F32 sweep --write removes every stray backup folder", not _left, str(_left))
check("F32 sweep leaves real world content alone",
      all(os.path.exists(os.path.join(_w32c, s, "real.txt")) for s in ("budgets", "legal")),
      "world content deleted")
check("F32 sweep removes OS junk too",
      not os.path.exists(os.path.join(_w32c, "budgets", ".DS_Store")), "junk left")


# --- F33: spreadsheets must actually be read -------------------------------------------------------
# Reported from the field: "it doesn't process spreadsheets, it logs a silent note and treats them as
# empty, which makes the scan results look clean." Three separate causes, all of which end in a
# confident zero.
import shutil as _sh33
d33 = os.path.join(base, "f33"); w33 = os.path.join(d33, "W"); os.makedirs(w33)
_wb33 = _ox.Workbook(); _ws33 = _wb33.active
_ws33["A1"] = "Vendor"
_ws33["A5"] = "Marcus Ellery"          # deliberately below a run of BLANK cells
_ws33["B5"] = 670000000
_wb33.save(os.path.join(w33, "model.xlsx"))
_sh33.copy(os.path.join(w33, "model.xlsx"), os.path.join(w33, "macro.xlsm"))
open(os.path.join(w33, "legacy.xls"), "wb").write(b"\xd0\xcf\x11\xe0old")

import scan_world as _sw33
_sw33.UNREAD.clear()
check("F33 an .xlsx is read, and blank cells do not abort the sheet",
      len(_sw33.extract_chunks(os.path.join(w33, "model.xlsx"))) > 0, "still zero chunks")
check("F33 a macro-enabled .xlsm is read too",
      len(_sw33.extract_chunks(os.path.join(w33, "macro.xlsm"))) > 0, "xlsm unsupported")

o33 = run_script("scan_world.py", "occurrences", "Marcus Ellery", w33)
check("F33 a value in a spreadsheet is actually found",
      "2 occurrence" in o33 and "model.xlsx" in o33 and "macro.xlsm" in o33,
      o33.replace(chr(10), " ")[:200])
check("F33 a file that could not be opened is reported loudly, not silently",
      "COULD NOT BE READ" in o33 and "legacy.xls" in o33, o33.replace(chr(10), " ")[-260:])

_sw33.UNREAD.clear()
_sw33.extract_chunks(os.path.join(w33, "legacy.xls"))
check("F33 an unsupported type is recorded rather than passed off as empty",
      len(_sw33.UNREAD) == 1, str(_sw33.UNREAD))


print("\n" + "="*60)
p=sum(1 for _,c,_ in results if c); f=len(results)-p
print(f"LAYER 1 BATTERY: {p} PASS / {f} FAIL  (of {len(results)})")
sys.exit(1 if f else 0)
