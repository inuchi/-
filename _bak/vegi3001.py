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

# プレイヤーのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player_carrot.png") # プレイヤーの画像を読み込む
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
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy_veggie.png") # 敵の画像を読み込む
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)

# 弾のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')  # 弾の画像
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# ゲームの初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ベジタブルウォーズ")
clock = pygame.time.Clock()

# スプライトグループの作成
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

bullets = pygame.sprite.Group()


# ゲームループ
running = True
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

    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    screen.fill(WHITE)
    all_sprites.draw(screen)

    if not running:
        # ゲームオーバー時に文字を表示
        font = pygame.font.SysFont(None, 36)
        text = font.render("Game Over", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        # 1秒待機
        pygame.display.flip()
        time.sleep(1)

    pygame.display.flip()

    screen.fill(WHITE) # 背景を白で塗りつぶす
    all_sprites.draw(screen) # スプライトを描画する
    pygame.display.flip() # 画面を更新する
    clock.tick(60) # フレームレートを60に設定

print("end")
pygame.quit() # Pygameを終了する
