from utils import read_day
from collections import deque
from math import lcm

BROADCAST = 1
FLIPFLOP = 2
CONJUNCTION = 3
OFF = 0
ON = 1
HI = 2
LO = 3

def build_graph(lines):
  graph = {}
  for line in lines:
    label, dest = line.split(' -> ')
    destinations = dest.split(', ')
    if label.startswith('broadcaster'):
      t = BROADCAST
    elif label.startswith('%'):
      t = FLIPFLOP
      label = label[1:]
    elif label.startswith('&'):
      t = CONJUNCTION
      label = label[1:]
    graph[label] = (t, destinations)
  return graph

graph = build_graph(read_day(20))

def init_states(graph):
  states = {}
  for k, v in graph.items():
    if v[0] == FLIPFLOP:
      states[k] = OFF
    elif v[0] == CONJUNCTION:
      m = {}
      for k2, v2 in graph.items():
        if k in v2[1]:
          m[k2] = LO
      states[k] = m
  return states

def push_button(graph, states):
  q = deque()
  q.append(('broadcaster', LO, 'button'))
  totals = {LO: 0, HI: 0}
  while q:
    label, pulse, source = q.popleft()
    totals[pulse] += 1
    if label not in graph:
      # Output node
      continue
    t, neighbors = graph[label]
    if t == BROADCAST:
      for n in neighbors:
        q.append((n, pulse, label))
    elif t == FLIPFLOP and pulse == LO:
      if states[label] == ON:
        states[label] = OFF
        pulse = LO
      else:
        states[label] = ON
        pulse = HI
      for n in neighbors:
        q.append((n, pulse, label))
    elif t == CONJUNCTION:
      m = states[label]
      m[source] = pulse
      if all(v == HI for v in m.values()):
        pulse = LO
      else:
        pulse = HI
      for n in neighbors:
        q.append((n, pulse, label))
  return totals

def part1():
  states = init_states(graph)
  totals = {LO: 0, HI: 0}
  for _ in range(1000):
    pulses = push_button(graph, states)
    totals[LO] += pulses[LO]
    totals[HI] += pulses[HI]
  return totals[LO] * totals[HI]

print(f'Part 1: {part1()}')

def push_button2(graph, states, cycles, i):
  q = deque()
  q.append(('broadcaster', LO, 'button'))
  totals = {LO: 0, HI: 0}
  while q:
    label, pulse, source = q.popleft()
    totals[pulse] += 1
    if label not in graph:
      if label == 'rx' and pulse == LO:
        return True
      continue
    t, neighbors = graph[label]
    if t == BROADCAST:
      for n in neighbors:
        q.append((n, pulse, label))
    elif t == FLIPFLOP and pulse == LO:
      if states[label] == ON:
        states[label] = OFF
        pulse = LO
      else:
        states[label] = ON
        pulse = HI
      for n in neighbors:
        q.append((n, pulse, label))
    elif t == CONJUNCTION:
      m = states[label]
      m[source] = pulse
      if all(v == HI for v in m.values()):
        pulse = LO
      else:
        pulse = HI
        if label in cycles.keys():
          cycles[label].append(i)
      for n in neighbors:
        q.append((n, pulse, label))
  return False

def part2():
  states = init_states(graph)
  # Not a general solution!
  # For this input, 'rm' conjunction outputs to 'rx'
  cycles = {k: [] for k in states['rm'].keys()}
  for i in range(1_000_000):
    push_button2(graph, states, cycles, i)
    if all(len(l) > 1 for l in cycles.values()):
      break
  return lcm(*(l[1] - l[0] for l in cycles.values()))

print(f'Part 2: {part2()}')
