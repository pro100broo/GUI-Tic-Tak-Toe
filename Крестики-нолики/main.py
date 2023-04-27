"""
Курсовая работа по предмету "Введение в программирование", по теме "Крестики-нолики"
Выполнил: Шальнев Семен. Группа: Прог - С-21

В программе реализована игра крестики-нолики для двух игроков
"""

import customtkinter as ctk
from tkinter import Canvas

from turns import TurnsManager
from config import coordinates_by_position
from exceptions import NotEmptyPosition, GameDraw
from warning_window import WarningWindow

ctk.set_appearance_mode("Dark")


class MainWindow(ctk.CTk):
    """ Главная форма программы наследуется от класса CTk """

    def __init__(self):
        super().__init__()

        self.geometry("660x490")
        self.resizable(False, False)

        self.grid_columnconfigure(2)
        self.grid_rowconfigure(2)

        """ Формы игрового поля """
        self.field_frame = ctk.CTkFrame(self, width=500, height=500)
        self.field_frame.grid(column=1, row=1, rowspan=2, padx=25, pady=25)

        self.board_canvas = Canvas(self.field_frame, bg="grey", width=600, height=600, highlightbackground="blue")
        self.board_canvas.grid(padx=25, pady=25)

        """ Формы игрового меню. Расположены в порядке отрисовки """

        self.menu_label = ctk.CTkLabel(self, text="Main menu")
        self.menu_label.grid(column=2, row=1, pady=(10, 0), sticky="ns")

        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.grid(column=2, row=2, pady=(0, 25), sticky="ns")

        self.rounds_label = ctk.CTkLabel(self.menu_frame, text="Rounds counter")
        self.rounds_label.grid(row=1, padx=5, pady=8)

        self.rounds_canvas = Canvas(self.menu_frame, bg="grey", width=200, height=100, highlightbackground="blue")
        self.rounds_canvas.grid(row=2, padx=5, pady=15)

        self.buttons_label = ctk.CTkLabel(self.menu_frame, text="Choose position")
        self.buttons_label.grid(row=3, padx=5, pady=(0, 15))

        self.buttons_grid = ctk.CTkFrame(self.menu_frame)
        self.buttons_grid.grid(row=4, padx=5, pady=(0, 15), sticky="ew")

        self.clear_button = ctk.CTkButton(self.menu_frame, text="Clear the board", command=self.__clear_board)
        self.clear_button.grid(row=5, padx=5, pady=(0, 15))

        self.restart_button = ctk.CTkButton(self.menu_frame, text="Restart the game", command=self.__restart_game)
        self.restart_button.grid(row=6, padx=5, pady=(0, 15))

        self.exit_button = ctk.CTkButton(self.menu_frame, text="Exit", command=self.destroy)
        self.exit_button.grid(row=7, padx=5, sticky="ew")

        """ Инициализация игрового поля, кнопок ввода позиции и счётчика очков """
        self.__print_game_field()
        self.__generate_buttons()

        MainWindow.__update_scores(self, turn_validator.get_rounds_counter())

    @staticmethod
    def _validate_turn(function):
        """
        Декоратор для валидации нажатия на кнопку выбора позиции нового символа
        Обрабатываются следующие события:
        1. Очередной ход
        2. Победный ход ноликов/крестиков (победа в очередном раунде)
        3. Попытка постановки нового символа в уже занятую клетку
        4. Ничья в партии, после последнего хода
        """
        def wrapper(*args):
            try:
                if winner := turn_validator.check_winner(args[1]):
                    WarningWindow(f"The winner is: {winner.upper()}")
                    MainWindow.__clear_board(args[0])
                    MainWindow.__update_scores(args[0], turn_validator.get_rounds_counter())
                else:
                    function(*args)
                    turn_validator.increment_turns_counter()
            except NotEmptyPosition:
                WarningWindow("Chosen position is not empty!!!")
            except GameDraw:
                WarningWindow("Draw!")
                MainWindow.__clear_board(args[0])
                turn_validator.update_turns_counter()
        return wrapper

    def __generate_buttons(self) -> None:
        """
        Каждая кнопка соотвествует своей ячейке, в соответствии с номером.
        При помощи цикла генерируется сетка, состоящая из девяти кнопок
        """
        for i in range(9):
            button = ctk.CTkButton(self.buttons_grid, width=40, height=20, text=f"{i + 1}")
            button.configure(command=lambda text=f"{i + 1}", event=button: self.__print_symbol(int(text) - 1))
            button.grid(row=i // 3, column=i % 3, padx=3, pady=3)

    def __print_game_field(self) -> None:
        """ Отрисовка четырех линий в виде 'клетки' """
        self.board_canvas.create_line((0, 200, 600, 200))
        self.board_canvas.create_line((0, 400, 600, 400))
        self.board_canvas.create_line((200, 0, 200, 600))
        self.board_canvas.create_line((400, 0, 400, 600))

    @_validate_turn
    def __print_symbol(self, symbol_position: int) -> None:
        """
        Печать нолика, либо крестика в зависимости от текущего хода.
        В случае крестика, в нужно клетке рисуется две перекрёстные лении.
        В случае нолика, рисуется овал

        :param symbol_position: Номер клетки типа integer, соответствуйщий номеру кнопки.
        Поступает в метод, при обработке события нажатия на кнопку
        """
        if turn_validator.get_current_symbol() == "x":
            self.board_canvas.create_line(coordinates_by_position["x"][symbol_position][0], width="5", fill="red")
            self.board_canvas.create_line(coordinates_by_position["x"][symbol_position][1], width="5", fill="red")
        else:
            self.board_canvas.create_oval(coordinates_by_position["o"][symbol_position], width="5", outline="blue")

        self.board_canvas.update_idletasks()

    def __update_scores(self, scores: dict[str, int]) -> None:
        """
        Обновление формы с счётчиком очков за раунды

        :param scores: Словарь, с текущим количеством очков для ноликов и крестиков
        """
        self.rounds_canvas.delete("all")
        self.rounds_canvas.create_text(30, 50, text="X", fill="red", font=("Arial", 30))
        self.rounds_canvas.create_text(100, 50, text=f"{scores['x']} : {scores['o']}", font=("Arial", 30), fill="black")
        self.rounds_canvas.create_text(170, 50, text="O", fill="blue", font=("Arial", 34))
        self.rounds_canvas.update_idletasks()

    def __clear_board(self) -> None:
        """ Очистка формы игрового поля """
        turn_validator.create_board()
        turn_validator.update_turns_counter()
        self.board_canvas.delete("all")
        self.__print_game_field()
        self.board_canvas.update_idletasks()

    def __restart_game(self) -> None:
        """ Рестарт текущей партии. При этом, обновляются все необходимые данные"""
        turn_validator.update_turns_counter()
        turn_validator.update_rounds_counter()
        self.__clear_board()
        self.__update_scores(turn_validator.get_rounds_counter())


if __name__ == "__main__":
    """ Инициализация всех необхожимых объектов """
    turn_validator = TurnsManager()
    turn_validator.create_board()

    app = MainWindow()
    app.title("Курсовая работа. Шальнев Семен Валерьевич. Прог-С-21")
    app.mainloop()
