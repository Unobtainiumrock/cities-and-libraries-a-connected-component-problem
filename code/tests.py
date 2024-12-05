# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Tuple, Optional
from solution import roads_and_libraries as correct_roads_and_libraries
from user_solution import roads_and_libraries as user_roads_and_libraries

import unittest
import random

# Global list to store user-provided test cases
user_provided_test_cases: List[Tuple[int, int, int, List[List[int]]]] = []

def generate_random_test_case(
    n_min: int,
    n_max: int,
    c_lib_min: int,
    c_lib_max: int,
    c_road_min: int,
    c_road_max: int,
    seed: Optional[int] = None
) -> Tuple[int, int, int, List[List[int]]]:
    """
    Generates a random test case for the roads and libraries problem.

    Args:
        n_min (int): Minimum number of cities.
        n_max (int): Maximum number of cities.
        c_lib_min (int): Minimum cost of building a library.
        c_lib_max (int): Maximum cost of building a library.
        c_road_min (int): Minimum cost of building a road.
        c_road_max (int): Maximum cost of building a road.
        seed (Optional[int]): Seed for random number generation.

    Returns:
        Tuple[int, int, int, List[List[int]]]: Generated test case parameters.
    """
    
    if seed is not None:
        random.seed(seed)
        
    n = random.randint(n_min, n_max)
    c_lib = random.randint(c_lib_min, c_lib_max)
    c_road = random.randint(c_road_min, c_road_max)
    max_edges = n * (n - 1) // 2
    m = random.randint(0, max_edges)
    edges = set()
    
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u != v:
            edge = (min(u, v), max(u, v))
            edges.add(edge)
            
    city_edges = [list(edge) for edge in edges]
    
    return n, c_lib, c_road, city_edges

class TestRoadsAndLibraries(unittest.TestCase):
    def test_case_1(self) -> None:
        n = 7
        c_lib = 3
        c_road = 2
        city_edges = [[1, 2], [2, 3], [3, 1], [4, 1], [5, 6], [6, 7]]
        expected = correct_roads_and_libraries(n, c_lib, c_road, city_edges)
        result = user_roads_and_libraries(n, c_lib, c_road, city_edges)
        
        print(f"\nTest Case 1:")
        print(f"  Parameters: n={n}, c_lib={c_lib}, c_road={c_road}")
        print(f"Number of City Edges: {len(city_edges)}")
        print(f"  City Edges: {city_edges}")
        print(f"  Expected Result: {expected}")
        print(f"  User Result: {result}")
        
        self.assertEqual(result, expected)

    def test_case_2(self) -> None:
        n = 6
        c_lib = 2
        c_road = 5
        city_edges = [[1, 3], [3, 4], [2, 4], [1, 2], [2, 3], [5, 6]]
        expected = correct_roads_and_libraries(n, c_lib, c_road, city_edges)
        result = user_roads_and_libraries(n, c_lib, c_road, city_edges)
        
        print(f"\nTest Case 2:")
        print(f"  Parameters: n={n}, c_lib={c_lib}, c_road={c_road}")
        print(f"Number of City Edges: {len(city_edges)}")
        print(f"  City Edges: {city_edges}")
        print(f"  Expected Result: {expected}")
        print(f"  User Result: {result}")
        
        self.assertEqual(result, expected)
        
    def test_user_provided_cases(self) -> None:
        for idx, test_case in enumerate(user_provided_test_cases):
            n, c_lib, c_road, city_edges = test_case
            with self.subTest(test_case=idx):
                
                expected = correct_roads_and_libraries(n, c_lib, c_road, city_edges)
                result = user_roads_and_libraries(n, c_lib, c_road, city_edges)
                
                print(f"\nUser Test Case {idx+1}:")
                print(f"  Parameters: n={n}, c_lib={c_lib}, c_road={c_road}")
                print(f"Number of City Edges: {len(city_edges)}")
                print(f"  City Edges: {city_edges}")
                print(f"  Expected Result: {expected}")
                print(f"  User Result: {result}")
                
                self.assertEqual(
                    result, expected,
                    f"Failed on user-provided test case {idx + 1}\n"
                    f"Parameters:\n"
                    f"n={n}, c_lib={c_lib}, c_road={c_road}\n"
                    f"Edges={city_edges}\n"
                    f"Expected={expected}, Got={result}"
                )

    def test_random_cases(self) -> None:
        for seed in range(1, 11):  # Generate 10 random test cases
            with self.subTest(seed=seed):
                n, c_lib, c_road, city_edges = generate_random_test_case(
                    n_min=2, n_max=100,
                    c_lib_min=1, c_lib_max=100,
                    c_road_min=1, c_road_max=100,
                    seed=seed
                )
                
                expected = correct_roads_and_libraries(n, c_lib, c_road, city_edges)
                result = user_roads_and_libraries(n, c_lib, c_road, city_edges)
                
                print(f"\nRandom Test Case (Seed {seed}):")
                print(f"  Parameters: n={n}, c_lib={c_lib}, c_road={c_road}")
                print(f"Number of City Edges: {len(city_edges)}")
                print(f"  City Edges: {city_edges}")
                print(f"  Expected Result: {expected}")
                print(f"  User Result: {result}")
                
                self.assertEqual(
                    result, expected,
                    f"Failed on random test case with seed {seed}\n"
                    f"Parameters:\n"
                    f"n={n}, c_lib={c_lib}, c_road={c_road}\n"
                    f"Edges={city_edges}\n"
                    f"Expected={expected}, Got={result}"
            )

