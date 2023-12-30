from utils import read_day

def parse_seeds(line):
  return [int(n) for n in line.split(': ')[1].split()]

def parse_maps(lines):
  all_maps = []
  m = {}
  for line in lines:
    if line == '':
      all_maps.append(m)
      m = []
    elif ':' in line:
      continue
    else:
      nums = [int(n) for n in line.split()]
      m.append(nums)
  all_maps.append(m)
  return all_maps

lines = read_day(5)
seeds = parse_seeds(lines[0])
soil_map = parse_maps(lines[1:])

def find_mapping(n, rows):
  for row in rows:
    if n >= row[1] and n < row[1] + row[2]:
      return row[0] + n - row[1]
  return n

def find_location(seed):
  n = seed
  for m in soil_map:
    n = find_mapping(n, m)
  return n

def part1():
  return min(map(find_location, seeds))

print(f'Part 1: {part1()}')

def find_mapping2(n, rows):
  for row in rows:
    if n >= row[0] and n < row[0] + row[2]:
      return row[1] + n - row[0]
  return n

def find_seed(loc):
  n = loc
  for m in soil_map[::-1]:
    n = find_mapping2(n, m)
  return n

def is_seed(i):
  for x in range(0, len(seeds), 2):
    s = seeds[x]
    n = seeds[x+1]
    if i >= s and i < s + n:
      return True
  return False

def part2():
  m = 1000000000
  for i in range(31102000, m):
    if is_seed(find_seed(i)):
      return i
  return m

print(f'Part 2: {part2()}')
