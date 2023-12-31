from utils import read_day, char_grid, copy_grid

ASH  = '.'
ROCK = '#'

def parse_grids(lines):
  grids = []
  grid = []
  for line in lines:
    if line == '':
      grids.append(grid)
      grid = []
    else:
      grid.append([c for c in line])
  grids.append(grid)
  return grids

lines = read_day(13)
grids = parse_grids(lines)

def h_pattern(grid):
  for r in range(1, len(grid)):
    n = min(r, len(grid) - r)
    if all (grid[r - 1 - (s - r)] == grid[s] for s in range(r, r + n)):
      return r
  return 0

def v_pattern(grid):
  for c in range(1, len(grid[0])):
    n = min(c, len(grid[0]) - c)
    if all (grid[r][c - 1 - (d - c)] == grid[r][d] for d in range(c, c + n) for r in range(len(grid))):
      return c
  return 0

def part1():
  h = 0
  v = 0
  for grid in grids:
    h += h_pattern(grid)
    v += v_pattern(grid)
    h2 = h_pattern(grid)
    v2 = v_pattern(grid)
  return v + 100 * h

print(f'Part 1: {part1()}')

def h_patterns(grid):
  for r in range(1, len(grid)):
    n = min(r, len(grid) - r)
    if all (grid[r - 1 - (s - r)] == grid[s] for s in range(r, r + n)):
      yield r

def v_patterns(grid):
  for c in range(1, len(grid[0])):
    n = min(c, len(grid[0]) - c)
    if all (grid[r][c - 1 - (d - c)] == grid[r][d] for d in range(c, c + n) for r in range(len(grid))):
      yield c

def fix_smudge(grid, r, c):
  new_grid = copy_grid(grid)
  v = new_grid[r][c]
  new_grid[r][c] = ASH if v == ROCK else ROCK
  return new_grid

def find_smudge(grid):
  h = h_pattern(grid)
  v = v_pattern(grid)
  for r, row in enumerate(grid):
    for c, col in enumerate(row):
      new_grid = fix_smudge(grid, r, c)
      for h2 in h_patterns(new_grid):
        if h2 != h:
          return h2, 0
      for v2 in v_patterns(new_grid):
        if v2 != v:
          return 0, v2

def part2():
  h_sum = 0
  v_sum = 0
  for grid in grids:
    h, v = find_smudge(grid)
    h_sum += h
    v_sum += v
  return v_sum + 100 * h_sum

print(f'Part 2: {part2()}')
