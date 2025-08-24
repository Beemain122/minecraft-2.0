import pygame
import sys
import subprocess
import threading

pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minecraft - Меню")

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)
input_font = pygame.font.SysFont(None, 30)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOVER = (100, 100, 255)
GRAY = (50, 50, 50)
INPUT_BG = (40, 40, 40)

# Фон
try:
    bg = pygame.image.load("fon.jpg").convert()
    bg = pygame.transform.scale(bg, (width, height))
except:
    bg = pygame.Surface((width, height))
    bg.fill((30, 30, 30))


class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = HOVER if self.hovered else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.txt_surface = input_font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:
                    self.text += event.unicode
            self.txt_surface = input_font.render(self.text, True, WHITE)

    def draw(self, surface):
        pygame.draw.rect(surface, INPUT_BG, self.rect, border_radius=5)
        surface.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))
        if self.active:
            pygame.draw.rect(surface, BLUE, self.rect, 2, border_radius=5)


# ===== Состояние
current_screen = "main"  # main, connect, loading
error_message = ""


def switch_screen(name):
    global current_screen, error_message
    current_screen = name
    error_message = ""


# ===== Поля ввода
input_host = InputBox(530, 230, 250, 35)
input_port = InputBox(530, 280, 250, 35)
input_nick = InputBox(530, 330, 250, 35)


# ===== Кнопки
def open_connect_menu():
    switch_screen("connect")

def back_to_main():
    switch_screen("main")

def try_connect():
    global error_message
    host = input_host.text.strip()
    port = input_port.text.strip()
    nick = input_nick.text.strip()

    if host and port and nick:
        switch_screen("loading")
        threading.Thread(target=connect_to_server, args=(host, port, nick), daemon=True).start()
    else:
        error_message = "Все поля должны быть заполнены"

def connect_to_server(host, port, nick):
    global error_message
    try:
        subprocess.Popen(['python', 'main.py', host, port, nick])
        pygame.quit()
        sys.exit()
    except Exception as e:
        error_message = f"Ошибка подключения: {e}"
        switch_screen("connect")


# Кнопки меню
play_button = Button("Играть", 540, 300, 200, 50, lambda: subprocess.Popen(['python', 'main.py', 'localhost', '0', 'Player']) or sys.exit())
connect_button_main = Button("Подключиться к серверу", 440, 370, 400, 50, open_connect_menu)
exit_button = Button("Выйти", 540, 440, 200, 50, lambda: sys.exit())

# Кнопки подключения
connect_button = Button("Подключиться", 540, 400, 200, 50, try_connect)
back_button = Button("Назад", 540, 470, 200, 50, back_to_main)


# ===== Главный цикл
clock = pygame.time.Clock()

while True:
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_screen == "main":
            play_button.handle_event(event)
            connect_button_main.handle_event(event)
            exit_button.handle_event(event)
        elif current_screen == "connect":
            input_host.handle_event(event)
            input_port.handle_event(event)
            input_nick.handle_event(event)
            connect_button.handle_event(event)
            back_button.handle_event(event)

    # Отрисовка
    if current_screen == "main":
        window.blit(bg, (0, 0))
        title = font.render("Minecraft - Меню", True, WHITE)
        window.blit(title, (480, 150))
        play_button.draw(window)
        connect_button_main.draw(window)
        exit_button.draw(window)

    elif current_screen == "connect":
        window.blit(bg, (0, 0))
        title = font.render("Подключение к серверу", True, WHITE)
        window.blit(title, (400, 100))

        labels = [("Хост:", 430, 230), ("Порт:", 430, 280), ("Ник:", 430, 330)]
        for txt, x, y in labels:
            window.blit(small_font.render(txt, True, WHITE), (x, y))

        input_host.draw(window)
        input_port.draw(window)
        input_nick.draw(window)
        connect_button.draw(window)
        back_button.draw(window)

        if error_message:
            err_surf = small_font.render(error_message, True, (255, 0, 0))
            window.blit(err_surf, (400, 520))

    elif current_screen == "loading":
        window.fill((0, 0, 0))
        loading_text = font.render("Поиск игроков...", True, WHITE)
        tr = loading_text.get_rect(center=(width // 2, height // 2))
        window.blit(loading_text, tr)

    pygame.display.update()
    clock.tick(60)
