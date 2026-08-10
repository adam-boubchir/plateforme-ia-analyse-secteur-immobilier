from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

__all__ = (
    "StorageService",
)


class StorageService:
    """
    Storage service responsible for persisting
    generated documents.

    Responsibilities
    ----------------
    - Create storage directories.
    - Save generated PDF reports.
    - Save generated charts.
    - Save future exports (Word, Excel, PowerPoint).
    - Return browser-accessible URLs for stored files.
    """

    # ======================================================
    # INITIALIZATION
    # ======================================================

    def __init__(
        self,
        *,
        root_directory: str = "storage",
    ) -> None:

        self._root = Path(
            root_directory,
        )

        self._reports = (
            self._root / "reports"
        )

        self._charts = (
            self._root / "charts"
        )

        self._documents = (
            self._root / "documents"
        )

        self._create_directories()

    # ======================================================
    # REPORTS
    # ======================================================

    def save_report(
        self,
        source_path: str,
    ) -> str:
        """
        Save a generated PDF report.

        Returns
        -------
        str
            Browser-accessible URL of the saved report.
        """

        destination = (
            self._reports
            / f"{uuid4().hex}.pdf"
        )

        shutil.copy2(
            source_path,
            destination,
        )

        return self._build_url(
            category="reports",
            filename=destination.name,
        )

    # ======================================================
    # CHARTS
    # ======================================================

    def save_chart(
        self,
        source_path: str,
    ) -> str:
        """
        Save a generated chart.

        Returns
        -------
        str
            Browser-accessible URL of the saved chart.
        """

        extension = Path(
            source_path,
        ).suffix

        destination = (
            self._charts
            / f"{uuid4().hex}{extension}"
        )

        shutil.copy2(
            source_path,
            destination,
        )

        return self._build_url(
            category="charts",
            filename=destination.name,
        )

    # ======================================================
    # DOCUMENTS
    # ======================================================

    def save_document(
        self,
        source_path: str,
    ) -> str:
        """
        Save a generic document.

        Returns
        -------
        str
            Browser-accessible URL of the saved document.
        """

        extension = Path(
            source_path,
        ).suffix

        destination = (
            self._documents
            / f"{uuid4().hex}{extension}"
        )

        shutil.copy2(
            source_path,
            destination,
        )

        return self._build_url(
            category="documents",
            filename=destination.name,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        path: str,
    ) -> None:
        """
        Delete a stored file.

        Accepts either:
            - an absolute filesystem path
            - a relative filesystem path
        """

        file = Path(
            path,
        )

        if file.exists():
            file.unlink()

    # ======================================================
    # PRIVATE
    # ======================================================

    @staticmethod
    def _build_url(
        *,
        category: str,
        filename: str,
    ) -> str:
        """
        Build the public URL used by the frontend.
        """

        return (
            f"/storage/{category}/{filename}"
        )

    def _create_directories(
        self,
    ) -> None:
        """
        Create all required storage directories.
        """

        self._root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._reports.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._charts.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._documents.mkdir(
            parents=True,
            exist_ok=True,
        )