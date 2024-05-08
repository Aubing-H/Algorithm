import sys
import string
import random

import pygame
from pygame.locals import *

from macvar import dir_ego

from coordinate import (
    INV_WIDTH, INV_HEIGHT,
    GRID_WIDTH, GRID_HEIGHT,
    pos2grid_num,
    grid_num2pos,
    itemname2gridnum,
)

num2name = dict(zip(itemname2gridnum.values(), itemname2gridnum.keys()))


# 初始化Pygame
pygame.init()

# 设置屏幕尺寸和显示模式
vec = pygame.math.Vector2
HEIGHT, WIDTH = INV_HEIGHT + 150, INV_WIDTH + 150
CURSOR_HEIGHT, CURSOR_WIDTH = 20, 12
# drag parameters
ACC, FRIC = 1.0, -0.24  # ACC, FRIC = 0.5, -0.12
FPS = 60

''' left top point of inventory image '''
inv_x, inv_y = (WIDTH - INV_WIDTH) // 2, (HEIGHT - INV_HEIGHT) // 2

FramePerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft Crafting Interface")

# 加载图像资源
cursor_image = pygame.image.load(f"{dir_ego}/resources/custom_cursor.png")
cursor_image = pygame.transform.scale(cursor_image, (20, 12)) 
cursor_rect = cursor_image.get_rect()


class ActionHolder:

    def __init__(self):
        self.store_key = {K_p: False}
        pass

    def get_action(self, fmt='dict'):
        action = {'accx': 0, 'accy': 0, 'drag': 0}
        pressed_key = pygame.key.get_pressed()
        # action-drag
        if pressed_key[K_p]:
            if not self.store_key[K_p]:
                ''' jump True '''
                action['drag'] = 1
        # action-accx
        if pressed_key[K_LEFT] and not pressed_key[K_RIGHT]:
            action['accx'] = -1
        elif not pressed_key[K_LEFT] and pressed_key[K_RIGHT]:
            action['accx'] = 1
        # action-accy
        if pressed_key[K_UP] and not pressed_key[K_DOWN]:
            action['accy'] = -1
        elif not pressed_key[K_UP] and pressed_key[K_DOWN]:
            action['accy'] = 1
        
        self.store_key[K_p] = True if pressed_key[K_p] else False
        if fmt == 'dict':
            return action
        elif fmt == 'list':
            return [action['accx'], action['accy'], action['drag']]


''' 静态精灵 '''
class Inventory(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        cursor_image = pygame.image.load(f"{dir_ego}/resources/Inventory3_3.png")
        self.surf = cursor_image
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT/2))


class Item(pygame.sprite.Sprite):

    def __init__(self, item_name):
        super().__init__()
        self.id = ''.join(random.sample(string.ascii_letters, k=10))
        self.item_name = item_name
        item_image = pygame.image.load(f"{dir_ego}/resources/{item_name}.png")
        self.surf = pygame.transform.scale(item_image, (GRID_WIDTH, GRID_HEIGHT))

        if self.item_name in itemname2gridnum:
            self.grid_num = itemname2gridnum[self.item_name]
        else:
            self.grid_num = 0 
        x, y = grid_num2pos(self.grid_num, True)
        self.rect = self.surf.get_rect(center=(x + inv_x, y + inv_y))

    def update_rect(self, x, y):
        self.rect = self.surf.get_rect(center=(x, y))


class ItemGroup:

    def __init__(self):
        self.group = []
        self.dragged = None

    def find_pos(self, num):
        for i, item in enumerate(self.group):
            if item.grid_num == num:
                return i
        return -1
    
    def drag_up_table(self, num):
        pos = self.find_pos(num)
        if pos != -1:
            self.dragged = self.group.pop(pos)
    
    def drag_up_inv(self, num):
        self.dragged = Item(num2name[num])
        



class JungingEnv:

    def __init__(self) -> None:
        pass

    def reset(self, ):

        pass

    def step(self, action):
        ''' 
            action:
                accx = -1, 0, 1
                accy = -1, 0, 1
                drag = 0, 1 
        '''
        pass