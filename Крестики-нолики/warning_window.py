"""
Универсальная форма для взаимодействия с пользователем.
Текст формы меняется в соответствии с событием
"""

import customtkinter as ctk


class WarningWindow(ctk.CTkToplevel):
    def __init__(self, text: str):
        super().__init__()

        self.resizable(False, False)
        self.title("")

        self.label = ctk.CTkLabel(self, text=text)
        self.label.grid(padx=5, pady=5)

        self.button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.button.grid(padx=5, pady=5, sticky="ew")






