import random
import sys
import utils
import menu
from grid import *

class NonogramGame:
    def __init__(self):
        pygame.init()

        #Variables iniciales
        self.ROWS = DEFAULT_ROWS
        self.COLS = DEFAULT_COLS
        self.SQUARE_SIZE = SQUARE_SIZE
        self.TOP_MARGIN = TOP_MARGIN_BASE + 7 * self.ROWS
        self.LEFT_MARGIN = LEFT_MARGIN_BASE + 7 * self.COLS
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

    def run_tutorial(self):
        instructions = [
            "",
            "",
            "1. Las Reglas Básicas del Nonograma:",
            "Debes llenar celdas en una cuadrícula basándote en los números que aparecen en los bordes.",
            "Los números indican cuántas celdas consecutivas debes llenar en cada fila o columna.",
            "",
            "2. Cómo Interpretar Múltiples Números en una Fila o Columna:",
            "Si hay N cantidad de números, significa que hay N grupos de celdas correctas",
            "y al menos una celda vacía entre cada grupo.",
            "",
            "3. Cómo Empezar:",
            "Comienza con filas o columnas donde los números",
            "llenan completamente la cuadrícula o casi lo hacen.",
            "",
            "4. Marcar las Celdas Vacías:",
            "Usa el Clic derecho para marcar celdas que no son correctas.",
            "",
            "5. Completa el Nonograma:",
            "Sigue deduciendo hasta completar la imagen oculta.",
            "¡Buena suerte!"
        ]

        # Limpiar pantalla y mostrar fondo blanco
        self.screen.fill(WHITE)

        # Mostrar cada línea de instrucciones centrada en pantalla
        for i, line in enumerate(instructions):
            instruction_surface = FONT.render(line, True, BLACK)
            self.screen.blit(
                instruction_surface,
                (self.WIDTH // 2 - instruction_surface.get_width() // 2, 20 + i * 25)
            )

        pygame.display.flip()

        # Esperar a que el jugador presione una tecla para salir de las instrucciones
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False  # Salir de las instrucciones al presionar cualquier tecla

    def main_loop(self):
        while True:  #Bucle externo para reiniciar el juego
            #Restablecer el tamaño de la pantalla al tamaño del menú
            self.WIDTH = 800
            self.HEIGHT = 600
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            #Mostrar menú inicial
            option = menu.show_menu(self.screen, self.WIDTH // 2, self.HEIGHT // 2)

            if option == "random":
                #Generar tablero aleatorio de tamaño aleatorio
                rows = random.randint(5, 10)
                cols = random.randint(5, 10)
            elif option == "choose_size":
                #Permitir al usuario ingresar el tamaño del tablero
                rows, cols = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)
            elif option == "tutorial":
                self.run_tutorial()  # Llamada a la función de tutorial
                continue  # Reinicia el menú al finalizar el tutorial
            else:
                #Salir del juego
                pygame.quit()
                sys.exit()

            #Ajustar tamaño de la pantalla según el tamaño del tablero
            self.adjust_screen_size(rows, cols)

            #Generar solución y pistas
            solution = self.generate_solution(rows, cols)
            row_clues, col_clues = utils.generate_clues(solution, rows, cols)

            #Crear la cuadrícula del juego
            grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
                        grid.handle_click(pygame.mouse.get_pos(), event.button)
                grid.draw(row_clues, col_clues)
                if not grid.win and utils.check_win(grid.get_grid(), solution, rows, cols):
                    grid.display_win_message(self.WIDTH, self.HEIGHT)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False
                pygame.display.flip()
