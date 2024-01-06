import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
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


class ShulteMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ShulteMenu.ui', self)
        self.goButton.clicked.connect(self.startGame)
        file = open('log.txt', mode='r')
        info = file.readline()
        self.lastRezLabel.setText(info)
        file.close()

    def startGame(self):
        pygame.init()
        board = Shulte(self.widthBox.value(), self.heightBox.value())
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
            print(board.ticks)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShulteMenu()
    ex.show()
    sys.exit(app.exec_())