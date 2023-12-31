from utils import read_day, int_grid, Vec2d
import heapq

NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)

grid = read_day(17, int_grid)

def is_valid(pos, grid):
  return pos.x >= 0 and pos.x < len(grid) and pos.y >= 0 and pos.y < len(grid[0])

def to_tuple(v):
  return (v.x, v.y)

def from_tuple(t):
  return Vec2d(t[0], t[1])

def find_path(grid, start, end):
  q = []
  heapq.heappush(q, (0, to_tuple(start), to_tuple(EAST), 0, []))
  checked = {(start, EAST, 0): 0}
  while q:
    heat, pos_t, d_t, d_step, path = heapq.heappop(q)
    pos = from_tuple(pos_t)
    d = from_tuple(d_t)
    if pos == end:
      return heat
    for p, nd in (
        (pos, d), 
        (pos, d.turn_left()),
        (pos, d.turn_right()),
        ):
      np = p + nd
      np_tuple = to_tuple(np)
      if is_valid(np, grid) and (d != nd or d_step < 3):
        n_step = d_step + 1 if d == nd else 1
        n_heat = heat + grid[np.x][np.y]
        if n_heat < checked.get((np, nd, n_step), 10000):
          checked[(np, nd, n_step)] = n_heat
          heapq.heappush(q, (n_heat, np_tuple, to_tuple(nd), n_step, path + [np_tuple]))
  return -1

def part1():
  return find_path(grid, Vec2d(0, 0), Vec2d(len(grid) - 1, len(grid[0]) - 1))

print(f'Part 1: {part1()}')

def find_path2(grid, start, end):
  q = []
  heapq.heappush(q, (0, to_tuple(start), to_tuple(EAST), 0, []))
  heapq.heappush(q, (0, to_tuple(start), to_tuple(SOUTH), 0, []))
  checked = {(start, EAST, 0): 0, (start, SOUTH, 0): 0}
  while q:
    heat, pos_t, d_t, d_step, path = heapq.heappop(q)
    pos = from_tuple(pos_t)
    d = from_tuple(d_t)
    if pos == end and d_step >= 4:
      return heat
    for p, nd in (
        (pos, d), 
        (pos, d.turn_left()),
        (pos, d.turn_right()),
        ):
      if d == nd and d_step >= 10:
        continue
      if d != nd and d_step < 4:
        continue
      np = p + nd
      np_tuple = to_tuple(np)
      if is_valid(np, grid):
        n_step = d_step + 1 if d == nd else 1
        n_heat = heat + grid[np.x][np.y]
        if n_heat < checked.get((np, nd, n_step), 10000):
          checked[(np, nd, n_step)] = n_heat
          heapq.heappush(q, (n_heat, np_tuple, to_tuple(nd), n_step, path + [np_tuple]))
  return -1

def part2():
  return find_path2(grid, Vec2d(0, 0), Vec2d(len(grid) - 1, len(grid[0]) - 1))

print(f'Part 2: {part2()}')
