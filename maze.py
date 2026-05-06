import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

R, C = 20, 20
CELL_SIZE = 0.6

northWall = [[1 for _ in range(C)] for _ in range(R + 1)] 
eastWall = [[1 for _ in range(C + 1)] for _ in range(R)] 
visited_gen = [[False for _ in range(C)] for _ in range(R)] 

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

def remove_wall(r, c, nr, nc):
    if nc == c + 1: eastWall[r][c + 1] = 0
    elif nc == c - 1: eastWall[r][c] = 0
    elif nr == r + 1: northWall[r + 1][c] = 0
    elif nr == r - 1: northWall[r][c] = 0

def draw_dot(r, c, color):
    x, y = (c - C/2) * CELL_SIZE + (CELL_SIZE/2), (r - R/2) * CELL_SIZE + (CELL_SIZE/2)
    glPointSize(8); glBegin(GL_POINTS); glColor3fv(color)
    glVertex2f(x, y); glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init_opengl(800, 600)

    gen_stack = [(random.randint(0, R-1), random.randint(0, C-1))]
    visited_gen[gen_stack[0][0]][gen_stack[0][1]] = True
    gen_done = False

    solver_stack = []
    visited_solver = [[False for _ in range(C)] for _ in range(R)]
    start_pos, end_pos = (0,0), (0,0)
    solving = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()

        if not gen_done:
            r, c = gen_stack[-1]
            neighbors = [(r+dr, c+dc) for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)] 
                        if 0 <= r+dr < R and 0 <= c+dc < C and not visited_gen[r+dr][c+dc]]
            if neighbors:
                nr, nc = random.choice(neighbors)
                gen_stack.append((nr, nc)); remove_wall(r, c, nr, nc)
                visited_gen[nr][nc] = True
            elif len(gen_stack) > 1: gen_stack.pop()
            else:
                s_r, e_r = random.randint(0, R-1), random.randint(0, R-1)
                eastWall[s_r][0] = 0   # Entry
                eastWall[e_r][C] = 0   # Exit
                start_pos, end_pos = (s_r, 0), (e_r, C-1)
                solver_stack = [start_pos]
                gen_done = True
                solving = True
        # 2. ANIMATE SOLVER
        if solving and solver_stack:
            curr_r, curr_c = solver_stack[-1]
            visited_solver[curr_r][curr_c] = True
            
            if (curr_r, curr_c) == end_pos:
                solving = False  # We found the exit!
            else:
                moved = False
                # Directions to try: (row change, col change, wall to check)
                dirs = [(0, 1, 'e'), (1, 0, 'n'), (0, -1, 'w'), (-1, 0, 's')]
                random.shuffle(dirs) 
                
                for dr, dc, wall_type in dirs:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < R and 0 <= nc < C and not visited_solver[nr][nc]:
                        can_pass = False
                        # Check if the wall between current and neighbor is broken
                        if wall_type == 'e' and eastWall[curr_r][curr_c+1] == 0: can_pass = True
                        elif wall_type == 'w' and eastWall[curr_r][curr_c] == 0: can_pass = True
                        elif wall_type == 'n' and northWall[curr_r+1][curr_c] == 0: can_pass = True
                        elif wall_type == 's' and northWall[curr_r][curr_c] == 0: can_pass = True
                        
                        if can_pass:
                            solver_stack.append((nr, nc))
                            moved = True
                            break
                
                if not moved:
                    # Backtrack: remove from red path and it will turn blue later
                    solver_stack.pop()
        

        if gen_done and solver_stack:
            for sr, sc in solver_stack: draw_dot(sr, sc, (1, 0, 0))
        pygame.display.flip()

if __name__ == "__main__": main()