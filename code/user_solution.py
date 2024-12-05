# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

# from typing import List

# def roads_and_libraries(n: int, c_lib: int, c_road: int, city_edges: List[List[int]]) -> int:
#   """
#   Determines the minimum cost to provide library access to all citizens of HackerLand.

#   Args:
#       n (int): The number of cities.
#       c_lib (int): The cost to build a single library.
#       c_road (int): The cost to build a single road.
#       city_edges (List[List[int]]): A list of edges representing possible roads between cities.
#           Each sublist contains two integers indicating a bidirectional road
#           between the specified cities.

#   Returns:
#       int: The minimal total cost to ensure all citizens have access to a library.

#   Example:
#       >>> n = 7
#       >>> c_lib = 3
#       >>> c_road = 2
#       >>> city_edges = [[1, 2], [2, 3], [3, 1], [4, 1], [5, 6], [6, 7]]
#       >>> roads_and_libraries(n, c_lib, c_road, city_edges)
#       16
#   """
#   ...

# Comment out this and uncomment the top part to try to implement a solution yourself.
from typing import List
from collections import defaultdict, deque

def roads_and_libraries(n: int, c_lib: int, c_road: int, city_edges: List[List[int]]) -> int:
  """
    Determines the minimum cost to provide library access to all citizens of HackerLand.

    Args:
        n (int): The number of cities.
        c_lib (int): The cost to build a single library.
        c_road (int): The cost to build a single road.
        city_edges (List[List[int]]): A list of edges representing possible roads between cities.
            Each sublist contains two integers indicating a bidirectional road
            between the specified cities.

    Returns:
        int: The minimal total cost to ensure all citizens have access to a library.

    Example:
        >>> n = 7
        >>> c_lib = 3
        >>> c_road = 2
        >>> city_edges = [[1, 2], [2, 3], [3, 1], [4, 1], [5, 6], [6, 7]]
        >>> roads_and_libraries(n, c_lib, c_road, city_edges)
        16
    """

  # build the graph
  graph = defaultdict(list)
  for u, v in city_edges:
    graph[u].append(v)
    graph[v].append(u)

  visited = [False] * (n + 1)
  total_cost = 0

  for city in range(1, n + 1):
    if not visited[city]:
      # Start BFS from this city
      queue = deque()
      queue.append(city)
      visited[city] = True
      num_cities_in_component = 1

      while queue:
        current_city = queue.popleft()
        for neighbor in graph[current_city]:
          if not visited[neighbor]:
            visited[neighbor] = True
            queue.append(neighbor)
            num_cities_in_component += 1

      # Calculate the cost for this connected component
      cost_libs_in_all_cities = num_cities_in_component * c_lib
      cost_one_lib_with_roads = c_lib + (num_cities_in_component - 1) * c_road
      min_component_cost = min(cost_libs_in_all_cities, cost_one_lib_with_roads)
      total_cost += min_component_cost
  
  return total_cost
