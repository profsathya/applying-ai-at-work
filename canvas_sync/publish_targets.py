"""Resolve reviewed course targets for the protected publish workflow.

Shared code changes validate but do not implicitly authorize a whole-repo
course publish. Operators can dispatch a selected course after review.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


COURSE_KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def resolve_targets(
    root: Path, changed_paths: list[str], *, course: str | None = None
) -> list[str]:
    if course is not None:
        if not COURSE_KEY.fullmatch(course):
            raise ValueError("Course must be a lowercase kebab-case root directory")
        manifest = f"{course}/manifests/production.json"
        if not (root / manifest).is_file():
            raise ValueError(f"Manifest not found: {manifest}")
        return [manifest]
    targets = set()
    for changed in changed_paths:
        key, separator, rest = changed.partition("/")
        if not separator or not COURSE_KEY.fullmatch(key):
            continue
        if rest.startswith("sprints/") or rest in (
            "homepage.yaml",
            "manifests/production.json",
        ):
            manifest = f"{key}/manifests/production.json"
            if (root / manifest).is_file():
                targets.add(manifest)
    return sorted(targets)


def main() -> None:
    root = Path.cwd()
    if os.environ.get("EVENT_NAME") == "workflow_dispatch":
        targets = resolve_targets(root, [], course=os.environ.get("INPUT_COURSE", ""))
    else:
        before = os.environ.get("BEFORE_SHA", "")
        if not before or set(before) == {"0"}:
            raise ValueError(
                "No base commit for automatic target selection; dispatch a reviewed course explicitly"
            )
        result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "-z",
                before,
                os.environ["GITHUB_SHA"],
                "--",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        targets = resolve_targets(root, result.stdout.split("\0"))
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"has_targets={str(bool(targets)).lower()}\n")
        output.write("manifests<<TARGETS\n" + "\n".join(targets) + "\nTARGETS\n")
    print(
        "\n".join(targets)
        if targets
        else "No course targets. Shared changes validate only; dispatch a reviewed course to deploy them."
    )


if __name__ == "__main__":
    main()
