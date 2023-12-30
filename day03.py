from utils import read_day, char_grid, prod

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
NON_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

def is_valid(r, c, grid):
  return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])

def next_num(grid, r, c):
  n = 0
  while c < len(grid[r]) and grid[r][c] in DIGITS:
    if n == 0:
      n = int(grid[r][c])
    else:
      n = n * 10 + int(grid[r][c])
    c += 1
  return (n, c)

def build_values(grid):
  values = {}
  for r, line in enumerate(grid):
    row = {}
    c = 0
    while c < len(line): 
      (n, cn) = next_num(grid, r, c)
      for i in range(c, cn):
        row[i] = n
      c = cn + 1
    values[r] = row
  return values

grid = read_day(3, char_grid)
values = build_values(grid)

def check_part(grid, r, c):
  for i in range(-1, 2):
    for j in range(-1, 2):
      if (i, j) == (0, 0):
        continue
      rn, cn = r + i, c + j
      if is_valid(rn, cn, grid) and grid[rn][cn] not in NON_SYMBOLS:
        return True
  return False

def check_row(grid, r, c):
  valid = False
  n = 0
  while c < len(grid[r]) and grid[r][c] in DIGITS:
    if check_part(grid, r, c):
      valid = True
    if n == 0:
      n = int(grid[r][c])
    else:
      n = n * 10 + int(grid[r][c])
    c += 1
  return (n, c + 1) if valid else (0, c + 1)

def part1():
  total = 0
  for r, line in enumerate(grid):
    c = 0
    while c < len(line): 
      (n, c) = check_row(grid, r, c)
      total += n
  return total

print(f'Part 1: {part1()}')

def gear_value(grid, r, c):
  vals = set()
  for i in range(-1, 2):
    for j in range(-1, 2):
      if (i, j) == (0, 0):
        continue
      rn = r + i
      cn = c + j
      if is_valid(rn, cn, grid) and grid[rn][cn] in DIGITS:
        v = values.get(rn, {}).get(cn, 0)
        if v != 0:
          vals.add(v)
  if len(vals) == 2:
    return prod(vals)
  return 0

def part2():
  total = 0
  for r, line in enumerate(grid):
    for c, x in enumerate(line):
      if x == '*':
        total += gear_value(grid, r, c)
  return total

print(f'Part 2: {part2()}')
