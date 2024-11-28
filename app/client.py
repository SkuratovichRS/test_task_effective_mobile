from pprint import pprint

from app.constants import Commands, Status
from app.library import CommandExecutionError, Library


class Client:
    def __init__(self, library: Library):
        self._library = library
        self._commands = [
            (Commands.ADD, self._add),
            (Commands.DEL, self._delete),
            (Commands.FIND, self._find),
            (Commands.SHOW_ALL, self._show_all),
            (Commands.CHANGE_STATUS, self._change_status),
            (Commands.EXIT, None),
        ]
        self._statuses = [Status.AVAILABLE, Status.NOT_AVAILABLE]

    def run(self) -> None:
        """Запускает основной цикл клиента"""

        input_string = f"Введите команду из списка ({', '.join([f"{i}-{command[0]}" for i, command in enumerate(self._commands)])}): "

        while True:
            command = input(input_string)

            try:
                command = int(command)
                executable = self._commands[command][1]

            except (ValueError, IndexError):
                print("Некорректная команда")
                continue

            try:
                if executable is None:
                    return
                executable()

            except CommandExecutionError as e:
                print(e)

    def _add(self) -> None:
        """Добавление книги в базу данных"""

        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = input("Введите год издания книги: ")
        if not self._validate_year(year):
            print("Год издания должен быть числом")
            return
        self._library.add_book(title, author, year)
        print("Книга успешно добавлена")

    def _delete(self) -> None:
        """Удаление книги из базы данных"""

        book_id = input("Введите id книги: ")
        self._library.del_book(book_id)
        print("Книга успешно удалена")

    def _find(self) -> None:
        """Поиск книг по заданным полям"""

        title = input("Введите название книги или 'enter' для пропуска: ")
        author = input("Введите автора книги или 'enter' для пропуска: ")
        year = input("Введите год издания книги или 'enter' для пропуска: ")
        if not self._validate_year(year):
            print("Год издания должен быть числом")
            return
        pprint(self._library.find_book(title, author, year))

    def _show_all(self) -> None:
        """Вывод всех книг"""

        pprint(self._library.show_all_books())

    def _change_status(self) -> None:
        """Изменение статуса книги"""

        book_id = input("Введите id книги: ")
        status = input(
            f"Введите новый статус книги из списка ({",".join([f'{i}-{status}' for i, status in enumerate(self._statuses)])}): "
        )
        try:
            status = int(status)
            self._library.change_book_status(book_id, self._statuses[status])
            print("Статус успешно изменен")
        except (ValueError, IndexError):
            print("Некорректный статус")

    def _validate_year(self, year: str) -> bool:
        """Проверка валидности года издания книги"""

        if year != "" and not year.isdigit():
            return False
        return True


if __name__ == "__main__":
    client = Client(Library("library.json"))
    client.run()
