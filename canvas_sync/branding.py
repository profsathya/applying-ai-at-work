"""Shared partner-brand markup for generated hosted course pages."""

from __future__ import annotations

import html


def partner_brand_row(
    cti_logo_url: str,
    deanza_logo_url: str,
    *,
    decorative: bool = False,
    cti_fallback: bool = False,
) -> str:
    """Render the paired CTI and De Anza logo row used by Course 1 pages."""
    cti_alt = "" if decorative else "Computing Talent Initiative"
    deanza_alt = "" if decorative else "De Anza College"
    cti_error = "this.style.display='none'"
    cti_markup = (
        f'<span class="cti-mark">'
        f'<img class="brand-logo cti-logo" src="{html.escape(cti_logo_url, quote=True)}" '
        f'alt="{cti_alt}" onerror="{cti_error};this.nextElementSibling.style.display=\'block\';">'
        '<span class="cti-logo-fallback">Computing Talent<br>Initiative</span>'
        '</span>'
        if cti_fallback
        else (
            f'<img class="brand-logo cti-logo" src="{html.escape(cti_logo_url, quote=True)}" '
            f'alt="{cti_alt}" onerror="{cti_error}">'
        )
    )
    deanza_markup = (
        f'<img class="brand-logo deanza-logo" src="{html.escape(deanza_logo_url, quote=True)}" '
        f'alt="{deanza_alt}" onerror="this.style.display=\'none\'">'
    )
    return (
        '<div class="brand-row" aria-label="Course partners">'
        f'{cti_markup}'
        '<span class="brand-divider" aria-hidden="true"></span>'
        f'{deanza_markup}'
        '</div>'
    )
