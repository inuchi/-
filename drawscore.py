import pygame
import time

# pygameの初期化
pygame.init()

# ウィンドウのサイズ
window_width = 400
window_height = 400

# ウィンドウの作成
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("スコア表示")

# フォントの設定
font = pygame.font.Font(None, 36)

# スコアの初期値
score = 0


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


colorBG = (255,235,39)
colorSCORE =(232,56,47)
def draw_score(screen, score):
    """スコアを描画する関数"""
    score_text = font.render("スコア: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

# スコア表示
def draw_score2(screen, score, gameover):
    """スコアを描画する関数"""
    font = pygame.font.SysFont(None, 136)
    score_text = font.render("score: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    if(1):
        if(gameover):
            # ゲームオーバー時に文字を表示
            font = pygame.font.SysFont(None, 136)
            text = font.render("Game Over", True, colorSCORE)
            posx = SCREEN_WIDTH // 2 - text.get_width() // 2
            posy = SCREEN_HEIGHT // 2 - text.get_height() // 2

            screen.blit(text, (posx, posy))
        else:
            font = pygame.font.SysFont(None, 236) 
            text = font.render(str(score), True, colorSCORE)
            posx = SCREEN_WIDTH // 2 - text.get_width() // 2
            posy = SCREEN_HEIGHT // 2 - text.get_height() // 2
            screen.blit(text, (posx, posy))


# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面のクリア
    screen.fill((255, 255, 255))

    # スコアの描画
    #draw_score(screen, score)
    draw_score2(screen, score, False)

    # 画面の更新
    pygame.display.flip()

    # スコアの更新
    score += 1

    # 一定時間待機
    time.sleep(0.1)

# pygameの終了
pygame.quit()
