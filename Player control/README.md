# First-PyGame-Test

* ###### 控制飛船的上下左右鍵
* ###### 不讓飛船超出視窗

<ol><pre>
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
&nbsp;&nbsp;#更新遊戲
&nbsp;&nbsp;all_sprites.update()
</pre>
</ol>
