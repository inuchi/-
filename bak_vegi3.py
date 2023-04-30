import pygame
import random
import time
import math


#- - - - - - - - - - - -
# スコアを保存する関数
def save_score(score):
    with open(SCORE_FILE, "a") as file:
        file.write(str(score) + "\n")

# スコアを読み込む関数
def load_scores():
    scores = []
    try:
        with open(SCORE_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                score = int(line.strip())
                scores.append(score)
    except FileNotFoundError:
        pass
    return scores

#- - - - - - - - - - - -
# 敵の大きさに応じて音声を再生
def play_enemy_down_sound(enemy_size):
    try:
        if enemy_size == 1:
            enemy_down_sound_1.play()
        elif enemy_size == 2:
            enemy_down_sound_2.play()
        elif enemy_size == 3:
            enemy_down_sound_3.play()
        else:
            raise ValueError("Invalid enemy size: {}".format(enemy_size))
    except ValueError as ve:
        print("エラーが発生しました: {}".format(ve))
        # ここでエラーの処理を行う (例: デフォルトのサウンドを再生する、ログにエラー情報を出力するなど)

#- - - - - - - - - - - -
# スコア表示
def draw_score(screen, goodscore, badscore, gameover):
    if(gameover):
        # ゲームオーバー時に文字を表示
        font = pygame.font.SysFont(None, 136)
        text = font.render("Game Over", True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 -50
        screen.blit(text, (posx, posy))
        # プラス/マイナススコア表示
        font = pygame.font.SysFont(None, 80) 
        if(badscore<0):
            text = font.render("score:"+str(goodscore)+str(badscore), True, colorSCORE_inner)
        else:
            text = font.render("score:"+str(goodscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 + 20
        screen.blit(text, (posx, posy))
        # スコアを保存, 読み出し
        totalscore = goodscore - badscore
        save_score(totalscore)
        scores = load_scores()
        # ランキングを表示する
        scores.sort(reverse=True) # スコアを降順にソート
        rank=-1
        #print("Ranking:")
        for i, rankscore in enumerate(scores):
            #print("Rank {}: {}".format(i+1,rankscore))
            if((totalscore ==rankscore) and (rank==-1)):
                rank = i+1
        # ランク表示
        font = pygame.font.SysFont(None, 60) 
        text = font.render("rank: "+str(rank)+" / "+str(len(scores)), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 + 80
        screen.blit(text, (posx, posy))

    else:
        # 通常のスコア表示
        font = pygame.font.SysFont(None, 236) 
        text = font.render(str(goodscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 2 - text.get_height() // 2 - 80
        screen.blit(text, (posx, posy))
        # 落下到達したスコア
        text = font.render(str(badscore), True, colorSCORE_inner)
        posx = WIDTH_OF_SCREEN // 2 - text.get_width() // 2
        posy = HEIGHT_OF_SCREEN // 4 * 3 - text.get_height() // 2
        screen.blit(text, (posx, posy))


#- - - - - - - - - - - - - - - - - - - - - - - - - - - -
# プレイヤーのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("files/ninjin4b.png") # プレイヤーの画像を読み込む
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.centery = HEIGHT_OF_SCREEN
        self.speed_y = 0

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.center < 0:
            self.rect.center = 0
        if self.rect.center > HEIGHT_OF_SCREEN:
            self.rect.center = WIDTH_OF_SCREEN

    def shoot(self):
        # 弾を撃つ処理をここに追加する
        pass

# 敵のクラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, size):
        super().__init__()
        self.type = type
        #----
        if(type == 1):
            self.image = pygame.image.load('files/nin-enemy5.png')
        else:
            # self.image = pygame.image.load('files/blockoly-3c.png')
            self.image = pygame.image.load('files/blockoly-5.png')            
        #----
        self.size = size
        if size == 1:
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
        elif size == 2:
            self.image = pygame.transform.scale(self.image, (75, 75))
            self.rect = self.image.get_rect()
        else:            
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()

        print("type="+str(type)+" size="+str(size))
        self.rect.x = WIDTH_OF_SCREEN
        self.rect.y = random.randrange(0+10, HEIGHT_OF_SCREEN-10)   # 画面両端にマージン
        self.speed_x = random.randrange(1, 5)
    def updateEnemy(self):
        # （bad スコア更新のために）敵の位置もここで更新する
        if(self.type == 1): # 敵の種類
            self.rect.x -= self.speed_x # 位置更新
        else:   
            if(self.size==1):   # 小さい
                self.rect.x += self.speed_x
            elif(self.size==2): # 中サイズ
                self.rect.x += self.speed_x
            else:   # 大きい
                self.rect.x += self.speed_x
                self.rect.x += math.sin(self.rect.x*0.1)*5
        if self.rect.x < 0:
            self.rect.x = WIDTH_OF_SCREEN
            self.rect.y = random.randrange(0+10, HEIGHT_OF_SCREEN-10)   # +位置調整
            self.speed_x = random.randrange(-5, -1)
            return -1
        else:
            return 0
        # 
        #(0,0) ------------------------------------------------------------------(WIDTH_OF_SCREEN, 0)
        #                                      <=enemy
        #                                    (+=speed_x)
        # player
        # (+=speed_y)
        #
        #(0, HEIGHT_OF_SCREEN)-------------------------------------(WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN)
        totalminusscore = minusscore-1
    def update(self):
        return  # なにもしない

# 敵の大きさに応じて音声を再生
def play_enemy_down_sound(enemy_size):
    if enemy_size == 1:
        enemy_down_sound_1.play()
    elif enemy_size == 2:
        enemy_down_sound_2.play()
    elif enemy_size == 3:
        enemy_down_sound_3.play()
        
# 通常弾のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, wide=0, speed_x=0, speed_y=0):
        super().__init__()
        self.image_org = pygame.image.load('files/bullet-Lw.png')  # 弾の画像
        resized_image = pygame.transform.scale(self.image_org, (10,10))
        self.image = resized_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.initial_x = x
        if((speed_x==0)and(speed_y==0)):
            self.speed_y = -5   # speed(0,0)(=停止)は上向きに
        else:
            self.speed_y = speed_y
        self.speed_x = speed_x
        self.wide = wide

    def update(self):
        if(self.wide!=0):
            dx = math.sin(self.rect.y / 100 * 2* math.pi) *self.wide
            self.rect.centerx = self.initial_x + dx
            self.rect.centery += self.speed_y
        else:
            self.rect.centerx += self.speed_x
            self.rect.centery += self.speed_y
        if(self.rect.y < 0):
            self.kill()
# 拡散弾のクラス
class SplashBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, z, wide=0, numofbullet=3):
        super().__init__()        
        self.image_org =  pygame.image.load('files/bullet-Lw.png')  # 弾の画像
        self.image = pygame.transform.scale(self.image_org, (20+z, 20+z))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.straightx = x  #直進時の軌道
        self.pos_z = 0
        self.speed_y = -1.5
        self.speed_z = 1
        self.accel_z = -0.02
        self.numofbullet = numofbullet
        self.timer = 0
        self.wide = wide
    def update(self):
        if((self.timer>0)and(self.pos_z<0.1)):
            #spread
            i=0
            while(i<self.numofbullet):
                rx = random.randrange(-10,10)
                ry = random.randrange(-10,10)
                bullet = Bullet(self.rect.centerx, self.rect.centery, 0, rx, ry )
                all_sprites.add(bullet)
                bullets.add(bullet)
                i+=1
    
        if(self.pos_z>=0):
            self.rect.centery += self.speed_y        
            z = self.pos_z
            v = self.speed_z
            a = self.accel_z
            self.pos_z += v
            self.speed_z += a 
            #self.accel_z = a # same
            self.image = pygame.transform.scale(self.image_org, (20+z, 20+z))
            # ゆらゆら
            if(self.speed_z<0): # 下に落ちるときだけ
                dx = math.sin(self.speed_z / 100* math.pi) * self.wide
                self.rect.centerx = self.straightx +dx
            # すすむ
            self.rect.centery += self.speed_y 
            self.timer += 1    
        else:
            self.kill()


# パワーアップ豆のクラス
class Bean(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if(type==0):
            # bad
            self.image = pygame.image.load("files/beans4_bad_s.png").convert_alpha()  # 豆の画像を読み込み
            self.type=-1
        else:
            # good
            self.image = pygame.image.load("files/beans_s.png").convert_alpha()  # 豆の画像を読み込み
            self.type=1
        self.rect = self.image.get_rect()
        self.speed_y = 3 # 仮


    def update(self):
        self.rect.y += self.speed_y  # 豆の落下速度
        if(self.rect.y > SCREEN_HEIGHT):
            self.kill()
#---------------------------------------------
# メイン 
#---------------------------------------------
if __name__ == '__main__':

    # ゲームの初期化
    pygame.init()

    # サウンドのロード
    enemy_down_sound_1 = pygame.mixer.Sound('files/sound1.wav')
    enemy_down_sound_2 = pygame.mixer.Sound('files/sound2.wav')
    enemy_down_sound_3 = pygame.mixer.Sound('files/sound3.wav')
    pygame.mixer.set_num_channels(16) 

    # ウィンドウのサイズ
    WIDTH_OF_SCREEN = 800
    HEIGHT_OF_SCREEN= 600

    # スコアを保存するファイル名
    SCORE_FILE = "scores.txt"
    screen = pygame.display.set_mode((WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN))
    pygame.display.set_caption("ベジタブルウォーズ")
    clock = pygame.time.Clock()

    # フォントの設定
    font = pygame.font.Font(None, 36)

    # 色の定義
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    # 描画色
    colorBG = (6,26,50)
    #colorSCORE_outer =(
    colorSCORE_outer = ((0,155,155),(33,188,188),(66,200,200),(155,0,250),(244,247,249),(44,248,252),(33,247,249),(155,248,252),(160,247,249),(155,248,252))
    #colorSCORE_inner = (201,243,247)
    colorSCORE_inner = (155,243,247)

    # スプライトグループの作成
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    beans = pygame.sprite.Group()

    # プレイヤーの生成
    player = Player()
    all_sprites.add(player)

    # 敵の生成
    for i in range(10):
        enemy_type = random.randint(1, 3)
        enemy_size = random.randint(1, 4)
        enemy = Enemy(enemy_type, enemy_size)
        all_sprites.add(enemy)
        enemies.add(enemy)



    # ゲームループ
    running = True
    player_powered_up = 0
    good_score = 0
    bad_score = 0
    while running:
        # キー操作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 通常弾発射
                    bullet = Bullet(player.rect.right, player.rect.centery)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    # パワーアップ弾発射
                    if(player_powered_up==1):
                        bullet = Bullet(player.rect.right, player.rect.centery,8)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    elif(player_powered_up ==2):
                        bullet = Bullet(player.rect.right, player.rect.centery-5,12)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        bullet = Bullet(player.rect.right, player.rect.centery+5,-12)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    elif(player_powered_up ==3):
                        bullet = Bullet(player.rect.right, player.rect.centery-10,17)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        bullet = Bullet(player.rect.right, player.rect.centery+10,-17)
                        all_sprites.add(bullet)
                    elif(player_powered_up >3):
                        x=player.rect.right
                        y=player.rect.centery
                        z=0
                        wide = 30   # ゆらゆらの幅
                        bullet_num = player_powered_up  # 拡散弾の数
                        bullet = SplashBullet(x, y, z, wide, bullet_num)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                                       
        # 弾が上端まで到達したら消去
        for bullet in bullets:
            if bullet.rect.right < 0:
                bullet.kill()
        # 左右キー操作
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.speed_y = -5
        elif keys[pygame.K_DOWN]:
            player.speed_y = 5
        else:
            player.speed_y = 0

        # 全部更新
        all_sprites.update()    
        #弾の衝突判定
        # スプライトの画像を読み込み
        #sprite_image = pygame.image.load("files/nin-enemy5.png").convert_alpha()
        # スプライトの画像からマスクを生成
        #sprite_mask = pygame.mask.from_surface(sprite_image)
        #if sprite_mask.overlap(target_mask, sprite_mask):

        # Circle(丸)同士で比較
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True, pygame.sprite.collide_circle_ratio(0.75))
        # 判定結果を反映
        for enemy in hits:
            # 弾があたった
            enemy_size = enemy.size
            good_score += 1
    #        print("size= "+str(enemy_size)+", score= "+str(score))
            play_enemy_down_sound(enemy_size)
            # 敵が size = 2 のときだけ
            if(enemy.size==2):
                bonus = random.randrange(0, 20)
                print("bonus rand-value: "+str(bonus))
                if(bonus <3):
                    print("(added)")
                    # パワーアップ豆を追加
                    bean = Bean(bonus)
                    bean.rect.x = enemy.rect.x
                    bean.rect.y = enemy.rect.y
                    bean.speed_x = enemy.speed_x / 3 + 1
                    beans.add(bean)
                    all_sprites.add(bean)
            # 敵は再利用して右から出す
            enemy.kill()
            type = random.randrange(1, 3)
            size = random.randrange(1, 4)
            # size とtype は更新
            enemy_new = Enemy(type, size)
            speed_x = random.randrange(1, 5)
            all_sprites.add(enemy_new)
            enemies.add(enemy_new)

        # 自分と敵との衝突判定
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            # 敵にあたったらゲーム終了
            running = False
        # 自分とパワーアップ豆との当たり判定（パワーアップするかどうか）
        for bean in beans:
            if bean.rect.colliderect(player.rect):
                if(bean.type==-1):
                    min = 0
                    if(player_powered_up > min):
                        player_powered_up -= 1 # パワーダウン
                        print("(down) current power= "+str(player_powered_up)+"")
                else:
                    max = 10
                    if(player_powered_up < max):
                        player_powered_up += 1 # パワーアップ
                        print("(up) current power= "+str(player_powered_up))
                bean.kill()
        # badscore の更新
        for enemy in enemies:
            curPoint = enemy.updateEnemy()
            bad_score += curPoint
            if(curPoint < 0):
                print("bad: " + str(bad_score)+", "+str(curPoint))
        # 描画
        screen.fill(colorBG) # 背景を塗りつぶす
        
        # 再描画
        all_sprites.draw(screen)

        # スコア表示
        if not running:
            # スコアを描画して終了
            draw_score(screen, good_score, bad_score, True) #game over
            pygame.display.flip()
            # 1秒待機
            time.sleep(3)

        else:
            # 背景
            screen.fill(colorBG)
            # スコアの描画
            draw_score(screen, good_score, bad_score, False)
            # スプライトも表示    
            all_sprites.draw(screen) # スプライトを描画する
            pygame.display.flip()
        
        clock.tick(60) # フレームレートを60に設定

    print("end")
    pygame.quit() # Pygameを終了する
