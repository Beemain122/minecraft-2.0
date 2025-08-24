import pygame
import socket
import sys

if len(sys.argv) < 4:
    print("Использование: python main.py HOST PORT NICK")
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
NICK = sys.argv[3]

sock = None
connected = False

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(NICK.encode('utf-8'))
    print(f"[Клиент] Подключён как {NICK} к {HOST}:{PORT}")
    connected = True
except Exception as e:
    print("[Ошибка подключения]:", e)

pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

grass_height = 60
player = pygame.Rect(50, height - 80 - grass_height, 40, 80)
player_speed = 5
gravity = 0.3
jump_strength = -6
player_y_speed = 0

bg_color = (100, 180, 255)
ground_color = (100, 250, 100)
player_color = (255, 255, 255)

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
    if keys[pygame.K_d]:
        player.x += player_speed

    player_y_speed += gravity
    player.y += player_y_speed

    if player.bottom >= height - grass_height:
        player.bottom = height - grass_height
        player_y_speed = 0

    window.fill(bg_color)
    pygame.draw.rect(window, ground_color, (0, height - grass_height, width, grass_height))
    pygame.draw.rect(window, player_color, player)

    pygame.display.update()

pygame.quit()

if connected:
    sock.close()
