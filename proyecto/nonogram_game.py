import random
import sys
import utils
import menu
from grid import *
import datetime 
import os

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

    def show_pause_menu(self,screen, width, height):
        options = ["Resume", "Restart", "Exit"]
        selected_option = 0  # Opción inicialmente seleccionada

        while True:
            screen.fill(WHITE)  # Rellena la pantalla con blanco

            # Renderiza las opciones
            for i, option in enumerate(options):
                color = BLACK if i == selected_option else GRAY
                option_surface = FONT.render(option, True, color)
                screen.blit(option_surface, (width // 2 - option_surface.get_width() // 2, height // 2 - 50 + i * 30))

            pygame.display.flip()  # Actualiza la pantalla

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Mover hacia arriba
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:  # Mover hacia abajo
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_RETURN:  # Seleccionar opción
                        return selected_option


    def main_loop(self):
        while True:  # Bucle externo para reiniciar el juego
            # Restablecer el tamaño de la pantalla al tamaño del menú
            self.WIDTH = 800
            self.HEIGHT = 600
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            # Mostrar menú inicial
            option = menu.show_menu(self.screen, self.WIDTH // 2, self.HEIGHT // 2)

            if option == "random":
                rows = random.randint(5, 10)
                cols = random.randint(5, 10)
            elif option == "choose_size":
                rows, cols = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)
            elif option == "tutorial":
                self.run_tutorial()
                continue
            else:
                pygame.quit()
                sys.exit()

            # Ajustar tamaño de la pantalla según el tamaño del tablero
            self.adjust_screen_size(rows, cols)

            # Generar solución y pistas
            solution = self.generate_solution(rows, cols)
            row_clues, col_clues = utils.generate_clues(solution, rows, cols)

            # Crear la cuadrícula del juego
            grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

            # Iniciar el cronómetro
            start_time = pygame.time.get_ticks()  # Tiempo en milisegundos
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # Presiona Enter para pausar
                            selected_option = self.show_pause_menu(self.screen, self.WIDTH, self.HEIGHT)

                            if selected_option == 0:  # Resume
                                continue  # Vuelve al juego
                            elif selected_option == 1:  # Restart
                               grid.reset()  # Reinicia la cuadrícula
                            elif selected_option == 2:  # Exit
                               running = False  # Sal de este bucle para reiniciar el juego
                               break  # Sal del bucle mientras el juego
                    
                    if not grid.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            grid.handle_click(pygame.mouse.get_pos(), event.button)

                # Calcular el tiempo transcurrido
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convertir a segundos

                # Convertir a horas, minutos y segundos
                hours = elapsed_time // 3600
                minutes = (elapsed_time % 3600) // 60
                seconds = elapsed_time % 60

                # Formatear el texto del cronómetro
                time_display = f"{hours:02}:{minutes:02}:{seconds:02}"  # Formato HH:MM:SS

                # Dibujar el tablero y el tiempo
                grid.draw(row_clues, col_clues)
                # Renderizar el tiempo en la esquina inferior derecha
                timer_surface = FONT.render(f"Tiempo: {time_display}", True, BLACK)
                self.screen.blit(timer_surface, (self.WIDTH - timer_surface.get_width() - 10, self.HEIGHT - timer_surface.get_height() - 10))

                # Comprobar si el jugador ha ganado
                if not grid.win and utils.check_win(grid.get_grid(), solution, rows, cols):
                    
                    # Generar el nombre de archivo con la fecha y hora actual
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y%m%d_%H%M%S")  # Formato: YYYYMMDD_HHMMSS
                    filename = f"nonograma_ganado_{timestamp}.png"  # Nombre del archivo

                    # Crear la carpeta "partidas-ganadas" si no existe
                    directory = "partidas-ganadas"
                    if not os.path.exists(directory):
                        os.makedirs(directory)  # Crear la carpeta

                    # Guardar la imagen del Nonograma
                    filepath = os.path.join(directory, filename)  # Ruta completa del archivo
                    screenshot_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                    screenshot_surface.blit(self.screen, (0, 0))  # Copia la pantalla actual
                    pygame.image.save(screenshot_surface, filepath)  # Guarda la imagen

                    
                    
                    grid.display_win_message(self.WIDTH, self.HEIGHT)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False

                pygame.display.flip()


