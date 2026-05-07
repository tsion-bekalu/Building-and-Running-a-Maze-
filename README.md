# Building and Running a Maze

Name: Tsion Bekalu  
ID: UGR/9277/16  
Section: 1

---

## Project Overview

This project is about building a maze and then solving it using an algorithm instead of doing it manually. The maze is generated randomly every time the program runs, so each result is different. After the maze is created, the program finds a path from the left side to the right side.

The program also shows the process visually, so you can actually see how the maze is built and how it is solved.

---

## Maze Representation

The maze is stored using two arrays called northWall and eastWall. These are used to represent whether a wall exists or not.

If the value is 1, the wall is there. If it is 0, the wall has been removed.

I used an extra row and column (phantom boundaries) to make it easier to handle the edges of the maze without special cases.

---

## Maze Generation

To generate the maze, I used a stack-based DFS approach. You can think of it like a mouse moving through the maze and breaking walls.

The mouse starts at a random cell and looks at its neighbors. If it finds a neighbor that hasn’t been visited yet, it removes the wall between them and moves there. Before moving, it stores its current position in a stack.

If the mouse reaches a point where all neighbors are already visited, it goes back by popping from the stack. This continues until all cells are visited.

This method makes sure the maze is fully connected and there is only one path between any two cells.

---

## Maze Solving

After generating the maze, the program solves it using another DFS-like approach.

It starts from the entry point and tries to move in different directions. If a move is possible (no wall), it goes forward and saves the position.

If it reaches a dead end, it goes back and tries another path. While doing this, the current path is shown in red and dead ends are shown in blue.

---

## Visualization

The program uses OpenGL for drawing and Pygame for handling the window.

When you run it, you first see the maze being created step by step. After that, the solving process starts automatically. You can see how the algorithm explores the maze until it finds the exit.

---

## How to Run

Make sure Python is installed first.

Then install the required libraries:

pip install pygame PyOpenGL PyOpenGL_accelerate

After that, run the file:

python maze.py

---

## Notes

Each time you run the program, the maze will look different because it is generated randomly. The approach used guarantees that all cells are connected, so the maze is always solvable.
