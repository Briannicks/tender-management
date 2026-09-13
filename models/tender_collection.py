from pathlib import Path

from utils.storage import load_json, save_json


class Book:
    def __init__(self, title, author, genre, status="Available", added_by=""):
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status
        self.added_by = added_by

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "status": self.status,
            "added_by": self.added_by,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["author"],
            data["genre"],
            data.get("status", "Available"),
            data.get("added_by", ""),
        )


class BookCollection:
    def __init__(self, books_file="data/books.json"):
        self.books_file = Path(books_file)

    def _load_books(self):
        return [Book.from_dict(item) for item in load_json(self.books_file)]

    def _save_books(self, books):
        save_json(self.books_file, [book.to_dict() for book in books])

    def add_book(self, book):
        books = self._load_books()
        books.append(book)
        self._save_books(books)

    def view_books(self):
        return self._load_books()

    def search_books(self, search_text):
        search_text = search_text.lower()
        return [
            book
            for book in self._load_books()
            if search_text in book.title.lower()
            or search_text in book.author.lower()
        ]

    def update_status(self, title, new_status):
        books = self._load_books()

        for book in books:
            if book.title.lower() == title.lower():
                book.status = new_status
                self._save_books(books)
                return True

        return False

    def delete_book(self, title):
        books = self._load_books()

        for book in books:
            if book.title.lower() == title.lower():
                books.remove(book)
                self._save_books(books)
                return True

        return False
