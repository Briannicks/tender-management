from models.tender import Tender
from utils.storage import load_json, save_json


class TenderCollection:
    """Wraps all tender persistence so nothing else touches the JSON file."""

    def __init__(self, file_path="data/tenders.json"):
        self._file_path = file_path

    def add(self, tender):
        tenders = self._load_all()
        tenders.append(tender)
        self._save_all(tenders)
        return tender

    def all(self):
        return self._load_all()

    def find_by_id(self, tender_id):
        for tender in self._load_all():
            if tender.id == tender_id:
                return tender
        return None

    def filter_by_status(self, status):
        return [t for t in self._load_all() if t.status == status]

    def update(self, tender):
        tenders = self._load_all()
        for i, existing in enumerate(tenders):
            if existing.id == tender.id:
                tenders[i] = tender
                break
        self._save_all(tenders)

    def _load_all(self):
        return [Tender.from_dict(d) for d in load_json(self._file_path)]

    def _save_all(self, tenders):
        save_json(self._file_path, [t.to_dict() for t in tenders])