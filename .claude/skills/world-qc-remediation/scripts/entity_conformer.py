#!/usr/bin/env python3
"""Domain-agnostic entity conformer: check that every reference to a canonical entity across the
filesystem matches the master (right name for the ID, right ID for the name), and, with `apply`,
fix the safe, fully-determined cases in place. Catches the HR name mess, the vendor-crosswalk "46",
hallucinated / inconsistent names and mis-stamped IDs.

It is NOT HR-specific: you point it at whatever table the spec declares as the canonical master and
name the key + name columns. Employees, vendors, parties, accounts, SKUs, same engine.

  map   <master.(csv|xlsx)> --id-col ID --name-col NAME
          Print the canonical id<->name map (sanity check).

  check <master.(csv|xlsx)> <world_dir> --id-col ID --name-col NAME
          For every CSV/XLSX row in the world that contains a canonical ID, confirm the canonical
          name for that ID is in the same row. Flags: (a) an ID paired with a DIFFERENT entity's
          name, (b) a canonical name paired with a value that structurally resembles the master's
          ID scheme but isn't a valid ID (a hallucinated/wrong ID), (c) an ID over-used as a
          constant fill across a table that also carries other IDs. Detection only. Diff-only.

  apply <master.(csv|xlsx)> <world_dir> --id-col ID --name-col NAME [--write] [--backup-dir DIR]
          Same detection, but FIX the two fully-determined cases in place: a cell that is exactly a
          wrong canonical name (-> the right name for the ID stamped in its row), and a cell that is
          exactly a wrong ID-shaped token (-> the right ID for the entity named in its row). These
          are whole-cell, exact substitutions, no prose surgery, no guessing. Everything that needs
          judgment (a name missing entirely, a name buried in a sentence, a constant-fill column) is
          reported for you to handle, never auto-changed. Default is a DRY RUN; add --write to modify.
          Every file is backed up first, and change_manifest.md + comments.txt are written into the
          world folder. After --write, run metadata_hygiene.py clean on each changed file.

Requires the master's IDs to follow an alpha-prefix + digit-run pattern (e.g. HR-EMP-00046) for the
wrong-ID check; purely numeric ID schemes fall back to the wrong-name and constant-fill checks only.

Deps: openpyxl for xlsx; csv stdlib.
"""
import argparse, io, os, re, sys, glob, csv, collections
import _common
_common.setup_console()

def norm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").lower())

def idnorm(s):
    s = str(s or "").strip()
    return s.lstrip("0") or "0" if s.isdigit() else s

_ID_SHAPE_RE = re.compile(r"^([A-Za-z][A-Za-z_-]*)(\d+)$")

def id_shape_signature(ids):
    """Infer the master's own ID scheme (alpha-prefix + trailing digit-run) from its real ID
    values, e.g. HR-EMP-00046 -> prefix 'HR-EMP-', digit length 5. Empty if the master's IDs
    don't follow that shape (e.g. purely numeric), callers must treat that as 'can't tell'."""
    prefixes, lens = set(), set()
    for i in ids:
        m = _ID_SHAPE_RE.match(i)
        if m:
            prefixes.add(m.group(1).upper())
            lens.add(len(m.group(2)))
    return prefixes, lens

def looks_like_unresolved_id(v, prefixes, lens):
    """True if v structurally resembles the master's ID scheme (same prefix + digit-run length)
    but is not itself a value we'd recognize, i.e. a plausible hallucinated/wrong ID, not just
    any word."""
    if not v or not prefixes:
        return False
    m = _ID_SHAPE_RE.match(v)
    if not m:
        return False
    return m.group(1).upper() in prefixes and len(m.group(2)) in lens

# --------------------------------------------------------------------------------------------------
# Coordinate-aware row iteration: yields, per data row, the header->value dict AND a `setter(key,val)`
# that writes a new value back to the underlying cell. check() ignores the setter; apply() uses it.
# Using one iterator for both means detection and fixing can never drift apart.
# --------------------------------------------------------------------------------------------------

def _iter_csv(path):
    text = _common.read_text(path)

    # io.StringIO, NOT text.splitlines(). splitlines() strips the line terminators, so csv.reader
    # can no longer tell a newline INSIDE a quoted field from the end of a record: a Notes or
    # Address field spanning two lines comes back with its line break deleted, and save() then
    # writes that mangled version over the whole file. splitlines() also breaks on \x0b, \x0c,
    # \x85 and \u2028, so those inside a field invent phantom rows.
    delim = "\t" if path.lower().endswith((".tsv", ".tab")) else ","
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delim))
    if not rows:
        return [], None
    hdr = rows[0]

    # Duplicate header names are real (a second "Notes", a stray "Name"). Reading kept the LAST
    # such column while writing used hdr.index(), the FIRST, so the fix landed on a different
    # column than the one it was checked against: unrelated data destroyed, the reported problem
    # still there. Bind each row's cells to a COLUMN INDEX and never look a name up twice.
    dirty = {"changed": False}
    body = [list(r) for r in rows[1:]]

    def emit():
        for ridx, r in enumerate(body):
            cells, col_of = {}, {}
            for i, name in enumerate(hdr):
                if name in cells:          # first occurrence wins, consistently, both ways
                    continue
                cells[name] = r[i] if i < len(r) else ""
                col_of[name] = i

            def make_setter(rowlist, col_of=col_of):
                def setter(key, val):
                    ci = col_of.get(key)
                    if ci is None:
                        return
                    while len(rowlist) <= ci:
                        rowlist.append("")
                    rowlist[ci] = val
                    dirty["changed"] = True
                return setter
            yield ridx + 2, cells, make_setter(r)

    def save():
        if not dirty["changed"]:
            return False
        # Emit the file's OWN line ending as the record terminator, then write with no
        # translation. Letting write_text translate would also rewrite the newlines inside a
        # quoted field, corrupting the multi-line values this parser exists to preserve.
        out = io.StringIO(newline="")
        w = csv.writer(out, delimiter=delim, lineterminator=_common.detect_newline(path))
        w.writerow(hdr)
        w.writerows(body)
        _common.write_text(path, out.getvalue(), newline="")   # same encoding it arrived in
        return True
    return emit(), save

def _iter_xlsx(path):
    import openpyxl
    # data_only=False so we never destroy formulas by round-tripping computed values back as literals.
    wb = openpyxl.load_workbook(path)
    dirty = {"changed": False}
    touched = []          # (sheet, coord, old value) so the save knows what may now be stale
    def emit():
        for ws in wb.worksheets:
            rows = list(ws.iter_rows())
            if not rows:
                continue
            hdr = [("" if c.value is None else str(c.value)) for c in rows[0]]
            for excel_row in rows[1:]:
                cells = {}
                colcell = {}
                for i, c in enumerate(excel_row):
                    if i < len(hdr):
                        cells[hdr[i]] = "" if c.value is None else str(c.value)
                        colcell[hdr[i]] = c
                def make_setter(cc, sheet=ws.title):
                    def setter(key, val):
                        if key in cc:
                            touched.append((sheet, cc[key].coordinate, cc[key].value))
                            cc[key].value = val
                            dirty["changed"] = True
                    return setter
                yield excel_row[0].row, cells, make_setter(colcell)
    def save():
        if not dirty["changed"]:
            return False
        # Not wb.save(). openpyxl blanks the cached result of every formula on save, and
        # AutoQC reads cached results, so conforming a name would silently empty every
        # computed cell in the workbook. Names are text; the numbers are unaffected and
        # get carried across.
        _common.save_xlsx_preserving_values(wb, path, changed=touched)
        return True
    return emit(), save

def iter_rows(path):
    """Return (row_generator, save_fn) or (None, None) if unreadable. row_generator yields
    (rowlabel, cells_dict, setter)."""
    ext = path.lower().rsplit(".", 1)[-1]
    try:
        if ext in ("csv", "tsv"):
            return _iter_csv(path)
        if ext in ("xlsx", "xlsm"):
            return _iter_xlsx(path)
    except Exception as e:
        print(f"[UNREADABLE] {path}: {e}", file=sys.stderr)
    return None, None

def load_master(path, id_col, name_col):
    gen, _ = iter_rows(path)
    if gen is None:
        sys.exit(f"master: could not read {path}")
    rows = list(gen)
    if not rows:
        sys.exit(f"master: no data rows in {path}")
    hdr = list(rows[0][1].keys())
    def findcol(want):
        exact = [h for h in hdr if norm(want) == norm(h)]
        if exact: return exact[0]
        sub = [h for h in hdr if norm(want) in norm(h)]
        if len(sub) > 1:
            sys.exit(f"master: ambiguous column '{want}' matches {sub} in {hdr}, use a more specific --id-col/--name-col")
        return sub[0] if sub else None
    ic, nc = findcol(id_col), findcol(name_col)
    if not ic or not nc:
        sys.exit(f"master: could not find id-col '{id_col}' or name-col '{name_col}' in {hdr}")
    id2name, name2id = {}, {}
    for _, cells, _ in rows:
        i, n = str(cells.get(ic, "")).strip(), str(cells.get(nc, "")).strip()
        if i and n:
            id2name[i] = n
            name2id[norm(n)] = i
    return id2name, name2id

def row_findings(cells, id2name, name2id, ids, idmap, id_prefixes, id_lens):
    """The single detection rule. Returns a list of findings for one row:
       {kind, key, old, new, applyable}
    `key` is the header of the offending cell (None if we couldn't localize to one cell).
    `applyable` is True only for a whole-cell exact substitution we can make safely."""
    out = []
    stripped = {k: str(v).strip() for k, v in cells.items()}
    row_text_norm = norm(" ".join(stripped.values()))
    present_ids = []
    for v in stripped.values():
        if v in ids: present_ids.append(v)
        elif idnorm(v) in idmap: present_ids.append(idmap[idnorm(v)])
    present_id_set = set(present_ids)
    explained_names = set()
    for cid in present_ids:
        canon = id2name[cid]
        if norm(canon) in row_text_norm:
            explained_names.add(norm(canon))
            continue
        other = [id2name[oid] for oid in ids
                 if oid != cid and norm(id2name[oid]) in row_text_norm]
        if other:
            wrong = other[0]
            explained_names.update(norm(n) for n in other)
            # can we localize the wrong name to a single cell that IS exactly that name?
            key = next((k for k, v in stripped.items() if norm(v) == norm(wrong)), None)
            out.append({"kind": "WRONG NAME", "key": key, "old": wrong, "new": canon,
                        "applyable": key is not None,
                        "msg": f"ID {cid} (={canon}) but row names {wrong!r}"})
        # NOTE: an ID present WITHOUT any name is NOT flagged, ID-only reference rows (timesheets,
        # ledgers, transaction lines, vendor→employee crosswalks) are legitimate and ubiquitous.
        # The "stamped the same ID everywhere" defect is caught by CONSTANT FILL instead.
    bogus_ids = [v for v in stripped.values()
                 if looks_like_unresolved_id(v, id_prefixes, id_lens)
                 and v not in ids and idnorm(v) not in idmap]
    if bogus_ids:
        for cnorm, cid in name2id.items():
            if cnorm in explained_names: continue
            if cnorm in row_text_norm and cid not in present_id_set:
                bogus = bogus_ids[0]
                key = next((k for k, v in stripped.items() if v == bogus), None)
                out.append({"kind": "WRONG ID", "key": key, "old": bogus, "new": cid,
                            "applyable": key is not None,
                            "msg": f"name {id2name[cid]!r} present but ID {cid} missing (found {bogus!r})"})
    return out

def _world_tables(world_dir, master):
    return [f for f in glob.glob(os.path.join(world_dir, "**", "*"), recursive=True)
            if os.path.isfile(f) and f.lower().rsplit(".", 1)[-1] in ("csv", "tsv", "xlsx", "xlsm")
            and os.path.abspath(f) != os.path.abspath(master)
            and not _common.is_qc_artifact(f)]

def cmd_map(path, id_col, name_col):
    id2name, _ = load_master(path, id_col, name_col)
    print(f"{len(id2name)} canonical entities")
    for i, n in list(id2name.items())[:15]:
        print(f"  {i} -> {n}")

def _constant_fill(per_file, id2name):
    """Flag an ID that dominates a table which ALSO carries other IDs (a real fill artifact),
    NOT a legitimately single-entity table like a 12-week timesheet for one person."""
    out = []
    for base, ctr in per_file.items():
        total = sum(ctr.values())
        if len(ctr) <= 1:
            continue  # single-entity table, normal, never a fill artifact
        for cid, n in ctr.items():
            if n >= 10 and n / total >= 0.9:
                out.append((base, cid, n, id2name[cid]))
    return out

def cmd_check(master, world_dir, id_col, name_col):
    if not os.path.isdir(world_dir):
        sys.exit(f"check: world_dir not found or not a directory: {world_dir}")
    id2name, name2id = load_master(master, id_col, name_col)
    ids = set(id2name); idmap = {idnorm(i): i for i in ids}
    id_prefixes, id_lens = id_shape_signature(ids)
    print(f"ENTITY CONFORMER, {len(ids)} canonical entities from {os.path.basename(master)}.\n")
    problems = skipped = 0
    per_file = collections.defaultdict(collections.Counter)
    for f in sorted(_world_tables(world_dir, master)):
        base = os.path.relpath(f, world_dir)
        gen, _ = iter_rows(f)
        if gen is None:
            skipped += 1; print(f"[UNREADABLE] {base}, skipped, could not parse"); continue
        for label, cells, _ in gen:
            for v in cells.values():
                cid = v if v in ids else idmap.get(idnorm(v))
                if cid: per_file[base][cid] += 1
            for fd in row_findings(cells, id2name, name2id, ids, idmap, id_prefixes, id_lens):
                problems += 1
                print(f"[{fd['kind']}] {base} row {label}: {fd['msg']}")
    for base, cid, n, nm in _constant_fill(per_file, id2name):
        problems += 1
        print(f"[CONSTANT FILL] {base}: ID {cid} (={nm}) appears in {n} rows, likely a fill artifact")
    skip_note = f" ({skipped} file(s) unreadable, not scanned)" if skipped else ""
    print(f"\n--- {problems} entity issue(s){skip_note}. Fix toward the master; confirm none is a declared trap. ---")
    return problems

def cmd_apply(master, world_dir, id_col, name_col, write, backup_dir):
    if not os.path.isdir(world_dir):
        sys.exit(f"apply: world_dir not found or not a directory: {world_dir}")
    id2name, name2id = load_master(master, id_col, name_col)
    ids = set(id2name); idmap = {idnorm(i): i for i in ids}
    id_prefixes, id_lens = id_shape_signature(ids)
    if backup_dir is None:
        backup_dir = _common.default_backup_dir(world_dir)
    mode = "WRITE" if write else "DRY RUN (no files changed; add --write to apply)"
    print(f"ENTITY CONFORMER apply, {mode}, {len(ids)} canonical entities.\n")
    changes, review = [], []
    fixed = flagged = 0
    for f in sorted(_world_tables(world_dir, master)):
        base = os.path.relpath(f, world_dir)
        gen, save = iter_rows(f)
        if gen is None:
            review.append(f"{base}: unreadable, skipped"); continue
        file_edits = []          # (label, key, old, new)
        for label, cells, setter in gen:
            for fd in row_findings(cells, id2name, name2id, ids, idmap, id_prefixes, id_lens):
                if fd["applyable"]:
                    if write:
                        setter(fd["key"], fd["new"])
                    file_edits.append((label, fd["key"], fd["old"], fd["new"]))
                else:
                    flagged += 1
                    review.append(f"{base} row {label}: {fd['kind']}, {fd['msg']} (needs your judgment)")
        if file_edits:
            if write:
                _common.backup_file(f, backup_dir)
                save()
            for label, key, old, new in file_edits:
                fixed += 1
                print(f"[FIX] {base} row {label} [{key}]: {old!r} -> {new!r}")
                changes.append((base, f"row {label}, col {key}", old, new))
    if write and changes:
        _common.append_manifest(backup_dir, "entity_conformer", changes, review)
    verb = "Fixed" if write else "Would fix"
    print(f"\n--- {verb} {fixed} whole-cell mismatch(es); {flagged} case(s) need your judgment "
          f"(see the list above). ---")
    if write and changes:
        print(f"Backups + change_manifest.md / comments.txt in {backup_dir} (beside your world, not inside it).")
        print("NEXT: run metadata_hygiene.py clean on each changed file (writing an xlsx re-stamps the tool fingerprint).")
    elif not write and fixed:
        print("This was a dry run. Re-run with --write to apply the fixes above.")
    return fixed

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("map"); m.add_argument("master")
    m.add_argument("--id-col", required=True); m.add_argument("--name-col", required=True)
    c = sub.add_parser("check"); c.add_argument("master"); c.add_argument("world_dir")
    c.add_argument("--id-col", required=True); c.add_argument("--name-col", required=True)
    a = sub.add_parser("apply"); a.add_argument("master"); a.add_argument("world_dir")
    a.add_argument("--id-col", required=True); a.add_argument("--name-col", required=True)
    a.add_argument("--write", action="store_true", help="actually modify files (default: dry run)")
    a.add_argument("--backup-dir", default=None, help="where to copy originals (default: <world>/_qc_backup)")
    args = ap.parse_args()
    if args.cmd == "map": cmd_map(args.master, args.id_col, args.name_col)
    elif args.cmd == "check": cmd_check(args.master, args.world_dir, args.id_col, args.name_col)
    elif args.cmd == "apply": cmd_apply(args.master, args.world_dir, args.id_col, args.name_col,
                                        args.write, args.backup_dir)

if __name__ == "__main__":
    main()
