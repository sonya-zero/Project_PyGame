import pygame
import os
from math import *
pass
pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color("white"),
                                 (self.left + i * self.cell_size, self.top + j * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def check_cell(self, point):
        A = point[0] < self.left
        B = point[0] > self.left + (self.width + 1) * self.cell_size
        C = point[1] < self.top
        D = point[1] > self.top + (self.height - 1) * self.cell_size
        if A or B or C or D:
            print("None")
        else:
            cell_x = (point[0] - self.left) // self.cell_size
            cell_y = (point[1] - self.top) // self.cell_size
            print((cell_x, cell_y))
            screen2 = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
            if self.board[cell_x][cell_y] == 0:
                color_cell = "white"
                self.board[cell_x][cell_y] = 1
            else:
                color_cell = "black"
                self.board[cell_x][cell_y] = 0
            screen2.fill(color_cell)
            screen.blit(screen2, (self.left + cell_x * self.cell_size + 1,
                                  self.top + cell_y * self.cell_size + 1))


class Robot(pygame.sprite.Sprite):
    image = load_image("robot0.png")

    def __init__(self, group):
        # РќР•РћР‘РҐРћР”РРњРћ РІС‹Р·РІР°С‚СЊ РєРѕРЅСЃС‚СЂСѓРєС‚РѕСЂ СЂРѕРґРёС‚РµР»СЊСЃРєРѕРіРѕ РєР»Р°СЃСЃР° Sprite
        super().__init__(group)
        self.image = Robot.image
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 25
        self.angle = 0

    def cor(self):
        self.rect.x += 50 * cos(radians(self.angle))
        self.rect.y += 50 * sin(radians(self.angle))
        return (50 * cos(radians((self.angle))), 50 * sin(radians(self.angle)))

    def update(self, side):
        if side == "down":
            self.image = load_image("robot1.png")
            self.angle = 90
            print(self.angle)
        elif side == "up":
            self.image = load_image("robot3.png")
            self.angle = 270
            print(self.angle)
        elif side == "left":
            self.image = load_image("robot2.png")
            self.angle = 180
            print(self.angle)
        elif side == "right":
            self.image = load_image("robot0.png")
            self.angle = 0
            print(self.angle)
        elif side == "ff":
            self.rect = self.rect.move(50 * cos(radians(self.angle)), 50 * sin(radians(self.angle)))
            print(self.rect.x, self.rect.y)

# main part
pass

if __name__ == "__main__":
    pygame.init()
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    board = Board(6, 6)
    board.set_view(50, 50, 50)
    screen.fill((0, 0, 0))
    board.render(screen)
    running = True
    # all_sprites = pygame.sprite.Group()
    Robot(all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.check_cell(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    all_sprites.update("up")
                elif event.key == pygame.K_DOWN:
                    all_sprites.update("down")
                elif event.key == pygame.K_LEFT:
                    all_sprites.update("left")
                elif event.key == pygame.K_RIGHT:
                    all_sprites.update("right")
                elif event.key == pygame.K_SPACE:
                    all_sprites.update("ff")
                # print(board.board[0][0])
                # print(event.pos)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        # all_sprites.update(1, 1)
        board.render(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()


