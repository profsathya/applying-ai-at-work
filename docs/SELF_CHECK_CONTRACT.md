# Self-check reconciliation and implementation boundary

PR213's guide is the authority for the rules and the settled First frames example. The normalized records in `course1/design/self-check-records/` are the shared input to `canvas_sync/self_check.py`. They preserve author wording and exact points; null means unresolved, never zero or permission to round a percentage. No deployment IDs belong in these records.

The JSON `version` identifies the contract version. Scoring results also carry a SHA-256 of the entire canonical record, so a result cannot silently survive a content revision. Record IDs and criterion IDs are stable lookup keys. Full, `3`, and `1` are labels; the stored points are the only numeric lookup.

| Record | Full / partial / minimal totals | Remaining author decisions |
| --- | --- | --- |
| First frames | 50 / 36 / 11 | Numeric grade on gate failure; first-batch rung review |
| Problem Frame | 50 / unresolved / unresolved | Exact partial/minimal points; unique ranks |
| Three Sprint 2 records | 50 / unresolved / unresolved | Exact partial/minimal points; unique ranks; applicable gates |
| Stakeholder Map | 50 / 35 / 9 | Unique ranks and tags; full-line counts and compound tests; set thresholds |
| Stakeholder Conversation | 50 / 35 / 11 | Unique ranks and tags; applicable gate; wording and set thresholds |

The Sprint 3 blank-row zero rule is superseded by the guide: blank receives the criterion's minimal rung points. The Conversation principles' copied 66/24/10 split is corrected to its actual 10/18/20/14/18/20 split. Eight and ten criteria are allowed, so neither rubric is collapsed or reweighted. Existing Sprint 1 Problem Frame and Sprint 2 tied priorities are not converted into an invented order. Their prose records remain drafts.

The guide's worked First frames example replaces the older five-line table with six criteria and exact ranks. The earlier Sprint 1 shape and open questions are historical wherever the guide settles them. Sprint 3's older quick-check-only presentation principles are likewise superseded. Author review must still reconcile other full-line wording to the actual prompts before rollout.

## Rendering and validation

Opt in a walkthrough with this field under `guided_assignment`:

```yaml
self_check_record: course1/design/self-check-records/first-frames.json
```

The existing walkthrough renderer then places an always-visible Self-check before submission controls, replacing `final_check` with the record's full-credit lines and points. Rungs, tags, ranks, gate internals, and open questions never enter the HTML or browser payload. Existing per-task guidance is unchanged. No course artifact is opted in by this PR: rollout needs the normal source/Canvas drift review and content-owner checks. Standard/native pages still need their own integration; this change does not pretend to support them. Checkbox persistence and checked-state export from item 39 are also not implemented.

`schema.py --all` validates normalized records even if no artifact references them. Artifact validation additionally checks reference syntax, total points, and walkthrough presentation. Draft validation permits explicit null ranks/tags/rung points. `validate_record(..., grading=True)` requires exact rung points, allowed tags and a permutation of ranks 1 through N. `score_rungs` also blocks an unresolved gate rule; authors can explicitly state that no gate applies when that is their decision. Gate failure grade must remain null until a policy is implemented. `score_rungs` refuses incomplete records and requires exactly one allowed rung per criterion. It performs deterministic lookup only, not evidence interpretation or AI grading.

A failed gate returns the raw sum separately, `passes: false`, and `numeric_grade: null`. An unreviewed gate returns no pass decision or numeric grade. A passed gate permits the summed grade, but every result still requires human review. There is deliberately no assumed zero, 34-point cap, 35-point floor, or late-penalty policy. The team must specify those policies, including absent submissions versus blank parts, before any posting adapter is enabled. `gate.failure_grade: null` documents that unresolved decision; the scorer never uses it to invent a rule.

## Grading implementation boundary

Common-Curriculum `scripts/submission-analyzer.js` at main `e1c273d0d623e0e0ad5e58db2c0b09e279d006e2` uses a holistic grading prompt. Supplying this record as text does not turn its full/80/60/0 guidance into a per-criterion contract. Course-wide-list item 46 already identifies that mismatch. This PR changes neither that analyzer nor its configuration and makes no claim that it consumes these records.

The separate private JeremyCSUMB/canvas-grading-bridge baseline supplied for coordination is `db28249617a3fa0de5f89405239f35e1f066bd77`. That worker owns instructor-local deidentification, anonymous submission bundles, returned score bundles, local recoupling and review, and separately confirmed Canvas posting. It should carry record ID, contract version, record hash, criterion IDs, and result IDs through the anonymous exchange; mappings and credentials stay instructor-local. Per-criterion evidence references, rank-selected feedback, gate evidence and result-bundle validation belong in that adapter. This module is only the rubric lookup/rendering boundary, not a drop-in bridge or a posting authorization. Only synthetic tests were used here.

## Validation

Run from the repository root with the repository virtualenv:

```sh
python -m unittest discover
python canvas_sync/schema.py --all
python canvas_sync/link_audit.py --all
python -m py_compile canvas_sync/*.py
```

The mocked publish tests expect the synthetic `CANVAS_API_URL=https://example.instructure.com/`; no live publishing is part of these checks.

The validation workflow also renders all enabled hosted manifests locally. Its path filters include self-check records and source self-check Markdown so record-only PRs receive validation. Contract tests independently compare every normalized criterion and authored rung against its source table, check internal-field exclusion and HTML escaping, and reject malformed fields and unresolved gate rules.
