from utils import read_day

lines = read_day(1)

digit_chars = {str(i): i for i in range(10)}
digit_words = {
  'one': 1,
  'two': 2,
  'three': 3,
  'four': 4,
  'five': 5,
  'six': 6,
  'seven': 7,
  'eight': 8,
  'nine': 9,
}

def calibration_value(line, digit_map):
  first = -1
  last = -1
  for i, c in enumerate(line):
    for k in digit_map:
      d = digit_map.get(str(line[i:i + len(k)]))
      if d is not None:
        last = d
        if first == -1:
          first = last
  return 10 * first + last

def part1():
  return sum(calibration_value(l, digit_chars) for l in lines)

print(f'Part 1: {part1()}')

def part2():
  return sum(calibration_value(l, digit_chars | digit_words) for l in lines)

print(f'Part 2: {part2()}')
