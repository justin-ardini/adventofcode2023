from utils import read_day, char_grid, Vec2d
from collections import deque

NE = 'L'
NW = 'J'
SW = '7'
SE = 'F'
NS = '|'
WE = '-'
GROUND = '.'
START = 'S'
NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)

grid = read_day(10, char_grid)

def find_start(grid):
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      if v == START:
        return Vec2d(r, c)
  return Vec2d(-1, -1)

def move(grid, pos, d):
  next_pos = pos + d
  v = grid[next_pos.x][next_pos.y]
  diff = -d
  if v == NE:
    d = EAST if diff == NORTH else NORTH
  elif v == NW:
    d = WEST if diff == NORTH else NORTH
  elif v == SW:
    d = WEST if diff == SOUTH else SOUTH
  elif v == SE:
    d = EAST if diff == SOUTH else SOUTH
  return (next_pos, d)

def part1():
  pos = find_start(grid)
  # Initial direction from manual inspection.
  d = SOUTH
  loop = set()
  while pos not in loop:
    loop.add(pos)
    pos, d = move(grid, pos, d)
  return len(loop) // 2

print(f'Part 1: {part1()}')

def in_loop(pos, grid, loop):
  # Odd-even rule: cast a ray north and check intersections.
  if pos in loop:
    return False
  intersections = 0
  while pos.x >= 0:
    pos += NORTH
    if pos in loop and grid[pos.x][pos.y] in (NE, SE, WE):
      intersections += 1
  return intersections % 2 == 1

def part2():
  pos = find_start(grid)
  d = SOUTH
  loop = set()
  while pos not in loop:
    loop.add(pos)
    pos, d = move(grid, pos, d)
  total = 0
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      pos = Vec2d(r, c)
      total += in_loop(pos, grid, loop)
  return total

print(f'Part 2: {part2()}')
