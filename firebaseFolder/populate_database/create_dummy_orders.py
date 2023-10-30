import datetime
import random

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_order import FirebaseOrder


def __get_random_address() -> str:
    random_street_prefix_pool = ["Rua", "Avenida", "Alameda", "Travessa", "Praça", "Viela", "Estrada", "Rodovia"]
    random_street_suffix_pool = ["da Paz", "da Saudade", "da Harmonia", "da Felicidade", "da Alegria", "da União",
                                 "da Liberdade", "da Justiça", "da Igualdade", "da Fraternidade"]
    random_prefix = random.choice(random_street_prefix_pool)
    random_suffix = random.choice(random_street_suffix_pool)
    random_street_number = str(random.randint(1, 9999)).zfill(4)
    return f"{random_prefix} {random_suffix} {random_street_number}"


def __get_random_name() -> str:
    random_name_pool = ["João", "Maria", "José", "Ana", "Pedro", "Francisco", "Carlos", "Antônio", "Paulo", "Luiz",
                        "Luis", "Manoel", "Valdir", "Valdemar", "Valdomiro", "Valentim", "Valentino", "Valério",
                        "Valmir", "Valter", "Vanderlei", "Vanderlei", "Janderson", "Vânia", "Vanilda", "Vanilde",
                        "Vera", "Verônica", "Vicente", "Vicetina", "Victor", "Vilma", "Vilmar", "Vilson",
                        "Vinícius", "Virgílio", "Virgínia", "Vitória", "Viviane", "Vladimir"]
    return random.choice(random_name_pool)


def __get_random_email(name: str) -> str:
    email_pool = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com", "@bol.com.br", "@uol.com.br"]
    random_email = random.choice(email_pool)
    return f"{name}{random_email}"


def __get_random_pizza() -> str:
    pizza_pool = ["Calabresa", "Mussarela", "Portuguesa", "Frango com Catupiry", "Marguerita", "Quatro Queijos",
                  "Brócolis", "Bacon", "Chocolate", "Banana", "Romeu e Julieta", "Lombo", "Atum", "Escarola",
                  "Palmito", "Camarão", "Alho e Óleo", "Cinco Queijos", "Camarão com Catupiry", "Lombo com Catupiry",
                  "Bacon com Catupiry", "Chocolate com Morango", "Chocolate com Banana", "Chocolate com Morango",
                  "Banana com Canela", "Banana com Chocolate", "Banana com Morango", "Banana com Canela e Chocolate",
                  "Banana com Canela e Morango", "Banana com Canela e Chocolate e Morango",
                  "Banana com Canela e Chocolate e Morango"]
    return random.choice(pizza_pool)


def __get_random_platform() -> str:
    platform_pool = ["Instagram", "Whatsapp", "Facebook"]
    return random.choice(platform_pool)


def __get_random_order_status() -> str:
    status_pool = ["Confirmado", "Em preparação", "A caminho", "Entregue", "Cancelado"]
    return random.choice(status_pool)


def generate_random_order_dict() -> dict:
    name = __get_random_name()
    now = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f")[:-3]
    return {"address": __get_random_address(),
            "communication": __get_random_email(name),
            "customerName": name,
            "observation": "None",
            "pizzaName": __get_random_pizza(),
            "platform": __get_random_platform(),
            "status": __get_random_order_status(),
            "timestamp": now}


def populate_database_with_dummy_orders(n: int):
    fc = FirebaseConnection()
    fo = FirebaseOrder(fc)
    for _ in range(n):
        dummy_dict = generate_random_order_dict()
        fo.createOrder(dummy_dict)


def __main():
    populate_database_with_dummy_orders(15)
    return


if __name__ == "__main__":
    __main()
