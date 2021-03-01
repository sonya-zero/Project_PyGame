import os
import sys
import pygame
import create_board  # create board happens and finish cell from import in file create_board
import variable as var


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

    def get_cell(self, mouse_pos):  # get cell's coord on which clicked
        x_cell, y_cell = (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size
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

    def get_click(self, mouse_pos):  # clicked on cell or not
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


if __name__ == "__main__":
    pygame.init()
    board = Board(var.size, var.size)
    size = width, height = var.size * 50 + board.left * 2, var.size * 50 + board.top * 2
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("help_for_AI")
    running = True
    print(board.board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill("black")
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
