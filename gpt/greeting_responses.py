import random


class PizzaGreetingResponses:
    def __init__(self):
        self.greetingResponses = [
            "Bem-vindo à Pizza do Bill! Como posso ajudá-lo?",
            "Primeiramente boa noite! Gostaria de pedir uma pizza?",
            "Bem-vindo à Pizza do Bill! Será um prazer te atender hoje! Seja muito bem-vindo!",
            "Olá! Bem-vindo à Pizza do Bill! Estamos prontos para receber o seu pedido.",
            "Que bom tê-lo aqui na Pizza do Bill! Como posso ajudá-lo hoje?",
            "Oi! Você chegou à Pizzaria do Bill, onde as melhores pizzas são feitas com amor. "
            "O que posso fazer por você?",
            "Seja bem-vindo à Pizza do Bill! Estamos ansiosos para preparar a sua pizza perfeita.",
            "Ei, que coisa boa te ver por aqui! A Pizza do Bill está pronta para satisfazer seu desejo por "
            "uma pizza deliciosa. Como posso te ajudar?"
        ]

    def sendGreetingResponse(self) -> str:
        return random.choice(self.greetingResponses)