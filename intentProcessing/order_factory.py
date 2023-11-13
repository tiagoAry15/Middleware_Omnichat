from typing import List


def get_order_mocked_data():
    mocked_order_items = [{'price': 16.5, 'tag': '1 x Pizza meio calabresa meio margherita (R$16.50)'},
                          {'price': 18.9, 'tag': '1 x Pizza de frango (R$18.90)'},
                          {'price': 4.99, 'tag': '1 x Guaraná (R$4.99)'},
                          {'price': 13.0, 'tag': '2 x Suco de laranja (R$13.00)'}]
    mocked_structured_order = {'Bebida': [{'guaraná': 1.0},
                                          {'suco de laranja': 2.0}],
                               'Pizza': [{'calabresa': 0.5, 'margherita': 0.5},
                                         {'frango': 1.0}]}
    mocket_price_note = ('Vai ser: '
                         '\n- 1 x Pizza meio calabresa meio margherita (R$16.50)'
                         '\n- 1 x Pizza de frango (R$18.90)'
                         '\n- 1 x Guaraná (R$4.99)'
                         '\n- 2 x Suco de laranja (R$13.00)'
                         '\n- Total → [R$53.39]'
                         '\n Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)')
    return mocked_order_items, mocked_structured_order, mocket_price_note


def format_order_data(order_items: List[dict], structured_order: dict):
    order_pool = []

    # Iterate through the structured order to construct the desired format
    for category, items in structured_order.items():
        for item in items:
            formatted_item = {}

            # Determine the type of item
            if category == 'Pizza':
                formatted_item['type'] = 'pizza'
                formatted_item['flavors'] = [flavor.capitalize() for flavor in item.keys()]
            elif category == 'Bebida':
                formatted_item['type'] = 'drink'
                formatted_item['flavors'] = [flavor.capitalize() for flavor in item.keys()]

            # Extract the quantity and price
            formatted_item['quantity'] = sum(item.values())

            matching_tag = ' '.join(formatted_item['flavors'])
            for sub_item in order_items:
                if matching_tag in sub_item['tag']:
                    formatted_item['price'] = sub_item['price']
                    break

            order_pool.append(formatted_item)

    return {"orderItems": order_pool}


def __main():
    mocked_order_items, mocked_structured_order, mocket_price_note = get_order_mocked_data()
    formatted_order_data = format_order_data(mocked_order_items, mocked_structured_order)
    return


if __name__ == "__main__":
    __main()
