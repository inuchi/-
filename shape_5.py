import pygame
import math
import time

# pygameの初期化
pygame.init()

# ウィンドウのサイズ
window_width = 400
window_height = 400

# ウィンドウの作成
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("上向きのバラン")

# 三角形の頂点を計算
center_x = window_width // 2
center_y = window_height // 2
triangle_height = 100
triangle_base = 100
triangle_top_x = center_x - triangle_base // 2  # 三角形の頂点のx座標
triangle_top_y = center_y - triangle_height  # 三角形の頂点のy座標
if 0:
    vertices = [
        (triangle_top_x, triangle_top_y),  # 上の頂点
        (center_x - triangle_base // 2, center_y),  # 左下の頂点
        (center_x + triangle_base // 2, center_y),  # 右下の頂点
    ]
else:
    vertices = [(10,0), (20,14),(30,0),(40,14),(50,0),(46,35),(14,35)]
    #
    #          (10,0)       (30,0)        (50,0)
    #         
    #         (10,14)   (20,14)    (40,14)
    #
    #          (14,35)                  (46,35)
    #
    #
    
    
pos=(0,0)
speed=(6,2.3)
# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 画面のクリア
    screen.fill((255, 255, 255))
    # 位置をセット
    pos = (pos[0]+speed[0], pos[1]+speed[1])
    # 反射の判定
    if((pos[0]>(window_width-45))or(pos[0]<-15)):    # -1
        speed = (speed[0]*-1, speed[1])
    if((pos[1]>(window_height-30))or(pos[1]<-5)):
        speed = (speed[0], speed[1]*-1)
    
    dx = pos[0]
    dy = pos[1]
    cur_vertices = []
    for vertex in vertices:
        cur_x = vertex[0] + dx
        cur_y = vertex[1] + dy
        cur_vertices.append((cur_x, cur_y))
    #print(cur_vertices)
    #print(vertices)
    #print(pos)
    #print(dx)
    #print(dy)
    #print("----")
    # 三角形の描画
    pygame.draw.polygon(screen, (0, 0, 0), cur_vertices)
    time.sleep(0.02)
    # 画面の更新
    pygame.display.flip()

# pygameの終了
pygame.quit()
