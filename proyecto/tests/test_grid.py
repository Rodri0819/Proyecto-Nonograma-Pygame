import pytest
from grid import Grid

def test_handle_click_left_button():
    rows, cols = 3, 3
    grid = Grid(rows, cols, 30, 0, 0, None)

    # Simular un click izquierdo en la celda (1,1)
    pos = (30 + 1, 30 + 1)  # Coordenadas de (1,1)
    grid.handle_click(pos, button=1)

    assert grid.grid[1][1] == 1  # La celda debe estar marcada con 1 (BLACK)

def test_handle_click_right_button():
    rows, cols = 3, 3
    grid = Grid(rows, cols, 30, 0, 0, None)

    # Simular un click derecho en la celda (0,0)
    pos = (1, 1) # Coordenadas de (0,0)
    grid.handle_click(pos, button=3)

    assert grid.grid[0][0] == -1  # La celda debe estar marcada con -1 (RED)

def test_handle_click_toggle():
    rows, cols = 3, 3
    grid = Grid(rows, cols, 30, 0, 0, None)

    # Simular clicks izquierdos consecutivos en la celda (2,2)
    pos = (60 + 1, 60 + 1)
    grid.handle_click(pos, button=1)
    grid.handle_click(pos, button=1)
    grid.handle_click(pos, button=1)

    assert grid.grid[2][2] == 0 # La celda debe estar marcada con 0 (estado inicial)

def test_get_grid():
    rows, cols = 2, 2
    grid = Grid(rows, cols, 30, 0, 0, None)

    grid.grid = [
        [1, -1],
        [0, 1]
    ]

    result_grid = grid.get_grid()

    assert result_grid == grid.grid