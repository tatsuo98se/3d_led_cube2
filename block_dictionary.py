# 2017.12 gadget fes

order_2017_12_gadget_fes = {
'blue' : {2: 'object-ghost', 3:'filter-swaying', 4:'filter-bk-wave'},
'green' : {2: 'object-tree', 3:'filter-zoom', 4:'filter-bk-mountain'},
'orange' : {2: 'object-note', 3:'filter-rainbow', 4:'filter-bk-fireworks'},
'white' : {2: 'object-snowman', 3:'filter-rolldown', 4:'filter-bk-snows'},
'red' : {2: 'object-heart', 3:'filter-jump', 4:'filter-bk-sakura'},
'brown' : {2: 'object-socks', 3:'filter-spiral2', 4:'filter-bk-cloud'},
'yellowgreen' : {2: 'object-yacht', 3:'filter-wakame', 4:'filter-bk-grass'},
'yellow' : {2: 'object-star', 3:'filter-skewed', 4:'filter-bk-stars'},
}

# 2018.08 Maker Faire Tokyo
order_2018_08_maker_faire_tokyo = {
'blue' : {2: 'object-ghost', 3:'filter-swaying', 4:'filter-bk-wave'},
'green' : {2: 'object-tree', 3:'filter-zoom-ctrl', 4:'filter-bk-mountain'},
'orange' : {2: 'object-note', 3:'filter-rainbow-ctrl', 4:'filter-bk-fireworks'},
'white' : {2: 'object-snowman', 3:'filter-rolling-ctrl', 4:'filter-bk-snows'},
'red' : {2: 'object-heart', 3:'filter-jump-ctrl', 4:'filter-bk-sakura'},
'brown' : {2: 'object-socks', 3:'filter-spiral2', 4:'filter-bk-cloud'},
'yellowgreen' : {2: 'object-yacht', 3:'filter-wakame-ctrl', 4:'filter-bk-grass'},
'yellow' : {2: 'object-star', 3:'filter-skewed-ctrl', 4:'filter-bk-stars'},
}

# this array is used for test to check whether all tables are correct.
order_all = [ 
    order_2017_12_gadget_fes,
    order_2018_08_maker_faire_tokyo,
]

order_default = order_2018_08_maker_faire_tokyo

def convert_json(input_orders, order_table=order_default):
    color = input_orders['color']
    width = int(input_orders['width'])
    if color in order_table and width in order_table[color]:
        return order_table[color][width]
    else:
        print("unexcepted block type has spacified. color={0} width={1}".format(color, width) )
        return 'object-filter-rainbow'

