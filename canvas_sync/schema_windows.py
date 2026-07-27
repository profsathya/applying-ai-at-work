"""
Windows-compatible entry point for the repository schema validator.

This delegates all validation work to canvas_sync.schema. The compatibility
shim exists because homepage validation imports canvas_sync.state, whose
Unix-only fcntl dependency is used for state-file writes, not validation.

Usage matches schema.py:
  python canvas_sync/schema_windows.py --homepage course1/homepage.yaml
  python canvas_sync/schema_windows.py --all
"""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _install_validation_only_fcntl_shim() -> None:
    """Allow read-only validation imports on Windows."""
    if os.name != "nt" or "fcntl" in sys.modules:
        return

    fcntl = types.ModuleType("fcntl")
    fcntl.LOCK_EX = 2
    fcntl.LOCK_UN = 8

    def flock(_file, _operation) -> None:
        raise RuntimeError(
            "The Windows validator cannot perform Unix file locking. "
            "Use it only for read-only schema validation."
        )

    fcntl.flock = flock
    sys.modules["fcntl"] = fcntl


_install_validation_only_fcntl_shim()

from canvas_sync.schema import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main())
