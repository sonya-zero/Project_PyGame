from random import choice

size = 6  # number of cell
CELLS = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],  # variations of cells
         [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1],
         [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 0], [1, 1, 1, 1],
         [1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]]
board = [[[0, 0, 0, 0] for i in range(size)] for j in range(size)]  # board
ways = [(0, 0)]  # coords cells which we must create
visited_cells = []  # coords cells which created

def change_cell(x, y):  # random change cell
    cell_limit = [[0, 1], [0, 1], [0, 1], [0, 1]]  # ways which cell can have
    '''limits on ways'''
    if x == 0:
        cell_limit[3] = [0]
    elif x == size - 1:
        cell_limit[1] = [0]
    if y == 0:
        cell_limit[0] = [0]
    elif y == size - 1:
        cell_limit[2] = [0]
    if (x, y - 1) in visited_cells:
        cell_limit[0] = [board[y - 1][x][2]]
    if (x + 1, y) in visited_cells:
        cell_limit[1] = [board[y][x + 1][3]]
    if (x, y + 1) in visited_cells:
        cell_limit[2] = [board[y + 1][x][0]]
    if (x - 1, y) in visited_cells:
        cell_limit[3] = [board[y][x - 1][1]]

    possibilities = list(filter(lambda elem: (elem[0] in cell_limit[0])  # possibility variations of this cell
                                             and (elem[1] in cell_limit[1])
                                             and (elem[2] in cell_limit[2])
                                             and (elem[3] in cell_limit[3])
                                             and sum(elem) > one_way(cell_limit, (x, y)), CELLS))
    cell = choice(possibilities)  # choice cell
    return cell

def find_ways(cell, x, y):  # find cells which we must create
    if cell[0] == 1 and not ((x, y - 1) in visited_cells) and not ((x, y - 1) in ways):
        ways.append((x, y - 1))
    if cell[1] == 1 and not ((x + 1, y) in visited_cells) and not ((x + 1, y) in ways):
        ways.append((x + 1, y))
    if cell[2] == 1 and not ((x, y + 1) in visited_cells) and not ((x, y + 1) in ways):
        ways.append((x, y + 1))
    if cell[3] == 1 and not ((x - 1, y) in visited_cells) and not ((x - 1, y) in ways):
        ways.append((x - 1, y))

def one_way(cell_limit, my_place):  # limit on "ones" ways in cell
    if my_place != (0, 0) and len(ways) < 2 and len(visited_cells) < size ** 2 * 0.9 and (sum(cell_limit[0])
                                                                                          + sum(cell_limit[1])
                                                                                          + sum(cell_limit[2])
                                                                                          + sum(cell_limit[3])) > 1:
        return 1
    return 0

def compilation_board():  # create board
    while len(ways) != 0:
        my_place = ways.pop(0)  # cell which is creating
        cell = change_cell(my_place[0], my_place[1])  # created cell
        find_ways(cell, my_place[0], my_place[1])  # add coords ells which we must to create
        board[my_place[1]][my_place[0]] = cell  # add new cell in list board
        visited_cells.append(my_place)  # add coords cells which created

    return board
