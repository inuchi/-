import pygame
import random
import time

# ウィンドウのサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WIDTH_CHAR=80
HEIGHT_CHAR =80
# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# スコアを保存するファイル名
SCORE_FILE = "scores.txt"

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

# ゲームの初期化
pygame.init()


# サウンドのロード
enemy_down_sound_1 = pygame.mixer.Sound('files/sound1.wav')
enemy_down_sound_2 = pygame.mixer.Sound('files/sound2.wav')
enemy_down_sound_3 = pygame.mixer.Sound('files/sound3.wav')
pygame.mixer.set_num_channels(16) 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ベジタブルウォーズ")
clock = pygame.time.Clock()

# フォントの設定
font = pygame.font.Font(None, 36)

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

# スコア表示
def draw_score(screen, score, gameover):
    if(gameover):
        # ゲームオーバー時に文字を表示
        font = pygame.font.SysFont(None, 136)
        text = font.render("Game Over", True, colorSCORE)
        posx = SCREEN_WIDTH // 2 - text.get_width() // 2
        posy = SCREEN_HEIGHT // 2 - text.get_height() // 2 -50
        screen.blit(text, (posx, posy))
        # 最後のスコア表示
        font = pygame.font.SysFont(None, 60) 
        text = font.render("score:"+str(score), True, colorSCORE)
        posx = SCREEN_WIDTH // 2 - text.get_width() // 2
        posy = SCREEN_HEIGHT // 2 - text.get_height() // 2 + 20
        screen.blit(text, (posx, posy))


        save_score(score)
        scores = load_scores()
        # ランキングを表示する関数
        scores.sort(reverse=True) # スコアを降順にソート
        rank=-1
        print("Ranking:")
        for i, rankscore in enumerate(scores):
            print("Rank {}: {}".format(i+1,rankscore))
            if((score ==rankscore) and (rank==-1)):
                rank = i+1
        # ランク表示
        font = pygame.font.SysFont(None, 60) 
        text = font.render("rank: "+str(rank)+" / "+str(len(scores)), True, colorSCORE)
        posx = SCREEN_WIDTH // 2 - text.get_width() // 2
        posy = SCREEN_HEIGHT // 2 - text.get_height() // 2 + 80
        screen.blit(text, (posx, posy))

    else:
        # 通常のスコア表示
        font = pygame.font.SysFont(None, 236) 
        text = font.render(str(score), True, colorSCORE)
        posx = SCREEN_WIDTH // 2 - text.get_width() // 2
        posy = SCREEN_HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (posx, posy))


#- - - - - - - - - - - -
# プレイヤーのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("files/ninjin4b.png") # プレイヤーの画像を読み込む
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        # 弾を撃つ処理をここに追加する
        pass

# 敵のクラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = pygame.image.load('files/nin-enemy5.png')
        self.size =size
        if size == 1:
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
        elif size == 2:
            self.image = pygame.transform.scale(self.image, (75, 75))
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)


# 敵の大きさに応じて音声を再生
def play_enemy_down_sound(enemy_size):
    if enemy_size == 1:
        enemy_down_sound_1.play()
        print("1")
    elif enemy_size == 2:
        enemy_down_sound_2.play()
        print("2")
    elif enemy_size == 3:
        enemy_down_sound_3.play()
        print("3")
        
# 弾のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('files/bullet.png')  # 弾の画像
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


#----------------------
# メイン 
# スプライトグループの作成
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(10):
    enemy_size = random.randint(1, 3)
    enemy = Enemy(enemy_size)
    all_sprites.add(enemy)
    enemies.add(enemy)

bullets = pygame.sprite.Group()


# ゲームループ
running = True
score = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    for bullet in bullets:
        if bullet.rect.bottom < 0:
            bullet.kill()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.speed_x = -5
    elif keys[pygame.K_RIGHT]:
        player.speed_x = 5
    else:
        player.speed_x = 0

    all_sprites.update()    
    #弾の衝突判定
    hits = pygame.sprite.groupcollide(enemies, bullets, False, True) # 第3引数を False に変更して敵を削除しないようにする
    for enemy in hits:
        enemy_size = enemy.size
        score += 1
        print("size= "+str(enemy_size)+", score= "+str(score))
        play_enemy_down_sound(enemy_size)
        enemy.rect.x = random.randrange(0, SCREEN_WIDTH - enemy.rect.width)
        enemy.rect.y = random.randrange(-100, -40)
        enemy.speed_y = random.randrange(1, 5)
    #自分の衝突判定
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    colorBG = (255,235,39)
    colorSCORE =(232,56,47)
    screen.fill(colorBG) # 背景を塗りつぶす
    
    
    all_sprites.draw(screen)

    if not running:
        # スコアの描画
        draw_score(screen, score, True) #game over

        # 1秒待機
        pygame.display.flip()
        time.sleep(1)

    else:
        screen.fill(colorBG) # 背景を塗りつぶす
        # スコアの描画
        draw_score(screen, score, False)
    
        all_sprites.draw(screen) # スプライトを描画する
    
        pygame.display.flip()
    
    clock.tick(60) # フレームレートを60に設定

print("end")
pygame.quit() # Pygameを終了する
