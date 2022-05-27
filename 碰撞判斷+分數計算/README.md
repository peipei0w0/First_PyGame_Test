# 碰撞判斷 + 分數計算

<div align = "center"><img width="293" alt="12" src="https://user-images.githubusercontent.com/59371107/170766526-4f56ba2b-b2a1-4387-a216-996580b8faab.png"></div>

* ###### 碰撞判斷
  * ###### 預設是矩形
     * ###### False：if player 跟 enemy 射出的子彈碰撞，不要刪掉 player
     * ###### spritecollide(物件, sprite群組, bool值, bool值)
        ```python
        pygame.sprite.spritecollide(player, enemy_bullets, False)
        ```
  * ###### 圓形碰撞判斷 - pygame.sprite.collide_circle
    ```python
    pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)
    ```

  * ###### Final 碰撞判斷
      ```python
      player_hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle)
            enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, False, pygame.sprite.collide_circle)
            tie_hits = pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_circle)
      ```
    
* ###### 添加文字
     * ###### 引入字體
        ```python
        font_name = pygame.font.match_font('Calibri')
        ```
     * ###### 定義 draw_text
        ```python
        def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)  #將文字渲染出來
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)  #將文字畫到屏幕上
        ```
        
* ###### 建立分數
    * ###### 在遊戲迴圈的【# 渲染/顯示遊戲畫面】新增 player 及 enemy 的分數
        ```python
        while running:
            # 渲染/顯示遊戲畫面
            draw_text(screen, str(enemy_score), 18, WIDTH/2, 10)
            draw_text(screen, str(player_score), 18, WIDTH/2, HEIGHT-20)
        ```
