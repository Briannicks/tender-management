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
        class Args:
            pass

        reg = Args()
        reg.name, reg.email, reg.password, reg.role = "Ada", "ada@test.com", "secret", "admin"
        self.app.cmd_register(reg)

        login = Args()
        login.email, login.password = "ada@test.com", "secret"
        self.app.cmd_login(login)
        self.assertIsNotNone(self.app.current_user)

        add = Args()
        add.title, add.description, add.deadline, add.budget = "Road works", "desc", "2026-01-01", 500000
        self.app.cmd_add_tender(add)
        self.assertEqual(len(self.app.tenders.all()), 1)

        close = Args()
        close.tender_id = 1
        self.app.cmd_close_tender(close)
        self.assertEqual(self.app.tenders.find_by_id(1).status, "closed")


if __name__ == "__main__":
    unittest.main()