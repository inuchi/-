import pygame
import random

# ウィンドウのサイズ
WIDTH = 800
HEIGHT = 600

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
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        # 弾を撃つ処理をここに追加する
        pass

# 敵のクラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy_veggie.png") # 敵の画像を読み込む
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)

# ゲームの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.shoot() # スペースキーで弾を撃つ

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

    all_sprites.update() # スプライトの更新
    hits = pygame.sprite.spritecollide(player, enemies, False) # プレイヤーと敵の衝突判定
    if hits:
        running = False # プレイヤーが敵と衝突した場合はゲームオーバー

    screen.fill(WHITE) # 背景を白で塗りつぶす
    all_sprites.draw(screen) # スプライトを描画する
    pygame.display.flip() # 画面を更新する
    clock.tick(60) # フレームレートを60に設定

pygame.quit() # Pygameを終了する
