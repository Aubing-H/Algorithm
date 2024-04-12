import sys

import pygame
from pygame.locals import *

from coordinate import (
    INV_WIDTH, INV_HEIGHT,
    GRID_WIDTH, GRID_HEIGHT,
    pos2grid_num,
    grid_num2pos,
)

dir_ego = '/data1/houjinbing/project/ego'

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸和显示模式
vec = pygame.math.Vector2
HEIGHT, WIDTH = 400, 520
CURSOR_HEIGHT, CURSOR_WIDTH = 20, 12
ACC, FRIC = 0.5, -0.12
ACC, FRIC = 1.0, -0.24
FPS = 60

''' left top point of inventory image '''
inv_x, inv_y = (WIDTH - INV_WIDTH) // 2, (HEIGHT - INV_HEIGHT) // 2

FramePerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft Crafting Interface")

# 加载图像资源
cursor_image = pygame.image.load(f"{dir_ego}/mygame/custom_cursor.png")
cursor_image = pygame.transform.scale(cursor_image, (20, 12)) 
cursor_rect = cursor_image.get_rect()


''' 动态精灵 '''
class Cursor(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        cursor_image = pygame.image.load(f"{dir_ego}/mygame/custom_cursor.png")
        self.surf = pygame.transform.scale(cursor_image, (CURSOR_WIDTH, CURSOR_HEIGHT)) 
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.key_state = {K_p: False}

    def move(self):
        pressed_key = pygame.key.get_pressed()
        self.acc = vec(0, 0)
        if pressed_key[K_LEFT]:
            self.acc.x = -ACC
        if pressed_key[K_RIGHT]:
            self.acc.x = ACC
        if pressed_key[K_UP]:
            self.acc.y = -ACC
        if pressed_key[K_DOWN]:
            self.acc.y = ACC

        # friction 
        self.acc += self.vel * FRIC

        # vecility
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

    def attach(self, inv_data, groups_item):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_p]:
            self.key_state[K_p] = True
        elif self.key_state[K_p]:
            num = pos2grid_num(self.pos.x - inv_x, self.pos.y - inv_y)
            print(f'key up p, num: {num}, x: {self.pos.x}, y: {self.pos.y}')
            if num is not None:
                if num in inv_data:
                    for entity in groups_item:
                        if entity.id == inv_data[num]:
                            entity.drag(num, inv_data)
                            break
                else:
                    for entity in groups_item:
                        if entity.drag_on:
                            entity.put(num, inv_data)
                            break
            self.key_state[K_p] = False



''' 静态精灵 '''
class Inventory(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        cursor_image = pygame.image.load(f"{dir_ego}/mygame/Inventory3_3.png")
        self.surf = cursor_image
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT/2))

class Item(pygame.sprite.Sprite):

    def __init__(self, item_name, grid_num):
        super().__init__()
        self.id = f'{item_name}-{grid_num}'
        self.item_name = item_name

        self.grid_num = grid_num
        self.drag_on = False

        item_image = pygame.image.load(f"{dir_ego}/mygame/all_items/{item_name}.png")
        self.surf = pygame.transform.scale(item_image, (GRID_WIDTH, GRID_HEIGHT)) 
        x, y = grid_num2pos(grid_num, True)
        self.rect = self.surf.get_rect(center=(x + inv_x, y + inv_y))
    
    def put(self, grid_num, inv_data):
        if grid_num not in inv_data:
            self.drag_on = False
            self.grid_num = grid_num
            inv_data[grid_num] = self.id

            x, y = grid_num2pos(grid_num, True)
            self.rect = self.surf.get_rect(center=(x + inv_x, y + inv_y))

    def drag(self, grid_num, inv_data):
        if grid_num in inv_data:
            self.drag_on = True
            self.grid_num = None
            inv_data.pop(grid_num)

    def update_rect(self, x, y):
        if self.drag_on:
            self.rect = self.surf.get_rect(center=(x, y))


inv_data = {
    0: 'oak_planks-0',
    24: 'stick-24',
    38: 'diamond-38',
    45: 'wooden_pickaxe-45',
}

cursor_sprite = Cursor()
inv_sprite = Inventory()

groups = pygame.sprite.Group()
groups.add(cursor_sprite)

groups_static = pygame.sprite.Group()
groups_static.add(inv_sprite)

groups_item = pygame.sprite.Group()
for k, v in inv_data.items():
    sp = Item(v.split('-')[0], k)
    groups_item.add(sp)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    cursor_sprite.move()
    cursor_sprite.attach(inv_data, groups_item)
    for entity in groups_item:
        topleft = cursor_sprite.pos - vec(CURSOR_WIDTH, CURSOR_HEIGHT) // 2
        entity.update_rect(topleft.x, topleft.y)
    

    screen.fill((168, 168, 168))
    for entity in groups_static:
        screen.blit(entity.surf, entity.rect)
    for entity in groups_item:
        screen.blit(entity.surf, entity.rect)
    for entity in groups:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSecond.tick(FPS)