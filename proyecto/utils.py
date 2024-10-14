def generate_clues(solution, rows, cols):
    row_clues = []
    col_clues = []

    for row in solution:
        clues = []  #Lista temporal para almacenar las pistas de la fila actual
        contador = 0  #Contador
        for cell in row:
            if cell == 1:  #Si la celda está marcada
                contador += 1  #Incrementa el contador
            elif contador > 0:  #Si se encuentra un 0 y hay una secuencia anterior de 1s
                clues.append(contador)  #Añade la secuencia de 1s a las pistas
                contador = 0  #Reinicia el contador
        if contador > 0:  #Si hay una secuencia de'1s al final de la fila
            clues.append(contador)  #Añádela a las pistas
        row_clues.append(clues or [0])  #Si no hay pistas, añade 0 para indicar que la fila está vacía

    #Generar pistas para las columnas
    for col in range(cols):
        clues = []  #Lista temporal para almacenar las pistas de la columna actual
        count = 0  #Contador para contar secuencias de 1 (celdas marcadas)
        for row in range(rows):
            if solution[row][col] == 1:  #Si la celda está marcada
                count += 1  #Incrementa el contador
            elif count > 0:  #Si se encuentra un 0 y hay una secuencia anterior de 1s
                clues.append(count)  #Añade la secuencia de 1s a las pistas
                count = 0  #Reinicia el contador
        if count > 0:  #Si hay una secuencia de 1s al final de la columna
            clues.append(count)  #Añádela a las pistas
        col_clues.append(clues or [0])  #Si no hay pistas, añade 0 para indicar que la columna está vacía

    return row_clues, col_clues  #Devuelve las pistas de filas y columnas


#Función para verificar si el jugador ha completado correctamente el Nonograma
def check_win(grid, solution, rows, cols):
    #Recorrer cada celda de la cuadrícula y compararla con la solución
    for row in range(rows):
        for col in range(cols):
            #Verificar si hay una discrepancia entre la cuadrícula y la solución
            if grid[row][col] == 1 and solution[row][col] != 1:
                return False  #Si el jugador ha marcado una celda que no debería estar marcada
            if grid[row][col] == 0 and solution[row][col] == 1:
                return False  #Si el jugador no ha marcado una celda que debería estar marcada
            if grid[row][col] == -1 and solution[row][col] == 1:
                return False  #Si el jugador ha marcado como incorrecta una celda que debería estar marcada
    return True  #Si no se encuentran discrepancias, el jugador ha ganado
