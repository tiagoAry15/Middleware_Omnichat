import tkinter as tk
from tkinter import ttk


class ChatbotTesterGUI(tk.Tk):
    PAD_X = 100
    PAD_Y = 40
    DROPDOWN_WIDTH = 20
    DROPDOWN_STYLE = 'Clam.TCombobox'

    def __init__(self):
        super().__init__()
        self.geometry("+800+250")
        self.title("Chatbot Tester GUI")

        self.larger_font = ('Arial', 14)
        self.style = ttk.Style(self)

        # Initialize the main label
        self.main_label = ttk.Label(self, text="Choose a Category:")
        self.main_label.pack(padx=self.PAD_X, pady=self.PAD_Y)

        # Use the custom style for Combobox
        self.main_options = ["1- Greeting", "2- Pizza Choose", "3- Drink Choose", "4- Finish"]
        self.main_dropdown = ttk.Combobox(self, values=self.main_options, width=self.DROPDOWN_WIDTH,
                                          style=self.DROPDOWN_STYLE)
        self.main_dropdown.bind("<<ComboboxSelected>>", self.on_main_dropdown_change)
        self.main_dropdown.pack(padx=self.PAD_X - 2, pady=self.PAD_Y)

        self.frame_options = ttk.Frame(self)
        self.frame_options.pack(padx=self.PAD_X - 2, pady=self.PAD_Y - 2)

        self.user_input = tk.Text(self, width=35, height=3)  # Setting a font for better aesthetics
        self.user_input.pack(pady=self.PAD_Y - 2)

        self.send_button = ttk.Button(self, text="Send", command=self.on_send_click)
        self.send_button.pack(pady=self.PAD_Y - 2)

    def on_send_click(self):
        # Logic for when the Send button is clicked
        print("Send button clicked!")  # For now, it just prints a message.
        return

    def on_main_dropdown_change(self, event):
        chosen_option = self.main_dropdown.get()

        for widget in self.frame_options.winfo_children():
            widget.destroy()

        dropdown = None

        if chosen_option == "1- Greeting":
            dropdown = self.create_greeting_dropdown()

        elif chosen_option == "2- Pizza Choose":
            pizza_a_dropdown, pizza_b_dropdown = self.create_pizza_dropdowns("First Pizza")
            self.create_pizza_dropdowns("Second Pizza")
            self.update_pizza_input(None)

        elif chosen_option == "3- Drink Choose":
            dropdown = self.create_drink_dropdown()

        elif chosen_option == "4- Finish":
            dropdown = self.create_finish_dropdown()

        if 'dropdown' in locals() and dropdown:
            dropdown.event_generate("<<ComboboxSelected>>")

    def create_dropdown(self, label_text, options, message_format, initial_option=None):
        label = ttk.Label(self.frame_options, text=label_text)
        label.pack(pady=10)

        dropdown = ttk.Combobox(self.frame_options, values=options, width=self.DROPDOWN_WIDTH,
                                style=self.DROPDOWN_STYLE)
        dropdown.pack(pady=10)
        default_option = initial_option or options[0]
        dropdown.set(default_option)

        dropdown.bind("<<ComboboxSelected>>", self.generate_input_callback(message_format, dropdown))
        return dropdown

    def generate_input_callback(self, message_format, dropdown):
        def callback(event):
            self.user_input.delete(1.0, tk.END)
            if "{}" in message_format:
                self.user_input.insert(tk.END, message_format.format(dropdown.get()))
            else:
                self.user_input.insert(tk.END, dropdown.get())

        return callback

    def create_greeting_dropdown(self):
        return self.create_dropdown("Select Greeting:", ["Oi", "Olá", "Boa tarde", "Boa noite"],
                                    "{}", initial_option="Oi")

    def create_drink_dropdown(self):
        return self.create_dropdown("Select Drink:", ["Coca", "Guaraná", "Fanta"],
                                    "Vou querer uma {}")

    def create_finish_dropdown(self):
        return self.create_dropdown("Payment Method:", ["Cartão", "Dinheiro", "Pix"],
                                    "Vou pagar com {}")

    def create_pizza_dropdowns(self, label_text):
        pizza_label = ttk.Label(self.frame_options, text=label_text)
        pizza_label.pack(pady=10)

        pizza_a_options = ["Calabresa", "Frango", "Queijo"]
        pizza_a_dropdown = ttk.Combobox(self.frame_options, values=pizza_a_options, width=self.DROPDOWN_WIDTH,
                                        style=self.DROPDOWN_STYLE)
        pizza_a_dropdown.pack(pady=10)
        pizza_a_default_option = pizza_a_options[0]
        pizza_a_dropdown.set(pizza_a_default_option)

        pizza_b_options = ["Calabresa", "Frango", "Queijo"]
        pizza_b_dropdown = ttk.Combobox(self.frame_options, values=pizza_b_options, width=self.DROPDOWN_WIDTH,
                                        style=self.DROPDOWN_STYLE)
        pizza_b_dropdown.pack(pady=10)
        pizza_b_default_option = pizza_b_options[1]
        pizza_b_dropdown.set(pizza_b_default_option)

        pizza_a_dropdown.bind("<<ComboboxSelected>>", self.update_pizza_input)
        pizza_b_dropdown.bind("<<ComboboxSelected>>", self.update_pizza_input)
        return pizza_a_dropdown, pizza_b_dropdown

    def update_pizza_input(self, event):
        children = self.frame_options.winfo_children()
        pizza_values = [child.get() for child in children if isinstance(child, ttk.Combobox) and child.get()]
        pizzas = '+'.join(pizza_values)
        self.user_input.delete(1.0, tk.END)
        self.user_input.insert(tk.END, pizzas)


def __main():
    app = ChatbotTesterGUI()
    app.mainloop()


if __name__ == "__main__":
    __main()
