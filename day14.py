from utils import read_day, char_grid, copy_grid

ROCK = 'O'
CUBE = '#'
OPEN = '.'

grid = read_day(14, char_grid)

def tilt_north(grid):
  new_grid = copy_grid(grid)
  for r, row in enumerate(grid):
    for c, x in enumerate(row):
      if x == ROCK:
        rp = r - 1
        while rp >= 0 and new_grid[rp][c] == OPEN:
          rp -= 1
        if rp + 1 != r:
          new_grid[rp + 1][c] = ROCK
          new_grid[r][c] = OPEN
  return new_grid

def tilt_south(grid):
  new_grid = copy_grid(grid)
  for r in range(len(grid)-1, -1, -1):
    row = grid[r]
    for c, x in enumerate(row):
      if x == ROCK:
        rn = r + 1
        while rn < len(grid) and new_grid[rn][c] == OPEN:
          rn += 1
        if rn - 1 != r:
          new_grid[rn - 1][c] = ROCK
          new_grid[r][c] = OPEN
  return new_grid

def tilt_east(grid):
  new_grid = copy_grid(grid)
  for r, row in enumerate(grid):
    for c in range(len(row)-1, -1, -1):
      x = row[c]
      if x == ROCK:
        cn = c + 1
        while cn < len(row) and new_grid[r][cn] == OPEN:
          cn += 1
        if cn - 1 != c:
          new_grid[r][cn - 1] = ROCK
          new_grid[r][c] = OPEN
  return new_grid

def tilt_west(grid):
  new_grid = copy_grid(grid)
  for r, row in enumerate(grid):
    for c, x in enumerate(row):
      if x == ROCK:
        cp = c - 1
        while cp >= 0 and new_grid[r][cp] == OPEN:
          cp -= 1
        if cp + 1 != c:
          new_grid[r][cp + 1] = ROCK
          new_grid[r][c] = OPEN
  return new_grid

def get_load(grid):
  n_rows = len(grid)
  total = 0
  for r, row in enumerate(grid):
    load = n_rows - r
    total += load * sum(x == ROCK for x in row)
  return total

def part1():
  new_grid = tilt_north(grid)
  return get_load(new_grid)

print(f'Part 1: {part1()}')

LIMIT = 1_000_000_000

def hash_grid(grid):
  return ''.join([''.join(r) for r in grid])

def part2():
  g = grid
  hashes = {}
  n_to_g = {}
  for n in range(LIMIT):
    n_to_g[n] = g
    h = hash_grid(g)
    if h in hashes:
      start = hashes[h]
      cycle = n - start
      offset = LIMIT % cycle
      return get_load(n_to_g[start + (offset - start) % cycle])
    else:
      hashes[h] = n
    g = tilt_north(g)
    g = tilt_west(g)
    g = tilt_south(g)
    g = tilt_east(g)
  return get_load(g)

print(f'Part 2: {part2()}')
