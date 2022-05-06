# python-maze

Generates a PNG maze. Thanks to [Orestis Zekai](https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e) for the original algorithm.

## Included Maze Types


### Line maze
- Grid with separate wall segments
- Generates 2 PNGs -- one solved, one unsolved
- Every grid square is usable as a maze cell
- Can make more interesting maze generation by adding iterations
  - Iteration is currently very simple -- it's set to maximize the length of the solved path
- Smart Mode: Turn on for generating smarter mazes, that make up more of the area
- Usage:
  `python line_maze.py [-S] (smart mode) [-H <maze_height>] [-W <maze_width>] [-I <iterations> ]`

### Multithreaded Line Maze Generator
- Generates line mazes, using smart mode
- May melt CPU's
- Defaults are:
  - 50 by 50 maze
  - iterated 100 times
  - 10 threads
- Currently the best maze generator in this repo. 
- Usage:
  `python multithreaded_maze.py [-H <maze_height>] [-W <maze_width>] [-I <iterations> -T <threads> ]`

#### Line Maze Example:
![A Line Maze generated using multithreading](examples/50x50_maze.PNG?raw=true "Multi-Threaded Line Maze Example")

#### Line Maze Example:
![The solution of the line maze above](examples/50x50_maze_solution.PNG?raw=true "Line Maze Solution Example")

### Square maze
- Kept for historical purposes only. Don't use this. It probably doesn't even work.
- Grid
- Solving/Optimization isn't working yet
- Uses grid squares for walls
- Usage:
  `python square_maze.py <maze_height> <maze_width>`

## Fair warning: 
__This code is horribly inefficient, and large mazes take quite a long time to generate, especially if they are run through many iterations__ 
