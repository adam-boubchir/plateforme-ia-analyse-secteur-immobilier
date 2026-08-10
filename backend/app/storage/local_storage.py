from pathlib import Path
from datetime import datetime
import shutil


class LocalStorage:
    """
    Service de stockage local.
    Tous les rapports PDF seront sauvegardés dans backend/storage/reports/.
    """

    def __init__(self):
        self.base_path = Path("storage/reports")
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_report(self, source_file: str) -> str:
        """
        Copie un PDF généré vers le dossier storage/reports
        et retourne son chemin.
        """

        source = Path(source_file)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        destination = self.base_path / f"report_{timestamp}.pdf"

        shutil.copy(source, destination)

        return str(destination)

    def list_reports(self):
        """
        Retourne la liste des rapports enregistrés.
        """

        return sorted(
            self.base_path.glob("*.pdf"),
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )

    def delete_report(self, filename: str):
        """
        Supprime un rapport.
        """

        file_path = self.base_path / filename

        if file_path.exists():
            file_path.unlink()
            return True

        return False