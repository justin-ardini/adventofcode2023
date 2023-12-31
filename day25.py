from utils import read_day
from collections import defaultdict

def build_graph(lines):
  graph = defaultdict(set)
  for line in lines:
    a, neighbors = line.split(': ')
    for b in neighbors.split():
      graph[a].add(b)
      graph[b].add(a)
  return graph

lines = read_day(25)
graph = build_graph(lines)

def count_connections(neighbors, external_nodes):
  return len(neighbors & external_nodes)

def total_connections(graph, s1, s2):
  return sum(count_connections(graph[k], s2) for k in s1)

def part1():
  s1 = set(graph.keys())
  s2 = set()
  while total_connections(graph, s1, s2) != 3:
    m = max(s1, key=lambda k: count_connections(graph[k], s2))
    s1.remove(m)
    s2.add(m)
  return len(s1) * len(s2)

print(f'Part 1: {part1()}')
