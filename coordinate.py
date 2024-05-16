
INV_WIDTH, INV_HEIGHT = 352, 216
GRID_WIDTH, GRID_HEIGHT = 36, 36

grid_info = {
    'inv-1': (10, 3, (1, 3), (50, 166), (158, 202)),
    'inv-2': (13, 3, (1, 3), (194, 166), (302, 202)),
    'craft': (1, 9, (3, 3), (58, 32), (166, 140)),  # 3x3 x 36x36
    'resul': (0, 1, (1, 1), (246, 68), (282, 104)),  # 238,60 290,112 52x52
    'button': {16, 1, (1, 1), (231, 121), (298, 143)}   # 
}

pattern2name = {
    '## ##  # ': 'axe',
    '##  #  # ': 'hoe',
    ' #  #  # ': 'sword',
}

recipes = {}
for color in ['red', 'green', 'blue']:
    for mater in ['wooden', 'iron', 'diamond']:
        recipes[f'{color}_{mater}_axe'] = {
            'plan': [[mater, 0], [mater, 1], [mater, 3], [f'stick-{color}', 4], [f'stick-{color}', 7]],
            'additions': [0, 1],
        }
        recipes[f'{color}_{mater}_hoe'] = {
            'plan': [[mater, 0], [mater, 1], [f'stick-{color}', 4], [f'stick-{color}', 7]],
            'additions': [0, 1],
        }
        recipes[f'{color}_{mater}_sword'] = {
            'plan': [[mater, 0], [mater, 3], [f'stick-{color}', 6]],
            'additions': [0, 1, 2],
        }

itemname2gridnum = {
    'wooden': 10,
    'iron': 11,
    'diamond': 12,
    'stick-red': 13,
    'stick-green': 14,
    'stick-blue': 15,
}

''' position -> grid number '''
def pos2grid_num(x, y):
    for k in grid_info:
        start_num, total_num, shape, pos_s, pos_e = grid_info[k]
        r_num, c_num = shape
        if pos_s[0] <= x < pos_e[0] and pos_s[1] <= y < pos_e[1]:
            if k == 'button' or k == 'resul':
                dc = dr = 0
            else:
                dc = (x - pos_s[0]) // GRID_WIDTH 
                dr = (y - pos_s[1]) // GRID_HEIGHT
            return start_num + dr * c_num + dc
    return None


''' grid number -> position '''
def grid_num2pos(grid_num, center=False):
    assert 0 <= grid_num < 46, f'Error grid number: {grid_num}'
    for k in grid_info:
        start_num, total_num, shape, pos_s, pos_e = grid_info[k]
        r_num, c_num = shape
        if start_num <= grid_num < start_num + total_num:
            c = (grid_num - start_num) % c_num
            r = (grid_num - start_num) // c_num
            x = pos_s[0] + c * GRID_WIDTH
            y = pos_s[1] + r * GRID_HEIGHT
            if center:
                x, y = x + GRID_WIDTH // 2, y + GRID_HEIGHT // 2
            return x, y
    raise f'[Error code] Error grid number: {grid_num}'
        

def test_pos2grid_num():
    cases = [
        ([224, 141], None),
        ([0, 0], None),
        ([250, 185], 15),
        ([86, 59], 36),
        ([263, 84], 45),
        ([55, 285], 1),
    ]
    for i, (input, res) in enumerate(cases):
        pred = pos2grid_num(*input)
        print(i+1, pred == res, f'output: {pred}, true: {res}')


def test_grid_num2pos():
    cases = [
        ([0, False], (14, 281)),
        ([1, False], (50, 281)),
        ([1, True], (68, 299)),
        ([9, False], (14, 165)),
        ([36, False], (57, 31)),
        ([19, False], (50, 201)),
        ([45, False], (245, 67)),
    ]
    for i, (input, res) in enumerate(cases):
        pred = grid_num2pos(*input)
        print(i+1, pred == res, f'output: {pred}, true: {res}')



if __name__ == '__main__':
    test_pos2grid_num()
    test_grid_num2pos()