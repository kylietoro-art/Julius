# Assets

## `verification_bench.html`, the Verification Bench

Double-click it. It opens in your browser. **Chrome or Edge**, because it reads a folder you choose
using the File System Access API, which Safari and Firefox don't have.

It makes no network requests, loads no libraries, and sends nothing anywhere. Every file it reads
stays on your machine. Full instructions are in `verification_bench_README.txt`.

## What it covers: both the spec and the files

The bench is a viewer and a checker, not a QC skill. It does not replace the skills that own each
side. Here is the split:

| Thing you want | Use |
|---|---|
| Decide whether a spec is good enough to build (Gate A) | `world-spec-qc` skill |
| Find defects in a built corpus | `world-qc` skill, or AutoQC |
| Fix defects in a built corpus | `world-qc-remediation`, this skill |
| Read any file in the corpus without unzipping or converting it | bench, **Open** |
| Check whether an AutoQC finding is actually true | bench, **Paste findings** |
| See whether the spec's own internal references hold together | bench, **Check the spec** |
| See what an artifact must match, and who depends on it | bench, **Trace** |

## Where it fits in remediation

Two of its features do work this skill would otherwise pay tokens for. Both happen in **Phase 0,
before anything is edited**:

1. **Paste findings.** Paste the raw AutoQC report in. It splits it into findings, pulls out the
   filenames, A## IDs, quoted strings and page-count claims, and maps each finding to the real files in
   your folder. It then verifies **two specific kinds of claim** against the file's actual extracted
   text: whether a string AutoQC put in quotes really appears in that file (it reads PDF text and
   unzips xlsx/docx/pptx XML, so it sees where grep can't), and whether a stated page count matches.
   **That is the whole of it.** It catches AutoQC quoting text that isn't there and miscounting pages.
   It cannot tell you whether a footing, date or consistency claim is true. Use it as a cheap first
   filter on the mechanical half of a finding, not as a verdict on the finding.

2. **Check the spec.** Audits the World Spec against itself: artifacts that don't resolve to a real
   file, two artifacts claiming the same file, a canonical value that is its own corroborator, a task
   citing evidence that doesn't exist. **Here this is a diagnostic, not a gate.** You are answering
   one question: is the reason this world keeps failing upstream of the files I can edit? If the
   spec's own references don't hold, no amount of file fixing ends the loop, and it goes to the world
   lead with the failing rows attached. Gate A spec review stays with `world-spec-qc`.

Then in **Phase 4**, re-paste the same findings. Everything you fixed should now fail to match.

**Trace** is also the fastest way to scope a blast radius by hand: it shows the canonical values an
artifact must match, the tasks that depend on it, and the other artifacts it has to agree with. That
is the dependency set you need to bring into line in one pass.

The bench is optional in the sense that every command in this skill runs without it. It is not
optional in the sense that skipping it means paying tokens for a check that is free.
