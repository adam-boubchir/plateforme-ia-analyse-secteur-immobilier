from __future__ import annotations

from app.storage.local_storage import LocalStorage


class StorageService:
    """
    Façade utilisée par toute l'application.

    Aujourd'hui :
        -> stockage local

    Demain :
        -> Azure Blob
        -> AWS S3
        -> NAS Ministère
        -> SharePoint
    """

    def __init__(self) -> None:
        self._provider = LocalStorage()

    # =====================================================
    # REPORTS
    # =====================================================

    def save_report(
        self,
        source_file: str,
    ) -> str:
        """
        Sauvegarde un rapport PDF.

        Returns
        -------
        str
            Chemin du rapport sauvegardé.
        """

        return self._provider.save_report(
            source_file,
        )

    def list_reports(self):
        """
        Retourne les rapports disponibles.
        """

        return self._provider.list_reports()

    def delete_report(
        self,
        filename: str,
    ) -> bool:
        """
        Supprime un rapport.
        """

        return self._provider.delete_report(
            filename,
        )