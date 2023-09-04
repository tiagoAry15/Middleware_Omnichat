import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox
from typing import List, Callable


class DropdownComponent:
    def __init__(self, parent, label_text: str, options: List[str], message_format: str, user_input: tk.Text,
                 initial_option=None, callback: Callable[[tk.Event], None] = None,
                 name: str = None):
        self.user_input = user_input
        label = ttk.Label(parent, text=label_text)
        label.pack(pady=10)

        self.dropdown = ttk.Combobox(parent, values=options, width=20, style='Clam.TCombobox', name=name)
        self.dropdown.pack(pady=10)
        default_option = initial_option or options[0]
        self.dropdown.set(default_option)

        if callback:
            self.dropdown.bind("<<ComboboxSelected>>", callback)
        else:
            self.dropdown.bind("<<ComboboxSelected>>", self.generate_input_callback(message_format, self.dropdown))

    def generate_input_callback(self, message_format: str, dropdown: Combobox):
        def callback(event):
            self.user_input.delete(1.0, tk.END)
            if "{}" in message_format:
                self.user_input.insert(tk.END, message_format.format(dropdown.get()))
            else:
                self.user_input.insert(tk.END, dropdown.get())
        return callback


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()