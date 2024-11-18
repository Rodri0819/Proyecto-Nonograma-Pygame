import random
import sys
import utils
import menu
from grid import *
import datetime
import os
import pickle

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
        options = ["Resume", "Guardar partida", "Restart", "Exit"]
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

    def create_nonogram(self):
        # Ajustar tamaño de la pantalla para el editor
        self.adjust_screen_size(self.ROWS, self.COLS)
        grid = Grid(self.ROWS, self.COLS, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

        editing = True
        while editing:
            self.screen.fill(WHITE)
            grid.draw([], [])  # Dibuja el tablero sin pistas (las pistas se generarán después)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)  # Permite "dibujar" en el tablero
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Finalizar diseño
                        # Generar pistas y guardar el diseño
                        solution = grid.get_grid()
                        row_clues, col_clues = utils.generate_clues(solution, self.ROWS, self.COLS)
                        self.save_custom_nonogram(solution, row_clues, col_clues)
                        editing = False  # Salir del editor
                    elif event.key == pygame.K_ESCAPE:  # Cancelar diseño
                        editing = False

            pygame.display.flip()

    def save_custom_nonogram(self, solution, row_clues, col_clues):
        directory = "nonogramas_creados"
        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"nonograma_{timestamp}.pkl")

        data = {
            'solution': solution,
            'row_clues': row_clues,
            'col_clues': col_clues
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        print(f"Nonograma guardado en: {filename}")

    def save_game(self, grid, rows, cols, elapsed_time, save_filename=None):

        """Guarda el estado de la partida en un archivo usando pickle."""
        # Crear la carpeta si no existe
        directory = "partidas_guardadas"
        if not os.path.exists(directory):
            os.makedirs(directory)

        if save_filename is None:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")  # Formato: YYYYMMDD_HHMMSS
            save_filename = f"{timestamp}.pkl"  # Nombre del archivo con la fecha y hora

        filepath = os.path.join(directory, save_filename)  # Ruta completa del archivo

        data = {
            'grid': grid,  # El estado de la cuadrícula
            'rows': rows,  # Número de filas
            'cols': cols,  # Número de columnas
            'elapsed_time': elapsed_time
        }
        with open(filepath, 'wb') as f:  # Modo binario
            pickle.dump(data, f)

    def load_game(self, load_filename):
        #Carga el estado de la partida desde un archivo usando pickle
        with open(load_filename, 'rb') as f:  # Modo binario
            data = pickle.load(f)
        return data['grid'], data['rows'], data['cols'], data['elapsed_time']  # Devuelve la cuadrícula, sus dimensiones y tiempo transcurrido

    def play_custom_nonogram(self):
        # Directorio donde se guardan los nonogramas creados
        directory = "nonogramas_creados"
        files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

        if not files:
            print("No hay nonogramas creados.")
            return

        # Mostrar lista para seleccionar el nonograma
        selected_file = self.select_custom_nonogram(files)
        if not selected_file:
            print("Selección cancelada.")
            return  # Salir si no se selecciona nada

        filepath = os.path.join(directory, selected_file)

        # Cargar el archivo seleccionado
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        solution = data['solution']
        row_clues = data['row_clues']
        col_clues = data['col_clues']

        # Ajustar el tamaño de la pantalla y jugar
        self.ROWS = len(solution)
        self.COLS = len(solution[0])
        self.adjust_screen_size(self.ROWS, self.COLS)

        grid = Grid(self.ROWS, self.COLS, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
        grid.reset()  # Inicia con una cuadrícula vacía

        # Ciclo principal para jugar el nonograma seleccionado
        running = True
        while running:
            self.screen.fill(WHITE)
            grid.draw(row_clues, col_clues)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)

            # Verificar si el jugador ha completado el nonograma
            if utils.check_win(grid.get_grid(), solution, self.ROWS, self.COLS):
                grid.display_win_message(self.WIDTH, self.HEIGHT)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

            pygame.display.flip()

    def main_loop(self):
        while True:  # Bucle externo para reiniciar el juego
            # Restablecer el tamaño de la pantalla al tamaño del menú
            self.WIDTH = 800
            self.HEIGHT = 600
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            # Mostrar menú inicial
            option = menu.show_menu(self.screen, self.WIDTH // 2, self.HEIGHT // 2)

            if option == "cargar_partida":
                # Mostrar partidas guardadas
                selected_game = menu.show_saved_games(self.screen)
                if selected_game == "menu_principal":
                    continue  # Regresar al menú principal
                if selected_game:  # Si se seleccionó un archivo
                    game_filename = os.path.join("partidas_guardadas", selected_game)
                    grid_data, rows, cols, elapsed_time = self.load_game(game_filename)
                    start_time = pygame.time.get_ticks() - elapsed_time * 1000
                    grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen, grid_data)
            elif option == "random":
                rows = random.randint(5, 10)
                cols = random.randint(5, 10)
            elif option == "choose_size":
                rows, cols = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)
            elif option == "tutorial":
                self.run_tutorial()
                continue  # Vuelve al menú después del tutorial
            elif option == "create_nonogram":
                self.create_nonogram()  # Llama al editor para crear un nonograma
                continue  # Regresa al menú principal después de guardar el nonograma
            elif option == "play_custom":
                self.play_custom_nonogram()  # Juega un nonograma personalizado
                continue  # Regresa al menú principal después de jugar
            else:
                pygame.quit()
                sys.exit()

            # Ajustar tamaño de la pantalla según el tamaño del tablero
            self.adjust_screen_size(rows, cols)

            # Generar solución y pistas
            solution = self.generate_solution(rows, cols)
            row_clues, col_clues = utils.generate_clues(solution, rows, cols)

            # Si se carga un juego, no reiniciar el tiempo
            if option != "cargar_partida":
                start_time = pygame.time.get_ticks()
                grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

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
                                continue
                            elif selected_option == 1:  # Save game
                                self.save_game(grid.get_grid(), rows, cols, elapsed_time)
                            elif selected_option == 2:  # Restart
                                start_time = pygame.time.get_ticks()
                                grid.reset()
                            elif selected_option == 3:  # Exit
                                running = False
                                break
                        elif event.key == pygame.K_h:  # Presiona 'H' para ayuda
                            utils.mostrar_ayuda(grid.get_grid(), solution)

                    if not grid.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            grid.handle_click(pygame.mouse.get_pos(), event.button)

                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Tiempo en segundos

                # Formatear tiempo como HH:MM:SS
                hours = elapsed_time // 3600
                minutes = (elapsed_time % 3600) // 60
                seconds = elapsed_time % 60
                time_display = f"{hours:02}:{minutes:02}:{seconds:02}"

                # Dibujar el tablero y el tiempo
                grid.draw(row_clues, col_clues)
                timer_surface = FONT.render(f"Tiempo: {time_display}", True, BLACK)
                self.screen.blit(timer_surface, (
                self.WIDTH - timer_surface.get_width() - 10, self.HEIGHT - timer_surface.get_height() - 10))

                # Verificar si el jugador gana
                if not grid.win and utils.check_win(grid.get_grid(), solution, rows, cols):
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y%m%d_%H%M%S")
                    screenshot_filename = f"nonograma_ganado_{timestamp}.png"
                    directory = "partidas-ganadas"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    filepath = os.path.join(directory, screenshot_filename)
                    screenshot_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                    screenshot_surface.blit(self.screen, (0, 0))
                    pygame.image.save(screenshot_surface, filepath)
                    grid.display_win_message(self.WIDTH, self.HEIGHT)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    running = False

                pygame.display.flip()

    def select_custom_nonogram(self, files):
        # Método para seleccionar un archivo de nonogramas personalizados
        selected_index = 0

        while True:
            self.screen.fill(WHITE)

            # Título
            title_surface = FONT.render("Selecciona un Nonograma:", True, BLACK)
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 20))

            # Mostrar archivos disponibles
            for i, file in enumerate(files):
                color = BLACK if i == selected_index else GRAY
                file_surface = FONT.render(f"{i + 1}. {file}", True, color)
                self.screen.blit(file_surface, (self.WIDTH // 2 - file_surface.get_width() // 2, 80 + i * 30))

            # Instrucciones
            instructions_surface = FONT.render("Usa UP/DOWN para mover, ENTER para seleccionar", True, BLACK)
            self.screen.blit(instructions_surface,
                             (self.WIDTH // 2 - instructions_surface.get_width() // 2, self.HEIGHT - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(files)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(files)
                    elif event.key == pygame.K_RETURN:
                        return files[selected_index]
                    elif event.key == pygame.K_ESCAPE:
                        return None

    def play_custom_nonogram(self):
        # Método para jugar un nonograma personalizado
        directory = "nonogramas_creados"
        files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

        if not files:
            print("No hay nonogramas creados.")
            return

        # Selección del nonograma personalizado
        selected_file = self.select_custom_nonogram(files)
        if not selected_file:
            print("Selección cancelada.")
            return

        filepath = os.path.join(directory, selected_file)

        # Cargar el archivo seleccionado
        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        solution = data['solution']
        row_clues = data['row_clues']
        col_clues = data['col_clues']

        # Ajustar la pantalla al tamaño del nonograma
        self.ROWS = len(solution)
        self.COLS = len(solution[0])
        self.adjust_screen_size(self.ROWS, self.COLS)

        grid = Grid(self.ROWS, self.COLS, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
        grid.reset()  # Iniciar cuadrícula vacía

        # Ciclo principal del juego
        running = True
        while running:
            self.screen.fill(WHITE)
            grid.draw(row_clues, col_clues)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)

            # Verificar si el jugador completó el nonograma
            if utils.check_win(grid.get_grid(), solution, self.ROWS, self.COLS):
                grid.display_win_message(self.WIDTH, self.HEIGHT)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

            pygame.display.flip()
    def ask_board_size(self):
        """Permite al usuario ingresar el tamaño del tablero en formato NxM."""
        running = True
        input_text = ""

        while running:
            self.screen.fill(WHITE)

            # Mensajes en pantalla
            title_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 100))

            # Mostrar el texto ingresado por el usuario
            input_surface = FONT.render(input_text, True, BLACK)
            self.screen.blit(input_surface, (self.WIDTH // 2 - input_surface.get_width() // 2, 200))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Confirmar entrada con Enter
                        if "x" in input_text and input_text.replace("x", "").isdigit():
                            rows, cols = map(int, input_text.split("x"))
                            if 5 <= rows <= 20 and 5 <= cols <= 20:  # Validar límites
                                return rows, cols
                            else:
                                print("Tamaño inválido. Elija dimensiones entre 5 y 20.")
                                input_text = ""  # Limpiar entrada
                        else:
                            print("Formato inválido. Use NxM (ejemplo: 10x10).")
                            input_text = ""  # Limpiar entrada
                    elif event.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit() or event.unicode == "x":  # Aceptar números y "x"
                        input_text += event.unicode

        return 5, 5  # Valor por defecto si se cancela


    def create_nonogram(self):
        """Crea un nonograma personalizado permitiendo elegir el tamaño del tablero."""
        # Pedir al usuario el tamaño del tablero
        self.ROWS, self.COLS = self.ask_board_size()
        self.adjust_screen_size(self.ROWS, self.COLS)

        grid = Grid(self.ROWS, self.COLS, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
        editing = True

        while editing:
            self.screen.fill(WHITE)
            grid.draw([], [])  # Dibuja el tablero sin pistas (se generarán después)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)  # Permitir dibujo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Finalizar diseño
                        solution = grid.get_grid()
                        row_clues, col_clues = utils.generate_clues(solution, self.ROWS, self.COLS)
                        self.save_custom_nonogram(solution, row_clues, col_clues)
                        editing = False  # Salir del editor
                    elif event.key == pygame.K_ESCAPE:  # Cancelar diseño
                        editing = False

            pygame.display.flip()
