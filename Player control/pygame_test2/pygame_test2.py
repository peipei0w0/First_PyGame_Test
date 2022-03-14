import pygame

pygame.init()

#設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 500
HEIGHT = 600

#color
WHITE = (255,255,255)
GREEN = (0,255,0)

Background_Color = WHITE
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
pygame.display.set_caption("PyGame Test")

clock = pygame.time.Clock()
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (50,40) )
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-40)
        self.speed = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()     #判斷按鍵是否被按
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:       #防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.bottom <= 0:
            self.rect.top = HEIGHT

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

while running:
    clock.tick(FPS)

    #取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #更新遊戲
    all_sprites.update()


    #渲染/顯示遊戲畫面
    screen.fill(Background_Color)
    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
