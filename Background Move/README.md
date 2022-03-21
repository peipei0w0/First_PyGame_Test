# 飛船背景移動

<pre>
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
            
  bg1 = Background()
  bg2 = Background(is_alt=True)
  all_sprites.add(bg1,bg2)
</pre>
