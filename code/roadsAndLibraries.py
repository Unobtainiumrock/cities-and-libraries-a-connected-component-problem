# Copyright 2024 Nicholas Fleischhauer
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from tests import TestRoadsAndLibraries, user_provided_test_cases
from user_solution import roads_and_libraries

def run_unit_tests(user_test_cases):
    # Add the user test cases to the global variable
    user_provided_test_cases.extend(user_test_cases)

    # Load tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoadsAndLibraries)
    # Run tests
    unittest.TextTestRunner(verbosity=2, buffer=False).run(suite)

def main():
    print("Welcome to the Roads and Libraries Problem Solver!")

    user_test_cases = []  # List to store user-entered test cases

    # Prompting for number of test cases
    q = int(input("Enter the number of test cases: ").strip())

    for test_num in range(1, q + 1):
        print(f"\nTest case {test_num}:")

        # Prompting for cities, roads, library cost, and road cost
        print("Enter n (number of cities), m (number of roads), c_lib (cost of library), c_road (cost of road) separated by spaces:")
        n, m, c_lib, c_road = map(int, input().strip().split())

        city_edges = []
        print(f"Enter {m} roads (two cities per road):")

        # Reading roads
        for _ in range(m):
            u, v = map(int, input().strip().split())
            city_edges.append([u, v])

        # Store the test case for unit testing later
        user_test_cases.append((n, c_lib, c_road, city_edges))

        # Calculating result and printing feedback
        result = roads_and_libraries(n, c_lib, c_road, city_edges)
        print(f"Minimum cost: {result}")

    print("\nNow running unit tests...")
    # Running the unit tests after processing user input
    run_unit_tests(user_test_cases)

if __name__ == '__main__':
    main()
