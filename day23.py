from utils import read_day, Vec2d, char_grid
from collections import deque

NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)

grid = read_day(23, char_grid)

def is_valid(pos, grid):
  return pos.x >= 0 and pos.x < len(grid) and pos.y >= 0 and pos.y < len(grid[0]) and grid[pos.x][pos.y] != '#'

def longest_path(grid, start, end):
  stack = deque()
  v = set()
  v.add(start)
  stack.append((0, start, v))
  checked = {start: 0}
  m = 0
  while stack:
    steps, pos, visited = stack.pop()
    if pos == end:
      m = max(m, steps)
    v = grid[pos.x][pos.y]
    neighbors = []
    if v == '^' or v == '.':
      neighbors.append(pos + NORTH)
    if v == '>' or v == '.':
      neighbors.append(pos + EAST)
    if v == 'v' or v == '.':
      neighbors.append(pos + SOUTH)
    if v == '<' or v == '.':
      neighbors.append(pos + WEST)
    for neighbor in neighbors:
      if is_valid(neighbor, grid) and neighbor not in visited:
        n_steps = steps + 1
        if n_steps > checked.get(neighbor, 0):
          checked[neighbor] = n_steps
          stack.append((n_steps, neighbor, visited | set([neighbor])))
  return m

def part1():
  start = Vec2d(0, 1)
  end = Vec2d(len(grid) - 1, len(grid[0]) - 2)
  return longest_path(grid, start, end)

print(f'Part 1: {part1()}')

def build_graph(grid):
  graph = {}
  for r, row in enumerate(grid):
    for c, v in enumerate(row):
      pos = Vec2d(r, c)
      if is_valid(pos, grid):
        ns = []
        for neighbor in ((pos + NORTH),
            pos + WEST,
            pos + SOUTH,
            pos + EAST):
          if is_valid(neighbor, grid):
            ns.append(neighbor)
        graph[pos] = ns
  return prune_graph(graph)

def find_end(prev, curr, graph, prunable):
  distance = 1
  while curr in prunable:
    ns = graph[curr]
    n = ns[0] if ns[0] != prev else ns[1]
    prev = curr
    curr = n
    distance += 1
  return curr, distance

def prune_graph(graph):
  prunable = set()
  for k, ns in graph.items():
    if len(ns) == 2:
      prunable.add(k)
  pruned = {}
  for k in prunable:
    p, p_dist = find_end(k, graph[k][0], graph, prunable)
    n, n_dist = find_end(k, graph[k][1], graph, prunable)
    distance = p_dist + n_dist
    pruned.setdefault(p, set()).add((n, distance))
    pruned.setdefault(n, set()).add((p, distance))
  return pruned

def longest_path2(graph, start, end):
  stack = deque()
  v = set()
  v.add(start)
  stack.append((0, start, v))
  checked = {start: 0}
  m = 0
  while stack:
    steps, pos, visited = stack.pop()
    if pos == end:
      m = max(m, steps)
      continue
    for neighbor, distance in graph[pos]:
      if neighbor not in visited:
        n_steps = steps + distance
        stack.append((n_steps, neighbor, visited | set([neighbor])))
  return m

def part2():
  start = Vec2d(0, 1)
  end = Vec2d(len(grid) - 1, len(grid[0]) - 2)
  return longest_path2(build_graph(grid), start, end)

print(f'Part 2: {part2()}')
