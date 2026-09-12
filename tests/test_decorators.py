import unittest

from utils.decorators import admin_required, login_required


class FakeUser:
    def __init__(self, role):
        self.role = role


class FakeApp:
    def __init__(self, current_user=None):
        self.current_user = current_user

    @login_required
    def protected_action(self):
        return "ok"

    @admin_required
    def admin_action(self):
        return "ok"


class TestDecorators(unittest.TestCase):
    def test_login_required_blocks_when_logged_out(self):
        app = FakeApp(current_user=None)
        self.assertIsNone(app.protected_action())

    def test_login_required_allows_when_logged_in(self):
        app = FakeApp(current_user=FakeUser("user"))
        self.assertEqual(app.protected_action(), "ok")

    def test_admin_required_blocks_regular_user(self):
        app = FakeApp(current_user=FakeUser("user"))
        self.assertIsNone(app.admin_action())

    def test_admin_required_allows_admin(self):
        app = FakeApp(current_user=FakeUser("admin"))
        self.assertEqual(app.admin_action(), "ok")


if __name__ == "__main__":
    unittest.main()