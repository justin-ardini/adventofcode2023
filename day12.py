from utils import read_day
from functools import cache

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

def parse_line(line):
  a, b = line.split()
  parts = tuple(int(n) for n in b.split(','))
  return a, parts

lines = read_day(12, parse_line)

@cache
def count_rec(fields, splits):
  if not splits:
    return int(DAMAGED not in fields)
  n_split = splits[0]
  total = 0
  for i in range(len(fields) - n_split + 1):
    # Count iff all fields are damaged and the field after is empty.
    if all(f == DAMAGED or f == UNKNOWN for f in fields[i:i+n_split]):
      if i+n_split == len(fields) or fields[i+n_split] != DAMAGED:
        total += count_rec(fields[i+n_split+1:], splits[1:])
    if fields[i] == DAMAGED:
      break
  return total

def part1():
  return sum(count_rec(a, b) for a, b in lines)

print(f'Part 1: {part1()}')

def unfold(line):
  a, b = line
  ua = ((a + '?') * 5)[:-1]
  ub = b * 5
  return ua, ub

def part2():
  return sum(count_rec(*unfold(l)) for l in lines)

print(f'Part 2: {part2()}')
