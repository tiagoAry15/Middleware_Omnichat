def get_order_mocked_data():
    mocked_dict = {'Bebida': [{'guaraná': 1.0}, {'suco de laranja': 2.0}],
                   'Pizza': [{'calabresa': 0.5, 'margherita': 0.5}, {'frango': 1.0}]}
    mocket_price_note = ('Vai ser: '
                         '\n- 1 x Pizza meio calabresa meio margherita (R$16.50)'
                         '\n- 1 x Pizza de frango (R$18.90)'
                         '\n- 1 x Guaraná (R$4.99)'
                         '\n- 2 x Suco de laranja (R$13.00)'
                         '\n- Total → [R$53.39]'
                         '\n Qual vai ser a forma de pagamento? (pix/cartão/dinheiro)')
    return mocked_dict, mocket_price_note

