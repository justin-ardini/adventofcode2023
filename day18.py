from utils import read_day, Vec2d
from collections import deque
from itertools import tee

DIRECTIONS = {
  'U': Vec2d(-1, 0),
  'R': Vec2d(0, 1),
  'D': Vec2d(1, 0),
  'L': Vec2d(0, -1),
}

def pairwise(iterable):
  # Note: Use itertools.pairwise on v3.10+
  a, b = tee(iterable)
  next(b, None)
  return zip(a, b)

def parse_line(line):
  d, n, c = line.split()
  return (d, int(n), c[1:-1])

lines = read_day(18, parse_line)

def calc_area(vertices):
  '''Area of simple polygon using Shoelace theorem.'''
  return abs(sum(a.x * b.y - a.y * b.x for a, b in pairwise(vertices)) // 2)

def internal_points(area, perimeter):
  '''Points in a polygon using Pick's theorem.'''
  return area - perimeter // 2 + 1

def part1():
  pos = Vec2d(0, 0)
  vertices = [pos]
  perimeter = 0
  p1 = False
  for d, n, _ in lines:
    pos += DIRECTIONS[d] * n
    perimeter += n
    vertices.append(pos)
  area = calc_area(vertices)
  return perimeter + internal_points(area, perimeter)

print(f'Part 1: {part1()}')

def parse_color(color):
  n = int(color[1:-1], 16)
  if color[-1] == '0':
    return 'R', n
  elif color[-1] == '1':
    return 'D', n
  elif color[-1] == '2':
    return 'L', n
  elif color[-1] == '3':
    return 'U', n
  return 'D', -1

def part2():
  pos = Vec2d(0, 0)
  vertices = [pos]
  perimeter = 0
  p1 = False
  for _, _, color in lines:
    d, n = parse_color(color)
    pos += DIRECTIONS[d] * n
    perimeter += n
    vertices.append(pos)
  area = calc_area(vertices)
  return perimeter + internal_points(area, perimeter)

print(f'Part 2: {part2()}')
