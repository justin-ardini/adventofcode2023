from utils import read_day

steps = read_day(15)[0].split(',')

def run_hash(step):
  val = 0
  for c in step:
    val += ord(c)
    val *= 17
    val = val % 256
  return val

def part1():
  return sum(run_hash(s) for s in steps)

print(f'Part 1: {part1()}')

DASH = 1
EQUAL = 2

def parse_op(step):
  if step.endswith('-'):
    return step[:-1], DASH, None
  else:
    a, b = step.split('=')
    return a, EQUAL, int(b)

def run_op(op, boxes):
  label = op[0]
  b = run_hash(label)
  box = boxes[b]
  if op[1] == DASH:
    if label in box:
      del box[label]
  else:
    box[label] = op[2]

def total_focus(ops):
  boxes = [{} for _ in range(256)]
  for op in ops:
    run_op(op, boxes)

  total = 0
  for i, box in enumerate(boxes):
    for j, (label, focus) in enumerate(box.items()):
      total += (i + 1) * (j + 1) * focus
  return total

def part2():
  ops = [parse_op(s) for s in steps]
  return total_focus(ops)

print(f'Part 2: {part2()}')
