import json

from references.pathReference import getSpeisekartePath


def loadSpeisekarte() -> dict:
    path = getSpeisekartePath()
    with path.open(encoding='utf-8') as file:
        return json.load(file)


def createMenuString(menu):
    menuString = "Cardápio de bebidas:\n"

    for item in menu["Bebidas"]:
        name = item['nome']
        price = item['preço']
        size = item['tamanho']

        itemString = f"- {name} ({size}) - R${price:.2f}\n"
        menuString += itemString

    return menuString


def __main():
    speisekarte = loadSpeisekarte()
    print(createMenuString(speisekarte))
    return


if __name__ == '__main__':
    __main()
