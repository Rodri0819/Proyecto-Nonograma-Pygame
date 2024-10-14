import pytest
from utils import generate_clues, check_win

def test_generate_clues_simple():
    solution = [
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 0]
    ]
    expected_row_clues = [[2], [2], [2]]
    expected_col_clues = [[1, 1], [3], [1]]

    row_clues, col_clues = generate_clues(solution, 3, 3)
    assert row_clues == expected_row_clues
    assert col_clues == expected_col_clues

def test_check_win_correct_solution():
    solution = [
        [1, 0],
        [0, 1]
    ]
    grid = [
        [1, 0],
        [0, 1]
    ]
    assert check_win(grid, solution, 2, 2) == True

def test_check_win_incorrect_solution():
    solution = [
        [1, 0],
        [0, 1]
    ]
    grid = [
        [1, 1],
        [0, 1]
    ]
    assert check_win(grid, solution, 2, 2) == False

def test_generate_clues_empty_solution():
    solution = [
        [0, 0],
        [0, 0]
    ]
    expected_row_clues = [[0], [0]]
    expected_col_clues = [[0], [0]]

    row_clues, col_clues = generate_clues(solution, 2, 2)
    assert row_clues == expected_row_clues
    assert col_clues == expected_col_clues