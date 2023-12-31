from utils import read_day, char_grid, Vec2d

EMPTY = '.'
GALAXY = '#'
NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)

grid = read_day(11, char_grid)

def expand(grid):
  new_grid = []
  for row in grid:
    new_grid.append(row[:])
    if all(x == EMPTY for x in row):
      new_grid.append(row[:])
  for c in range(len(new_grid[0]) - 1, -1, -1):
    if all(r[c] == EMPTY for r in new_grid):
      for new_row in new_grid:
        new_row.insert(c, EMPTY)
  return new_grid

def find_pairs(grid):
  galaxies = []
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      if v == GALAXY:
        galaxies.append(Vec2d(r, c))
  for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
      yield galaxies[i], galaxies[j]

def part1():
  new_grid = expand(grid)
  total = 0
  for a, b in find_pairs(new_grid):
    total += a.distance(b)
  return total

print(f'Part 1: {part1()}')

MULT = 1_000_000

def to_expand(grid):
  rows = []
  for r, row in enumerate(grid):
    if all(x == EMPTY for x in row):
      rows.append(r)
  cols = []
  for c in range(len(grid[0])):
    if all(r[c] == EMPTY for r in grid):
      cols.append(c)
  return rows, cols

def find_path(grid, a, b, rows, cols):
  nr = sum(r > min(a.x, b.x) and r < max(a.x, b.x) for r in rows)
  nc = sum(c > min(a.y, b.y) and c < max(a.y, b.y) for c in cols)
  return abs(a.x - b.x) + nr * (MULT - 1) + abs(a.y - b.y) + nc * (MULT - 1)

def part2():
  rows, cols = to_expand(grid)
  total = 0
  for a, b in find_pairs(grid):
    total += find_path(grid, a, b, rows, cols)
  return total

print(f'Part 2: {part2()}')
