from utils import read_day, char_grid, Vec2d
from collections import deque

NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)
ROCK = '#'
OPEN = '.'
START = 'S'

LIMIT = 64
NUM_SQUARES = (26501365 - 65) // 131

grid = read_day(21, char_grid)

def is_valid(pos, grid):
  return pos.x >= 0 and pos.x < len(grid) and pos.y >= 0 and pos.y < len(grid[0]) and grid[pos.x][pos.y] != ROCK

def build_graph(grid):
  graph = {}
  vc = {}
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      pos = Vec2d(r, c)
      val = vc.get(pos)
      if val is None:
        val = vc[pos] = is_valid(pos, grid)
      if val:
        graph[pos] = []
        for neighbor in (
            pos + NORTH,
            pos + EAST,
            pos + SOUTH,
            pos + WEST,
            ):
          nval = vc.get(neighbor)
          if nval is None:
            nval = vc[neighbor] = is_valid(neighbor, grid)
          if nval:
            graph[pos].append(neighbor)
  return graph

def find_path(graph, start):
  q = deque()
  q.append((start, 0))
  odd = {}
  even = {start: 0}
  while q:
    pos, steps = q.popleft()
    if steps == LIMIT:
      continue
    n_steps = steps + 1
    for neighbor in graph[pos]:
      if n_steps % 2 == 1 and n_steps < odd.get(neighbor, 1000):
        odd[neighbor] = n_steps
        q.append((neighbor, n_steps))
      if n_steps % 2 == 0 and n_steps < even.get(neighbor, 1000):
        even[neighbor] = n_steps
        q.append((neighbor, n_steps))
  return len(even)

def find_start(grid):
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      if v == 'S':
        return Vec2d(r, c)
  return Vec2d(0, 0)

def part1():
  start = find_start(grid)
  graph = build_graph(grid)
  return find_path(graph, start)

print(f'Part 1: {part1()}')

def find_path2(graph, start):
  q = deque()
  q.append((start, 0))
  odd = {}
  even = {start: 0}
  while q:
    pos, steps = q.popleft()
    n_steps = steps + 1
    for neighbor in graph[pos]:
      if n_steps % 2 == 1 and n_steps < odd.get(neighbor, 1000):
        odd[neighbor] = n_steps
        q.append((neighbor, n_steps))
      if n_steps % 2 == 0 and n_steps < even.get(neighbor, 1000):
        even[neighbor] = n_steps
        q.append((neighbor, n_steps))
  return even, odd

def part2():
  start = find_start(grid)
  graph = build_graph(grid)

  # This part is hard! Derived from:
  # https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
  even, odd = find_path2(graph, start)
  even_corners = [n for n, s in even.items() if s > 65]
  odd_corners = [n for n, s in odd.items() if s > 65]

  total_even = NUM_SQUARES ** 2 * len(even)
  total_odd = (NUM_SQUARES + 1) ** 2 * len(odd)

  total_even_corners = NUM_SQUARES * len(even_corners)
  total_odd_corners = (NUM_SQUARES + 1) * len(odd_corners)

  return total_odd + total_even - total_odd_corners + total_even_corners

print(f'Part 2: {part2()}')
