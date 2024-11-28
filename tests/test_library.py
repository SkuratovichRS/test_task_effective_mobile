import json
import os
import unittest
import uuid

from app.constants import Status
from app.library import CommandExecutionError, Library


class TestLibrary(unittest.TestCase):
    file_name = "tests/test_library.json"

    def tearDown(self) -> None:
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        return super().tearDown()

    def test_add_book(self):
        library = Library(self.file_name)
        library.add_book("title", "author", "year")
        with open(self.file_name, "r") as f:
            data = json.load(f)
            for book_data in data.values():
                self.assertEqual(book_data["title"], "title")
                self.assertEqual(book_data["author"], "author")
                self.assertEqual(book_data["year"], "year")
                self.assertEqual(book_data["status"], Status.AVAILABLE)

        with self.assertRaises(CommandExecutionError):
            library.add_book("title", "author", "year")

    def test_delete_book(self):
        library = Library(self.file_name)
        book_1_id = str(uuid.uuid4())
        book_2_id = str(uuid.uuid4())
        with open(self.file_name, "w") as f:
            json.dump(
                {
                    book_1_id: {"title": "title", "author": "author", "year": "123", "status": Status.AVAILABLE},
                    book_2_id: {"title": "title2", "author": "author2", "year": "123", "status": Status.AVAILABLE},
                },
                f,
            )

        library.del_book(book_1_id)
        with open(self.file_name, "r") as f:
            data = json.load(f)
            self.assertEqual(
                data, {book_2_id: {"title": "title2", "author": "author2", "year": "123", "status": Status.AVAILABLE}}
            )

        with self.assertRaises(CommandExecutionError):
            library.del_book(book_1_id)

    def test_find_book(self):
        library = Library(self.file_name)
        book_1_id = str(uuid.uuid4())
        book_2_id = str(uuid.uuid4())
        with open(self.file_name, "w") as f:
            json.dump(
                {
                    book_1_id: {"title": "title", "author": "author", "year": "123", "status": Status.AVAILABLE},
                    book_2_id: {"title": "title2", "author": "author2", "year": "123", "status": Status.AVAILABLE},
                },
                f,
            )

        result = library.find_book("title2", "author2", "123")
        self.assertEqual(
            result, {book_2_id: {"title": "title2", "author": "author2", "year": "123", "status": Status.AVAILABLE}}
        )

        with self.assertRaises(CommandExecutionError):
            library.find_book("title", "author", "year")

    def test_show_all_books(self):
        library = Library(self.file_name)
        book_1_id = str(uuid.uuid4())
        book_2_id = str(uuid.uuid4())
        with open(self.file_name, "w") as f:
            json.dump(
                {
                    book_1_id: {"title": "title", "author": "author", "year": "123", "status": Status.AVAILABLE},
                    book_2_id: {"title": "title2", "author": "author2", "year": "123", "status": Status.AVAILABLE},
                },
                f,
            )

        result = library.show_all_books()

        with open(self.file_name, "r") as f:
            data = json.load(f)

        self.assertEqual(result, data)

    def test_change_book_status(self):
        library = Library(self.file_name)
        book_id = str(uuid.uuid4())
        with open(self.file_name, "w") as f:
            json.dump(
                {
                    book_id: {"title": "title", "author": "author", "year": "123", "status": Status.AVAILABLE},
                },
                f,
            )

        library.change_book_status(book_id, Status.NOT_AVAILABLE)
        with open(self.file_name, "r") as f:
            data = json.load(f)
        self.assertEqual(data[book_id]["status"], Status.NOT_AVAILABLE)

        with self.assertRaises(CommandExecutionError):
            library.change_book_status("123", Status.NOT_AVAILABLE)


if __name__ == "__main__":
    unittest.main()
