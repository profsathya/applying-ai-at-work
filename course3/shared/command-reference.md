# Command Reference

This is a technical appendix. The main learner workflow is Codex app or IDE, not Codex CLI.

## When To Use Commands

Use commands only when the repo requires local setup, validation, Canvas inspection, or deterministic Canvas operations. If you are non-technical, ask Codex to explain the command and expected output before running it.

## Setup Commands

Create and activate the local Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
```

Create `.env` from an example only if the example exists in your checkout:

```bash
cp .env.example .env
```

Fill `.env` with placeholders first:

```text
CANVAS_API_URL=https://example.instructure.com
CANVAS_API_TOKEN=CANVAS_API_TOKEN
DEFAULT_COURSE_ID=181
```

Do not commit `.env`.

## Validation Commands

Validate one artifact:

```bash
.venv/bin/python canvas_sync/schema.py --artifact course3/sprints/sprint-0/example.md
```

Validate all courses discovered by the repo:

```bash
.venv/bin/python canvas_sync/schema.py --all
```

Run unit tests:

```bash
.venv/bin/python -m unittest discover
```

Check whitespace and patch safety:

```bash
git diff --check
```

## Read-Only Canvas Inspection

This requires valid Canvas credentials and authorized access:

```bash
.venv/bin/python canvas_sync/inspect_canvas.py --manifest course3/manifests/production.json --include-items --write-ledger --format markdown
```

Add `--drift` only when you need a reconcile-readiness report:

```bash
.venv/bin/python canvas_sync/inspect_canvas.py --manifest course3/manifests/production.json --include-items --drift --write-ledger --format markdown
```

## Canvas Write Commands

These are risky in production. Use only after review and explicit approval.

Push one reviewed artifact:

```bash
.venv/bin/python canvas_sync/push.py --file course3/sprints/sprint-0/example.md --manifest course3/manifests/production.json
```

Reconcile dry run:

```bash
.venv/bin/python canvas_sync/pull.py --manifest course3/manifests/production.json --dry-run
```

Reconcile apply after explicit approval:

```bash
.venv/bin/python canvas_sync/pull.py --manifest course3/manifests/production.json --apply
```

Removal dry run:

```bash
.venv/bin/python canvas_sync/remove.py --manifest course3/manifests/production.json --target module_item_id:123 --dry-run
```

Removal apply after a fresh matching confirmation token:

```bash
.venv/bin/python canvas_sync/remove.py --manifest course3/manifests/production.json --target module_item_id:123 --apply --confirm-token CONFIRMATION_TOKEN
```

## To Verify

If a command is inferred from docs but not tested in your checkout, label it `to verify` in your notes. In this repo, the commands above were confirmed by script help, tests, or existing docs.
