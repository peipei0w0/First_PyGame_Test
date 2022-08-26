# 更新
* ###### 增加變數 <i>Keyboard = "Null"</i>、Keyboard_Space_Speed = 0
  1. ###### Keyboard：與手部辨識的 "介面傳輸變數"
      1. ###### "Space"：發射子彈
      2. ###### "A"：重新關卡
      3. ###### "Z"：只有現在 or 曾經破關成功，才能跳轉至下一關卡
  2. ###### Keyboard_Space_Speed：調節與手勢辨識結合時的 "子彈發射頻率"
      ```python
      # 設定好就不會輕易改變的變數用大寫
      score = [100, 50, 50, 50]    # 玩家, 敵人1, 敵人2, 敵人3
      once_win = False
      Keyboard = "Null"
      Keyboard_Space_Speed = 0

      def player_control(Keyboard):
        if Keyboard == "Space":
            player_bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)
            Keyboard = "Null"
            return Keyboard

      while running:
        if result == '無':
            for event in pygame.event.get():   # 鍵盤控制 => 測試用
                if event.type == pygame.QUIT:  # 按X
                    running = False
                player_control_Keyboard_and_Mouse()
            # 取得玩家輸入 & Space 控制
            if Keyboard_Space_Speed >= 7:      # 變數控制 => 結合用
                Keyboard = player_control(Keyboard)
                Keyboard_Space_Speed = 0
      ```
* ###### 敵人生命 == 0 => 刪除整個敵人物件、敵人子彈、敵人爆炸... => 以 Level_2.py 為例
    ```python
    def getHit(score, enemy_is_exist):
        # draw_text(screen, str("now is hitting"), 18, 100, 10)
        player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True,
                                                  pygame.sprite.collide_circle)  # False：不要刪掉 player

        IsBreak = False
        if score[0] == 0 or (score[1] == 0 and score[2] == 0 and score[3] == 0):
            IsBreak = True

        ## 分數
        for hit in player_hits:
            if IsBreak: break
            score[0] -= deduction
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        if enemy_is_exist[0]: 
            enemy0_hits = pygame.sprite.spritecollide(enemy[0], player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy0_hits:
                if IsBreak: break
                score[1] -= deduction
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
        if enemy_is_exist[1]: 
            enemy1_hits = pygame.sprite.spritecollide(enemy[1], player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy1_hits:
                if IsBreak: break
                score[2] -= deduction
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
        if enemy_is_exist[2]: 
            enemy2_hits = pygame.sprite.spritecollide(enemy[2], player_bullets, True, pygame.sprite.collide_circle)
            for hit in enemy2_hits:
                if IsBreak: break
                score[3] -= deduction
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)

        # 使分數不小於 0
        for i in range(enemy_number + 1):
            if score[i] <= 0:
                score[i] = 0

        return score

    def enemy_shoot():
        for i in range(enemy_number):
            if score[i+1] != 0:
                enemy_bullet = Enemy_Bullet(enemy[i].rect.centerx, enemy[i].rect.bottom)
                all_sprites.add(enemy_bullet)
                enemy_bullets.add(enemy_bullet)
                
    # 加入群組
    all_sprites.add(bg1,bg2)
    all_sprites.add(player)
    enemy_is_exist = [0]*enemy_number
    for i in range(enemy_number):
        all_sprites.add(enemy[i])
        enemy_is_exist[i] = True
    enemy_group.add(enemy)

    while running:
        # 敵人分數 == 0 => 刪掉敵人物件
        for i in range(enemy_number):
            if score[i+1] == 0:
                enemy[i].kill()
                enemy_is_exist[i] = False

        # 分數判斷
        score = getHit(score, enemy_is_exist)
    ```
