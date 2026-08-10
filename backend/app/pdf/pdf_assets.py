from __future__ import annotations

from pathlib import Path

__all__ = (
    "PDFAssets",
)


class PDFAssets:
    """
    Centralized location of all assets used
    by the PDF engine.
    """

    ROOT = Path(__file__).resolve().parents[2]

    ASSETS = ROOT / "assets"

    # =====================================================
    # LOGOS
    # =====================================================

    MINISTRY_LOGO = (
        ASSETS / "ministry_logo.png"
    )

    HABITAT_AI_LOGO = (
        ASSETS / "habitat_ai_logo.png"
    )

    # =====================================================
    # HEADER
    # =====================================================

    MINISTRY_HEADER = (
        ASSETS / "ministry_header.png"
    )

    # =====================================================
    # FOOTER
    # =====================================================

    MINISTRY_FOOTER = (
        ASSETS / "ministry_footer.png"
    )

    # =====================================================
    # FONTS
    # =====================================================

    FONTS = (
        ASSETS / "fonts"
    )