# Cloud And Multi-Institution Setup

This repo supports two setup paths and more than one Canvas instance (one per
institution). Everything here is additive: the existing local install and the
current CTI production flow behave exactly as before.

- Path A: Local install (unchanged) - run the tools on your own machine.
- Path B: Open in GitHub Codespaces - a ready-to-use cloud environment in the
  browser, with no local install.

Multi-institution support means each institution (CTI, De Anza, ...) has its
own Canvas instance profile (a manifest) and its own Canvas token. You pick the
profile when you run.

## Path A: Local install (unchanged)

Follow `README.md` -> "One-Time Setup". In short: create a virtualenv, install
`canvas_sync/requirements.txt`, install your AI CLI, and copy `.env.example` to
`.env` with your Canvas credentials. Nothing about that path changed.

## Path B: Open in GitHub Codespaces (cloud)

A Codespace is a container built from `.devcontainer/devcontainer.json`. It
gives you Python 3.11, Node, the Canvas sync dependencies, and both AI CLIs
without any local install.

### 1. Open the Codespace in the browser

- On GitHub, open this repository.
- Click the green "Code" button, choose the "Codespaces" tab, and create a
  Codespace on your branch. It also opens from the web editor and the
  "Open in Codespaces" flow.
- The first launch runs the container's on-create step automatically:
  - `python -m pip install -r canvas_sync/requirements.txt`
  - `npm i -g @anthropic-ai/claude-code @openai/codex`
  You do not run these by hand.

### 2. Add your own Canvas credentials as Codespaces secrets

Credentials are never hardcoded in the repo. Codespaces injects them as
environment variables from your own account secrets:

- Go to GitHub -> your avatar -> Settings -> Codespaces -> Secrets.
- Add two secrets and scope both to this repository:
  - `CANVAS_API_URL`   for example `https://deanza.instructure.com`
  - `CANVAS_API_TOKEN` a personal access token for that same Canvas instance
    (Canvas -> Account -> Settings -> New Access Token).
- Rebuild or reopen the Codespace so the secrets are present. Confirm with:

  ```bash
  echo "$CANVAS_API_URL"     # your institution's Canvas URL
  # CANVAS_API_TOKEN is set too; do not echo it.
  ```

Each institution's instructor supplies their OWN url and token for their OWN
Canvas instance. Your secrets are private to your account and your Codespaces.

### 3. Sign in to your AI tool once

Sign in with your own account:

```bash
claude        # Claude Code
# or
codex         # Codex
```

### 4. How your login persists

`.devcontainer/devcontainer.json` mounts `~/.claude` and `~/.codex` as named
Docker volumes. Those directories hold each tool's config and credentials, so
your login survives a container REBUILD, not just stop/start. You sign in once
and stay signed in across rebuilds. The volumes are per user and per Codespace;
they are not shared and are never committed.

## Select an institution profile when you run (the instance selector)

Each institution is a separate manifest under `course1/manifests/`:

| Institution | Profile (manifest)                  | Canvas instance                |
|-------------|-------------------------------------|--------------------------------|
| CTI         | `course1/manifests/production.json` | `cti-courses.instructure.com`  |
| De Anza     | `course1/manifests/deanza.json`     | `deanza.instructure.com`       |

The manifest is the instance selector. Choose a profile by passing it as
`--manifest` to the deterministic scripts, for example:

```bash
# Read-only inventory of the selected instance
python canvas_sync/inspect_canvas.py \
  --manifest course1/manifests/deanza.json \
  --include-items --write-ledger --format markdown
```

When you drive the tools through Codex or Claude Code, name the profile you
want ("use the De Anza profile") and the assistant passes the matching
`--manifest`.

Guardrail: the tools refuse to run against Canvas when your environment's
`CANVAS_API_URL` does not match the selected profile's `instance.base_url`. This
stops the silent failure where a token and URL for one institution are pointed
at another institution's profile. Set `CANVAS_API_URL` to match the profile you
selected.

## Finish the De Anza profile

`course1/manifests/deanza.json` is a scaffold. Its `instance.course_id` is a
clearly-marked placeholder, and it has no per-item Canvas IDs yet. To finish it
(no IDs are invented by hand):

1. Get a De Anza Canvas personal access token and the De Anza Canvas course ID
   for this course (the number in the course URL,
   `https://deanza.instructure.com/courses/<id>`).
2. Replace the placeholder `instance.course_id` in
   `course1/manifests/deanza.json` with the real De Anza course ID, and remove
   the `_setup_note`.
3. Add a `hosted_html` block to `course1/manifests/deanza.json` with its OWN
   `path_prefix`, distinct from the CTI course (which uses `path_prefix:
   deanza`), so De Anza hosted output does not collide. course1 has hosted
   AI-activity artifacts (`delivery_mode: ai_activity`) that require
   `hosted_html.enabled`; publishing course1 through this profile will fail
   before any Canvas call until this block is set. Copy the shape from
   `course1/manifests/production.json` and set your own De Anza hosted
   `base_url`, `path_prefix`, and `progress_endpoint`.
4. Set your Codespaces secrets (or local `.env`) so `CANVAS_API_URL` is
   `https://deanza.instructure.com` and `CANVAS_API_TOKEN` is your De Anza
   token.
5. Validate: `python canvas_sync/schema.py --manifest course1/manifests/deanza.json`.
6. Run the repo's normal bootstrap / inspect / publish flow against the De Anza
   profile to populate the per-item Canvas IDs. Inspect first (read-only), then
   publish only after review and explicit approval. See `README.md` and
   `README-BUILDER.md` for the publish flow.

Do not fabricate Canvas IDs and do not point a De Anza token at the CTI profile
(the guardrail will refuse that anyway).

## Safety notes

- Markdown is the source of truth. Canvas IDs live in deployment state, not in
  artifact frontmatter.
- No Canvas writes happen without explicit approval. Draft and validate first.
- Schema validation is a hard gate before any Canvas push:
  `python canvas_sync/schema.py --all`.
