from utils import read_day, Vec2d, prod
import re

GT = 'gt'
LT = 'lt'
LABEL = 'label'
ACCEPT = 'A'
REJECT = 'R'

def parse_order(line):
  name, order = line.split('{')
  cmds = order[:-1].split(',')
  commands = []
  for cmd in cmds:
    if '>' in cmd:
      m = re.search(r"(\w+)>(\w+):(\w+)", cmd)
      commands.append((GT, m.group(1), int(m.group(2)), m.group(3)))
    elif '<' in cmd:
      m = re.search(r"(\w+)<(\w+):(\w+)", cmd)
      commands.append((LT, m.group(1), int(m.group(2)), m.group(3)))
    else:
      commands.append((LABEL, cmd))
  return name, commands

def parse_part(line):
  m = re.search(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line)
  return {'x': int(m.group(1)), 'm': int(m.group(2)), 'a': int(m.group(3)), 's': int(m.group(4))}

def parse_lines(lines):
  b = lines.index('')
  orders = [parse_order(l) for l in lines[:b]]
  parts = [parse_part(l) for l in lines[b+1:]]
  return orders, parts

lines = read_day(19)
orders, parts = parse_lines(lines)

def process(part, order_map, o):
  if o == ACCEPT:
    return True
  if o == REJECT:
    return False

  for cmd in order_map[o]:
    if cmd[0] == GT:
      n = part[cmd[1]]
      if n > cmd[2]:
        return process(part, order_map, cmd[3])
    elif cmd[0] == LT:
      n = part[cmd[1]]
      if n < cmd[2]:
        return process(part, order_map, cmd[3])
    elif cmd[0] == LABEL:
      return process(part, order_map, cmd[1])
  return False

def part1():
  order_map = {name: cmd for name, cmd in orders}
  total = 0
  for part in parts:
    if process(part, order_map, 'in'):
      total += sum(part.values())
  return total

print(f'Part 1: {part1()}')

def valid_ranges(ranges, order_map, o):
  if o == ACCEPT:
    return [ranges]
  if o == REJECT:
    return []

  all_ranges = []
  for cmd in order_map[o]:
    label = cmd[1]
    if cmd[0] == GT:
      n = cmd[2]
      new_ranges = ranges.copy()
      a, b = ranges[label]
      ranges[label] = (a, n)
      new_ranges[label] = (n + 1, b)
      all_ranges += valid_ranges(new_ranges, order_map, cmd[3])
    elif cmd[0] == LT:
      n = cmd[2]
      new_ranges = ranges.copy()
      a, b = ranges[label]
      ranges[label] = (n, b)
      new_ranges[label] = (a, n - 1)
      all_ranges += valid_ranges(new_ranges, order_map, cmd[3])
    elif cmd[0] == LABEL:
      all_ranges += valid_ranges(ranges, order_map, label)
  return all_ranges

def range_size(r):
  return prod(b - a + 1 for a, b in r.values())

def part2():
  order_map = {name: cmd for name, cmd in orders}
  ranges = {
      'x': (1, 4000),
      'm': (1, 4000),
      'a': (1, 4000),
      's': (1, 4000),
  }
  all_ranges = valid_ranges(ranges, order_map, 'in')
  return sum(range_size(r) for r in all_ranges)

print(f'Part 2: {part2()}')
