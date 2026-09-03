#!/usr/bin/env python3
"""corpus.py, extract every file's text once and keep it.

WHY THIS EXISTS
---------------
Every scanner here re-extracts the whole corpus on every run. On a 51-file world with PDFs and decks
that is slow enough that a builder working a real world wrote their own extractor and their own JSON
cache twice in one session, and one leak scan timed out and had to be re-run against a hand-built
cache. When people route around a tool, the tool is the problem.

So: extract once, cache to disk, and reuse until a file actually changes.

The cache key is path plus mtime plus size. Any edit changes at least one of those, so a stale entry
cannot survive a fix. That matters more than speed: a scanner reading yesterday's text would clear a
file that is still broken.

WHERE IT LIVES
--------------
`<world>_qc_backup/corpus_cache.json`, beside the world like everything else this toolkit writes, so
re-zipping the world to upload can never ship it.

USAGE
-----
    import corpus
    docs = corpus.load(world)            # {relative_path: [(location, text), ...]}
    corpus.load(world, refresh=True)     # ignore the cache and re-extract

    python corpus.py build <world>       # warm the cache up front
    python corpus.py stats <world>       # what is cached, and how stale
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402
import scan_world  # noqa: E402

_common.setup_console()

CACHE = "corpus_cache.json"


def cache_path(world):
    return os.path.join(_common.default_backup_dir(world), CACHE)


def _sig(path):
    """Path signature. Any edit moves mtime or size, so a stale entry cannot survive one."""
    st = os.stat(path)
    return f"{getattr(st, 'st_mtime_ns', int(st.st_mtime * 1e9))}:{st.st_size}"   # nanoseconds: a same-length name fix inside one second must not read as unchanged


def load(world, refresh=False, quiet=True):
    """{relative_path: [(location, text), ...]} for every readable file under the world."""
    cp = cache_path(world)
    old = {}
    if not refresh and os.path.exists(cp):
        try:
            with open(cp, encoding="utf-8") as fh:
                old = json.load(fh).get("files", {})
        except (ValueError, OSError):
            old = {}

    out, fresh, reused = {}, 0, 0
    for path in scan_world.iter_files(world):
        rel = os.path.relpath(path, world).replace("\\", "/")
        try:
            sig = _sig(path)
        except OSError:
            continue
        hit = old.get(rel)
        if hit and hit.get("sig") == sig:
            out[rel] = [(c[0], c[1]) for c in hit.get("chunks", [])]
            reused += 1
            continue
        chunks = scan_world.extract_chunks(path) or []
        out[rel] = [(str(l), str(t)) for l, t in chunks if t]
        fresh += 1

    payload = {"taken": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "files": {rel: {"sig": _sig(os.path.join(world, rel)),
                               "chunks": [[l, t] for l, t in ch]}
                         for rel, ch in out.items()
                         if os.path.exists(os.path.join(world, rel))}}
    try:
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        with open(cp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh)
    except OSError as e:
        if not quiet:
            print(f"[note] could not write the corpus cache: {e}", file=sys.stderr)

    if not quiet:
        print(f"corpus: {len(out)} files, {fresh} extracted, {reused} reused from cache")
    return out


def main():
    p = argparse.ArgumentParser(description="Extract and cache the corpus text once.")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="warm the cache")
    b.add_argument("world")
    b.add_argument("--refresh", action="store_true", help="ignore any existing cache")
    s = sub.add_parser("stats", help="what is cached")
    s.add_argument("world")
    a = p.parse_args()

    if not os.path.isdir(a.world):
        print(f"ERROR: world folder not found: {a.world}")
        sys.exit(2)

    if a.cmd == "build":
        t0 = time.time()
        docs = load(a.world, refresh=a.refresh, quiet=False)
        chars = sum(len(t) for ch in docs.values() for _, t in ch)
        print(f"{chars:,} characters cached in {time.time() - t0:.1f}s")
        print(f"  {cache_path(a.world)}")
    else:
        cp = cache_path(a.world)
        if not os.path.exists(cp):
            print("No cache yet. Run: corpus.py build <world>")
            return
        with open(cp, encoding="utf-8") as fh:
            d = json.load(fh)
        files = d.get("files", {})
        stale = [rel for rel in files
                 if not os.path.exists(os.path.join(a.world, rel))
                 or files[rel].get("sig") != _sig(os.path.join(a.world, rel))]
        print(f"cached: {len(files)} files, taken {d.get('taken')}")
        print(f"stale or missing since: {len(stale)}")
        for rel in stale[:15]:
            print(f"  {rel}")


if __name__ == "__main__":
    main()
