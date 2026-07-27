"""Instance/token guardrail.

Refuse to run against Canvas when the environment's ``CANVAS_API_URL`` does not
match the selected profile's ``instance.base_url``. This catches the silent 401
(or wrong-course) failure that happens when a token and URL for one Canvas
instance (for example De Anza) are pointed at another institution's profile
(for example CTI).

The check is a no-op when the two agree, so the existing CTI production path is
unchanged. It is also a no-op when the manifest has no ``instance.base_url`` or
when no environment URL is set (``CanvasClient.from_env`` raises its own clear
error in that case).
"""

from __future__ import annotations

import os
from urllib.parse import urlparse

ENV_CANVAS_API_URL = "CANVAS_API_URL"


class InstanceMismatchError(ValueError):
    """Raised when CANVAS_API_URL does not match the selected instance.base_url.

    Subclasses ``ValueError`` so existing callers that already translate
    ``ValueError`` into a validation-style failure keep working unchanged.
    """


class InstanceDisabledError(ValueError):
    """Raised when the selected profile is a scaffold with instance.enabled false."""


class PlaceholderCourseIdError(ValueError):
    """Raised when the selected profile still carries the scaffold course id."""


SENTINEL_COURSE_ID = 999999999


def check_course_id_is_real(
    manifest: dict, *, manifest_label: str = "the selected profile"
) -> None:
    """Refuse Canvas runs against the scaffold placeholder course id.

    Independent of ``instance.enabled``: flipping a scaffold to enabled
    without replacing the placeholder course id must still refuse.
    """
    instance = manifest.get("instance") or {}
    if instance.get("course_id") == SENTINEL_COURSE_ID:
        raise PlaceholderCourseIdError(
            f"Refusing to run against Canvas: {manifest_label} still uses the "
            f"scaffold placeholder course_id {SENTINEL_COURSE_ID}. Replace it "
            "with the real Canvas course ID (see the manifest's _setup_note "
            "and docs/CLOUD_SETUP.md) before any Canvas run."
        )


def check_instance_ready(
    manifest: dict, *, manifest_label: str = "the selected profile"
) -> None:
    """All manifest-level readiness guards for a Canvas run."""
    check_instance_enabled(manifest, manifest_label=manifest_label)
    check_course_id_is_real(manifest, manifest_label=manifest_label)


def check_instance_enabled(
    manifest: dict, *, manifest_label: str = "the selected profile"
) -> None:
    """Refuse Canvas runs against an unfinished scaffold profile.

    A manifest may mark its instance block with ``"enabled": false`` while the
    profile is still a scaffold (placeholder course id, no hosted config).
    Every Canvas-touching entry point calls this before building a client, so
    a scaffold can never be hit by accident. An absent flag means enabled, so
    existing production manifests behave exactly as before.
    """
    instance = manifest.get("instance") or {}
    if instance.get("enabled") is False:
        name = instance.get("name") or "this instance"
        raise InstanceDisabledError(
            f"Refusing to run against Canvas: {manifest_label} ({name!r}) is a "
            "scaffold profile with instance.enabled set to false. Finish the "
            "profile first (see the manifest's _setup_note and "
            "docs/CLOUD_SETUP.md), then set instance.enabled to true."
        )


def _host(url: str) -> str:
    """Normalize a Canvas URL to a bare, lowercase host for comparison.

    Ignores scheme, trailing slashes, any path, and case, so
    ``https://deanza.instructure.com`` and ``https://deanza.instructure.com/``
    compare equal.
    """
    parsed = urlparse(url.strip())
    host = parsed.netloc or parsed.path
    return host.strip("/").split("/")[0].lower()


def instance_base_url(manifest: dict) -> str | None:
    """Return the selected profile's ``instance.base_url``, or ``None``."""
    return (manifest.get("instance") or {}).get("base_url")


def check_env_matches_instance(
    manifest: dict,
    env_url: str | None = None,
    *,
    manifest_label: str = "the selected profile",
) -> None:
    """Guard against running against the wrong Canvas instance.

    Raises :class:`InstanceMismatchError` when the environment's
    ``CANVAS_API_URL`` and the manifest's ``instance.base_url`` point at
    different Canvas hosts. Returns ``None`` (no-op) when they match, when the
    manifest has no ``instance.base_url``, or when no environment URL is set.

    ``env_url`` defaults to ``os.environ["CANVAS_API_URL"]`` when not provided,
    which is the value ``CanvasClient.from_env`` uses.
    """
    base_url = instance_base_url(manifest)
    if not base_url:
        return
    if env_url is None:
        env_url = os.environ.get(ENV_CANVAS_API_URL)
    if not env_url:
        return
    if _host(base_url) == _host(env_url):
        return
    raise InstanceMismatchError(
        f"Refusing to run against Canvas: {ENV_CANVAS_API_URL} ({env_url!r}) "
        f"does not match instance.base_url ({base_url!r}) in {manifest_label}. "
        "This usually means a token and URL for one institution are pointed at "
        f"another institution's profile. Set {ENV_CANVAS_API_URL} to "
        f"{base_url!r}, or select the matching profile."
    )
