import unittest
from pathlib import Path

from main import App


class TestCliFlow(unittest.TestCase):
    """End-to-end smoke test through the App object directly (no subprocess)."""

    def setUp(self):
        self.app = App()
        self.app.auth.users_file = "tests/_tmp_cli_users.json"
        self.app.tenders._file_path = "tests/_tmp_cli_tenders.json"

    def tearDown(self):
        for f in (self.app.auth.users_file, self.app.tenders._file_path):
            p = Path(f)
            if p.exists():
                p.unlink()

    def test_full_flow(self):
        # register + login directly through AuthManager, since register()/login()
        # on App use input() prompts meant for the interactive menu
        user = self.app.auth.register("Ada", "ada@test.com", "secret", role="admin")
        self.assertEqual(user.role, "admin")

        logged_in = self.app.auth.login("ada@test.com", "secret")
        self.assertIsNotNone(logged_in)
        self.app.current_user = logged_in

        
        from models.tender import Tender
        tender = Tender(
            title="Road works",
            description="desc",
            deadline="2026-01-01",
            budget=500000,
            created_by=self.app.current_user.email,
        )
        self.app.tenders.add(tender)
        self.assertEqual(len(self.app.tenders.all()), 1)

        
        saved_tender = self.app.tenders.find_by_id(tender.id)
        saved_tender.close()
        self.app.tenders.update(saved_tender)
        self.assertEqual(self.app.tenders.find_by_id(tender.id).status, "closed")


if __name__ == "__main__":
    unittest.main()