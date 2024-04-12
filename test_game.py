import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸和显示模式
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minecraft Crafting Interface")

# 加载图像资源
cursor_image = pygame.image.load("/data1/houjinbing/project/ego/mygame/custom_cursor.png")
cursor_image = pygame.transform.scale(cursor_image, (20, 20)) 
cursor_rect = cursor_image.get_rect()
# 定义光标初始位置
cursor_pos = [0, 0]

# 定义合成方阵、仓库和合成后物品的位置和尺寸
crafting_grid_size = (3, 3)  # 合成方阵大小
crafting_grid_position = (100, 100)  # 合成方阵位置
crafting_item_size = (50, 50)  # 合成方阵中物品的大小
inventory_grid_size = (9, 4)  # 仓库大小
inventory_grid_position = (100, 300)  # 仓库位置
inventory_item_size = (50, 50)  # 仓库中物品的大小
result_grid_position = (400, 200)  # 合成后物品位置
result_grid_size = (50, 50)  # 合成后物品的大小
cursor_speed = 5

# 定义方向变量
move_left = False
move_right = False
move_up = False
move_down = False

# 游戏循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        print('1')
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 按键按下，设置方向变量为True
            if event.key == pygame.K_w:
                move_up = True
            elif event.key == pygame.K_s:
                move_down = True
            elif event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True
        elif event.type == pygame.KEYUP:
            # 按键释放，设置方向变量为False
            if event.key == pygame.K_w: 
                move_up = False
            elif event.key == pygame.K_s:
                move_down = False
            elif event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False

    # 根据方向变量移动光标
    if move_left:
        cursor_rect.x -= cursor_speed
    if move_right:
        cursor_rect.x += cursor_speed
    if move_up:
        cursor_rect.y -= cursor_speed
    if move_down:
        cursor_rect.y += cursor_speed

    # 限制光标移动范围在屏幕内
    cursor_rect.x = max(0, min(cursor_rect.x, SCREEN_WIDTH - cursor_rect.width))
    cursor_rect.y = max(0, min(cursor_rect.y, SCREEN_HEIGHT - cursor_rect.height))

    # 绘制到屏幕上
    screen.fill((255, 255, 255))

 # 绘制合成方阵
    for i in range(crafting_grid_size[0]):
        for j in range(crafting_grid_size[1]):
            x = crafting_grid_position[0] + i * crafting_item_size[0]
            y = crafting_grid_position[1] + j * crafting_item_size[1]
            # 绘制格子内部的线条
            pygame.draw.rect(screen, (0, 0, 0), (x, y, crafting_item_size[0], crafting_item_size[1]), 1)
            

    # 绘制仓库
    for i in range(inventory_grid_size[0]):
        for j in range(inventory_grid_size[1]):
            x = inventory_grid_position[0] + i * inventory_item_size[0]
            y = inventory_grid_position[1] + j * inventory_item_size[1]
            # 绘制格子内部的线条
            pygame.draw.rect(screen, (0, 0, 0), (x, y, inventory_item_size[0], inventory_item_size[1]), 1)

    # 绘制合成后物品
    x = result_grid_position[0]
    y = result_grid_position[1]
    # 绘制格子内部的线条
    pygame.draw.rect(screen, (0, 0, 0), (x, y, result_grid_size[0], result_grid_size[1]), 1)

    # 绘制光标
    cursor_rect = pygame.Rect(crafting_grid_position[0] + cursor_pos[0] * cursor_speed,
                              crafting_grid_position[1] + cursor_pos[1] * cursor_speed,
                              crafting_item_size[0], crafting_item_size[1])
    screen.blit(cursor_image, cursor_rect)

    pygame.display.flip()

    # 控制帧率
    pygame.time.Clock().tick(60)

# 退出Pygame
pygame.quit()
sys.exit()