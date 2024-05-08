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


''' 动态精灵 '''
class Cursor(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        cursor_image = pygame.image.load(f"{dir_ego}/resources/custom_cursor.png")
        self.surf = pygame.transform.scale(cursor_image, (CURSOR_WIDTH, CURSOR_HEIGHT)) 
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH // 2, HEIGHT // 2))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self, action):
        self.acc.x = action['accx']
        self.acc.y = action['accy']

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

        self.rect.center = vec(self.pos.x + CURSOR_WIDTH//2, self.pos.y + CURSOR_HEIGHT//2)

    def attach(self, action, groups_craft, dragged_sprite):
        # get grid num if cursor is on grid
        vx, vy = self.pos.x, self.pos.y
        num = pos2grid_num(vx - inv_x, vy - inv_y)

        if not (action['drag'] and num != None and 0 < num < 16):
            # debug
            if action['drag']:
                print('num', num)

            return dragged_sprite
    
        if dragged_sprite == None:
            print(f'key up p, num: {num}, x: {self.pos.x}, y: {self.pos.y}')
            if 0 < num < 10:
                # drag the item from crafting table
                for id in groups_craft:
                    if groups_craft[id].grid_num == num:
                        dragged_sprite = groups_craft[id]
                        groups_craft.pop(id)
                        break
            elif 10 <= num < 16:
                # sponse new material and attach to cursor
                for name in itemname2gridnum:
                    if itemname2gridnum[name] == num:
                        print(name)
                        break
                dragged_sprite = Item(name)
        else:
            if 0 < num < 10:
                blank = True
                for id in groups_craft:
                    if groups_craft[id].grid_num == num:
                        blank = False
                        break
                if blank:
                    groups_craft[dragged_sprite.id] = dragged_sprite
                    # update position
                    x, y = grid_num2pos(num, center=True)
                    dragged_sprite.update_rect(x + inv_x, y + inv_y)
                    dragged_sprite = None
            elif 10 <= num < 16:
                for name in itemname2gridnum:
                    if (itemname2gridnum[name] == num and 
                        dragged_sprite.item_name == name):
                        dragged_sprite = None
                        break
        return dragged_sprite


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


inv_sprite = Inventory()

groups_static = pygame.sprite.Group()
groups_static.add(inv_sprite)
for item_name in itemname2gridnum:
    sp = Item(item_name)
    groups_static.add(sp)

class SpriteGroup:

    def __init__(self, item_list=[]) -> None:
        self.group = item_list
        pass

    def 


groups_craft = {}

dragged_sprite = None

cursor_sprite = Cursor()

holder = ActionHolder()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action = holder.get_action()
    # debug
        
    cursor_sprite.move(action)
    if action['drag']:
        print(f'x: {cursor_sprite.pos.x}, y: {cursor_sprite.pos.y}')

    dragged_sprite = cursor_sprite.attach(action, groups_craft, dragged_sprite)
    if dragged_sprite != None:
        # position align with cursor
        dragged_sprite.update_rect(cursor_sprite.pos.x - CURSOR_WIDTH//2, 
                                   cursor_sprite.pos.y - CURSOR_HEIGHT//2)

    
    screen.fill((168, 168, 168))
    for entity in groups_static:
        screen.blit(entity.surf, entity.rect)
    
    for entity in groups_craft.values():
        screen.blit(entity.surf, entity.rect)
        
    if dragged_sprite != None:
        screen.blit(dragged_sprite.surf, dragged_sprite.rect)        
    screen.blit(cursor_sprite.surf, cursor_sprite.rect)

    pygame.display.update()
    FramePerSecond.tick(FPS)

