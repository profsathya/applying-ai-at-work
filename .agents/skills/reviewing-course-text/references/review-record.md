# Authoring Review Record

The parent workflow owns this record. A `canvas-author` worker writes exactly one artifact; `homepage-maintainer` writes only homepage YAML; other restricted workers return findings. The parent is the coordinating task, including the main task when it performs authoring directly. Do not delegate a report write to a worker whose output contract excludes it.

For substantive authoring or revision, save one concise Markdown record per reviewed scope at:

```text
<course>/reports/authoring/<YYYYMMDDTHHMMSSZ>-<descriptive-scope-slug>.md
```

Get the timestamp from a clock in UTC, for example `date -u +%Y%m%dT%H%M%SZ`. If the path exists, obtain a new timestamp or add a disambiguating suffix; never overwrite an earlier record. Keep records outside participant content. Mechanical date changes, inspection, reconcile, and sync alone do not require authoring records.

## Required contents

- **Target and status:** course, sprint/artifact or homepage scope, requested change, and whether this is a draft, revision, or recommendations-only review. State that the editorial assessment is the agent's. Record human approval only if explicitly observed, with its scope; otherwise say it was not assessed or not requested. Authorization to draft is not approval of the resulting text.
- **Sources and files reviewed:** supplied prompt or design paths, relevant source revision when available, target files and neighbors actually read, and unavailable dependencies. Distinguish read-only context from changed output.
- **Skills consulted:** actual local paths and each skill's `metadata.local_revision`. For existing workflow skills without a revision, use their file SHA-256. Include skills read by workers with attribution; do not list a skill just because it exists or is linked. Record a SHA-256 for any additional skill reference used, including this record contract, so its version is identifiable.
- **Decisions and alignment:** the intended capability and value, prior work, practice, evidence, and relevant success criteria. State assumptions, material authoring choices, and how the result preserves the supplied design.
- **Findings:** resolved issues; intentionally deferred issues with reasons; consequential missing decisions for the human. Use "none found in this scope" rather than imply exhaustive certainty.
- **Observed validation:** exact commands/checks, scope, outcomes, and failures or checks not run. Separate worker-reported checks from checks the parent observed. Schema validity does not establish teaching effectiveness. Do not claim browser or Canvas inspection from local file checks.
- **Reviewed output fingerprints:** repository-relative output path and SHA-256 for every final reviewed artifact and any changed homepage YAML or planning output. For recommendations-only review, fingerprint the unchanged target. Fingerprint read-only neighbors separately if useful, labeled as context. Do not hash the report into itself.

Use `shasum -a 256 <path>` or Python `hashlib.sha256(Path(path).read_bytes()).hexdigest()` on the actual final bytes. Compute hashes after the final edits, homepage maintenance, and validation. If substantive content changes afterward, repeat the affected review and validation and save a new record. Mechanical changes such as a due-date update keep their narrow validation and do not require a new editorial record. In either case, the older record describes its original bytes only; a changed fingerprint distinguishes the later file.

Keep the narrative proportionate. A one-page revision may need only a few sentences and two small tables. State scope, source preservation, and approval status once rather than repeating them across sections. Group passing checks while retaining enough command detail to reproduce them; preserve exact details for material failures. Do not manufacture a long checklist, numerical quality score, or a human approval requirement.
