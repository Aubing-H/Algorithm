import sys

import pygame
from pygame.locals import *

dir_ego = '/data1/houjinbing/project/ego'

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸和显示模式
vec = pygame.math.Vector2
HEIGHT, WIDTH = 340, 360
ACC, FRIC = 0.5, -0.12
ACC, FRIC = 1.0, -0.24
FPS = 60

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
        self.surf = pygame.transform.scale(cursor_image, (20, 20)) 
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

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

    def attach(self, groups_items=None):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_p]:
            print(self.pos)


''' 静态精灵 '''
class Inventory(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        cursor_image = pygame.image.load(f"{dir_ego}/mygame/Inventory3_3.png")
        self.surf = cursor_image
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT/2))


inv_data = {}

sp1 = Cursor()
inv = Inventory()

groups = pygame.sprite.Group()
groups.add(sp1)

groups_static = pygame.sprite.Group()
groups_static.add(inv)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sp1.move()
    sp1.attach()

    screen.fill((168, 168, 168))
    for entity in groups_static:
        screen.blit(entity.surf, entity.rect)
    for entity in groups:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSecond.tick(FPS)