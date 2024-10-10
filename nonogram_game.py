import random
import sys
import utils
import menu
from constants import *
from grid import Grid

class NonogramGame:
    def __init__(self):
        pygame.init()

        # Variables iniciales
        self.ROWS = DEFAULT_ROWS
        self.COLS = DEFAULT_COLS
        self.SQUARE_SIZE = SQUARE_SIZE
        self.TOP_MARGIN = TOP_MARGIN_BASE + 7 * self.ROWS
        self.LEFT_MARGIN = LEFT_MARGIN_BASE + 7 * self.COLS

        # Establecer tamaño inicial de la ventana para el menú
        self.WIDTH = 800
        self.HEIGHT = 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Nonograma")

        # Fuentes
        self.font = FONT
        self.win_font = WIN_FONT
        self.menu_font = MENU_FONT

    @staticmethod
    def generate_solution(rows, cols):
        return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    def adjust_screen_size(self, rows, cols):
        self.TOP_MARGIN = TOP_MARGIN_BASE + 7 * rows
        self.LEFT_MARGIN = LEFT_MARGIN_BASE + 7 * cols
        self.WIDTH = 50 + self.LEFT_MARGIN + cols * self.SQUARE_SIZE
        self.HEIGHT = 50 + self.TOP_MARGIN + rows * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def main_loop(self):
        # Mostrar menú inicial
        option = menu.show_menu(self.screen, self.WIDTH, self.HEIGHT)

        if option == "random":
            # Generar tablero aleatorio de tamaño aleatorio
            rows = random.randint(5, 10)
            cols = random.randint(5, 10)
        elif option == "choose_size":
            # Permitir al usuario ingresar el tamaño del tablero
            rows, cols = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)
        else:
            # Opción inválida, salir del juego
            pygame.quit()
            sys.exit()

        # Ajustar tamaño de la pantalla según el tamaño del tablero
        self.adjust_screen_size(rows, cols)

        # Generar solución y pistas
        solution = self.generate_solution(rows, cols)
        row_clues, col_clues = utils.generate_clues(solution, rows, cols)

        # Crear la cuadrícula del juego
        grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)
            if not grid.win and grid.check_win(solution):
                grid.win = True
            grid.draw(row_clues, col_clues)
            if grid.win:
                grid.display_win_message(self.WIDTH, self.HEIGHT)
            pygame.display.flip()