import pygame
from pygame.locals import *
from random import randint
from pygame import sprite, transform, image
import sys

# Инициализация
pygame.init()

# Константы
win_width = 500
win_height = 500
FPS = 60
BG_COLOR = (200, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размеры платформы (увеличил толщину)
PLATFORM_WIDTH = 25      # было 15, теперь 25 (толще)
PLATFORM_HEIGHT = 100    # высота осталась та же
BALL_SIZE = 20

# Создание окна
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

# Шрифт для счёта
font = pygame.font.Font(None, 36)

# Загрузка изображений
try:
    platform_img = image.load("platform.png")
    ball_img = image.load("Ball.png")
except Exception as e:
    print("Ошибка загрузки картинок:", e)
    print("Убедись, что файлы platform.png и Ball.png лежат в папке со скриптом")
    pygame.quit()
    sys.exit()

# Масштабируем картинки под нужные размеры
platform_img = transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
ball_img = transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

# Класс платформы (ракетки)
class Racket(sprite.Sprite):
    def __init__(self, x, y, speed, up_key, down_key):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up_key] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.y < win_height - PLATFORM_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс мяча
class Ball(sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__()
        self.image = ball_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней стены
        if self.rect.y <= 0 or self.rect.y >= win_height - BALL_SIZE:
            self.speed_y = -self.speed_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def reset_position(self):
        self.rect.x = win_width // 2 - BALL_SIZE // 2
        self.rect.y = win_height // 2 - BALL_SIZE // 2
        self.speed_x = -self.speed_x

# Создание объектов
# Учитываем новую ширину платформы при расстановке
left_racket = Racket(20, win_height // 2 - PLATFORM_HEIGHT // 2, 7, K_w, K_s)
right_racket = Racket(win_width - 20 - PLATFORM_WIDTH, win_height // 2 - PLATFORM_HEIGHT // 2, 7, K_UP, K_DOWN)
ball = Ball(win_width // 2 - BALL_SIZE // 2, win_height // 2 - BALL_SIZE // 2, 4, 4)

# Счёт
left_score = 0
right_score = 0
game_over = False
winner = ""

# Игровой цикл
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if game_over and event.key == K_r:
                # Перезапуск игры
                game_over = False
                left_score = 0
                right_score = 0
                ball.reset_position()
                ball.speed_x = 4 if ball.speed_x > 0 else -4
                ball.speed_y = 4
                left_racket.rect.y = win_height // 2 - PLATFORM_HEIGHT // 2
                right_racket.rect.y = win_height // 2 - PLATFORM_HEIGHT // 2

    if not game_over:
        # Обновление
        left_racket.update()
        right_racket.update()
        ball.update()

        # Проверка столкновения с левой ракеткой
        if ball.rect.colliderect(left_racket.rect):
            ball.speed_x = -ball.speed_x
            ball.rect.x = left_racket.rect.x + PLATFORM_WIDTH

        # Проверка столкновения с правой ракеткой
        if ball.rect.colliderect(right_racket.rect):
            ball.speed_x = -ball.speed_x
            ball.rect.x = right_racket.rect.x - BALL_SIZE

        # Проверка гола
        if ball.rect.x <= 0:
            right_score += 1
            ball.reset_position()
            if right_score >= 5:
                game_over = True
                winner = "Игрок 2 (Правый)"

        if ball.rect.x >= win_width - BALL_SIZE:
            left_score += 1
            ball.reset_position()
            if left_score >= 5:
                game_over = True
                winner = "Игрок 1 (Левый)"

    # Отрисовка
    window.fill(BG_COLOR)
    left_racket.draw()
    right_racket.draw()
    ball.draw()

    # Счёт
    left_text = font.render(str(left_score), True, BLACK)
    right_text = font.render(str(right_score), True, BLACK)
    window.blit(left_text, (win_width // 4, 20))
    window.blit(right_text, (win_width * 3 // 4, 20))

    # Конец игры
    if game_over:
        game_over_text = font.render(f"Игра окончена! {winner} победил!", True, BLACK)
        restart_text = font.render("Нажми R для перезапуска", True, BLACK)
        window.blit(game_over_text, (win_width // 2 - game_over_text.get_width() // 2, win_height // 2 - 40))
        window.blit(restart_text, (win_width // 2 - restart_text.get_width() // 2, win_height // 2 + 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()