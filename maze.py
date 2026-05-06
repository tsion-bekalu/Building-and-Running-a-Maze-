import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

R, C = 20, 20
CELL_SIZE = 0.6

northWall = [[1 for _ in range(C)] for _ in range(R + 1)] 
eastWall = [[1 for _ in range(C + 1)] for _ in range(R)]  

def init_opengl(w, h):
    gluPerspective(45, (w/h), 0.1, 100.0)
    glTranslatef(-0.5, -0.5, -18) 

def draw_maze():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0) 
    for r in range(R):
        for c in range(C):
            x, y = (c - C/2) * CELL_SIZE, (r - R/2) * CELL_SIZE
            if northWall[r+1][c]:
                glVertex2f(x, y + CELL_SIZE); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
            if eastWall[r][c+1]:
                glVertex2f(x + CELL_SIZE, y); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    # Phantom Boundaries
    for c in range(C): 
        if northWall[0][c]:
            glVertex2f((c - C/2) * CELL_SIZE, (0 - R/2) * CELL_SIZE)
            glVertex2f((c - C/2 + 1) * CELL_SIZE, (0 - R/2) * CELL_SIZE)
    for r in range(R): 
        if eastWall[r][0]:
            glVertex2f((0 - C/2) * CELL_SIZE, (r - R/2) * CELL_SIZE)
            glVertex2f((0 - C/2) * CELL_SIZE, (r + 1 - R/2) * CELL_SIZE)
    glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init_opengl(800, 600)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()
        pygame.display.flip()
if __name__ == "__main__": main()