import tkinter as tk
from tkinter import ttk


class DropdownComponent:

    def __init__(self, parent, label_text, options, message_format, user_input, initial_option=None):
        self.user_input = user_input
        label = ttk.Label(parent, text=label_text)
        label.pack(pady=10)

        dropdown = ttk.Combobox(parent, values=options, width=20, style='Clam.TCombobox')
        dropdown.pack(pady=10)
        default_option = initial_option or options[0]
        dropdown.set(default_option)

        dropdown.bind("<<ComboboxSelected>>", self.generate_input_callback(message_format, dropdown))

    def generate_input_callback(self, message_format, dropdown):
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
