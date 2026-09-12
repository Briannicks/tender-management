import hashlib


class User:
    """Base user. Admin inherits from this (role-based access)."""

    role = "user"  

    def __init__(self, name, email, password_hash):
        self._name = name
        self._email = email
        self._password_hash = password_hash

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        return self._password_hash == self.hash_password(password)

    def to_dict(self):
        return {
            "name": self._name,
            "email": self._email,
            "password_hash": self._password_hash,
            "role": self.role,
        }

    def __str__(self):
        return f"{self._name} ({self.role}) <{self._email}>"


class Admin(User):
    """Same as User, but with elevated role for admin-only actions."""

    role = "admin"