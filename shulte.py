import pygame
import sys
import random
pygame.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 5
        self.finding_num = 1

    # настройка внешнего вида
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
        print(cell) ###


class Shulte(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
    
    def spawn(self, surface):
        sample_of_number = random.sample(range(1, self.width * self.height + 1), self.width * self.height)
        number = 0
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = sample_of_number[number]
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(str(sample_of_number[number]), False, (255, 0, 0))
                screen.blit(text, (x * self.cell_size, y * self.cell_size))
                number += 1
        super().render(surface)

    def render(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(str(self.board[y][x]), False, (pygame.color.Color('black')))
                screen.blit(text, (self.left + 5 + x * self.cell_size, self.top + 5 + y * self.cell_size))
        font = pygame.font.Font(None, self.cell_size * 2)
        text = font.render(str(self.finding_num), False, (pygame.color.Color('black')))
        screen.blit(text, (30, 30))
        self.time(ticks)
        super().render(surface)

    def check(self, cell, surface):
        global ticks
        if cell:
            y, x = cell
            if self.board[y][x] == self.finding_num:
                self.finding_num += 1
        if self.finding_num == self.width * self.height + 1:
            self.finding_num = 1
            self.spawn(surface)
            ticks = 0
    
    def time(self, time):
        font = pygame.font.Font(None, self.cell_size * 2)
        text = font.render(str(time // 100), False, (pygame.color.Color('black')))
        screen.blit(text, (300, 30))


if __name__ == '__main__':
    
    board = Shulte(2, 2)
    board.set_view(100, 100, 50)
    width = board.left * 2 + board.width * board.cell_size
    height = board.top * 2 + board.height * board.cell_size
    size = width, height
    screen = pygame.display.set_mode(size)
    board.spawn(screen)

    clock = pygame.time.Clock()
    ticks = 0
    
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
        clock.tick(100)
        ticks += 1
        pygame.display.flip()
    pygame.quit()