## _drink_processor.py_

This module is responsible for processing drink orders from user messages. It contains several private functions that help in identifying and structuring drink orders from the input messages. Here are the functionalities provided by this module:

- **__extra_s_count(original: str, word: str) -> int**: This function calculates the difference in the count of the letter 's' between the original word and the modified word.
  
- **__get_plural_form(drink: str) -> str**: This function returns the plural form of a given drink name. It assumes that plurals are formed by adding an 's' to the last word, except for words in the `skip_plural` list.
  
- **__getDrinkPluralForm(drinks: List[str]) -> dict**: This function creates a dictionary where the keys are plural forms of drink names (with spaces replaced by '@') and the values are the original drink names.
  
- **__replaceDrinkSynonym(drinks: List[str], userMessage: str) -> str**: This function replaces words in the user message that are synonyms or plural forms of drinks in the drinks list with a version where spaces are replaced by '@'.
  
- **structureDrink(parameters: dict, inputUserMessage: str) -> dict**: This function structures the drink order from the user message. It identifies the number and type of drinks ordered by the user and returns a dictionary with this information.
  
- **__main()**: A testing function that demonstrates the usage of the `structureDrink` function with various input examples.

### Usage

This module is used to process user messages to identify and structure drink orders. It can handle messages with different phrasing and plural forms of drink names.

### Examples

```python
result0 = structureDrink({'Drinks': ['suco de laranja']}, 'Vou querer dois Sucos de Laranja')
result1 = structureDrink({'Drinks': ['guaraná']}, 'vou querer um guaraná')
result2 = structureDrink({'Drinks': ['guaraná']}, 'vou querer quatro guaranás')
result3 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer um suco de laranja')
result4 = structureDrink({'Drinks': ['suco de laranja']}, 'vou querer dois sucos de laranja')
result5 = structureDrink({'Drinks': ['guaraná', 'suco de laranja']}, 'vou querer três guaranás e dois sucos de laranja')
```

### Results

```python
result0 = {'suco de laranja': 2.0}
result1 = {'guaraná': 1.0}
result2 = {'guaraná': 4.0}
result3 = {'suco de laranja': 1.0}
result4 = {'suco de laranja': 2.0}
result5 = {'guaraná': 3.0, 'suco de laranja': 2.0}
````