from utils import read_day

def parse_line(line):
  a, b = line.split(': ')
  w, p = b.split('|')
  win = set(int(n) for n in w.split())
  player = [int(n) for n in p.split()]
  return win, player

cards = read_day(4, parse_line)

def score(win, player):
  score = 0
  for n in player:
    if n in win:
      score = 1 if score == 0 else score * 2
  return score

def part1():
  total = 0
  for win, player in cards:
    total += score(win, player)
  return total

print(f'Part 1: {part1()}')

def score2(win, player):
  return sum(n in win for n in player)

def score_card(i, cards, scores):
  total = 0
  n = scores[i]
  for j in range(i + 1, min(i + 1 + n, len(cards))):
    total += 1 + score_card(j, cards, scores)
  return total

def part2():
  scores = {}
  for i, (win, player) in enumerate(cards):
    scores[i] = score2(win, player)
  total = sum(score_card(i, cards, scores) for i in range(len(cards)))
  return len(cards) + total

print(f'Part 2: {part2()}')
