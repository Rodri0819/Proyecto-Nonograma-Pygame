import pytest
from nonogram_game import NonogramGame

def test_generate_solution_dimensions():
    rows, cols = 5, 7
    solution = NonogramGame.generate_solution(rows, cols)
    assert len(solution) == rows
    assert all(len(row) == cols for row in solution)

def test_generate_solution_values():
    rows, cols = 3, 3
    solution = NonogramGame.generate_solution(rows, cols)
    valid_values = {0, 1}
    for row in solution:
        for cell in row:
            assert cell in valid_values