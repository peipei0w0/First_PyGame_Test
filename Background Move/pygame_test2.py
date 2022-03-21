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

Background_Color = WHITE
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
pygame.display.set_caption("PyGame Test")

clock = pygame.time.Clock()
running = True

# 載入圖片
bg_img = pygame.image.load(os.path.join("img",'background.jpg')).convert()
player_img = pygame.image.load(os.path.join("img",'player.png')).convert()
bg_anim = []
for i in range(2):
    bg_img = pygame.image.load(os.path.join("img",'background.jpg')).convert()
    bg_anim.append(pygame.transform.scale(bg_img, (500, 1000)))

class Background(pygame.sprite.Sprite):
    def __init__(self,is_alt=False):
        #super().__init__("img/background.jpg")
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = bg_img
        self.rect = self.image.get_rect()
        #self.rect.topleft = (0,0)
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

while running:
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
