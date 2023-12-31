from utils import read_day

def parse_brick(s):
  return [int(n) for n in s.split(',')]

def parse_line(line):
  a, b = line.split('~')
  return parse_brick(a), parse_brick(b)

def build_grid(bricks):
  grid = set()
  for brick in bricks:
    x_min = min(brick[0][0], brick[1][0])
    x_max = max(brick[0][0], brick[1][0])
    y_min = min(brick[0][1], brick[1][1])
    y_max = max(brick[0][1], brick[1][1])
    z_min = min(brick[0][2], brick[1][2])
    z_max = max(brick[0][2], brick[1][2])
    for x in range(x_min, x_max + 1):
      for y in range(y_min, y_max + 1):
        for z in range(z_min, z_max + 1):
          grid.add((x, y, z))
  return grid

start_bricks = read_day(22, parse_line)

def is_free(x, y, z, b, bricks):
  for i, brick in enumerate(bricks):
    if i == b:
      continue
    x_min = min(brick[0][0], brick[1][0])
    x_max = max(brick[0][0], brick[1][0])
    if x >= x_min and x <= x_max:
      y_min = min(brick[0][1], brick[1][1])
      y_max = max(brick[0][1], brick[1][1])
      if y >= y_min and y <= y_max:
        z_min = min(brick[0][2], brick[1][2])
        z_max = max(brick[0][2], brick[1][2])
        if z >= z_min and z <= z_max:
          return False
  return True

def all_free(i, z_offset, brick, bricks, grid):
  x_min = min(brick[0][0], brick[1][0])
  x_max = max(brick[0][0], brick[1][0])
  y_min = min(brick[0][1], brick[1][1])
  y_max = max(brick[0][1], brick[1][1])
  z_min = min(brick[0][2], brick[1][2])
  for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
      if (x, y, z_min - z_offset) in grid:
        return False
  return True

def maybe_fall(i, bricks, grid):
  brick = bricks[i]
  z_min = min(brick[0][2], brick[1][2])
  if z_min == 1:
    return brick, False
  new_brick = brick[0][:], brick[1][:]
  fell = False
  for z_offset in range(1, z_min):
    if all_free(i, z_offset, brick, bricks, grid):
      fell = True
      new_brick[0][2] -= 1
      new_brick[1][2] -= 1
    else:
      break
  return new_brick, fell

def fall(bricks, grid):
  fell = False
  next_bricks = bricks[:]
  for i, brick in enumerate(bricks):
    next_brick, brick_fell = maybe_fall(i, next_bricks, grid)
    next_bricks[i] = next_brick
    fell = fell or brick_fell
  return next_bricks, fell

def can_fall(b, bricks, grid):
  fell = False
  next_bricks = bricks[:]
  for i, brick in enumerate(bricks):
    next_brick, brick_fell = maybe_fall(i, next_bricks, grid)
    next_bricks[i] = next_brick
    fell = fell or brick_fell
    if fell:
      return True
  return False

def part1():
  fell = True
  bricks = start_bricks
  grid = build_grid(bricks)
  while fell:
    bricks, fell = fall(bricks, grid)
    grid = build_grid(bricks)
  total = 0
  for i, brick in enumerate(bricks):
    nb = [b for j, b in enumerate(bricks) if i != j]
    grid = build_grid(nb)
    if not can_fall(i, nb, grid):
      total += 1
  return total

print(f'Part 1: {part1()}')

def fall2(b, bricks, grid, fallen):
  fell = False
  next_bricks = bricks[:]
  for i, brick in enumerate(bricks):
    next_brick, brick_fell = maybe_fall(i, next_bricks, grid)
    next_bricks[i] = next_brick
    fell = fell or brick_fell
    if brick_fell:
      fell = True
      fallen.add(i)
  return next_bricks, fell

def part2():
  fell = True
  bricks = start_bricks
  grid = build_grid(bricks)
  while fell:
    bricks, fell = fall(bricks, grid)
    grid = build_grid(bricks)
  total = 0
  for i, brick in enumerate(bricks):
    nb = [b for j, b in enumerate(bricks) if i != j]
    grid = build_grid(nb)
    fallen = set()
    while True:
      nb, fell = fall2(i, nb, grid, fallen)
      grid = build_grid(nb)
      if not fell:
        break
    total += len(fallen)
  return total

print(f'Part 2: {part2()}')
