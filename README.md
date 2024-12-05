# Cities and Libraries: A Connected Component Problem

This project presents an analysis and solution to an algorithmic problem involving the optimization of library and road construction in a network of cities. It includes a detailed LaTeX document explaining the problem and its solution, as well as Python scripts that allow users to interact with the problem, implement their own solutions, and test them against provided and custom test cases.

## Table of Contents
- [Cities and Libraries: A Connected Component Problem](#cities-and-libraries-a-connected-component-problem)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [How to Use](#how-to-use)
    - [Running the Main Program: An Example Walkthrough](#running-the-main-program-an-example-walkthrough)
    - [Implementing Your Own Solution](#implementing-your-own-solution)
    - [Running Unit Tests](#running-unit-tests)
  - [Files Description](#files-description)
    - [main.tex](#maintex)
    - [code/roadsAndLibraries.py](#coderoadsandlibrariespy)
    - [code/solution.py](#codesolutionpy)
    - [code/user\_solution.py](#codeuser_solutionpy)
    - [code/tests.py](#codetestspy)
  - [Understanding the Problem](#understanding-the-problem)
  - [Contributing](#contributing)
  - [License](#license)
  - [License](#license-1)
  - [Contact](#contact)
## Overview

The problem is sourced from HackerRank and involves determining the minimum cost to provide library access to all citizens in a collection of cities, given the costs of building libraries and roads. The goal is to optimize infrastructure costs by strategically deciding where to build libraries and roads.

The project includes:

- A comprehensive LaTeX document (`main.tex`) that refines the problem, explores connected components within graphs, develops a cost-minimizing strategy, and implements an efficient solution.
- Python scripts that allow users to interact with the problem, test their own solutions, and run unit tests.

## Project Structure

- `main.tex`: LaTeX document containing the problem analysis and solution.
- `assets/`: Contains images used in the LaTeX document.
- `code/`: Directory containing Python scripts.
  - `roadsAndLibraries.py`: Main script for user interaction and testing.
  - `solution.py`: Correct (reference) solution to the problem.
  - `user_solution.py`: Template where users can implement their own solution.
  - `tests.py`: Contains unit tests for verifying solutions.

## Getting Started

### Prerequisites

- Python 3.x installed on your machine.
- Basic understanding of Python programming.
- LaTeX compiler (optional, if you wish to compile `main.tex`).

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/cities-and-libraries.git
```

2. **Navigate to the Project Directory**
  
```bash
cd cities-and-libraries
```

## How to Use

### Running the Main Program: An Example Walkthrough

The `roadsAndLibraries.py` script allows you to interact with the problem by entering custom test cases and seeing the results of your (or the provided) solution.

**Steps:**

1. **Navigate to the `code` Directory**

```bash
cd code
```

2. **Run the Script**

```bash
python3 roadsAndLibraries.py
```

3. **Follow the Prompts**
  - **Enter the number of test cases (`q`):**

     It will look like this

     ```bash
     Enter the number of test cases: 2
     ```

  - **For each test case, enter:**
    - **Number of cities (`n`), number of roads (`m`), cost of a library (`c_lib`), and cost of a road (`c_road`):**
  
       It will look like this

       ```bash
       Enter n (number of cities), m (number of roads), c_lib (cost of library), c_road (cost of road) separated by spaces:
       7 6 3 2
       ```

    - **Road connections (`m` lines of `u v` pairs):**
  
      It will look like this

      ```bash
      Enter 6 roads (two cities per road):
      1 2
      2 3
      3 1
      4 1
      5 6
      6 7
      ```
  - **View the Result**
    After entering the data for a test case, the program will compute and display the minimum cost:

      ```bash
      Minimum cost: 16
      ```

4. **Running Unit Tests**
   
  After all test cases have been entered, the program will automatically run unit tests, including your custom test cases.

  **Fulll Example Session**

  It should look something like this

  ```bash
  Welcome to the Roads and Libraries Problem Solver!
Enter the number of test cases: 1

Test case 1:
Enter n (number of cities), m (number of roads), c_lib (cost of library), c_road (cost of road) separated by spaces:
3 3 2 1
Enter 3 roads (two cities per road):
1 2
3 1
2 3
Minimum cost: 4

Now running unit tests...
test_case_1 (__main__.TestRoadsAndLibraries) ... ok
test_user_provided_cases (__main__.TestRoadsAndLibraries) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK

  ```
**note: keep in mind that your output will be more verbose, as I've set the logs to give more thorough outputs when I was building this.**

### Implementing Your Own Solution

If you'd like to test your own implementation of the solution:

1. **Open `user_solution.py` and comment out my solution and uncomment the incomplete part above it.**

2. **Save Your Changes**

3. **Run `roadsAndLibraries.py` Again**

Your implementations will now be used and the unit tests will compare your output against the correct solution.

**Note: Make sure your function returns the correct output format (an integer representing the minimum cost).

### Running Unit Tests

If you don't want to use the interactive application and test some custom inputs, then you can run the unit tests by doing the following:

1. **Run the Tests:**

```bash
python -m unittest tests.py
```

2. **Review the Results:**

Same as before, the tests will compare your solution in `user_solution.py` against the correct one in `solution.py`

## Files Description

### main.tex

- **Description:** LaTex document containig the problem statement, detailed analysis, solution, approach, and conclusions.
- **Usage:** Compile with LaTeX compiler to generate a PDF document

  The following is the one I use for my setup:

```bash
pdflatex --shell-escape -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

This will also engage compile on save for viewing the changes to `main.pdf` in live time.

Keep in mind that this also requires installation of certain packages, tools, and configuration setup on your system and most of that is out of scope. Here's the configuration that I use for my `settings.json`.

```json
{
  "workbench.colorTheme": "Default High Contrast",
  "remote.autoForwardPortsSource": "hybrid",
  "window.zoomLevel": -1,
  "files.insertFinalNewline": true,
  "latex-workshop.latex.tools": [
    {
      "name": "pdflatex",
      "command": "pdflatex",
      "args": [
        "--shell-escape",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "pdflatex",
      "tools": [
        "pdflatex"
      ]
    }
  ],
  "latex-workshop.latex.recipe.default": "pdflatex"
}
```

### code/roadsAndLibraries.py

- **Description:** Main script for interacting with the prolem.
- **Functionality:**
  - Prompts the user for input test cases.
  - Calls the `roads_and_libraries` function from `user_solution.py` (By default, it contains a pasted copy of my solutuion that will need to be toggled off)
  - Displays the minimum cost for each test case.
  - Runs unit tests after processing input.
  
### code/solution.py

- **Description:** Contains the correct (reference) implementation of the `roads_and_libraries` function. Its the same one I go over in the `main.pdf` analysis and walkthrough.
- **Usage:** Used by `tests.py` to compare against user's solution.

### code/user_solution.py

Self explanatory.

### code/tests.py
Compares user's solution against reference solution via unit tests.

## Understanding the Problem

See `main.pdf`, where the entire problem analysis and solution are discussed.

## Contributing

Contributions are welcome! If you'd like to contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**

```bash
git checkout -b feature/YourFeature
```

3. **Commit Your Changes**

```bash
git commit -am 'Add your message here'
```

4. **Push to the Branch**

```bash
git push origin feature/YourFeature
```

5. **Create a Pull Request**

The areas where I see further development being made would be to add in variable costs, or things like road maintenance costs. This would more closely model the real world and could be a lot of fun! I'm always open to new ideas.

## License

## License

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact:

- **Author: Nicholas Fleischhauer**
- **LinkedIn: https://www.linkedin.com/in/unobtainiumrock/**
