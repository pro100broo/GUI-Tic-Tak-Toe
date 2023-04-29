"""
Модуль, отвечающий за валидацию ходов.

"""
import numpy as np

from exceptions import NotEmptyPosition, GameDraw


class TurnsManager:
    """
    В классе реализован следующий функционал:
    1. Подсчёт количества выигранных раундов в текущей партии
    2. Подсчёт количества совершённых ходов в текущем раунде
    3. Обработка выигрышных комбинаций по вертикали, горизонатили, главной и побочной диагоналям

    Игровое поле представленно в виде матрицы из строк
    """
    __rounds_counter = {"x": 0, "o": 0}
    __turns_counter = 0
    __board = None

    @staticmethod
    def _is_empty_position(function):
        """ Декоратор для обработки попытки постановки нового символа в уже занятую клетку """
        def wrapper(*args):
            if TurnsManager.__board[args[1] // 3][args[1] % 3]:
                raise NotEmptyPosition
            else:
                return function(*args)
        return wrapper

    @staticmethod
    def _is_draw(function):
        """ Декоратор для обработки ничьей """
        def wrapper(*args):
            if not (result := function(*args)) and TurnsManager.get_turns_counter() == 8:
                raise GameDraw
            else:
                return result

        return wrapper

    @staticmethod
    def __get_board() -> np.ndarray:
        return TurnsManager.__board

    @staticmethod
    def get_turns_counter() -> int:
        return TurnsManager.__turns_counter

    @staticmethod
    def get_rounds_counter() -> dict[str: int]:
        return TurnsManager.__rounds_counter

    def get_current_symbol(self) -> str:
        return "o" if self.get_turns_counter() % 2 else "x"

    @staticmethod
    def increment_turns_counter() -> None:
        TurnsManager.__turns_counter += 1

    @staticmethod
    def __increment_rounds_counter(symbol: str) -> None:
        TurnsManager.__rounds_counter[symbol] += 1

    @staticmethod
    def update_turns_counter() -> None:
        TurnsManager.__turns_counter = 0

    @staticmethod
    def update_rounds_counter() -> None:
        TurnsManager.__rounds_counter = {"x": 0, "o": 0}

    @_is_draw
    def check_winner(self, symbol_position: int) -> str:
        """
        Проверка на победителя, после каждого хода

        :param symbol_position: Номер клетки типа integer, соответствуйщий номеру кнопки.
        :return: symbol: Символы: 'x', либо 'o', в зависимости от победителя раунда
        """
        if symbol := self.__set_symbol(symbol_position):
            if self.__check_rows_columns(symbol) or self.__check_diagonals(symbol):
                self.__increment_rounds_counter(symbol)
                return symbol

    @_is_empty_position
    def __set_symbol(self, symbol_position: int) -> str:
        """ Запись очередного хода в представление игрового поля """
        TurnsManager.__board[symbol_position // 3][symbol_position % 3] = self.get_current_symbol()
        return self.get_current_symbol()


    def __check_rows_columns(self, symbol: str) -> int | None:
        """
         Проверка выигрышной комбинации по строкам и столбцам

        :param symbol: Символы: 'x', либо 'o', в зависимости от текущего хода
        :return: Единица возвращается в случае назождения выигрышной комбинации
        """
        for i in range(3):
            if np.count_nonzero(self.__get_board()[i] == symbol) == 3 or \
                    np.count_nonzero(self.__get_board()[:, i] == symbol) == 3:
                return 1

    def __check_diagonals(self, symbol: str) -> int | None:
        """
        Проверка выигрышной по главной и побочной диагоналям

        :param symbol: Символы: 'x', либо 'o', в зависимости от текущего хода
        :return: Единица возвращается в случае назождения выигрышной комбинации
        """
        if np.count_nonzero(self.__get_board().diagonal() == symbol) == 3 or \
                np.count_nonzero(np.fliplr(self.__get_board()).diagonal() == symbol) == 3:
            return 1

    @staticmethod
    def create_board() -> None:
        """ Генерация представления игрового поля в виде матрицы из строк """
        TurnsManager.__board = np.array(
            [
                ["", "", ""],
                ["", "", ""],
                ["", "", ""]
            ]
        )




