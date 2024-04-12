import json


dir_ego = '/data1/houjinbing/project/ego'

with open(f'{dir_ego}/src/recipes.json') as f:
    recipes = json.load(f)


def is_synthesizable(recipes, crafting_table):
    ''' 
    输入：
        recipes中包含了多种物品合成的pattern，是一个dict;
            格式为：{
                'item_name': {
                    'plan': [['material_name', 36], ...],
                    'additions': [0, ...],
                },
                'diamond_hoe': {
                    'plan': [['diamond', 37], ['diamond', 36], ['stick', 40], ['stick', 43]],
                    'additions': [0, 1],
                },
                ...
            }
        crafting_table中包含了当前制作台上的物品，也是一个dict:
            例如：{38: "coal", 41: "stick"}, {36: 'diamond', 37: 'diamond', 40: 'stick', 43: 'stick'}
    输出：
        如果不能合成物品，输出 None，否则输出对应的物品名称。'''
    flag = 0
    for k,v in recipes.items():
        rcp_table = {pair[1]:pair[0] for pair in v['plan']}
        for i in range(len(v['additions'])):
            rcp_table = {rcp_k+v['additions'][i]:rcp_v for rcp_k,rcp_v in rcp_table.items()}
            if rcp_table == crafting_table:
                
                return k
    if not flag:
        return None   


    


def test_cases():
    '"light_gray_dye_from_gray_white_dye": {"plan": [["gray_dye", 36]], "additions": [0, 1, 2, 3, 4, 5, 6, 7, 8]},'
    cft_tables = [
        ({36: 'coal', 39: 'stick',}, 'torch'),
        ({42: 'gray_dye'}, 'light_gray_dye_from_gray_white_dye'),  # collide with gray_wool
        ({36: 'diamond', 37: 'diamond', 38: 'diamond', 40: 'stick', 43: 'stick'}, 'diamond_pickaxe'),
        ({36: 'coal', 39: 'stick', 44: 'coal'}, None),
        ({42: 'coal', }, None),
        ({36: 'diamond', 40: 'stick', 43: 'stick'}, None),
        ({}, None)
    ]
    for i, item in enumerate(cft_tables):
        output = is_synthesizable(recipes, crafting_table=item[0])
        print(f'测试-{i+1} 成功' if output == item[1] else f'测试-{i + 1} 失败，输出：{output}，真值：{item[1]}')


if __name__ == '__main__':
    test_cases()
