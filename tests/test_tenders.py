import unittest
from pathlib import Path

from models.tender import Tender
from models.tender_collection import TenderCollection


class TestTenderModel(unittest.TestCase):
    def test_status_validation(self):
        t = Tender("Road works", "Repave main road", "2026-01-01", 500000, "admin@test.com")
        t.close()
        self.assertEqual(t.status, "closed")
        with self.assertRaises(ValueError):
            t.status = "not-a-status"

    def test_to_from_dict_roundtrip(self):
        t = Tender("Road works", "Repave main road", "2026-01-01", 500000, "admin@test.com")
        data = t.to_dict()
        t2 = Tender.from_dict(data)
        self.assertEqual(t.id, t2.id)
        self.assertEqual(t.title, t2.title)


class TestTenderCollection(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/_tmp_tenders.json"
        self.collection = TenderCollection(file_path=self.file_path)

    def tearDown(self):
        p = Path(self.file_path)
        if p.exists():
            p.unlink()

    def test_add_and_find(self):
        t = Tender("Road works", "desc", "2026-01-01", 500000, "admin@test.com")
        self.collection.add(t)
        found = self.collection.find_by_id(t.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Road works")

    def test_filter_by_status(self):
        t1 = Tender("Road works", "desc", "2026-01-01", 500000, "admin@test.com")
        t2 = Tender("IT supply", "desc", "2026-02-01", 200000, "admin@test.com")
        t2.close()
        self.collection.add(t1)
        self.collection.add(t2)
        open_tenders = self.collection.filter_by_status("open")
        self.assertEqual(len(open_tenders), 1)
        self.assertEqual(open_tenders[0].title, "Road works")


if __name__ == "__main__":
    unittest.main()