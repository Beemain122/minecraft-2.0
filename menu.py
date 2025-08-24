import pygame
import sys
import subprocess

pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("")

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)
input_font = pygame.font.SysFont(None, 30)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HOVER = (100, 100, 255)
GRAY = (50, 50, 50)
INPUT_BG = (40, 40, 40)

# Загрузка фона
try:
    bg = pygame.image.load("fon.jpg").convert()
    bg = pygame.transform.scale(bg, (width, height))
except Exception as e:
    print("Ошибка загрузки фона:", e)
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


# ==== Флаги состояния ====
current_screen = "main"  # main / connect

# ==== Поля ввода ====
input_host = InputBox(530, 230, 250, 35)
input_port = InputBox(530, 280, 250, 35)
input_nick = InputBox(530, 330, 250, 35)


# ==== Колбэки кнопок ====
def play_offline():
    try:
        subprocess.Popen(['python', 'main.py', 'localhost', '0', 'Player'])  # Параметры по умолчанию
        pygame.quit()
        sys.exit()
    except Exception as e:
        print("[Ошибка запуска main.py]:", e)


def open_connect_menu():
    global current_screen
    current_screen = "connect"


def run_game():
    host = input_host.text.strip()
    port = input_port.text.strip()
    nick = input_nick.text.strip()

    if host and port and nick:
        try:
            subprocess.Popen(['python', 'main.py', host, port, nick])
            pygame.quit()
            sys.exit()
        except Exception as e:
            print("[Ошибка запуска main.py]:", e)
    else:
        print("Все поля должны быть заполнены")


# ==== Кнопки ====
play_button = Button("Играть", 540, 300, 200, 50, play_offline)
connect_menu_button = Button("Подключиться к серверу", 440, 370, 400, 50, open_connect_menu)
exit_button = Button("Выйти", 540, 440, 200, 50, lambda: sys.exit())

connect_button = Button("Подключиться", 540, 400, 200, 50, run_game)
back_button = Button("Назад", 540, 470, 200, 50, lambda: switch_screen("main"))


def switch_screen(name):
    global current_screen
    current_screen = name


clock = pygame.time.Clock()
while True:
    window.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_screen == "main":
            play_button.handle_event(event)
            connect_menu_button.handle_event(event)
            exit_button.handle_event(event)
        elif current_screen == "connect":
            input_host.handle_event(event)
            input_port.handle_event(event)
            input_nick.handle_event(event)
            connect_button.handle_event(event)
            back_button.handle_event(event)

    # Рисуем интерфейс в зависимости от экрана
    if current_screen == "main":
        title = font.render("", True, WHITE)
        window.blit(title, (480, 150))
        play_button.draw(window)
        connect_menu_button.draw(window)
        exit_button.draw(window)

    elif current_screen == "connect":
        title = font.render("", True, WHITE)
        window.blit(title, (400, 100))

        labels = [("Хост:", 430, 230), ("Порт:", 430, 280), ("Ник:", 430, 330)]
        for txt, x, y in labels:
            window.blit(small_font.render(txt, True, WHITE), (x, y))

        input_host.draw(window)
        input_port.draw(window)
        input_nick.draw(window)
        connect_button.draw(window)
        back_button.draw(window)

    pygame.display.update()
    clock.tick(60)


