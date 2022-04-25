# python-maze

Generates a PNG maze. Thanks to [Orestis Zekai](https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e) for the original algorithm.

## Included Maze Types
### Square maze
 - Grid
 - Solving/Optimization isn't working yet
 - Uses grid squares for walls
 - Usage:
    `python square_maze.py <maze_height> <maze_width>`

### Line maze
- Grid with separate wall segments
- Generates 2 PNGs -- one solved, one unsolved
- Every grid square is usable as a maze cell
- Can optimize for more interesting maze generation by adding iterations
  - Optimization is currently very simple -- it's set to maximize the length of the solved path
- Usage:
  `python line_maze.py <maze_height> <maze_width> <iterations>`

##Fair warning: 
__This code is horribly inefficient, and large mazes take quite a long time to generate, especially if they are run through many iterations__ 
