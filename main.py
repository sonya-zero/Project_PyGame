import pygame
import os
import sys
import time
import create_board  # create board happens and finish cell from import in file create_board
import variable as var  # import variables
from math import *


def load_image(name):  # load image
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:  # class board
    def __init__(self, width, height):  # board size & place on screen
        self.width = width
        self.height = height
        self.board = var.board
        self.board_look = [[0] * height for _ in range(width)]
        self.on_click(var.start_cell)
        self.left = var.left
        self.top = var.top
        self.cell_size = var.cell_size

    def render(self, screen):  # draw board
        font = pygame.font.Font(None, 20)  # text in finish cell
        text = font.render("finish", True, (0, 0, 0))
        for i in range(self.width):
            for j in range(self.height):
                x = self.left + self.cell_size * i
                y = self.top + self.cell_size * j
                pygame.draw.rect(screen, "white", (x, y, self.cell_size, self.cell_size), 1)
                if (i, j) == var.finish_cell:  # draw finish cell
                    pygame.draw.rect(screen, "green", (x, y, self.cell_size, self.cell_size), 0)
                    text_x = x + self.cell_size // 2 - text.get_width() // 2
                    text_y = y + self.cell_size // 2 - text.get_height() // 2
                    screen.blit(text, (text_x, text_y))
                if self.board_look[j][i]:  # draw opened cells
                    screen.blit(self.board_look[j][i], (x, y))

    def render_finish(self, screen):  # draw finish if you win
        screen.fill("black")
        image = load_image("you_win.jpg")
        image = pygame.transform.scale(image, size)
        screen.blit(image, (0, 0))

    def render_end(self, screen):  # draw game over if you die
        screen.fill("black")
        image = load_image("game_over.png")
        image = pygame.transform.scale(image, size)
        screen.blit(image, (0, 0))

    def get_cell(self, robot_pos):  # get cell's coord on which clicked
        x_cell, y_cell = (robot_pos[0] - self.left) // self.cell_size, \
                         (robot_pos[1] - self.top) // self.cell_size
        if x_cell < 0 or x_cell >= self.width or y_cell < 0 or y_cell >= self.height:
            return None
        return x_cell, y_cell

    def on_click(self, cell_coords):  # load image on board on click
        cell = self.board[cell_coords[1]][cell_coords[0]]
        if sum(cell) == 4:
            image = load_image("cross.png")
        elif sum(cell) == 3:
            image = load_image("t-cross.png")
            image = pygame.transform.rotate(image, -90 * cell.index(0))
        elif sum(cell) == 2:
            cell = ''.join(list(map(lambda x: str(x), cell)))
            if '101' in cell:
                image = load_image("line.png")
                image = pygame.transform.rotate(image, -90 * cell.index('10'))
            else:
                image = load_image("rotate.png")
                try:
                    image = pygame.transform.rotate(image, -90 * (cell.index('11') + 1))
                except ValueError:
                    pass
        elif sum(cell) == 1:
            image = load_image("impasse.png")
            image = pygame.transform.rotate(image, -90 * cell.index(1))
        try:
            self.board_look[cell_coords[1]][cell_coords[0]] = image
        except UnboundLocalError:
            pass

    def get_click(self, robot_pos):  # clicked on cell or not
        cell = self.get_cell(robot_pos)
        if cell:
            self.on_click(cell)


class Robot(pygame.sprite.Sprite):  # class robot
    image = load_image("robot0.png")

    def __init__(self, group):  # parameters of robot
        super().__init__(group)
        self.image = Robot.image
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 40
        self.angle = 0
        self.start = None

    def check(self):  # check choose way on opportunity of move
        x_cell, y_cell = (self.rect.x - var.left) // var.cell_size, (self.rect.y - var.top) // var.cell_size
        cell = var.board[y_cell][x_cell][1::] + [var.board[y_cell][x_cell][0]]
        if cell[(self.angle) // 90]:
            return True
        else:
            return False

    def check_finish(self):  # check finish
        x_cell, y_cell = (self.rect.x - var.left) // var.cell_size, (self.rect.y - var.top) // var.cell_size
        if (x_cell, y_cell) == var.finish_cell:
            return True
        else:
            return False

    def update(self, side):  # move of robot
        if side == "down":
            self.image = load_image("robot1.png")
            self.angle = 90
        elif side == "up":
            self.image = load_image("robot3.png")
            self.angle = 270
        elif side == "left":
            self.image = load_image("robot2.png")
            self.angle = 180
        elif side == "right":
            self.image = load_image("robot0.png")
            self.angle = 0
        elif side == "ff":
            print(self.rect.x, self.rect.y)
            self.rect.move(self.rect.x, self.rect.y)

    def cor(self):  # return robot coords
        self.rect.x += 50 * cos(radians(self.angle))
        self.rect.y += 50 * sin(radians(self.angle))
        return int(self.rect.x), int(self.rect.y)


if __name__ == "__main__":  # run the program
    pygame.init()  # initialize pygame
    board = Board(var.size, var.size)  # create class board
    size = width, height = var.size * 50 + board.left * 2, var.size * 50 + board.top * 2  # size window
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("help_for_AI")  # name game
    all_sprites = pygame.sprite.Group()
    running = True  # condition of run game
    game_over = False  # lose in game
    win = False  # win in game
    robot = Robot(all_sprites)  # create class robot
    while running:  # cycle of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # exit of game
                running = False
            if event.type == pygame.KEYDOWN:  # click on buttons
                if event.key == pygame.K_UP:
                    all_sprites.update("up")  # return robot in up
                elif event.key == pygame.K_DOWN:
                    all_sprites.update("down")  # return robot in down
                elif event.key == pygame.K_LEFT:
                    all_sprites.update("left")  # return robot on left
                elif event.key == pygame.K_RIGHT:
                    all_sprites.update("right")  # return robot on right
                elif event.key == pygame.K_SPACE:  # go forvard
                    if robot.check():  # check on opportunity of move
                        board.get_click(robot.cor())  # open cell
                        all_sprites.update("ff")  # move of robot
                        if robot.check_finish():  # check of finish
                            win = True
                    else:
                        game_over = True
        # draw board
        screen.fill("black")
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        if game_over:  # draw board if game over
            board.render_end(screen)
            pygame.display.flip()
            time.sleep(3)
            running = False
        if win:  # draw board if you win
            board.render_finish(screen)
            pygame.display.flip()
            time.sleep(3)
            running = False
    pygame.quit()  # exit of game
