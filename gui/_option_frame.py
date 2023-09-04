from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import List

from gui._dropdown_component import clear_frame, DropdownComponent


class OptionFrame(ttk.Frame):

    def __init__(self, parent, user_input: tk.Text):
        super().__init__(parent)
        self.user_input = user_input
        self.pizza_dropdown_values = []

    def update_frame(self, chosen_option: str):
        clear_frame(self)
        default_message = ""

        if chosen_option == "1- Greeting":
            greeting_options = ["Oi", "Olá", "Boa tarde", "Boa noite"]
            default_message = greeting_options[0]
            DropdownComponent(self, "Select Greeting:", greeting_options,
                              "{}", self.user_input)
        elif chosen_option == "2- Pizza Choose":
            pizzaFlavors = ["Margherita", "Pepperoni", "Veggie", "BBQ Chicken"]
            default_message = pizzaFlavors[0]
            self.__pizzaChooseLogic(pizzaFlavors)
        elif chosen_option == "3- Drink Choose":
            drink_options = ["Coca", "Guaraná", "Fanta"]
            default_message = drink_options[0]
            DropdownComponent(self, "Select Drink:", drink_options,
                              "Vou querer uma {}", self.user_input)
        elif chosen_option == "4- Finish":
            payment_options = ["Cartão", "Dinheiro", "Pix"]
            default_message = payment_options[0]
            DropdownComponent(self, "Payment Method:", payment_options,
                              "Vou pagar com {}", self.user_input)
        return default_message

    def __pizzaChooseLogic(self, pizzaFlavors: List[str]):
        self.pizza_dropdown_values = [tk.StringVar(value=pizzaFlavors[0]), tk.StringVar(value=pizzaFlavors[1]),
                                      tk.StringVar(value=pizzaFlavors[2]), tk.StringVar(value=pizzaFlavors[3])]
        # Add your pizza dropdown components here
        first_pizza_dropdown = DropdownComponent(self, "Select First Pizza:", pizzaFlavors, "",
                                                 self.user_input, initial_option=pizzaFlavors[0], name="first_pizza",
                                                 callback=self.on_pizza_change)
        first_pizza_dropdown.create_extra_dropdown(pizzaFlavors, initial_option=pizzaFlavors[1],
                                                   callback=self.on_pizza_change, name="first_pizza_extra")
        second_pizza_dropdown = DropdownComponent(self, "Select Second Pizza:", pizzaFlavors, "",
                                                  self.user_input, initial_option=pizzaFlavors[2],
                                                  callback=self.on_pizza_change, name="second_pizza")
        second_pizza_dropdown.create_extra_dropdown(pizzaFlavors, initial_option=pizzaFlavors[3],
                                                    callback=self.on_pizza_change, name="second_pizza_extra")
        self.update_pizza_text()

    def on_pizza_change(self, event: tk.Event):
        widget = event.widget
        widget_name = widget.winfo_name()
        widget_name_to_idx = {
            "first_pizza": 0,
            "first_pizza_extra": 1,
            "second_pizza": 2,
            "second_pizza_extra": 3
        }

        idx = widget_name_to_idx.get(widget_name, 3)  # default to 3 if widget_name is not found
        self.pizza_dropdown_values[idx].set(widget.get())
        self.update_pizza_text()

    def update_pizza_text(self):
        self.user_input.delete(1.0, tk.END)
        pizzas = [val.get() for val in self.pizza_dropdown_values]
        isFirstPizzaHomogeneous = pizzas[0] == pizzas[1]
        isSecondPizzaHomogeneous = pizzas[2] == pizzas[3]
        firstPizzaTag = f"pizza meia {pizzas[0]} meia {pizzas[1]}" if not isFirstPizzaHomogeneous else \
            f"pizza {pizzas[0]}"
        secondPizzaTag = f"pizza meia {pizzas[2]} meia {pizzas[3]}" if not isSecondPizzaHomogeneous else \
            f"pizza {pizzas[2]}"
        newValue = f"Vou querer uma {firstPizzaTag} e uma {secondPizzaTag}"
        self.user_input.insert(tk.END, newValue)
