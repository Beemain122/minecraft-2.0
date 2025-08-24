import pygame
import socket
import sys

# ===== Получаем параметры из командной строки: HOST, PORT, NICK
if len(sys.argv) < 4:
    print("Использование: python main.py HOST PORT NICK")
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]

# ===== Попытка подключения к серверу
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(NICK.encode())
    print(f"[CLIENT] Подключён как {NICK}")
except Exception as e:
    print("[Ошибка подключения]:", e)
    sock = None

# ===== Инициализация Pygame и загрузка изображений
pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

grass_height = 60
player_speed = 5
gravity = 0.3
jump_strength = -6
player = pygame.Rect(50, height - 80 - grass_height, 40, 80)
player_y_speed = 0

level = 1
show_text = True
text_timer = 0

# Загрузка изображений из папки assets
bg1 = pygame.image.load("mur.jpg").convert()
bg1 = pygame.transform.scale(bg1, (width, height))
bg2 = pygame.image.load("ad.jpg").convert()
bg2 = pygame.transform.scale(bg2, (width, height))

grass1 = pygame.image.load("dern.jpg").convert_alpha()
grass1 = pygame.transform.scale(grass1, (width, grass_height))
grass2 = pygame.image.load("nezer.jpg").convert_alpha()
grass2 = pygame.transform.scale(grass2, (width, grass_height))

player_stand = pygame.image.load("stend.jpg").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (40, 80))

player_right_frames = [pygame.transform.scale(pygame.image.load("right.jpg").convert_alpha(), (40, 80))]
player_left_frames = [pygame.transform.scale(pygame.image.load("left.jpg").convert_alpha(), (40, 80))]

direction = 'stand'
frame_index = 0
animation_timer = 0
animation_speed = 150

def draw_cloud(surface, x, y):
    pygame.draw.circle(surface, (255, 255, 255), (x, y), 20)
    pygame.draw.circle(surface, (255, 255, 255), (x + 25, y + 10), 25)
    pygame.draw.circle(surface, (255, 255, 255), (x + 55, y + 5), 20)
    pygame.draw.circle(surface, (255, 255, 255), (x + 40, y - 15), 20)
    pygame.draw.circle(surface, (255, 255, 255), (x + 15, y - 10), 15)

cloud_positions = [(50, 100), (150, 90), (250, 80), (350, 110), (450, 95), (550, 120), (650, 85), (750, 105)]

running = True
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            if player.bottom >= height - grass_height:
                player_y_speed = jump_strength

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= player_speed
        direction = 'left'
    elif keys[pygame.K_d]:
        player.x += player_speed
        direction = 'right'
    else:
        direction = 'stand'
        frame_index = 0

    player.y += (player_y_speed := player_y_speed + gravity if True else 0) or 0
    if player.bottom >= height - grass_height:
        player.bottom = height - grass_height
        player_y_speed = 0

    if player.x + player.width >= width and level == 1:
        level = 2
        show_text = True
        text_timer = 0
        player.x = 0
        player.y = height - 80 - grass_height

    if show_text:
        text_timer += dt
        if text_timer > 5000:
            show_text = False

    if level == 1:
        window.blit(bg1, (0, 0))
        window.blit(grass1, (0, height - grass_height))
        for pos in cloud_positions:
            draw_cloud(window, pos[0], pos[1])
    else:
        window.blit(bg2, (0, 0))
        window.blit(grass2, (0, height - grass_height))

    if direction == 'right':
        animation_timer = (animation_timer + dt) % (animation_speed * len(player_right_frames))
        frame_index = (frame_index + (1 if animation_timer < dt else 0)) % len(player_right_frames)
        window.blit(player_right_frames[frame_index], (player.x, player.y))
    elif direction == 'left':
        animation_timer = (animation_timer + dt) % (animation_speed * len(player_left_frames))
        frame_index = (frame_index + (1 if animation_timer < dt else 0)) % len(player_left_frames)
        window.blit(player_left_frames[frame_index], (player.x, player.y))
    else:
        window.blit(player_stand, (player.x, player.y))

    if show_text:
        level_text = "Мир" if level == 1 else "Ад"
        ts = font.render(level_text, True, (0, 0, 213))
        tr = ts.get_rect(center=(width // 2, height // 4))
        window.blit(ts, tr)

    pygame.display.update()

pygame.quit()
if sock:
    sock.close()

