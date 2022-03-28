import pygame
import random
import os

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 500
HEIGHT = 600

# color
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

Background_Color = BLACK
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
pygame.display.set_caption("PyGame Test")

clock = pygame.time.Clock()

# 載入圖片
bg_img = pygame.image.load(os.path.join("img",'background.jpg')).convert()
player_img = pygame.image.load(os.path.join("img",'player.png')).convert()

font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
def drow_init():
    draw_text(screen, '太空生存戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '<- -> 移動，space發射子彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '單人對戰請按 1，單人對戰請按 2', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    wating = True
    while wating:
        clock.tick(FPS)
        # 取得玩家輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
            elif event.type == pygame.KEYUP:     #按下鍵盤鍵
                wating = False

class Background(pygame.sprite.Sprite):
    def __init__(self,is_alt=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg_img
        self.rect = self.image.get_rect()
        self.speed = 1

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= screen_rect.height:
            self.rect.y = -self.rect.height
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-40)
        self.speed = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()     # 判斷按鍵是否被按
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:       # 防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (10,20) )
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:     #如果子彈超出螢幕視窗，就把該子彈刪掉
            self.kill()

all_sprites = pygame.sprite.Group()

bg1 = Background()
bg2 = Background(is_alt=True)
all_sprites.add(bg1,bg2)
player = Player()
background = Background()
all_sprites.add(background)
all_sprites.add(player)


running = True
show_init = True
while running:
    if show_init:
        drow_init()
        show_init = False

    clock.tick(FPS)
    # 取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     #按X
            running = False
        elif event.type == pygame.KEYDOWN:     #按下鍵盤鍵
            if event.key == pygame.K_SPACE:
                player.shoot()


    # 更新遊戲
    all_sprites.update()


    # 渲染/顯示遊戲畫面
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()