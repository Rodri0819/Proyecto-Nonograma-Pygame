def generate_clues(solution, rows, cols):
    row_clues = []
    col_clues = []

    # Generar pistas para las filas
    for row in solution:
        clues = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        row_clues.append(clues or [0])

    # Generar pistas para las columnas
    for col in range(cols):
        clues = []
        count = 0
        for row in range(rows):
            if solution[row][col] == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues or [0])

    return row_clues, col_clues



def check_win(grid, solution, rows, cols):
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1 and solution[row][col] != 1:
                return False
            if grid[row][col] == 0 and solution[row][col] == 1:
                return False
            if grid[row][col] == -1 and solution[row][col] == 1:
                return False
    return True
