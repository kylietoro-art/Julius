#!/usr/bin/env python3
"""Spec-driven, domain-agnostic checks: trap manifest, ties, referential integrity.

Reads the World Spec workbook (the builder's source of truth) and checks the built world against
what the SPEC declares, so the skill carries zero domain knowledge; the domain rides in with the
spec. Deterministic, diff-only output. It FLAGS, it never fixes.

The spec tabs it reads (v4.x "All Apps" layout; header names matched loosely):
  ② Canonical Values   Value name | Type | Value | Source artifact (ID) | Must match (IDs) | Note
  ③ Tasks              ... | Trap: What Misleads | Trap: How Agent Fails | Trap: Remediation Path
  ④ Artifacts          ID | Type | ... | Location / Address | Relates to (IDs) | Trap Content | Tasks
  REF · Schema Library App | Artifact | ... | Depends on | References / ties | Lookup key | Active

Subcommands:
  traps <spec.xlsx>                 Build & print the TRAP MANIFEST (② Note + ③ trap cols + ④ Trap
                                    Content). This is the guardrail: a value/divergence in here is
                                    intentional and must NOT be collapsed.
  ties  <spec.xlsx> <world_dir>     For every canonical value, confirm its source artifact and each
                                    'Must match' artifact actually carry the value, EXCEPT artifacts
                                    the manifest marks as a declared trap for that value. Flags
                                    absent/uncarried ties only.
  refs  <spec.xlsx> [world_dir]     Referential integrity: every ID referenced (② Must match, ④
                                    Relates to, ③ Primary Artifacts) resolves to a real ④ row; app
                                    tables named in REF · Schema Library 'Depends on' resolve their
                                    foreign keys (orphans / unexported parent keys).
  all   <spec.xlsx> <world_dir>     traps + ties + refs.

Deps: openpyxl (spec + xlsx world files). pdfplumber/pypdf, python-docx optional (else those files
are skipped with a note). CSV/TXT/MD/JSON/HTML read natively.
"""
import argparse, os, re, sys, glob, io

import _common
_common.setup_console()

try:
    import openpyxl
except ImportError:
    sys.exit("spec_check.py needs openpyxl: pip install openpyxl")

ID_RE = re.compile(r"\bA\d{1,4}\b")   # A1 and A1000 are real spec IDs; \d{2,3} made them invisible,
                                        # which zeroed the tie check AND the ref check and reported clean
PLACEHOLDER = re.compile(r"^\s*(\[.*\]|[—–-]+|n/?a|tbd|none|null)\.?\s*$", re.I)


def norm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def find_header(ws, needles):
    """Return (row_index, {normalized_needle: col_index}) for the first row containing all needles."""
    needn = [norm(n) for n in needles]
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        cells = {norm(v): j for j, v in enumerate(row) if v is not None and str(v).strip() != ""}
        if all(any(nd in c for c in cells) for nd in needn):
            colmap = {}; used = set()
            # exact normalized matches first (so needle "value" doesn't grab "value name")
            for nd in needn:
                for c, j in cells.items():
                    if c == nd and j not in used:
                        colmap[nd] = j; used.add(j); break
            # then substring for anything still unmatched, preferring an unused column
            for nd in needn:
                if nd in colmap: continue
                for c, j in cells.items():
                    if nd in c and j not in used:
                        colmap[nd] = j; used.add(j); break
            return i, colmap
    return None, None


def rows_after(ws, header_idx):
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        if i > header_idx:
            yield row


def cell(row, j):
    if j is None or j >= len(row): return ""
    v = row[j]
    return "" if v is None else str(v).strip()


def load(spec):
    try:
        return openpyxl.load_workbook(spec, data_only=True)
    except FileNotFoundError:
        sys.exit(f"spec_check.py: spec file not found: {spec}")
    except Exception as e:
        sys.exit(f"spec_check.py: could not read spec file {spec}: {e}")


def sheet(wb, *frags):
    fr = [norm(f) for f in frags if norm(f)]   # drop frags that normalize to empty (e.g. "④")
    for ws in wb.worksheets:
        t = norm(ws.title)
        if any(f in t for f in fr): return ws
    return None


# ---------------- trap manifest ----------------
def build_manifest(wb):
    """Return list of dicts: {source, artifact, value/desc, note}. Guardrail set."""
    manifest = []
    # ④ Artifacts · Trap Content
    a = sheet(wb, "Artifacts", "④")
    if a:
        hi, cm = find_header(a, ["ID", "Trap Content"])
        if hi:
            for row in rows_after(a, hi):
                aid = cell(row, cm.get(norm("ID")))
                trap = cell(row, cm.get(norm("Trap Content")))
                if ID_RE.match(aid or "") and trap and not PLACEHOLDER.match(trap):
                    manifest.append({"source": "④ Trap Content", "artifact": aid, "detail": trap})
    # ③ Tasks · Trap cols
    t = sheet(wb, "Tasks", "③")
    if t:
        hi, cm = find_header(t, ["Task", "Trap"])
        if hi:
            # collect all trap-ish columns
            hrow = list(t.iter_rows(values_only=True))[hi-1]
            trapcols = {j: str(v).strip() for j, v in enumerate(hrow) if v and "trap" in norm(v)}
            primc = None
            for j, v in enumerate(hrow):
                if v and "primaryartifact" in norm(v): primc = j
            for row in rows_after(t, hi):
                tid = cell(row, cm.get(norm("Task")))
                if not tid or PLACEHOLDER.match(tid): continue
                arts = cell(row, primc) if primc is not None else ""
                for j, label in trapcols.items():
                    val = cell(row, j)
                    if val and not PLACEHOLDER.match(val):
                        manifest.append({"source": f"③ {label}", "artifact": tid + (f" [{arts}]" if arts else ""), "detail": val})
    # ② Canonical Values · Note mentions trap, or row is Type=Trap
    cv = sheet(wb, "Canonical", "②")
    if cv:
        hi, cm = find_header(cv, ["Value name", "Type", "Note"])
        if hi:
            for row in rows_after(cv, hi):
                name = cell(row, cm.get(norm("Value name")))
                note = cell(row, cm.get(norm("Note")))
                vtype = cell(row, cm.get(norm("Type")))
                if name and not PLACEHOLDER.match(name) and ("trap" in note.lower() or "trap" in norm(vtype)):
                    manifest.append({"source": "② Note", "artifact": name, "detail": note or "Type=Trap"})
    return manifest


def cmd_traps(spec):
    wb = load(spec)
    m = build_manifest(wb)
    print(f"TRAP MANIFEST, {len(m)} declared trap(s). These are INTENTIONAL; never collapse them.\n")
    for e in m:
        print(f"  · [{e['source']}] {e['artifact']}: {e['detail'][:160]}")
    if not m:
        print("  (none found, if this world has traps, they aren't declared in the spec; do NOT")
        print("   collapse discrepancies. Ask the builder before reducing any divergence.)")
    return m


# ---------------- artifact registry ----------------
def artifact_index(wb):
    """Return {ID: {'loc':.., 'name':.., 'type':.., 'relates':[..], 'trap':..}}."""
    idx = {}
    a = sheet(wb, "Artifacts", "④")
    if not a: return idx
    hi, cm = find_header(a, ["ID", "Location"])
    if not hi:
        hi, cm = find_header(a, ["ID", "Name"])
    if not hi: return idx
    if norm("Name") not in cm:
        _, cm2 = find_header(a, ["ID", "Name"])
        if cm2 and norm("Name") in cm2:
            cm[norm("Name")] = cm2[norm("Name")]
    for row in rows_after(a, hi):
        aid = cell(row, cm.get(norm("ID")))
        if not ID_RE.match(aid or ""): continue
        idx[aid] = {
            "loc": cell(row, cm.get(norm("Location"))) if norm("Location") in cm else "",
            "name": cell(row, cm.get(norm("Name"))) if norm("Name") in cm else "",
        }
    return idx


# ---------------- text extraction ----------------
def extract_text(path):
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    try:
        if ext in ("csv", "tsv", "txt", "md", "json", "html", "htm", "eml"):
            return _common.read_text(path)
        if ext in ("xlsx", "xlsm"):
            wb = openpyxl.load_workbook(path, data_only=True)
            out = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    out.append(" ".join("" if c is None else str(c) for c in row))
            return "\n".join(out)
        if ext == "pdf":
            try:
                import pdfplumber
                with pdfplumber.open(path) as pdf:
                    return "\n".join((p.extract_text() or "") for p in pdf.pages)
            except Exception:
                try:
                    import pypdf
                    return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(path).pages)
                except Exception:
                    return None
        if ext == "pptx":
            try:
                from pptx import Presentation
                out = []
                for sl in Presentation(path).slides:
                    for sh in sl.shapes:
                        if sh.has_text_frame:
                            out.append(sh.text_frame.text)
                        if sh.has_table:
                            for r in sh.table.rows:
                                out.append(" ".join(c.text for c in r.cells))
                    if sl.has_notes_slide and sl.notes_slide.notes_text_frame:
                        out.append(sl.notes_slide.notes_text_frame.text)
                return "\n".join(out)
            except Exception:
                return None
        if ext == "docx":
            try:
                import docx
                d = docx.Document(path)
                parts = [p.text for p in d.paragraphs]
                # Financial figures live in TABLES far more often than in paragraphs. Reading
                # paragraphs only made every one of them read as absent: a [TIE MISS] on a value
                # that is plainly in the document. The documented cheapest way to close a bogus tie
                # finding is to add explanatory prose, which is exactly the answer leakage that
                # leak_scan exists to catch, so this false positive actively pushed builders toward
                # creating a real defect.
                for t in d.tables:
                    for row in t.rows:
                        for c in row.cells:
                            parts.append(c.text)
                for sec in d.sections:
                    for hf in (sec.header, sec.footer):
                        parts.extend(p.text for p in hf.paragraphs)
                return "\n".join(parts)
            except Exception:
                return None
    except Exception:
        return None
    return None


def resolve_path(world_dir, loc, name):
    """Best-effort: match the spec Location/Address or artifact name to a real file under world_dir."""
    cands = []
    if loc:
        base = loc.strip("/\\").replace("\\", "/").split("/")[-1]
        cands.append(base)
    if name:
        cands.append(name)
    allf = [f for f in glob.glob(os.path.join(world_dir, "**", "*"), recursive=True) if os.path.isfile(f)]
    for cand in cands:
        cn = norm(cand)
        if not cn: continue
        for f in allf:
            if cn == norm(os.path.basename(f)):
                return f
    for cand in cands:
        cn = norm(cand)
        cn_stem = norm(cand.rsplit(".", 1)[0])
        for f in allf:
            fn = norm(os.path.basename(f))
            if cn and (cn in fn or cn_stem and cn_stem in fn):
                return f
    return None


def value_variants(v):
    v = v.strip()
    out = {v}
    stripped = v.replace("$", "").replace(",", "").strip()
    out.add(stripped)
    m = re.match(r"^\$?([\d,.]+)\s*([MmKkBb])$", v)
    if m:
        num, suf = m.group(1).replace(",", ""), m.group(2).lower()
        out.add(num);
        try:
            f = float(num) * {"k": 1e3, "m": 1e6, "b": 1e9}[suf]
            out.add(f"{f:,.0f}"); out.add(f"{int(f)}")
        except Exception: pass
    # float vs int: "95.0" also matches "95"; "95" also matches "95.0"
    nplain = v.replace("$", "").replace(",", "").strip()
    if re.fullmatch(r"\d+\.0+", nplain):
        out.add(nplain.split(".")[0])
    elif re.fullmatch(r"\d+", nplain):
        out.add(nplain + ".0")
    return {x for x in out if x}


def _date_forms(value):
    """If value looks like a date (incl. openpyxl 'YYYY-MM-DD 00:00:00'), return common textual
    renderings so a datetime cell matches a plainly-written date. Empty set if not a date."""
    v = str(value).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[ T]\d{2}:\d{2}(?::\d{2})?)?$", v)
    if not m:
        m2 = re.match(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})$", v)
        if not m2:
            return set()
        mo, d, y = m2.group(1), m2.group(2), m2.group(3)
    else:
        y, mo, d = m.group(1), m.group(2), m.group(3)
    y, mo, d = int(y), int(mo), int(d)
    import calendar
    mon = calendar.month_name[mo]; mon_ab = calendar.month_abbr[mo]
    forms = {
        f"{y:04d}-{mo:02d}-{d:02d}", f"{mo:02d}/{d:02d}/{y:04d}", f"{mo}/{d}/{y}",
        f"{mon} {d}, {y}", f"{mon} {d} {y}", f"{mon_ab} {d}, {y}",
        f"{d} {mon} {y}", f"{mo:02d}-{d:02d}-{y:04d}",
    }
    return forms


def value_present(value, text):
    """True if `value` appears in `text`. Numbers match on digit boundaries (327 != 3270, commas
    ignored). Dates match across common formats (a datetime cell matches a written date)."""
    dforms = _date_forms(value)
    if dforms:
        return any(f in text for f in dforms)
    text_nc = re.sub(r"(?<=\d),(?=\d)", "", text)
    for var in value_variants(value):
        vv = var.strip()
        if not vv:
            continue
        num = vv.replace(",", "")
        if re.fullmatch(r"\d+(\.\d+)?", num):
            # The boundary has to reject a decimal point on either side, not just a digit.
            # "(?<!\d)" alone let 327 match inside 0.327 and 95 inside 0.95, so a canonical
            # value that is genuinely absent was reported present and no TIE MISS was raised.
            if re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d.]?\d)", text_nc):
                return True
        elif vv in text:
            return True
    return False


# ---------------- ties ----------------
def canonical_rows(wb):
    cv = sheet(wb, "Canonical", "②")
    if not cv: return []
    hi, cm = find_header(cv, ["Value name", "Type", "Value", "Source artifact", "Must match"])
    if not hi: return []
    rows = []
    for row in rows_after(cv, hi):
        name = cell(row, cm.get(norm("Value name")))
        val = cell(row, cm.get(norm("Value")))
        src = cell(row, cm.get(norm("Source artifact")))
        must = cell(row, cm.get(norm("Must match")))
        note = cell(row, cm.get(norm("Note"))) if norm("Note") in cm else ""
        vtype = cell(row, cm.get(norm("Type"))) if norm("Type") in cm else ""
        if not name or PLACEHOLDER.match(name) or not val or PLACEHOLDER.match(val):
            continue
        ids = ID_RE.findall((src or "") + " " + (must or ""))
        rows.append({"name": name, "value": val, "src": (ID_RE.findall(src or "") or [""])[0],
                     "ids": ids, "note": note, "type": vtype})
    return rows


def cmd_ties(spec, world_dir):
    wb = load(spec)
    if world_dir is not None and not os.path.isdir(world_dir):
        sys.exit(f"spec_check.py: world_dir not found or not a directory: {world_dir}")
    idx = artifact_index(wb)
    manifest = build_manifest(wb)
    # Skip only artifacts that are declared TRAP-BEARERS: ④ Trap Content rows (the artifact itself
    # carries the intentional divergence) and ② Notes that flag a trap. NOT ③ primary-artifact lists
    # (those include the correct sources too, so harvesting them would wrongly skip real ties).
    trap_arts = set()
    for e in manifest:
        src = e["source"]
        if src.startswith("④"):
            trap_arts |= set(ID_RE.findall(e["artifact"] + " " + e["detail"]))
        elif src.startswith("②"):
            trap_arts |= set(ID_RE.findall(e["detail"]))
        elif src.startswith("③") and "remediation" not in norm(src):
            # trap declared in a Task's "What Misleads"/"How Agent Fails" names the trap-bearer;
            # skip the Remediation Path (it names the CORRECT artifacts, not the trap).
            trap_arts |= set(ID_RE.findall(e["detail"]))
    rows = canonical_rows(wb)
    # a canonical value marked Type=Trap is an intentional divergence, never tie-check it
    skipped_traps = [r["name"] for r in rows if "trap" in norm(r.get("type", ""))]
    rows = [r for r in rows if "trap" not in norm(r.get("type", ""))]
    if skipped_traps:
        print(f"(skipped {len(skipped_traps)} Type=Trap canonical value(s), declared traps)\n")
    print(f"TIE CHECK, {len(rows)} canonical value(s). Flagging artifacts that don't carry the value")
    print("(declared-trap artifacts skipped). Presence heuristic, treat hits as candidates.\n")
    problems = 0
    cache = {}
    for r in rows:
        for aid in r["ids"]:
            if aid in trap_arts:
                continue  # intentional divergence, never flag
            meta = idx.get(aid)
            if not meta:
                print(f"  [UNRESOLVED ID] '{r['name']}' cites {aid}, no such artifact in ④."); problems += 1; continue
            path = cache.get(aid) or resolve_path(world_dir, meta["loc"], meta["name"])
            cache[aid] = path
            if not path:
                print(f"  [FILE NOT FOUND] {aid} ({meta['name'] or meta['loc']}) for '{r['name']}'."); problems += 1; continue
            txt = extract_text(path)
            if txt is None:
                print(f"  [UNREADABLE] {aid} ({os.path.basename(path)}), install pdf/docx lib to check '{r['name']}'."); continue
            if not value_present(r["value"], txt):
                problems += 1
                print(f"  [TIE MISS] '{r['name']}' = {r['value']} not found in {aid} ({os.path.basename(path)})")
    print(f"\n--- {problems} tie issue(s). Each: real drift (fix toward the source artifact) or a")
    print("    missing declared trap. Confirm against the manifest before changing anything. ---")
    return problems


# ---------------- referential integrity ----------------
def cmd_refs(spec, world_dir=None):
    wb = load(spec)
    if world_dir is not None and not os.path.isdir(world_dir):
        sys.exit(f"spec_check.py: world_dir not found or not a directory: {world_dir}")
    idx = artifact_index(wb)
    valid = set(idx)
    print(f"REFERENTIAL INTEGRITY, {len(valid)} artifacts in ④.\n")
    problems = 0
    # 1) referenced IDs resolve
    refs = {}
    cv = sheet(wb, "Canonical", "②")
    if cv:
        hi, cm = find_header(cv, ["Value name", "Must match"])
        if hi:
            for row in rows_after(cv, hi):
                for aid in ID_RE.findall(cell(row, cm.get(norm("Must match")))):
                    refs.setdefault(aid, "② Must match")
    a = sheet(wb, "Artifacts", "④")
    if a:
        hi, cm = find_header(a, ["ID", "Relates"])
        if hi:
            for row in rows_after(a, hi):
                for aid in ID_RE.findall(cell(row, cm.get(norm("Relates")))):
                    refs.setdefault(aid, "④ Relates to")
    t = sheet(wb, "Tasks", "③")
    if t:
        hi, cm = find_header(t, ["Task", "Primary Artifacts"])
        if hi:
            for row in rows_after(t, hi):
                for aid in ID_RE.findall(cell(row, cm.get(norm("Primary Artifacts")))):
                    refs.setdefault(aid, "③ Primary Artifacts")
    for aid, where in sorted(refs.items()):
        if aid not in valid:
            problems += 1
            print(f"  [BROKEN REF] {aid} referenced in {where} but not defined in ④ Artifacts.")
    # 2) app-data foreign keys (REF · Schema Library 'Depends on')
    sl = sheet(wb, "Schema Library")
    deps = []
    if sl:
        hi, cm = find_header(sl, ["App", "Artifact", "Depends on"])
        if hi:
            for row in rows_after(sl, hi):
                art = cell(row, cm.get(norm("Artifact")))
                dep = cell(row, cm.get(norm("Depends on")))
                if art and dep and not PLACEHOLDER.match(dep):
                    deps.append((art, dep))
    # App-data foreign-key/orphan checks are OUT OF SCOPE for filesystem-only remediation
    # (the app-load pipeline owns them). Only run if explicitly opted in.
    if deps and world_dir and os.environ.get("SPEC_CHECK_APPDATA") == "1":
        problems += _check_fk(world_dir, deps)
    elif deps:
        print(f"\n  (skipping {len(deps)} app-data key checks, filesystem-only; set SPEC_CHECK_APPDATA=1 to include.)")
    print(f"\n--- {problems} referential issue(s). ---")
    return problems


def _check_fk(world_dir, deps):
    import csv
    def find_csv(nameish):
        target = norm(nameish.rsplit(".", 1)[0])
        for f in glob.glob(os.path.join(world_dir, "**", "*.csv"), recursive=True):
            if target and target in norm(os.path.basename(f)): return f
        return None
    probs = 0
    for child, parent in deps:
        cf, pf = find_csv(child), find_csv(parent)
        if not cf or not pf: continue
        try:
            crows = list(csv.DictReader(io.StringIO(_common.read_text(cf))))
            prows = list(csv.DictReader(io.StringIO(_common.read_text(pf))))
        except Exception: continue
        if not crows or not prows: continue
        pnorm = norm(parent.rsplit(".", 1)[0])
        # parent key column: a column whose name matches parent entity, else first column
        pcols = list(prows[0].keys())
        pkey = next((c for c in pcols if pnorm in norm(c)), pcols[0])
        pkeys = {str(r.get(pkey, "")).strip() for r in prows if str(r.get(pkey, "")).strip()}
        # child FK column: a column matching parent entity name
        ccols = list(crows[0].keys())
        fk = next((c for c in ccols if pnorm in norm(c)), None)
        if not fk:
            print(f"  [KEY MISSING] {os.path.basename(cf)} has no column referencing {parent} (join to parent breaks).")
            probs += 1; continue
        orphans = sorted({str(r.get(fk, "")).strip() for r in crows
                          if str(r.get(fk, "")).strip() and str(r.get(fk, "")).strip() not in pkeys})
        if orphans:
            probs += 1
            print(f"  [ORPHAN FK] {os.path.basename(cf)}.{fk} -> {os.path.basename(pf)}.{pkey}: "
                  f"{len(orphans)} value(s) with no parent, e.g. {orphans[:5]}")
    return probs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("traps"); p.add_argument("spec")
    p = sub.add_parser("ties"); p.add_argument("spec"); p.add_argument("world_dir")
    p = sub.add_parser("refs"); p.add_argument("spec"); p.add_argument("world_dir", nargs="?")
    p = sub.add_parser("all"); p.add_argument("spec"); p.add_argument("world_dir")
    args = ap.parse_args()
    if args.cmd == "traps": cmd_traps(args.spec)
    elif args.cmd == "ties": cmd_ties(args.spec, args.world_dir)
    elif args.cmd == "refs": cmd_refs(args.spec, args.world_dir)
    elif args.cmd == "all":
        print("### TRAP MANIFEST ###"); cmd_traps(args.spec)
        print("\n### TIES ###"); cmd_ties(args.spec, args.world_dir)
        print("\n### REFS ###"); cmd_refs(args.spec, args.world_dir)


if __name__ == "__main__":
    main()
