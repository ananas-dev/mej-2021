import numpy as np
import pygame

import random

##############
# GAME LOGIC #
##############

CELLMAP_WIDTH = 128
CELLMAP_HEIGHT = 128

CELL_SIZE = 10
WIDTH = CELLMAP_WIDTH * CELL_SIZE
HEIGHT = CELLMAP_HEIGHT * CELL_SIZE

pygame.init()

global win
#win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 24)  # New 24-bit screen


class Cell:
  infection_level = 0
  
class CellMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.lenght = width * height

        # Les differents états des cellules peuvent être instanciés sur des arrays différents

        self.cells = np.zeros(self.lenght, dtype=np.uint8)
        self.temp_cells = np.zeros(self.lenght, dtype=np.uint8)

        self.once_infected = np.zeros(self.lenght, dtype=np.uint8)
        self.temp_once_infected = np.zeros(self.lenght, dtype=np.uint8)

        self.neighbors = np.zeros(self.lenght, dtype=np.uint8)
        self.temp_neighbors = np.zeros(self.lenght, dtype=np.uint8)

    def draw_cell(self, x, y, alive_color):
        global win
        pygame.draw.rect(win, alive_color, (x * CELL_SIZE,
                         y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_cell(self, cell_value, row, col):
        idx = self.get_index(row, col)

        height = int(self.height)
        width = int(self.width)

        self.cells[idx] = cell_value
        self.once_infected[idx] = 1

        if row == 0:
            north = height - 1
        else:
            north = row - 1

        if row == height - 1:
            south = 0
        else:
            south = row + 1

        if col == 0:
            west = width - 1
        else:
            west = col - 1

        if col == width - 1:
            east = 0
        else:
            east = col + 1

        nw = self.get_index(north, west)
        self.neighbors[nw] += 1

        n = self.get_index(north, col)
        self.neighbors[n] += 1

        ne = self.get_index(north, east)
        self.neighbors[ne] += 1

        w = self.get_index(row, west)
        self.neighbors[w] += 1

        e = self.get_index(row, east)
        self.neighbors[e] += 1

        sw = self.get_index(south, west)
        self.neighbors[sw] += 1

        s = self.get_index(south, col)
        self.neighbors[s] += 1

        se = self.get_index(south, east)
        self.neighbors[se] += 1

    def clear_cell(self, row, col):
        idx = self.get_index(row, col)

        self.cells[idx] = 0

        if row == 0:
            north = self.height - 1
        else:
            north = row - 1

        if row == self.height - 1:
            south = 0
        else:
            south = row + 1

        if col == 0:
            west = self.width - 1
        else:
            west = col - 1

        if col == self.width - 1:
            east = 0
        else:
            east = col + 1

        nw = self.get_index(north, west)
        self.neighbors[nw] -= 1

        n = self.get_index(north, col)
        self.neighbors[n] -= 1

        ne = self.get_index(north, east)
        self.neighbors[ne] -= 1

        w = self.get_index(row, west)
        self.neighbors[w] -= 1

        e = self.get_index(row, east)
        self.neighbors[e] -= 1

        sw = self.get_index(south, west)
        self.neighbors[sw] -= 1

        s = self.get_index(south, col)
        self.neighbors[s] -= 1

        se = self.get_index(south, east)
        self.neighbors[se] -= 1

    def get_index(self, row, col):
        return int(row * self.width + col)

    def some_update_behaviour(col, row):
        print(":)")

    def next_gen(self):
        self.temp_cells = np.copy(self.cells)
        self.temp_neighbors = np.copy(self.neighbors)
        self.temp_once_infected = np.copy(self.once_infected)

        for row in range(self.height):

            for col in range(self.width):

                idx = self.get_index(row, col)
                cell = self.temp_cells[idx]
                live_neighbors = self.temp_neighbors[idx]
                once_infected = self.temp_once_infected[idx]

                if cell == 0 and live_neighbors == 0:
                    continue

                if cell == 1 and live_neighbors <= 8:
                    continue

                if live_neighbors >= 1 and cell == 0 and not once_infected:
                    self.set_cell(5, row, col)
                    self.draw_cell(row, col, pygame.Color(255, 0, 0))

                if cell != 0:
                    next_value = cell - 1
                    self.set_cell(next_value, row, col)
                    self.draw_cell(row, col, pygame.Color(int((255 / 5) * next_value), 0, 0))




# Initialize the cellmap
cellmap = CellMap(CELLMAP_WIDTH, CELLMAP_HEIGHT)

def main():
    paused = True

    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and paused:
                pos = pygame.mouse.get_pos()

                x = pos[0]
                y = pos[1]

                row = min(np.floor(x / CELL_SIZE), HEIGHT)
                col = min(np.floor(y / CELL_SIZE), WIDTH)

                cellmap.set_cell(5, row, col)
                cellmap.draw_cell(row, col, pygame.Color(255, 255, 255))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                if event.key == pygame.K_n and paused:
                    cellmap.next_gen()

            if event.type == pygame.QUIT:
                running = False
            
        if not paused:
            cellmap.next_gen()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
