from utils import read_day, prod
from functools import reduce

# [red, green, blue]
MAX_CUBES = [12, 13, 14]

def parse_set(s):
  '''Outputs a rgb triple counting the number of balls.'''
  subsets = [x.strip() for x in s.split(',')]
  balls = [0, 0, 0]
  for s in subsets:
    num, color = s.split(' ')
    n = int(num)
    if color.endswith('red'):
      balls[0] = n
    elif color.endswith('green'):
      balls[1] = n
    elif color.endswith('blue'):
      balls[2] = n
  return balls

def parse_day(line):
  a, b = line.split(':')
  sets = [parse_set(s) for s in b.split(';')]
  return sets

games = read_day(2, parse_day)

def is_valid(game):
  return all(s[i] <= MAX_CUBES[i] for i in range(3) for s in game)

def part1():
  return sum(i + 1 if is_valid(g) else 0 for i, g in enumerate(games))

print(f'Part 1: {part1()}')

def calculate_power(game):
  return prod(reduce(lambda acc, s: [max(s[i], acc[i]) for i in range(3)], game))

def part2():
  return sum(calculate_power(g) for g in games)

print(f'Part 2: {part2()}')
