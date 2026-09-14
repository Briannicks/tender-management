import unittest
from pathlib import Path

from utils.auth import AuthManager


class TestAuthManager(unittest.TestCase):
    def setUp(self):
        self.users_file = "tests/_tmp_users.json"
        self.auth = AuthManager(users_file=self.users_file)

    def tearDown(self):
        p = Path(self.users_file)
        if p.exists():
            p.unlink()

    def test_register_and_login(self):
        self.auth.register("Ada", "ada@test.com", "secret", role="admin")
        user = self.auth.login("ada@test.com", "secret")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "admin")

    def test_duplicate_email_rejected(self):
        self.auth.register("Ada", "ada@test.com", "secret")
        with self.assertRaises(ValueError):
            self.auth.register("Ada2", "ada@test.com", "secret2")

    def test_wrong_password_returns_none(self):
        self.auth.register("Ada", "ada@test.com", "secret")
        self.assertIsNone(self.auth.login("ada@test.com", "wrong"))


if __name__ == "__main__":
    unittest.main()