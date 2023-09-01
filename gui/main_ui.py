import tkinter as tk
from tkinter import ttk

from gui._option_frame import OptionFrame


class MainUI(tk.Tk):
    PAD_X = 100
    PAD_Y = 40
    DROPDOWN_WIDTH = 20
    DROPDOWN_STYLE = 'Clam.TCombobox'

    def __init__(self):
        super().__init__()
        self.geometry("+800+250")
        self.title("Chatbot Tester GUI")
        self.style = ttk.Style(self)

        # Initialize the main label
        self.main_label = ttk.Label(self, text="Choose a Category:")
        self.main_label.pack(padx=self.PAD_X, pady=self.PAD_Y)

        self.main_options = ["1- Greeting", "2- Pizza Choose", "3- Drink Choose", "4- Finish"]
        self.main_dropdown = ttk.Combobox(self, values=self.main_options, width=self.DROPDOWN_WIDTH,
                                          style=self.DROPDOWN_STYLE)
        self.main_dropdown.bind("<<ComboboxSelected>>", self.on_main_dropdown_change)
        self.main_dropdown.pack(padx=self.PAD_X - 2, pady=self.PAD_Y)
        self.main_dropdown.set(self.main_options[0])

        self.user_input = tk.Text(self, width=35, height=3)

        self.option_frame = OptionFrame(self, self.user_input)
        self.option_frame.pack(padx=self.PAD_X - 2, pady=self.PAD_Y - 2)

        self.user_input.pack(pady=self.PAD_Y - 2)

        self.send_button = ttk.Button(self, text="Send", command=self.on_send_click)
        self.send_button.pack(pady=self.PAD_Y - 2)

        self.__update_text_field()

    def on_send_click(self):
        # Logic for when the Send button is clicked
        print("Send button clicked!")  # For now, it just prints a message.

    def on_main_dropdown_change(self, event):
        chosen_option = self.main_dropdown.get()
        self.option_frame.update_frame(chosen_option)

    def __update_text_field(self):
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, self.main_dropdown.get())


if __name__ == "__main__":
    app = MainUI()
    app.mainloop()
