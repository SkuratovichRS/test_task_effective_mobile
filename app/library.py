import json
import os
import uuid

from app.constants import Status


class CommandExecutionError(Exception):
    pass


class Library:
    def __init__(self, filename: str):
        self._filename = filename
        self._init_db()

    def add_book(self, title: str, author: str, year: str) -> dict:
        """Добавление книги в базу данных"""

        new_book_id = str(uuid.uuid4())
        new_book_data = {"title": title, "author": author, "year": year, "status": Status.AVAILABLE}

        data = self._read_data()

        for book_data in data.values():
            if book_data["title"] == title and book_data["author"] == author and book_data["year"] == year:
                raise CommandExecutionError("Книга уже есть в библиотеке")

        data[new_book_id] = new_book_data

        self._dump_data(data)

        return new_book_data

    def del_book(self, book_id: str) -> None:
        """Удаление книги из базы данных"""

        data = self._read_data()

        try:
            del data[book_id]
            self._dump_data(data)
        except KeyError:
            raise CommandExecutionError("Книга не найдена")

    def find_book(self, title: str = "", author: str = "", year: str = "") -> dict:
        """Поиск книг по заданным полям"""

        data = self._read_data()

        result = {}

        for book_id, book_data in data.items():
            title_ok = title == "" or book_data["title"] == title
            author_ok = author == "" or book_data["author"] == author
            year_ok = year == "" or book_data["year"] == year

            if title_ok and author_ok and year_ok:
                result[book_id] = book_data

        if not result:
            raise CommandExecutionError("Книга не найдена")

        return result

    def show_all_books(self) -> dict:
        """Вывод всех книг"""

        return self._read_data()

    def change_book_status(self, book_id: uuid.UUID, status: str) -> None:
        """Изменение статуса книги"""

        data = self._read_data()

        try:
            data[book_id]["status"] = status
            self._dump_data(data)
        except KeyError:
            raise CommandExecutionError("Книга не найдена")

    def _init_db(self) -> None:
        """Создание базы данных, если она не существует"""

        if not os.path.exists(self._filename):
            self._dump_data({})

    def _read_data(self) -> dict:
        with open(self._filename, "r") as f:
            return json.load(f)

    def _dump_data(self, data: dict) -> None:
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
