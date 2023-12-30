from utils import read_day, prod

lines = read_day(6)

def parse_line(line):
  return [int(n) for n in line.split(':')[1].split()]

def distance(n, t):
  return n * (t - n)

def paths(race):
  t, d = race
  count = 0
  for n in range(1, t):
    count += distance(n, t) > d
  return count

def part1():
  races = list(zip(parse_line(lines[0]), parse_line(lines[1])))
  return prod(paths(r) for r in races)

print(f'Part 1: {part1()}')

def parse_line2(line):
  return int(line.split(':')[1].replace(' ', ''))

def part2():
  race = (parse_line2(lines[0]), parse_line2(lines[1]))
  return paths(race)

print(f'Part 2: {part2()}')
