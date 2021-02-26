import os
import sys
import pygame
import create_board


def load_image(name):  # load image
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:  # class board
    def __init__(self, width, height):  # board size & place on screen
        self.width = width
        self.height = height
        self.board = create_board.compilation_board()
        self.board_look = [[0] * height for _ in range(width)]
        self.left = 30
        self.top = 30
        self.cell_size = 50

    def set_view(self, left, top, cell_size):  # view on screen
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):  # draw start board
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, "black", (self.left + self.cell_size * i, self.top + self.cell_size * j,
                                                   self.cell_size, self.cell_size), 1)
                if self.board_look[j][i]:
                    screen.blit(self.board_look[j][i], (self.left + self.cell_size * i,
                                                        self.top + self.cell_size * j))

    def get_cell(self, mouse_pos):  # get cell's coord on which clicked
        x_cell, y_cell = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
        if x_cell < 0 or x_cell >= self.width or y_cell < 0 or y_cell >= self.height:
            return None
        return x_cell, y_cell

    def on_click(self, cell_coords):
        cell = self.board[cell_coords[1]][cell_coords[0]]
        if sum(cell) == 4:
            image = load_image("cross.png")
        elif sum(cell) == 3:
            image = load_image("t-cross.png")
            #image = pygame.transform.rotate(image, cell.index(0))
        elif sum(cell) == 2:
            if '1, 1' in str(cell) or '0, 0' in str(cell):
                image = load_image("rotate.png")
                #image = pygame.transform.rotate(image, ''.join(cell).index('11'))
            else:
                image = load_image("line.png")
                image = pygame.transform.rotate(image, -90 * ''.join(list(map(lambda x: str(x), cell))).index('10'))
        elif sum(cell) == 1:
            image = load_image("impasse.png")
            image = pygame.transform.rotate(image, -90 * cell.index(1))
        try:
            self.board_look[cell_coords[1]][cell_coords[0]] = image
        except UnboundLocalError:
            pass

    def get_click(self, mouse_pos):  # clicked on cell or not
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

if __name__ == "__main__":
    pygame.init()
    board = Board(create_board.size, create_board.size)
    size = width, height = create_board.size * 50 + board.left * 2, create_board.size * 50 + board.top * 2
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("help_for_AI")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill("white")
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
