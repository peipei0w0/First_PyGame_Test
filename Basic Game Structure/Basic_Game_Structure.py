import pygame

pygame.init()

#設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 500
HEIGHT = 600

#color
WHITE = (255,255,255)

Background_Color = WHITE
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
pygame.display.set_caption("Basic Game Structure！")

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)

    #取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #更新遊戲


    #渲染/顯示遊戲畫面
    screen.fill(Background_Color)

    pygame.display.update()

pygame.quit()
