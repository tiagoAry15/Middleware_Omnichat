import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from typing import List, Callable


class DropdownComponent:
    def __init__(self, parent, label_text: str, options: List[str], message_format: str, user_input: tk.Text,
                 initial_option=None, callback: Callable[[tk.Event], None] = None,
                 name: str = None):
        self.parent = parent
        self.user_input = user_input
        self.message_format = message_format

        label = ttk.Label(parent, text=label_text)
        label.pack(pady=10)

        self.dropdowns = []

        self.create_dropdown(options, initial_option, callback, name)

    def create_dropdown(self, options, initial_option=None, callback=None, name=None):
        dropdown = ttk.Combobox(self.parent, values=options, width=20, style='Clam.TCombobox', name=name)
        dropdown.pack(pady=10)
        default_option = initial_option or options[0]
        dropdown.set(default_option)

        if callback:
            dropdown.bind("<<ComboboxSelected>>", callback)
        else:
            dropdown.bind("<<ComboboxSelected>>", self.generate_input_callback())

        self.dropdowns.append(dropdown)

    def create_extra_dropdown(self, options, initial_option=None, callback=None, name=None):
        self.create_dropdown(options, initial_option, callback, name)

    def generate_input_callback(self):
        def callback(event):
            self.user_input.delete(1.0, tk.END)
            formatted_message = self.message_format.format(*(dropdown.get() for dropdown in self.dropdowns))
            self.user_input.insert(tk.END, formatted_message)

        return callback


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
