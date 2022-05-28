# 固定時間射出子彈 + 爆炸動畫(2022.05.29)

1. ###### 敵方在固定時間射出子彈
    * ###### 設定子彈射出間隔時間、數量
        ```python
        enemy_number = 3
        enemy_shoot_time = 100
        ```
    * ###### 遊戲迴圈 => 控制子彈射出
        ```python
        enemy_shoot_time -= 1
        if enemy_shoot_time <= 0:
            for i in range(enemy_number):
                enemy[i].shoot()
            enemy_shoot_time = 100
        ```

2. ###### 爆炸動畫
    1. ###### 建立動畫字典
        ```python
        expl_anim = {}
        expl_anim['lg'] = []
        expl_anim['sm'] = []
        ```
    2. ###### 匯入爆炸圖片
        ```python
        for i in range(9):
            expl_img = pygame.image.load(os.path.join("img", f'expl{i}.png')).convert()
            expl_img.set_colorkey(BLACK)
            expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
            expl_anim['sm'].append(pygame.transform.scale(expl_img, (40, 40)))
        ```
    3. ###### 建立爆炸物件
        > ###### self.frame：更新到第幾張圖片
        > ###### self.last_update = pygame.time.get_ticks()：紀錄最後更新圖片的時間
        > ###### self.frame_rate：經過幾毫秒更新圖片
        ```python     
        class Explosion(pygame.sprite.Sprite):
            def __init__(self, center, size):
                pygame.sprite.Sprite.__init__(self)
                self.size = size
                self.image = expl_anim[self.size][0]
                self.rect = self.image.get_rect()
                self.rect.center  = center
                self.frame = 0
                self.last_update = pygame.time.get_ticks()
                self.frame_rate = 50
        ```
        > ###### 圖片更新間隔 > 自己設定的 frame_rate => 更新至下張圖
        > ###### if 圖片動畫撥放完 => kill
        > ###### else 設定下張圖片的爆炸位子
        ```python     
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
        ```
    4. ###### 在新增爆炸至遊戲
        > ###### player or enemy 被子彈射中 => 小爆炸
        > ###### player and enemy 互撞 => 大爆炸 => 遊戲結束(玩家輸)
        ```python  
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
        ```

