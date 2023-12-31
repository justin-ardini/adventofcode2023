from utils import read_day, char_grid, Vec2d

NORTH = Vec2d(-1, 0)
SOUTH = Vec2d(1, 0)
WEST = Vec2d(0, -1)
EAST = Vec2d(0, 1)

grid = read_day(16, char_grid)

def move(grid, beam, energized):
  pos, d = beam
  if (pos, d) in energized:
    return []
  energized.add((pos, d))
  tile = grid[pos.x][pos.y]
  if tile == '\\':
    d = d.turn_left() if d in (NORTH, SOUTH) else d.turn_right()
  elif tile == '/':
    d = d.turn_right() if d in (NORTH, SOUTH) else d.turn_left()
  elif tile == '-':
    if d == NORTH or d == SOUTH:
      d1 = d.turn_right()
      p1 = pos + d1
      d2 = d.turn_left()
      p2 = pos + d2
      return [(p1, d1), (p2, d2)]
  elif tile == '|':
    if d != NORTH and d != SOUTH:
      d1 = d.turn_right()
      p1 = pos + d1
      d2 = d.turn_left()
      p2 = pos + d2
      return [(p1, d1), (p2, d2)]
  pos += d 
  return [(pos, d)]

def remove_invalid(beams):
  return [(pos, d) for pos, d in beams if pos.x >= 0 and pos.x < len(grid) and pos.y >= 0 and pos.y < len(grid[0])]

def run_sim(beam):
  energized = set()
  beams = [beam]
  while True:
    new_beams = []
    for beam in beams:
      new_beams += move(grid, beam, energized)
    new_beams = remove_invalid(new_beams)
    beams = new_beams
    if len(beams) == 0:
      return len(set(e[0] for e in energized))

def part1():
  return run_sim((Vec2d(0, 0), EAST))

print(f'Part 1: {part1()}')

def part2():
  m = 0
  for r in range(len(grid)):
    m = max(m, run_sim((Vec2d(r, 0), EAST)), run_sim((Vec2d(r, len(grid[0]) - 1), WEST)))
  for c in range(len(grid[0])):
    m = max(m, run_sim((Vec2d(0, c), SOUTH)), run_sim((Vec2d(len(grid) - 1, c), NORTH)))
  return m

print(f'Part 2: {part2()}')
