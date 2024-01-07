import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
screen_width = 800
screen_height = 600

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

# Создание игрового окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра")

# Размеры и скорость блока
block_size = 50
block_speed = 5

# Изначальный скин блока
block_skin = pygame.Surface((block_size, block_size))
block_skin.fill(white)

clock = pygame.time.Clock()


# Главное меню игры
def main_menu():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(1, block_size, block_speed)  # Легкий уровень сложности
                elif event.key == pygame.K_2:
                    game_loop(2, block_size, block_speed)  # Средний уровень сложности
                elif event.key == pygame.K_3:
                    game_loop(3, block_size, block_speed)  # Тяжелый уровень сложности

        screen.fill(black)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Главное меню", True, white)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))

        font = pygame.font.SysFont(None, 30)
        text = font.render("Нажмите 1, 2 или 3 для выбора уровня сложности", True, white)
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 + 50))

        pygame.display.update()
        clock.tick(15)


# Основной игровой цикл
def game_loop(difficulty, block_size, block_speed):
    block_x = screen_width // 2
    block_y = screen_height // 2

    game_over = False

    if difficulty == 1:
        move_distance = 50
    elif difficulty == 2:
        move_distance = 100
    elif difficulty == 3:
        move_distance = 150

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if block_x <= mouse_x <= block_x + block_size and block_y <= mouse_y <= block_y + block_size:
                    block_x += random.randint(-move_distance, move_distance)
                    block_y += random.randint(-move_distance, move_distance)

        # Проверка на столкновение с границами окна
        if block_x < 0:
            block_x = 0
        if block_x + block_size > screen_width:
            block_x = screen_width - block_size
        if block_y < 0:
            block_y = 0
        if block_y + block_size > screen_height:
            block_y = screen_height - block_size

        # Отрисовка на экране
        screen.fill(black)
        screen.blit(block_skin, (block_x, block_y))

        pygame.display.update()
        clock.tick(60)  # Ограничение частоты обновления экрана


# Запуск главного меню
main_menu()
