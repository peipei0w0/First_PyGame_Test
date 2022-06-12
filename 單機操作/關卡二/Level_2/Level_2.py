import pygame
import random
import os
import time

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 1280
HEIGHT = 800
player_score = 1000
enemy_score = 1000
deduction = 1
enemy_number = 3
enemy_shoot_time = 100

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
bg_img = pygame.image.load(os.path.join("img",'bg1.png')).convert()
player_img = pygame.image.load(os.path.join("img",'player.png')).convert()
enemy_img = pygame.image.load(os.path.join("img",'enemy.png')).convert()
plane01R_img = pygame.image.load(os.path.join("img", "plane01_R30.png")).convert()    #飛機右轉
plane01L_img = pygame.image.load(os.path.join("img", "plane01_L30.png")).convert()    #飛機左轉
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f'expl{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (40, 40)))

# 引入字體 => 從目前程式執行之電腦尋找
font_name = pygame.font.match_font('Calibri')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # 改字體大小
    text_surface = font.render(text, True, WHITE)  # 製作文字圖片
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #將文字畫到屏幕上

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
        self.image = pygame.transform.scale(player_img, (100,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20  #碰撞判斷半徑(不可改名)
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)  #測試飛船的碰撞半徑大小
        self.rect.center = (WIDTH/2, HEIGHT-75)
        self.speed = 8

    def update(self):
        self.direction = 0  #預設圖片為正向

        key_pressed = pygame.key.get_pressed()     # 判斷按鍵是否被按
        if key_pressed[pygame.K_RIGHT]:
            self.direction = 1  #按下右鍵圖片改成右轉
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.direction = -1
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
        player_bullets.add(bullet)

    #左右移動時動畫
    def animate(self):
        if self.direction == -1:    #向左
            self.image = pygame.transform.scale(plane01L_img, (100,80))
            self.image.set_colorkey(BLACK)
        elif self.direction == 1:   #向右
            self.image = pygame.transform.scale(plane01R_img, (100,80))
            self.image.set_colorkey(BLACK)
        else:
            self.image = pygame.transform.scale(player_img, (100,80))
            self.image.set_colorkey(BLACK)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (90,75))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):

        if self.rect.right > WIDTH:       # 防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT/2:
            self.rect.bottom = HEIGHT/2

    def shoot(self):
        bullet = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
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
class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (10,20) )
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:     #如果子彈超出螢幕視窗，就把該子彈刪掉
            self.kill()
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center  = center
        self.frame = 0  #更新到第幾張圖片
        self.last_update = pygame.time.get_ticks()  #紀錄最後更新圖片的時間
        self.frame_rate = 50  #經過幾毫秒更新圖片

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# 建立 sprit 群組
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# 建立物件
bg1 = Background()
bg2 = Background(is_alt=True)
player = Player()
enemy = [0]*3
enemy[0] = Enemy(WIDTH/2, 50)
enemy[1] = Enemy(WIDTH/4, 50)
enemy[2] = Enemy(WIDTH*3/4, 50)
background = Background()

all_sprites.add(bg1,bg2)
all_sprites.add(background)
all_sprites.add(player)
for i in range(enemy_number):
    all_sprites.add(enemy[i])
enemy_group.add(enemy)

while running:
    clock.tick(FPS)
    enemy_shoot_time -= 1
    if enemy_shoot_time <= 0:
        for i in range(enemy_number):
            enemy[i].shoot()
        enemy_shoot_time = 100

    # 取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     #按X
            running = False
        elif event.type == pygame.KEYDOWN:     #按下鍵盤鍵
            if event.key == pygame.K_SPACE:
                player.shoot()
            #if event.key == pygame.K_p:
            #    enemy.shoot()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()


    # 更新遊戲
    all_sprites.update()
    Player.animate(player)  #角色移動動畫
    
    ## 碰撞判斷
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle) # False：不要刪掉 player
    close_hits = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_circle)
    for i in range(enemy_number):
        if i == 0:
            enemy_hits = pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
        else: enemy_hits += pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)

    ## 分數
    for hit in player_hits:
        player_score -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy_hits:
        enemy_score -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

    ## 關閉視窗
    if close_hits:
        expl = Explosion(close_hits[0].rect.center, 'lg')
        all_sprites.add(expl)
        running = False


    # 渲染/顯示遊戲畫面
    all_sprites.draw(screen)
    draw_text(screen, str(enemy_score), 18, WIDTH/2, 10)
    draw_text(screen, str(player_score), 18, WIDTH/2, HEIGHT-20)

    pygame.display.update()

pygame.quit()