from constants import *

#Clase que representa la cuadrícula del Nonograma
class Grid:
    def __init__(self, rows, cols, square_size, top_margin, left_margin, screen):
        #Inicialización de atributos de la cuadrícula
        self.rows = rows  #Número de filas del tablero
        self.cols = cols  #Número de columnas del tablero
        self.square_size = square_size  #Tamaño de cada celda en la cuadrícula
        self.top_margin = top_margin  #Margen superior donde comenzará el tablero
        self.left_margin = left_margin  #Margen izquierdo donde comenzará el tablero
        self.screen = screen  #Pantalla de Pygame donde se dibuja el tablero
        #Inicializa la cuadrícula vacía
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.win = False

    def reset(self):
        # Reinicia el estado de la cuadrícula
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.win = False

    #Método para dibujar la cuadrícula y las pistas en la pantalla
    def draw(self, row_clues, col_clues):
        #Rellena toda la pantalla con el color blanco
        self.screen.fill(WHITE)

        #Dibujar las pistas para las filas
        for i, clues in enumerate(row_clues):
            text = ' '.join(map(str, clues))  #Convierte las pistas de la fila en una cadena de texto
            clue_surface = FONT.render(text, True, BLACK)  #Renderiza el texto de las pistas usando la fuente
            #Coloca las pistas en la pantalla
            self.screen.blit(clue_surface, (10, self.top_margin + i * self.square_size))

        #Dibujar las pistas para las columnas
        for i, clues in enumerate(col_clues):
            for j, clue in enumerate(clues):
                clue_surface = FONT.render(str(clue), True, BLACK)  #Renderiza cada pista de columna como texto
                #Calcula la posición x e y para colocar la pista en la pantalla
                x = self.left_margin + i * self.square_size + self.square_size / 2 - 10
                y = 10 + j * 15
                #Dibuja las pistas de las columnas en la pantalla
                self.screen.blit(clue_surface, (x, y))

        #Dibujar la cuadrícula del jugador
        for row in range(self.rows):
            for col in range(self.cols):
                #Define un rectángulo en la cuadrícula con las dimensiones y posición correspondientes
                rect = pygame.Rect(
                    self.left_margin + col * self.square_size,
                    self.top_margin + row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                #Dibujar celdas basadas en el estado de cada celda en la cuadrícula
                if self.grid[row][col] == 1:  #Si la celda está marcada por el jugador
                    pygame.draw.rect(self.screen, GRAY, rect)  #Rellena la celda con color gris
                elif self.grid[row][col] == -1:  #Si la celda está marcada incorrectamente
                    pygame.draw.rect(self.screen, RED, rect)  #Rellena la celda con color rojo
                pygame.draw.rect(self.screen, BLACK, rect, 1)  #Dibuja el borde negro de la celda

    #Método para manejar los clics del jugador en la cuadrícula
    def handle_click(self, pos, button):
        #Obtiene las coordenadas x, y del clic del ratón
        x, y = pos
        #Calcula en qué fila y columna de la cuadrícula se hizo clic
        row = (y - self.top_margin) // self.square_size
        col = (x - self.left_margin) // self.square_size

        #Verifica si el clic está dentro de los límites de la cuadrícula
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if button == 1:  #Si se presionó el botón izquierdo del ratón
                if self.grid[row][col] == 0:  #Si la celda está vacía, márcala
                    self.grid[row][col] = 1
                elif self.grid[row][col] == 1:  #Si ya está marcada, cámbiala a incorrecta
                    self.grid[row][col] = -1
                else:  #Si está marcada como incorrecta, vacía la celda
                    self.grid[row][col] = 0
            elif button == 3:  #Si se presionó el botón derecho del ratón
                if self.grid[row][col] == 0:  #Si la celda está vacía, márcala como incorrecta
                    self.grid[row][col] = -1
                elif self.grid[row][col] == -1:  #Si está marcada como incorrecta, márcala
                    self.grid[row][col] = 1
                else:  #Si está marcada, vacía la celda
                    self.grid[row][col] = 0

    #Método para mostrar el mensaje de victoria cuando el jugador gana
    def display_win_message(self, width, height):
        #Renderiza el mensaje de victoria usando la fuente grande
        win_message = WIN_FONT.render("¡Ganaste!", True, GREEN)
        #Dibuja el mensaje de victoria en el centro de la pantalla
        self.screen.blit(win_message, (width // 2 - win_message.get_width() // 2, height // 2))

    #Método para obtener el estado actual de la cuadrícula (devuelve la matriz de celdas)
    def get_grid(self):
        return self.grid  #Retorna la cuadrícula actual
