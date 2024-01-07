import sys
import pygame
import sys
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 5
        self.finding_num = 1
        self.ticks = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surface):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(surface, pygame.Color('black'), 
                                 (self.left + self.cell_size * x,
                                  self.top + self.cell_size * y,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        column = (x - self.left) // self.cell_size
        raw = (y - self.top) // self.cell_size
        if 0 <= column < self.width and 0 <= raw < self.height:
            return raw, column
        return None

    def check(self, cell):
        pass

    def get_click(self, mouse_pos, surface):
        cell = self.get_cell(mouse_pos)
        self.check(cell, surface)

class Shulte(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
    
    def spawn(self, surface):
        global ticks
        sample_of_number = random.sample(range(1, self.width * self.height + 1), self.width * self.height)
        number = 0
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = sample_of_number[number]
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(str(sample_of_number[number]), False, (255, 0, 0))
                surface.blit(text, (x * self.cell_size, y * self.cell_size))
                number += 1
        super().render(surface)

    def render(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(str(self.board[y][x]), False, (pygame.color.Color('black')))
                surface.blit(text, (self.left + 5 + x * self.cell_size, self.top + 5 + y * self.cell_size))
        font = pygame.font.Font(None, self.left)
        text = font.render(str(self.finding_num), False, (pygame.color.Color('black')))
        surface.blit(text, (self.left - self.cell_size, 30))
        self.time(self.ticks, surface)
        super().render(surface)

    def check(self, cell, surface):
        if cell:
            y, x = cell
            if self.board[y][x] == self.finding_num:
                self.finding_num += 1
        if self.finding_num == self.width * self.height + 1:
            file = open('log.txt', mode='w')
            file.writelines([str(self.ticks // 60)])
            file.close()
            self.finding_num = 1
            self.spawn(surface)
            self.ticks = 0

    def time(self, time, surface):
        font = pygame.font.Font(None, self.left)
        text = font.render(str(time // 60), False, (pygame.color.Color('black')))
        surface.blit(text, (self.width * self.cell_size + self.left, 30))

def startShulte(si):
    board = Shulte(si, si)
    board.set_view(100, 100, 50)
    width = board.left * 2 + board.width * board.cell_size
    height = board.top * 2 + board.height * board.cell_size
    size = width, height
    screen = pygame.display.set_mode(size)
    board.spawn(screen)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    board.get_click(event.pos, screen)
        screen.fill(pygame.color.Color('white'))
        board.render(screen)
        clock.tick(60)
        board.ticks += 1
        pygame.display.flip()
    ShulteMenu()

def ShulteMenu():
    pygame.init()
    running = True
    screen_width = 400
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > 150 and x < 250:
                    if y > 280 and y < 330:
                        MainMenu()
                for i in range(4):
                    if x in range(50 * i + 30 * i + 50, 50 * i + 30 * i + 50 + 75) and y in range(200, 250):
                        startShulte(i + 2)
        screen.fill(pygame.color.Color('white'))
        for i in range(4):
            font = pygame.font.SysFont(None, 50)
            text = font.render(f'{i + 2}x{i + 2}', True, pygame.color.Color('black'))
            screen.blit(text, (50 * i + 30 * i + 50, 200, 75, 50))
        file = open('log.txt', mode='r')
        info = file.readline()
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Последний результат: {info}", True, pygame.color.Color('black'))
        screen.blit(text, (80, 120))
        file.close()
        font = pygame.font.SysFont(None, 50)
        text = font.render("Таблица Шульте", True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 5 - text.get_height() / 2))
        font = pygame.font.SysFont(None, 30)
        text = font.render('Выберите режим игры:', True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, 150))
        font = pygame.font.SysFont(None, 30)
        text = font.render('В меню', True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, 300))
        pygame.display.update()
        clock.tick(15)
    pygame.quit()


white = (255, 255, 255)
black = (0, 0, 0)
clock_rb = pygame.time.Clock()
screen_width_rb = 800
screen_height_rb = 600
block_size = 50
block_skin = pygame.Surface((block_size, block_size))
block_skin.fill(white)
block_speed = 5

def runBlock():
    running = True
    screen = pygame.display.set_mode((screen_width_rb, screen_height_rb))
    pygame.display.set_caption("Игра")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainMenu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(1, block_size, block_speed, screen)  # Легкий уровень сложности
                elif event.key == pygame.K_2:
                    game_loop(2, block_size, block_speed, screen)  # Средний уровень сложности
                elif event.key == pygame.K_3:
                    game_loop(3, block_size, block_speed, screen)  # Тяжелый уровень сложности

        screen.fill(black)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Главное меню", True, white)
        screen.blit(text, (screen_width_rb / 2 - text.get_width() / 2, screen_height_rb / 2 - text.get_height() / 2))

        font = pygame.font.SysFont(None, 30)
        text = font.render("Нажмите 1, 2 или 3 для выбора уровня сложности", True, white)
        screen.blit(text, (screen_width_rb / 2 - text.get_width() / 2, screen_height_rb / 2 - text.get_height() / 2 + 50))

        pygame.display.update()
        clock_rb.tick(15)

def game_loop(difficulty, block_size, block_speed, screen):
    block_x = screen_width_rb // 2
    block_y = screen_height_rb // 2
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
                runBlock()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if block_x <= mouse_x <= block_x + block_size and block_y <= mouse_y <= block_y + block_size:
                    block_x += random.randint(-move_distance, move_distance)
                    block_y += random.randint(-move_distance, move_distance)
        if block_x < 0:
            block_x = 0
        if block_x + block_size > screen_width_rb:
            block_x = screen_width_rb - block_size
        if block_y < 0:
            block_y = 0
        if block_y + block_size > screen_height_rb:
            block_y = screen_height_rb - block_size
        screen.fill(black)
        screen.blit(block_skin, (block_x, block_y))

        pygame.display.update()
        clock_rb.tick(60)  # Ограничение частоты обновления экрана

def MainMenu():
    pygame.init()
    running = True
    screen_width = 400
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > 100 and x < 300:
                    if y > 170 and y < 220:
                        ShulteMenu()
                    elif y > 230 and y < 280:
                        runBlock()
        screen.fill(pygame.color.Color('white'))
        font = pygame.font.SysFont(None, 50)
        text = font.render("Доступные игры:", True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 5 - text.get_height() / 2))
        font = pygame.font.SysFont(None, 30)
        text = font.render("Таблица Шульте", True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))
        font = pygame.font.SysFont(None, 30)
        text = font.render("Run block", True, pygame.color.Color('black'))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 + 50))
        pygame.display.update()
        clock.tick(15)
    pygame.quit()

MainMenu()
