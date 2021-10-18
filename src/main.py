from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

##############
# GAME LOGIC #
##############

class CellMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.cells = np.zeros(width * height, dtype=np.uint8)
        self.cells_next = np.zeros(width * height, dtype=np.uint8)

    def get_index(self, row: int, col: int) -> int:
        return int(row * self.width + col)

    def neighbor_count(self, row: int, col: int) -> int:
        count = 0

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
        count += self.cells[nw]

        n = self.get_index(north, col)
        count += self.cells[n]

        ne = self.get_index(north, east)
        count += self.cells[ne]

        w = self.get_index(row, west)
        count += self.cells[w]

        e = self.get_index(row, east)
        count += self.cells[e]

        sw = self.get_index(south, west)
        count += self.cells[sw]

        s = self.get_index(south, col)
        count += self.cells[s]

        se = self.get_index(south, east)
        count += self.cells[se]

        return count

    def tick(self):
        for row in range(self.height):

            for col in range(self.width):
                idx = self.get_index(row, col)
                cell = self.cells[idx]
                live_neighbors = self.neighbor_count(row, col)

                if cell == 1 and live_neighbors < 2:
                    next_cell = 0
                elif cell == 1 and (live_neighbors == 2 or live_neighbors == 3):
                    next_cell = 1
                elif cell == 1 and live_neighbors > 3:
                    next_cell = 0
                elif cell == 0 and live_neighbors == 3:
                    next_cell = 1
                else:
                    next_cell = cell

                self.cells_next[idx] = next_cell
            
        self.cells = np.copy(self.cells_next)
    
    def toogle_cell(self, row, col):
        idx = self.get_index(row, col)
        cell = self.cells[idx]

        if cell == 1:
            self.cells[idx] = 0
        elif cell == 0:
            self.cells[idx] = 1


    
#############
# RENDERING #
#############

cellmap = CellMap(64, 64)
paused = True

CELL_SIZE = 10
WIDTH = cellmap.width * CELL_SIZE
HEIGHT = cellmap.height * CELL_SIZE

def draw_cell(col, row):
    glBegin(GL_QUADS)
    glVertex2f(col * CELL_SIZE, row * CELL_SIZE)
    glVertex2f((col + 1) * CELL_SIZE, row * CELL_SIZE)
    glVertex2f((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE)
    glVertex2f(col * CELL_SIZE, (row + 1) * CELL_SIZE)
    glEnd()

def draw_cells():
    # Draw alive cells
    glColor3f(1.0, 1.0, 1.0)
    for row in range(cellmap.width):
        for col in range(cellmap.height):
            index = cellmap.get_index(row, col)

            cell = cellmap.cells[index]

            if cell != 1:
                continue

            draw_cell(col, row)

    # Draw dead cells
    glColor3f(0.0, 0.0, 0.0)
    for row in range(cellmap.width):
        for col in range(cellmap.height):
            index = cellmap.get_index(row, col)

            cell = cellmap.cells[index]

            if cell != 0:
                continue

            draw_cell(col, row)


def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WIDTH, HEIGHT, 0.0, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if not paused:
        cellmap.tick()

    draw_cells()
    glutSwapBuffers()


def mouseCallback(btn, state, x, y):
    if paused and btn == 0 and state == 1:
        row = min(np.floor(y / CELL_SIZE), HEIGHT)
        col = min(np.floor(x / CELL_SIZE), WIDTH)

        cellmap.toogle_cell(row, col)

def keyboardCallback(key, x, y):
    print(key)
    global paused
    if (key == b' '):
        paused = not paused



def main():
    # Initialize GLUT
    glutInit()

    # Window settings
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(0, 0)

    # Create the window
    wind = glutCreateWindow("Game of Life")

    # Set the callbacks
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutMouseFunc(mouseCallback)
    glutKeyboardFunc(keyboardCallback)
    glutMainLoop()


if __name__ == "__main__":
    main()
