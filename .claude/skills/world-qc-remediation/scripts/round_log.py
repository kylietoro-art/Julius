#!/usr/bin/env python3
"""round_log.py, cross-round memory for AutoQC remediation.

WHY THIS EXISTS
---------------
A world that takes 20+ AutoQC rounds is almost never a world with unusually many defects. It is a
world where each round fixed the *instances* AutoQC named instead of the *class* those instances
belong to, so the same defect keeps coming back under a different filename.

That is invisible round-to-round unless something remembers. This does. It records each round's
findings, buckets them into defect classes, and on the next round tells you which classes CAME BACK.

A repeat class is a diagnosis, not a nuisance: it means last round's fix was applied at the instance
level. Go wide on that class immediately.

WHAT IT IS NOT
--------------
It is not a detector and it does not read the world's files. It reads the AutoQC report text you
already have. Zero token cost, zero risk to the corpus.

STORAGE
-------
Everything lives in the world's sibling `_qc_backup` folder (never inside the world, so re-zipping
the world to upload can't ship it):

    <world>_qc_backup/round_log.json   machine-readable history
    <world>_qc_backup/round_log.md     human-readable, paste-able into a hand-off note

USAGE
-----
    python round_log.py start  <world> --round 3 --findings autoqc_round3.txt
    python round_log.py close  <world> --round 3 [--fixed 14] [--expanded 9] [--traps 2]
                                                 [--false 1] [--blocked 0] [--note "..."]
    python round_log.py status <world>

`start` prints the repeat-class report. `close` records the round's dispositions and enforces the
batch gate arithmetic in plain words. `status` prints the whole history.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

_common.setup_console()

LOG_JSON = "round_log.json"
LOG_MD = "round_log.md"

# --------------------------------------------------------------------------------------------------
# Defect classes.
#
# Deliberately coarse. The point is not a taxonomy, it is answering one question: "have I seen this
# KIND of thing before?" Ten buckets that a human agrees with beat forty that need a lookup table.
#
# Order matters: the first pattern that matches wins, so the specific, high-signal classes
# (build-artifact leakage, answer leakage) are listed before the general ones.
# --------------------------------------------------------------------------------------------------
CLASSES = [
    ("a_code_leakage", "Builder A## codes visible in world files", [
        r"\bA\d{2}\b", r"artifact[- ]index", r"build scaffold", r"spec\s+(?:id|code|reference)",
    ]),
    ("answer_leakage", "Solution or reasoning leaked into world files", [
        r"answer key", r"solution leak", r"reasoning leak", r"correct answer",
        r"task[- ]id", r"signpost",
    ]),
    ("metadata_fingerprint", "Tool fingerprints / build dates in file metadata", [
        r"openpyxl", r"reportlab", r"python-docx", r"python-pptx", r"pymupdf", r"fpdf",
        r"metadata", r"producer", r"fingerprint", r"creator tool", r"build date",
    ]),
    ("raw_markup", "Raw Markdown/HTML printed as visible text", [
        r"raw (?:markdown|html)", r"markup", r"<\s*(?:td|tr|div|p|table|br|h[1-6])\s*/?>",
        r"##\s", r"\*\*[A-Za-z]", r"unrendered",
    ]),
    ("placeholder_synthetic", "Placeholder, template residue, or synthetic filler", [
        r"placeholder", r"lorem ipsum", r"\bTODO\b", r"\bTBD\b", r"template residue",
        r"scaffold", r"\bXXX+\b", r"john doe", r"acme", r"sample (?:text|data)",
        r"synthetic marker", r"\[insert",
    ]),
    ("entity_inconsistency", "Same person/entity named, titled or ID'd differently across files", [
        r"\bpersonnel\b", r"inconsistent (?:name|title|id|role)", r"name mismatch",
        r"different (?:name|title|role|department)", r"roster", r"employee id",
        r"naming (?:is |are )?(?:in)?consistent", r"defined term",
    ]),
    ("math_footing", "Totals don't foot / calculations disagree with inputs", [
        r"\bfoot(?:s|ing|ed)?\b", r"does not (?:sum|add|total)", r"doesn'?t (?:sum|add|total)", r"sums? to",
        r"\bcalculation", r"\barithmetic", r"\breconcil", r"stale[- ]base", r"numerical value",
        r"structured data", r"tie[s]? to", r"mismatch(?:ed)? total",
    ]),
    ("temporal", "Dates, chronology or timeline don't hold together", [
        r"\bdate[sd]?\b", r"\bchronolog", r"\btimeline", r"\btemporal", r"anchor date", r"\btenure\b",
        r"expir", r"before the", r"after the", r"anachron",
    ]),
    ("broken_reference", "A referenced document or value doesn't resolve", [
        r"broken (?:reference|link|cross-reference)", r"unresolv", r"does not (?:exist|resolve)",
        r"missing (?:file|artifact|document)", r"phantom", r"not found in", r"dangling",
    ]),
    ("file_integrity", "File is corrupt, empty, unreadable or won't render", [
        r"corrupt", r"unreadable", r"empty file", r"zero[- ]byte", r"won'?t (?:open|render|parse)",
        r"fails? to (?:open|render|parse)", r"structurally broken", r"unusable",
    ]),
    ("realism_voice", "Voice, tone, texture or document authenticity reads machine-made", [
        r"\bvoice\b", r"tone", r"authenticity", r"letterhead", r"signature block", r"watermark",
        r"flattened", r"realis", r"texture", r"formatting match",
    ]),
    ("pii_copyright", "Real PII or copyrighted material in world files", [
        r"\bPII\b", r"copyright", r"real (?:individual|person|people)", r"\bSSN\b",
        r"phone (?:number|pattern)", r"reserved (?:fictional|range|pattern)",
        r"personally identifiable",
    ]),
    ("citation_facts", "Real-world references, citations or jurisdiction facts are wrong", [
        r"citation", r"statute", r"regulation", r"jurisdiction", r"standard[s]? reference",
        r"real[- ]world fact", r"fabricat", r"\bGDPR\b", r"\bHIPAA\b", r"\bSEC\b", r"\bOSHA\b",
    ]),
]

FALLBACK = ("other", "Uncategorised, read the finding text")

# A finding block: AutoQC output is line-oriented and inconsistently formatted across versions, so we
# split on blank lines and on obvious bullet/numbering starts rather than trusting one schema.
BULLET = re.compile(r"^\s*(?:[-*•]|\d{1,3}[.)]|\[[A-Za-z0-9]+\])\s+")
# Filenames with a real extension. Deliberately no spaces in the stem: AutoQC cites underscore/hyphen
# names, and allowing spaces makes the match swallow the preceding words of the sentence ("in
# leave_ledger.csv"), which then pollutes the per-class file list and breaks round-to-round comparison.
FILENAME = re.compile(r"[\w][\w\-.()]{0,80}\.(?:xlsx|xlsm|csv|tsv|docx|doc|pdf|pptx|txt|md|html|eml|json)\b",
                      re.IGNORECASE)
# AutoQC prefixes each finding with its dimension name ("[P0] No Out-of-World or Build Artifacts:").
# Those names are full of the same words the class patterns look for, so a metadata finding filed under
# the out-of-world dimension would classify as A## leakage. Strip the prefix and classify the body.
DIMENSION_PREFIX = re.compile(r"^\s*(?:[-*•]|\d{1,3}[.)])?\s*(?:\[[^\]]{1,12}\]\s*)?"
                              r"[A-Z][A-Za-z0-9 /&'\-]{6,90}:\s*")


def classify(text):
    """Return (class_key, class_label) for one finding block. First match wins.

    Two passes. The AQC dimension prefix is stripped first, because a finding filed under a
    dimension called "Metadata and Fingerprints" must not be classified by its dimension name
    instead of its content.

    But the same strip eats a prefix that IS the content: "Footing: the Q3 total does not equal
    the sum of its components" loses the only word that classifies it and lands in Uncategorised.
    Uncategorised findings never match each other, so REPEAT and CHRONIC go blind, which is the
    whole point of this log. So if the stripped pass finds nothing, try again with the prefix on.
    """
    def match(s):
        low = s.lower()
        for key, label, pats in CLASSES:
            for pat in pats:
                # A## and the HTML-tag patterns are case-sensitive-ish but the rest are not;
                # searching lowered text with IGNORECASE is close enough and much simpler.
                if re.search(pat, low, re.IGNORECASE):
                    return key, label
        return None

    text = text.strip()
    body = DIMENSION_PREFIX.sub("", text, count=1)
    return match(body if len(body) >= 20 else text) or match(text) or FALLBACK


def split_findings(raw):
    """Split a pasted AutoQC report into finding blocks.

    Two passes, because report formats vary: if the text has bullet/numbered lines, treat each as the
    start of a finding; otherwise fall back to blank-line-separated paragraphs. Either way, blocks
    shorter than 15 characters are dropped as headers/noise.
    """
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    bulleted = sum(1 for ln in lines if BULLET.match(ln))
    blocks, cur = [], []

    # Two bullets is enough to trust the bullets. The threshold used to be three, which meant a round
    # with two findings fell through to paragraph mode and merged them into one block: one ticket
    # containing two findings, and a finding count of 1. Late rounds are exactly where counts are
    # small, so the merge hit precisely when the count mattered most.
    if bulleted >= 2:
        # Anything before the first bullet is a report header, not a finding, drop it.
        started = False
        for ln in lines:
            if BULLET.match(ln):
                if cur:
                    blocks.append("\n".join(cur))
                cur = [ln]
                started = True
            elif started and cur:
                cur.append(ln)
        if cur:
            blocks.append("\n".join(cur))
    else:
        for ln in lines:
            if ln.strip():
                cur.append(ln)
            elif cur:
                blocks.append("\n".join(cur))
                cur = []
        if cur:
            blocks.append("\n".join(cur))

    out = []
    for b in blocks:
        b = b.strip()
        if len(b) >= 15:
            out.append(b)
    return out


def files_in(text):
    """Filenames cited by a finding, de-duplicated, lowercased for comparison across rounds."""
    return sorted({m.group(0).strip().lower() for m in FILENAME.finditer(text)})


def log_paths(world):
    d = _common.default_backup_dir(world)
    return d, os.path.join(d, LOG_JSON), os.path.join(d, LOG_MD)


def load(world):
    _, jf, _ = log_paths(world)
    if not os.path.exists(jf):
        return {"world": os.path.abspath(world), "rounds": []}
    try:
        with open(jf, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (ValueError, OSError) as e:
        print(f"ERROR: could not read the existing round log at {jf} ({e}).")
        print("Move or delete that file and re-run, or fix the JSON by hand.")
        sys.exit(2)


def save(world, data):
    d, jf, mf = log_paths(world)
    os.makedirs(d, exist_ok=True)
    with open(jf, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    render_md(data, mf)
    return jf, mf


def render_md(data, path):
    L = ["# AutoQC round log", "",
         f"World: `{data.get('world','')}`", "",
         "One row per round. `Repeats` are defect classes that already appeared in an earlier round,",
         "each one means that class was fixed at the instance level, not the class level.", "",
         "| Round | Opened | Findings | Classes | Repeats | Disposition |",
         "|---|---|---|---|---|---|"]
    for r in data.get("rounds", []):
        disp = r.get("disposition")
        if disp:
            dtxt = (f"fixed {disp.get('fixed',0)}, widened {disp.get('expanded',0)}, "
                    f"traps {disp.get('traps',0)}, false {disp.get('false',0)}, "
                    f"blocked {disp.get('blocked',0)}")
        else:
            dtxt = "_open_"
        L.append(f"| {r['round']} | {r['opened'][:16]} | {r['count']} | "
                 f"{len(r['classes'])} | {len(r.get('repeats', []))} | {dtxt} |")
    L += ["", "## Detail", ""]
    for r in data.get("rounds", []):
        L.append(f"### Round {r['round']}, {r['opened'][:16]}")
        L.append("")
        for key, info in sorted(r["classes"].items(), key=lambda kv: -kv[1]["n"]):
            flag = "  **(REPEAT)**" if key in r.get("repeats", []) else ""
            L.append(f"- **{info['label']}**: {info['n']} finding(s){flag}")
            if info.get("files"):
                L.append(f"  - files named: {', '.join(info['files'][:12])}"
                         + (" …" if len(info["files"]) > 12 else ""))
        if r.get("note"):
            L += ["", f"Note: {r['note']}"]
        L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


RULINGS_MD = "rulings.md"


def rulings_path(world):
    return os.path.join(_common.default_backup_dir(world), RULINGS_MD)


def add_ruling(world, text, rnd=None):
    """Record a decision that binds every later round.

    Rounds 5, 6 and 7 of one world each re-asked "which governs, the Plan or the Spec?" when the
    builder had answered it in round 4. The answer was sitting in the round log as a note, and nothing
    read it as binding, so the question came back every time the chat was fresh.

    Everything else this toolkit needs survives a new chat because it is on disk. Decisions did not.
    """
    p = rulings_path(world)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    new = not os.path.exists(p)
    with open(p, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Standing rulings\n\nDecisions that bind every later round. Read these before "
                     "triage.\nNever re-ask a question answered here.\n")
        stamp = datetime.now().strftime("%Y-%m-%d")
        fh.write(f"\n- **{stamp}**"
                 + (f" (round {rnd})" if rnd is not None else "")
                 + f": {text.strip()}\n")
    return p


def read_rulings(world):
    p = rulings_path(world)
    if not os.path.exists(p):
        return []
    return [l.strip() for l in _common.read_text(p).splitlines()
            if l.strip().startswith("- ")]


def write_tickets(world, rnd, blocks):
    """Write each finding to its own numbered file on disk.

    A round runs for many turns. The findings get pasted in once at the start, and by the time a fix
    is being made the original text is far back in the conversation behind script output. What comes
    out then is a summary of a summary, and summaries drop clauses. An AutoQC finding is usually
    several assertions in one paragraph, so a dropped clause is a half-finished fix that comes back
    next round.

    Putting each finding in its own file means the fixer re-reads the exact words one turn before
    acting on them, and no amount of context rot can touch it.
    """
    d = os.path.join(_common.default_backup_dir(world), "tickets", f"round{rnd:03d}")
    os.makedirs(d, exist_ok=True)
    for old in os.listdir(d):
        if old.endswith(".txt"):
            os.remove(os.path.join(d, old))
    paths = []
    for i, b in enumerate(blocks, 1):
        p = os.path.join(d, f"t{i:02d}.txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(f"TICKET {i} of {len(blocks)}  |  round {rnd}\n")
            fh.write("=" * 78 + "\n\n")
            fh.write("THE FINDING, VERBATIM. Read this immediately before you fix it, and quote it\n")
            fh.write("back in full. Then list every separate thing it asserts, one line each. A\n")
            fh.write("finding that says three things needs three lines, and a fix that answers two\n")
            fh.write("of them is not done.\n\n")
            fh.write("-" * 78 + "\n")
            fh.write(b.strip() + "\n")
        paths.append(p)
    return d, paths


def cmd_start(args):
    world = args.world
    if not os.path.isdir(world):
        print(f"ERROR: world folder not found: {world}")
        sys.exit(2)
    if not os.path.isfile(args.findings):
        print(f"ERROR: findings file not found: {args.findings}")
        print("Save the AutoQC report to a text file first, then pass it with --findings.")
        sys.exit(2)

    raw = _common.read_text(args.findings)
    blocks = split_findings(raw)
    if not blocks:
        print("ERROR: no findings could be read out of that file. Is it the AutoQC report text?")
        sys.exit(2)

    classes = {}
    for b in blocks:
        key, label = classify(b)
        e = classes.setdefault(key, {"label": label, "n": 0, "files": []})
        e["n"] += 1
        for f in files_in(b):
            if f not in e["files"]:
                e["files"].append(f)

    data = load(world)
    seen_before = {}
    for prev in data["rounds"]:
        if prev["round"] >= args.round:
            continue
        for k in prev["classes"]:
            seen_before.setdefault(k, []).append(prev["round"])

    repeats = [k for k in classes if k in seen_before]

    data["rounds"] = [r for r in data["rounds"] if r["round"] != args.round]
    data["rounds"].append({
        "round": args.round,
        "opened": datetime.now().isoformat(timespec="seconds"),
        "count": len(blocks),
        "classes": classes,
        "repeats": repeats,
        "disposition": None,
        "note": args.note or "",
    })
    data["rounds"].sort(key=lambda r: r["round"])
    jf, mf = save(world, data)

    rul = read_rulings(world)
    if rul:
        print("STANDING RULINGS, already decided. Do not re-ask these.")
        for r in rul:
            print(f"  {r}")
        print()
    print(f"Round {args.round}: {len(blocks)} findings, {len(classes)} defect classes.\n")
    for key, info in sorted(classes.items(), key=lambda kv: -kv[1]["n"]):
        mark = "  <-- REPEAT" if key in repeats else ""
        print(f"  {info['n']:>3}  {info['label']}{mark}")
        if info["files"]:
            shown = ", ".join(info["files"][:6])
            more = f" (+{len(info['files']) - 6} more)" if len(info["files"]) > 6 else ""
            print(f"       files named: {shown}{more}")
    print()

    if repeats:
        print("=" * 78)
        print("REPEAT CLASSES, these already appeared in an earlier round:")
        for k in repeats:
            print(f"  - {classes[k]['label']}  (also in round(s) {', '.join(str(x) for x in seen_before[k])})")
        print()
        print("A class that comes back was fixed at the instance level last time, not the class level.")
        print("Do NOT just fix the newly-named files. Sweep the whole corpus for this class now,")
        print("every file type it could touch, or it will cost you another round.")
        chronic = [k for k in repeats if len(seen_before[k]) >= 2]
        if chronic:
            print()
            print("CHRONIC (3rd+ appearance): " + ", ".join(classes[k]["label"] for k in chronic))
            print()
            print("STOP. Do not fix the newly-named files. Fixing instances is what got this class to")
            print("a third round. Run the STRUCTURAL PASS instead (SKILL.md Phase 2S):")
            print()
            print("    python blast_radius.py all <world>")
            print()
            print("It reads every change these scripts have made across all rounds and answers the")
            print("two questions a chronic class always turns on: did the earlier sweeps actually")
            print("finish (is the old value still standing somewhere else), and did fixing one thing")
            print("break another (does every edited file still foot, and who else carries the values")
            print("that changed). It ends with a plain verdict and what to do about it.")
            print()
            print("Only if that verdict comes back with nothing structural is this above your level")
            print("to fix - and then you escalate with the specifics it gives you, not a shrug.")
        print("=" * 78)
    else:
        print("No repeat classes. Last round's fixes held.")

    if args.round >= 12 and not repeats:
        print()
        print("NOTE: this is round %d with no repeat classes, which means each round is finding" % args.round)
        print("genuinely new things. Run `blast_radius.py all <world>` anyway before you fix more -")
        print("a fix that quietly breaks a neighbouring value shows up as a NEW class, not a repeat,")
        print("so a long clean-looking run can still be self-inflicted.")

    td, tpaths = write_tickets(world, args.round, blocks)
    print(f"\n{len(tpaths)} ticket(s) written to {td}")
    print("Read each one immediately before fixing it. Do not work from memory of the paste.")

    print(f"\nLog: {mf}")


def cmd_summary(args):
    """The only write-up anyone downstream actually reads.

    Rounds used to leave a trail of notes, hand-off files and per-round markdown in the builder's
    working folder. None of it is what RLS wants. RLS wants one sentence on what changed, and one
    sentence per disputed finding. This prints exactly that, ready to paste.
    """
    data = load(args.world)
    rounds = data.get("rounds", [])
    if not rounds:
        print("No rounds logged for this world yet.")
        return 0
    r = (next((x for x in rounds if x["round"] == args.round), None) if args.round
         else rounds[-1])
    if r is None:
        print(f"Round {args.round} was never logged.")
        return 0

    disp = r.get("disposition") or {}
    classes = [lbl for _, lbl in (r.get("classes") or [])] if isinstance(r.get("classes"), list) else []
    if not classes:
        counts = r.get("class_counts") or {}
        classes = list(counts) if isinstance(counts, dict) else []

    changed = r.get("changed")
    if not changed:
        fixed = disp.get("fixed", 0)
        widened = disp.get("expanded", 0)
        total = fixed + widened
        what = ", ".join(c.split("/")[0].strip().lower() for c in classes[:3]) if classes else ""
        changed = (f"Round {r['round']}: fixed {total} finding(s)"
                   + (f" covering {what}" if what else "")
                   + ".")

    print("=" * 78)
    print("FOR THE RLS REVISION NOTE")
    print("=" * 78)
    print(f"\n  {changed}\n")

    disputes = r.get("disputes") or []
    if disputes:
        print("  Disputed:")
        for d in disputes:
            print(f"    - {d}")
        print()
    elif disp.get("false") or disp.get("traps"):
        n = disp.get("false", 0) + disp.get("traps", 0)
        print(f"  {n} finding(s) were disputed or left as declared traps, but no reason was")
        print("  recorded. Add one with:")
        print(f"    round_log.py close <world> --round {r['round']} --dispute \"<one sentence>\"\n")

    print("  Paste the block above into RLS. Nothing else from this round needs to go anywhere.")
    return 0


def cmd_close(args):
    world = args.world
    data = load(world)
    match = [r for r in data["rounds"] if r["round"] == args.round]
    if not match:
        print(f"ERROR: round {args.round} was never started. Run `start` first.")
        sys.exit(2)
    r = match[0]

    disp = {"fixed": args.fixed, "expanded": args.expanded, "traps": args.traps,
            "false": getattr(args, "false"), "blocked": args.blocked}
    accounted = sum(disp.values())
    r["disposition"] = disp
    r["closed"] = datetime.now().isoformat(timespec="seconds")
    if getattr(args, "changed", ""):
        r["changed"] = args.changed.strip()
    if getattr(args, "dispute", None):
        r["disputes"] = [d.strip() for d in args.dispute if d.strip()]
    if args.note:
        r["note"] = (r.get("note", "") + " " + args.note).strip()
    jf, mf = save(world, data)

    print(f"Round {args.round} closed.")
    print(f"  findings on arrival: {r['count']}")
    print(f"  fixed:               {disp['fixed']}")
    print(f"  widened to class:    {disp['expanded']}")
    print(f"  left as traps:       {disp['traps']}")
    print(f"  ruled out as false:  {disp['false']}")
    print(f"  blocked on a person: {disp['blocked']}")
    print(f"  accounted for:       {accounted} of {r['count']}")
    print()
    if accounted < r["count"]:
        print("=" * 78)
        print("BATCH GATE: NOT DONE.")
        print(f"{r['count'] - accounted} finding(s) are in none of the four states and are not blocked")
        print("on a named person. Uploading now spends a full AutoQC round to be told things you")
        print("already know. Go back and finish them.")
        print("=" * 78)
        sys.exit(1)
    if disp["blocked"]:
        print(f"{disp['blocked']} finding(s) blocked on someone. Name them in the revision comment so")
        print("the next reviewer knows it was a decision, not an oversight.")
    print("Full batch. Upload it.")
    print(f"\nLog: {mf}")


def cmd_decide(args):
    if not os.path.isdir(args.world):
        print(f"ERROR: world folder not found: {args.world}")
        sys.exit(2)
    p = add_ruling(args.world, args.text, args.round)
    print(f"Recorded. Every later round reads this before triage.\n  {p}")
    for r in read_rulings(args.world):
        print(f"  {r}")


def cmd_rulings(args):
    rul = read_rulings(args.world)
    if not rul:
        print("No standing rulings recorded for this world.")
        return
    print("STANDING RULINGS, already decided. Do not re-ask these.")
    for r in rul:
        print(f"  {r}")


def cmd_status(args):
    data = load(args.world)
    if not data["rounds"]:
        print("No rounds logged yet for this world.")
        return
    print(f"World: {data['world']}")
    print(f"Rounds logged: {len(data['rounds'])}\n")
    all_classes = {}
    for r in data["rounds"]:
        disp = r.get("disposition")
        state = "closed" if disp else "OPEN"
        print(f"  Round {r['round']:>3}  {r['count']:>3} findings  "
              f"{len(r['classes']):>2} classes  {len(r.get('repeats', [])):>2} repeats  [{state}]")
        for k, info in r["classes"].items():
            all_classes.setdefault(k, {"label": info["label"], "rounds": []})["rounds"].append(r["round"])
    chronic = {k: v for k, v in all_classes.items() if len(v["rounds"]) >= 3}
    if chronic:
        print("\nCHRONIC CLASSES (3+ rounds), these are structural, not remediation misses:")
        for k, v in chronic.items():
            print(f"  - {v['label']}: rounds {', '.join(str(x) for x in v['rounds'])}")
        print("\n  See references/round-economics.md, 'A world already past 15 rounds'.")
    _, _, mf = log_paths(args.world)
    print(f"\nLog: {mf}")


def main():
    p = argparse.ArgumentParser(
        description="Cross-round memory for AutoQC remediation: which defect classes came back.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Reads the AutoQC report text you already have. Never reads or writes the world's files.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="log a new AutoQC round and report repeat classes")
    s.add_argument("world")
    s.add_argument("--round", type=int, required=True)
    s.add_argument("--findings", required=True, help="text file holding the pasted AutoQC report")
    s.add_argument("--note", default="")
    s.set_defaults(func=cmd_start)

    c = sub.add_parser("close", help="record how the round was disposed of; enforces the batch gate")
    c.add_argument("world")
    c.add_argument("--round", type=int, required=True)
    c.add_argument("--fixed", type=int, default=0)
    c.add_argument("--expanded", type=int, default=0, help="findings widened to their whole class")
    c.add_argument("--traps", type=int, default=0, help="left alone as declared traps")
    c.add_argument("--false", type=int, default=0, dest="false", help="ruled out as not real")
    c.add_argument("--blocked", type=int, default=0, help="blocked on a named person")
    c.add_argument("--note", default="")
    c.add_argument("--changed", default="", metavar="SENTENCE",
                   help="one sentence saying what you changed this round. Goes straight into the "
                        "RLS revision note.")
    c.add_argument("--dispute", action="append", default=[], metavar="SENTENCE",
                   help="one sentence per disputed finding, saying why. Repeat for each.")
    c.set_defaults(func=cmd_close)

    su = sub.add_parser("summary", help="the two things RLS needs: what changed, and any disputes")
    su.add_argument("world")
    su.add_argument("--round", type=int, default=None)
    su.set_defaults(func=cmd_summary)

    dec = sub.add_parser("decide", help="record a ruling that binds every later round")
    dec.add_argument("world")
    dec.add_argument("text", help="the ruling, in one plain sentence")
    dec.add_argument("--round", type=int, default=None)
    dec.set_defaults(func=cmd_decide)

    rl = sub.add_parser("rulings", help="print the standing rulings for a world")
    rl.add_argument("world")
    rl.set_defaults(func=cmd_rulings)

    t = sub.add_parser("status", help="print the round history for a world")
    t.add_argument("world")
    t.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
