from utils import read_day, Vec2d
from itertools import combinations

MIN_P = 200000000000000
MAX_P = 400000000000000

def parse_vec2d(s):
  parts = [int(n) for n in s.split(', ')]
  return Vec2d(parts[0], parts[1])

def parse_tuple(s):
  return tuple(int(n) for n in s.split(', '))

def parse_line2d(line):
  a, b = line.split(' @ ')
  return parse_vec2d(a), parse_vec2d(b)

def parse_line3d(line):
  a, b = line.split(' @ ')
  return parse_tuple(a), parse_tuple(b)

vectors_2d = read_day(24, parse_line2d)
vectors_3d = read_day(24, parse_line3d)

def intersect(vec1, vec2):
  '''
  Formula:
  # p = point, v = velocity
  # q = p + v
  # m = (q.y - p.y) / (q.x - p.x)
  # b = p.y - m * p.x
  # cx = (b2 - b1) / (m1 - m2)
  # cy = m1 * cx + b1
  '''

  p1, v1 = vec1
  p2, v2 = vec2

  q1 = p1 + v1
  q2 = p2 + v2

  if p1.x == q1.x or p2.x == q2.x:
    # Returns 0, 0 for anything invalid since it's outside of the test area
    return Vec2d(0, 0)
  m1 = (q1.y - p1.y) / (q1.x - p1.x)
  m2 = (q2.y - p2.y) / (q2.x - p2.x)

  b1 = p1.y - m1 * p1.x
  b2 = p2.y - m2 * p2.x

  if m1 == m2:
    return Vec2d(0, 0)
  cx = (b2 - b1) / (m1 - m2)
  cy = m1 * cx + b1

  if (cx - p1.x < 0) != (q1.x - p1.x < 0):
    return Vec2d(0, 0)
  if (cy - p1.y < 0) != (q1.y - p1.y < 0):
    return Vec2d(0, 0)
  if (cx - p2.x < 0) != (q2.x - p2.x < 0):
    return Vec2d(0, 0)
  if (cy - p2.y < 0) != (q2.y - p2.y < 0):
    return Vec2d(0, 0)

  return Vec2d(cx, cy)

def part1():
  total = 0
  for v1, v2 in combinations(vectors_2d, 2):
    p = intersect(v1, v2)
    total += int(p.x >= MIN_P and p.x <= MAX_P and p.y >= MIN_P and p.y <= MAX_P)
  return total

print(f'Part 1: {part1()}')

def axis_velocities(p1, v1, p2, v2):
  valid = set()
  if v1 == v2 and abs(v1) > 0:
    dp = abs(p2 - p1)
    dv = v2 - v1
    for v in range(1, 1000):
      if v == v1:
        valid.add(v)
        continue
      if dp % v == 0:
        valid.add(v1 + v)
        valid.add(v1 - v)
  return valid

def find_velocity(vectors):
  valid = [None, None, None]
  for vec1, vec2 in combinations(vectors, 2):
    p1, v1 = vec1
    p2, v2 = vec2
    for i in range(3):
      v = axis_velocities(p1[i], v1[i], p2[i], v2[i])
      if v:
        valid[i] = v if not valid[i] else valid[i] & v
    if all(v and len(v) == 1 for v in valid):
      break
  return *valid[0], *valid[1], *valid[2]

def find_position(vr, p1, v1, p2, v2):
  vrx, vry, vrz = vr
  p1x, p1y, p1z = p1
  v1x, v1y, v1z = v1
  p2x, p2y, p2z = p2
  v2x, v2y, v2z = v2
  m1 = (v1y - vry) / (v1x - vrx)
  m2 = (v2y - vry) / (v2x - vrx)
  b1 = p1y - m1 * p1x
  b2 = p2y - m2 * p2x
  xr = (b2 - b1) / (m1 - m2)
  yr = m1 * xr + b1
  t = (xr - p1x) / (v1x - vrx)
  zr = p1z + (v1z - vrz) * t
  return xr, yr, zr

def part2():
  vr = find_velocity(vectors_3d)
  p1, v1 = vectors_3d[0]
  p2, v2 = vectors_3d[1]
  return sum(int(n) for n in find_position(vr, p1, v1, p2, v2))

print(f'Part 2: {part2()}')
