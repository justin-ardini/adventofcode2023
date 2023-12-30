from collections import Counter
from utils import read_day

def score(hand):
  c = Counter(hand)
  triple = False
  pair = False
  for elm, n in c.most_common():
    if n == 5:
      return 70
    elif n == 4:
      return 60
    elif n == 3:
      triple = True
    elif n == 2:
      if triple:
        return 50
      elif pair:
        return 30
      else:
        pair = True
    elif n == 1:
      if triple:
        return 40
      elif pair:
        return 20
      else:
        return 10
  return 10

VALUES = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

def tiebreak(hand):
  l = len(hand)
  return sum(15**(l-i-1) * VALUES[c] for i, c in enumerate(hand))

def parse_hand(line):
  hand, b = line.split(' ')
  bid = int(b)
  return (score(hand), tiebreak(hand), bid, hand)

lines = read_day(7)

def winnings(rank, hand):
  return rank * hand[2]

def part1():
  hands = [parse_hand(l) for l in lines]
  sorted_hands = sorted(hands, reverse=True)
  l = len(sorted_hands)
  return sum(winnings(l-i, h) for i, h in enumerate(sorted_hands))

print(f'Part 1: {part1()}')

def score2(hand):
  c = Counter(hand)
  triple = False
  pair = False
  jokers = c['J']
  if jokers == 5:
    return 70
  use_joker = True
  for elm, m in c.most_common():
    if elm == 'J':
      continue
    n = m
    if use_joker:
      n += jokers
      use_joker = False
    if n == 5:
      return 70
    elif n == 4:
      return 60
    elif n == 3:
      triple = True
    elif n == 2:
      if triple:
        return 50
      elif pair:
        return 30
      else:
        pair = True
    elif n == 1:
      if triple:
        return 40
      elif pair:
        return 20
      else:
        return 10
  if triple:
    return 50
  elif pair:
    return 30
  return 10

VALUES2 = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1}

def tiebreak2(hand):
  l = len(hand)
  values = VALUES.copy()
  values['J'] = 1
  return sum(15**(l-i-1) * values[c] for i, c in enumerate(hand))

def parse_hand2(line):
  hand, b = line.split(' ')
  bid = int(b)
  return (score2(hand), tiebreak2(hand), bid, hand)

def part2():
  hands = [parse_hand2(l) for l in lines]
  sorted_hands = sorted(hands, reverse=True)
  l = len(sorted_hands)
  return sum(winnings(l-i, h) for i, h in enumerate(sorted_hands))

print(f'Part 2: {part2()}')
