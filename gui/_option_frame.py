import tkinter as tk
from tkinter import ttk

from gui._dropdown_component import clear_frame, DropdownComponent


class OptionFrame(ttk.Frame):

    def __init__(self, parent, user_input):
        super().__init__(parent)
        self.user_input = user_input

    def update_frame(self, chosen_option):
        clear_frame(self)

        if chosen_option == "1- Greeting":
            DropdownComponent(self, "Select Greeting:", ["Oi", "Olá", "Boa tarde", "Boa noite"],
                              "{}", self.user_input)
        elif chosen_option == "2- Pizza Choose":
            # Add your pizza dropdown components here
            DropdownComponent(self, "Select Pizza:", ["Margherita", "Pepperoni", "Veggie", "BBQ Chicken"],
                              "I'd like a {}", self.user_input)
            DropdownComponent(self, "Select Size:", ["Small", "Medium", "Large", "Extra Large"],
                              "of {} size.", self.user_input)
        elif chosen_option == "3- Drink Choose":
            DropdownComponent(self, "Select Drink:", ["Coca", "Guaraná", "Fanta"],
                              "Vou querer uma {}", self.user_input)
        elif chosen_option == "4- Finish":
            DropdownComponent(self, "Payment Method:", ["Cartão", "Dinheiro", "Pix"],
                              "Vou pagar com {}", self.user_input)
