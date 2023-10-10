from typing import List


def __extra_s_count(original: str, word: str) -> int:
    return word.count('s') - original.count('s')


def __get_plural_form(drink: str) -> str:
    words = drink.split()
    # Words which should not be pluralized
    skip_plural = ["de"]

    # Assuming plurals just add an 's' to the last word, except for words in skip_plural
    if len(words) > 1 and words[-2] not in skip_plural:
        words[-2] += 's'
    words[-1] += 's'

    return ' '.join(words)


def __getDrinkPluralForm(drinks: List[str]) -> dict:
    reverse_map = {}
    for drink in drinks:
        reverse_map[drink.replace(' ', '@')] = drink  # Singular form
        words = drink.split()

        # Handle plurals for last word
        words[-1] += 's'
        plural_drink_last = ' '.join(words)
        reverse_map[plural_drink_last.replace(' ', '@')] = drink

        # If the drink has multiple words, create more plural variations
        if len(words) > 1:
            # Only first word pluralized
            words[0] += 's'
            plural_drink_first = ' '.join(words)
            reverse_map[plural_drink_first.replace(' ', '@')] = drink

            # Remove the 's' added to the last word to get the sucos@de@laranja form
            words[-1] = words[-1][:-1]
            plural_drink_first_only = ' '.join(words)
            reverse_map[plural_drink_first_only.replace(' ', '@')] = drink

    return reverse_map


def __replaceDrinkSynonym(drinks: List[str], userMessage: str) -> str:
    replacedWords = set()  # Track words we've already replaced
    for drink in drinks:
        for word in userMessage.split():
            if word in replacedWords:
                continue
            if __extra_s_count(drink, word) > 0:
                userMessage = userMessage.replace(word, word.replace(' ', '@'))
                replacedWords.add(word)
            elif drink in word:
                userMessage = userMessage.replace(word, word.replace(' ', '@'))
                replacedWords.add(word)
    return userMessage


def structureDrink(parameters: dict, inputUserMessage: str) -> dict:
    drinks = parameters.get('Drinks', [])
    userMessage = __replaceDrinkSynonym(drinks, inputUserMessage.lower())

    numberEntity = {
        "uma": 1.0, "um": 1.0, "meio": 0.5, "meia": 0.5,
        "dois": 2.0, "duas": 2.0, "três": 3.0, "quatro": 4.0
    }

    reverseDrinkMap = __getDrinkPluralForm(drinks)

    order = {}
    words = userMessage.split()
    for i, word in enumerate(words):
        if word in numberEntity:
            for j in range(1, 5):
                potential_drink = '@'.join(words[i + 1:i + 1 + j])
                if potential_drink in reverseDrinkMap:
                    order[reverseDrinkMap[potential_drink]] = numberEntity[word]
                    break
    return order


def __main():
    result0 = structureDrink({'Drinks': ['suco de laranja']},
                             'Vou querer dois Sucos de Laranja')
    result1 = structureDrink({'Drinks': ['guaraná']}, 'vou querer um guaraná')
    result2 = structureDrink({'Drinks': ['guaraná']}, 'vou querer quatro guaranás')
    result3 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer um suco de laranja')
    result4 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer dois sucos de laranja')
    result5 = structureDrink({'Drinks': ['guaraná', 'suco de laranja']},
                             'vou querer três guaranás e dois sucos de laranja')
    orderList = [{'calabresa': 2.0}, {'pepperoni': 0.5, 'portuguesa': 0.5}, {'calabresa': 0.5, 'pepperoni': 0.5}]


if __name__ == '__main__':
    __main()
