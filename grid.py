from constants import *
import utils

class Grid:
    def __init__(self, rows, cols, square_size, top_margin, left_margin, screen):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.top_margin = top_margin
        self.left_margin = left_margin
        self.screen = screen
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.win = False

    def draw(self, row_clues, col_clues):
        self.screen.fill(WHITE)
        # Dibujar pistas de las filas
        for i, clues in enumerate(row_clues):
            text = ' '.join(map(str, clues))
            clue_surface = FONT.render(text, True, BLACK)
            self.screen.blit(clue_surface, (10, self.top_margin + i * self.square_size))
        # Dibujar pistas de las columnas
        for i, clues in enumerate(col_clues):
            for j, clue in enumerate(clues):
                clue_surface = FONT.render(str(clue), True, BLACK)
                x = self.left_margin + i * self.square_size + self.square_size / 2 - 10
                y = 10 + j * 15
                self.screen.blit(clue_surface, (x, y))
        # Dibujar la cuadrícula del jugador
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.left_margin + col * self.square_size,
                    self.top_margin + row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, GRAY, rect)
                elif self.grid[row][col] == -1:
                    pygame.draw.rect(self.screen, RED, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

    def handle_click(self, pos, button):
        x, y = pos
        row = (y - self.top_margin) // self.square_size
        col = (x - self.left_margin) // self.square_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if button == 1:
                if self.grid[row][col] == 0:
                    self.grid[row][col] = 1
                elif self.grid[row][col] == 1:
                    self.grid[row][col] = -1
                else:
                    self.grid[row][col] = 0
            elif button == 3:
                if self.grid[row][col] == 0:
                    self.grid[row][col] = -1
                elif self.grid[row][col] == -1:
                    self.grid[row][col] = 1
                else:
                    self.grid[row][col] = 0

    def display_win_message(self, width, height):
        win_message = WIN_FONT.render("¡Ganaste!", True, GREEN)
        self.screen.blit(win_message, (width // 2 - win_message.get_width() // 2, height // 2))

    def get_grid(self):
        return self.grid