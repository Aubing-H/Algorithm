
INV_WIDTH, INV_HEIGHT = 352, 332
GRID_WIDTH, GRID_HEIGHT = 36, 36

grid_info = {
    'inv-1': (0, 9, (1, 9), (14, 281), (338, 317)),
    'inv-2': (9, 27, (3, 9), (14, 165), (338, 273)),
    'craft': (36, 9, (3, 3), (57, 31), (165, 139)),
    'resul': (45, 1, (1, 1), (245, 67), (281, 103)),
}


''' position -> grid number '''
def pos2grid_num(x, y):
    for k in grid_info:
        start_num, total_num, shape, pos_s, pos_e = grid_info[k]
        r_num, c_num = shape
        if pos_s[0] <= x < pos_e[0] and pos_s[1] <= y < pos_e[1]:
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