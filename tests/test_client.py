import unittest
from unittest.mock import MagicMock, patch

from app.client import Client
from app.constants import Status
from app.library import CommandExecutionError, Library


class TestClient(unittest.TestCase):
    def setUp(self):
        self.library_mock = MagicMock(spec=Library)
        self.client = Client(self.library_mock)

    @patch("builtins.input", side_effect=["title", "author", "123"])
    @patch("builtins.print")
    def test_add_book(self, mock_print, mock_input):
        self.client._add()
        self.library_mock.add_book.assert_called_once_with("title", "author", "123")
        mock_print.assert_called_once_with("Книга успешно добавлена")

    @patch("builtins.input", side_effect=["title", "author", "invalid_year"])
    @patch("builtins.print")
    def test_add_book_invalid_year(self, mock_print, mock_input):
        self.client._add()
        self.library_mock.add_book.assert_not_called()
        mock_print.assert_called_once_with("Год издания должен быть числом")

    @patch("builtins.input", side_effect=["1234"])
    @patch("builtins.print")
    def test_delete_book(self, mock_print, mock_input):
        self.client._delete()
        self.library_mock.del_book.assert_called_once_with("1234")
        mock_print.assert_called_once_with("Книга успешно удалена")

    @patch("builtins.input", side_effect=["title", "author", "123"])
    def test_find_book(self, mock_input):
        self.library_mock.find_book.return_value = {"book_id": {"title": "title", "author": "author", "year": "123"}}
        self.client._find()
        self.library_mock.find_book.assert_called_once_with("title", "author", "123")

    def test_show_all_books(self):
        self.library_mock.show_all_books.return_value = {
            "book_id": {"title": "title", "author": "author", "year": "123"}
        }
        self.client._show_all()
        self.library_mock.show_all_books.assert_called_once()

    @patch("builtins.input", side_effect=["1234", "0"])
    @patch("builtins.print")
    def test_change_status(self, mock_print, mock_input):
        self.client._change_status()
        self.library_mock.change_book_status.assert_called_once_with("1234", Status.AVAILABLE)
        mock_print.assert_called_once_with("Статус успешно изменен")

    @patch("builtins.input", side_effect=["1234", "invalid"])
    @patch("builtins.print")
    def test_change_status_invalid(self, mock_print, mock_input):
        self.client._change_status()
        self.library_mock.change_book_status.assert_not_called()
        mock_print.assert_called_once_with("Некорректный статус")

    @patch("builtins.input", side_effect=["1234", "0"])
    @patch("builtins.print")
    def test_change_status_non_existent_book(self, mock_print, mock_input):
        self.library_mock.change_book_status.side_effect = CommandExecutionError("Книга не найдена")
        with self.assertRaises(CommandExecutionError):
            self.client._change_status()


if __name__ == "__main__":
    unittest.main()
