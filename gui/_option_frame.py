from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from gui._dropdown_component import clear_frame, DropdownComponent


class OptionFrame(ttk.Frame):

    def __init__(self, parent, user_input: tk.Text):
        super().__init__(parent)
        self.user_input = user_input
        self.pizza_dropdown_values = []

    def update_frame(self, chosen_option: str):
        clear_frame(self)

        if chosen_option == "1- Greeting":
            DropdownComponent(self, "Select Greeting:", ["Oi", "Olá", "Boa tarde", "Boa noite"],
                              "{}", self.user_input)
        elif chosen_option == "2- Pizza Choose":
            pizzaFlavors = ["Margherita", "Pepperoni", "Veggie", "BBQ Chicken"]
            self.pizza_dropdown_values = [tk.StringVar(value=pizzaFlavors[0]),
                                          tk.StringVar(value=pizzaFlavors[0])]
            # Add your pizza dropdown components here
            DropdownComponent(self, "Select First Pizza:", pizzaFlavors,
                              "", self.user_input, callback=self.on_pizza_change, name="first_pizza")

            DropdownComponent(self, "Select Second Pizza:", pizzaFlavors,
                              "", self.user_input, callback=self.on_pizza_change, name="second_pizza")

            self.__update_pizza_text()
        elif chosen_option == "3- Drink Choose":
            DropdownComponent(self, "Select Drink:", ["Coca", "Guaraná", "Fanta"],
                              "Vou querer uma {}", self.user_input)
        elif chosen_option == "4- Finish":
            DropdownComponent(self, "Payment Method:", ["Cartão", "Dinheiro", "Pix"],
                              "Vou pagar com {}", self.user_input)

    def on_pizza_change(self, event: tk.Event):
        widget = event.widget
        if widget.winfo_name() == "first_pizza":
            idx = 0
        else:
            idx = 1
        self.pizza_dropdown_values[idx].set(widget.get())
        self.__update_pizza_text()

    def __update_pizza_text(self):
        self.user_input.delete(1.0, tk.END)
        pizzas = [val.get() for val in self.pizza_dropdown_values]
        self.user_input.insert(tk.END, '+'.join(pizzas))
