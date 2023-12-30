from utils import read_day
from math import lcm

def build_graph(lines):
  graph = {}
  for line in lines:
    a, bc = line.split(' = ')
    b, c = bc.split(', ')
    b = b[1:]
    c = c[:-1]
    graph[a] = (b, c)
  return graph

lines = read_day(8)
steps = lines[0]
graph = build_graph(lines[2:])

def part1():
  node = 'AAA'
  t = 0
  while True:
    for step in steps:
      if step == 'L':
        node = graph[node][0]
      else:
        node = graph[node][1]
      t += 1
      if node == 'ZZZ':
        return t

print(f'Part 1: {part1()}')

def start_nodes(graph):
  return [k for k in graph.keys() if k.endswith('A')]

def at_end(nodes):
  return all(n.endswith('Z') for n in nodes)

def part2():
  nodes = start_nodes(graph)
  start_count = len(nodes)
  goal_steps = []
  t = 0
  while True:
    for step in steps:
      for i, node in enumerate(nodes):
        if step == 'L':
          nodes[i] = graph[node][0]
        else:
          nodes[i] = graph[node][1]
      t += 1
      new_nodes = [n for n in nodes if not n.endswith('Z')]
      goal_steps += ([t for _ in range(len(nodes) - len(new_nodes))])
      nodes = new_nodes
      if len(goal_steps) == start_count:
        return lcm(*goal_steps)

print(f'Part 2: {part2()}')
