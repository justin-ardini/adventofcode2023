from utils import read_day, int_list

lines = read_day(9, lambda x: int_list(x, sep=' '))

def build_diffs(row):
  all_rows = [row]
  while any(n != 0 for n in row):
    next_row = []
    for i in range(len(row) - 1):
      next_row.append(row[i+1] - row[i])
    all_rows.append(next_row)
    row = next_row
  return all_rows

def find_next(history):
  return sum(r[-1] for r in history)

def part1():
  total = 0
  for row in lines:
    history = build_diffs(row)
    n = find_next(history)
    total += n
  return total

print(f'Part 1: {part1()}')

def find_prev(history):
  n = 0
  for row in history[::-1]:
    n = row[0] - n
  return n

def part2():
  total = 0
  for row in lines:
    history = build_diffs(row)
    n = find_prev(history)
    total += n
  return total

print(f'Part 2: {part2()}')
