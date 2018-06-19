''' 2017.12 gadget fes
blue = {2: 'object-ghost', 3:'filter-swaying', 4:'filter-bk-wave'}
green = {2: 'object-tree', 3:'filter-zoom', 4:'filter-bk-mountain'}
orange = {2: 'object-note', 3:'filter-rainbow', 4:'filter-bk-fireworks'}
white = {2: 'object-snowman', 3:'filter-rolldown', 4:'filter-bk-snows'}
red = {2: 'object-heart', 3:'filter-jump', 4:'filter-bk-sakura'}
brown = {2: 'object-socks', 3:'filter-spiral2', 4:'filter-bk-cloud'}
yellowgreen = {2: 'object-yacht', 3:'filter-wakame', 4:'filter-bk-grass'}
yellow = {2: 'object-star', 3:'filter-skewed', 4:'filter-bk-stars'}
'''

# 2018.08 Maker Faire Tokyo
blue = {2: 'object-ghost', 3:'filter-swaying', 4:'filter-bk-wave'}
green = {2: 'object-tree', 3:'filter-zoom-ctrl', 4:'filter-bk-mountain'}
orange = {2: 'object-note', 3:'filter-rainbow-ctrl', 4:'filter-bk-fireworks'}
white = {2: 'object-snowman', 3:'filter-rolling-ctrl', 4:'filter-bk-snows'}
red = {2: 'object-heart', 3:'filter-jump-ctrl', 4:'filter-bk-sakura'}
brown = {2: 'object-socks', 3:'filter-spiral2', 4:'filter-bk-cloud'}
yellowgreen = {2: 'object-yacht', 3:'filter-wakame-ctrl', 4:'filter-bk-grass'}
yellow = {2: 'object-star', 3:'filter-skewed-ctrl', 4:'filter-bk-stars'}

orders = {
    'blue': blue,
    'green' : green,
    'orange' : orange,
    'white' : white,
    'red' : red,
    'brown' : brown,
    'yellowgreen' : yellowgreen,
    'yellow' : yellow
}
def convert_json(input_orders):
    color = input_orders['color']
    width = int(input_orders['width'])
    if color in orders and width in orders[color]:
        return orders[color][width]
    else:
        print("unexcepted block type has spacified. color={0} width={1}".format(color, width) )
        return 'object-filter-rainbow'

