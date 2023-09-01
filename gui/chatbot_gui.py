import tkinter as tk
from tkinter import ttk


class ChatbotTesterGUI(tk.Tk):
    PAD_X = 100
    PAD_Y = 40

    def __init__(self):
        super().__init__()
        self.geometry("+800+250")
        self.title("Chatbot Tester GUI")

        self.main_label = ttk.Label(self, text="Choose a Category:")
        self.main_label.pack(padx=self.PAD_X, pady=self.PAD_Y)

        self.main_options = ["1- Greeting", "2- Pizza Choose", "3- Drink Choose", "4- Finish"]
        self.main_dropdown = ttk.Combobox(self, values=self.main_options)
        self.main_dropdown.bind("<<ComboboxSelected>>", self.on_main_dropdown_change)
        self.main_dropdown.pack(padx=self.PAD_X, pady=self.PAD_Y)

        self.frame_options = ttk.Frame(self)
        self.frame_options.pack(padx=self.PAD_X-2, pady=self.PAD_Y-2)

        self.send_button = ttk.Button(self, text="Send", command=self.on_send_click)
        self.send_button.pack(pady=self.PAD_Y-2)

    def on_send_click(self):
        # Logic for when the Send button is clicked
        print("Send button clicked!")  # For now, it just prints a message.
        return

    def on_main_dropdown_change(self, event):
        chosen_option = self.main_dropdown.get()

        for widget in self.frame_options.winfo_children():
            widget.destroy()

        if chosen_option == "1- Greeting":
            self.create_greeting_dropdown()

        elif chosen_option == "2- Pizza Choose":
            self.create_pizza_dropdowns("First Pizza")
            self.create_pizza_dropdowns("Second Pizza")

        elif chosen_option == "3- Drink Choose":
            self.create_drink_dropdown()

        elif chosen_option == "4- Finish":
            self.create_finish_dropdown()

    def create_greeting_dropdown(self):
        greeting_label = ttk.Label(self.frame_options, text="Select Greeting:")
        greeting_label.pack(pady=10)

        greeting_options = ["Oi", "Olá", "Boa tarde", "Boa noite"]
        greeting_dropdown = ttk.Combobox(self.frame_options, values=greeting_options)
        greeting_dropdown.pack(pady=10)

    def create_pizza_dropdowns(self, label_text):
        pizza_label = ttk.Label(self.frame_options, text=label_text)
        pizza_label.pack(pady=10)

        pizza_a_options = ["Calabresa", "Frango", "Queijo"]
        pizza_a_dropdown = ttk.Combobox(self.frame_options, values=pizza_a_options)
        pizza_a_dropdown.pack(pady=10)

        pizza_b_options = ["Calabresa", "Frango", "Queijo"]
        pizza_b_dropdown = ttk.Combobox(self.frame_options, values=pizza_b_options)
        pizza_b_dropdown.pack(pady=10)

    def create_drink_dropdown(self):
        drink_label = ttk.Label(self.frame_options, text="Select Drink:")
        drink_label.pack(pady=10)

        drink_options = ["Coca", "Guaraná", "Fanta"]
        drink_dropdown = ttk.Combobox(self.frame_options, values=drink_options)
        drink_dropdown.pack(pady=10)

    def create_finish_dropdown(self):
        finish_label = ttk.Label(self.frame_options, text="Payment Method:")
        finish_label.pack(pady=10)

        finish_options = ["Cartão", "Dinheiro", "Pix"]
        finish_dropdown = ttk.Combobox(self.frame_options, values=finish_options)
        finish_dropdown.pack(pady=10)


def __main():
    app = ChatbotTesterGUI()
    app.mainloop()


if __name__ == "__main__":
    __main()
