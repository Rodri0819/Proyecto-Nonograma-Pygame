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

        self.top_scores = []

    @staticmethod
    def generate_solution(rows, cols):
        return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

    def adjust_screen_size(self, rows, cols):
        self.TOP_MARGIN = TOP_MARGIN_BASE + 7 * rows
        self.LEFT_MARGIN = LEFT_MARGIN_BASE + 7 * cols
        self.WIDTH = 50 + self.LEFT_MARGIN + cols * self.SQUARE_SIZE
        self.HEIGHT = 50 + self.TOP_MARGIN + rows * self.SQUARE_SIZE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def show_pause_menu(self, screen, width, height):
        options = ["Reanudar", "Guardar partida", "Reiniciar", "Salir"]
        button_width = 150
        button_height = 30
        spacing = 10  # Espacio entre botones

        while True:
            screen.fill(WHITE)  # Rellena la pantalla con blanco

            # Obtener la posición actual del mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Dibujar botones
            button_rects = []
            for i, option in enumerate(options):
                # Posición del botón
                button_x = width // 2 - button_width // 2
                button_y = height // 2 - (len(options) * (button_height + spacing)) // 2 + i * (button_height + spacing)

                # Detectar si el cursor está sobre el botón
                is_hovered = button_x <= mouse_x <= button_x + button_width and \
                             button_y <= mouse_y <= button_y + button_height

                # Establecer colores
                if option == "Salir":
                    button_color = DARK_RED if is_hovered else CHERRY
                else:
                    button_color = GRAY if is_hovered else DARK_GRAY

                # Dibujar botón
                pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
                pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)  # Borde negro

                # Renderizar texto
                text_surface = FONT.render(option, True, WHITE if is_hovered else BLACK)
                text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                screen.blit(text_surface, text_rect)

                # Guardar rectángulo del botón
                button_rects.append((button_x, button_y, button_width, button_height, i))  # i es el índice de la opción

            pygame.display.flip()  # Actualizar pantalla

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cerrar juego
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                    if event.button == 1:  # Solo manejar clic izquierdo
                        for button_x, button_y, button_width, button_height, index in button_rects:
                            if button_x <= event.pos[0] <= button_x + button_width and \
                                    button_y <= event.pos[1] <= button_y + button_height:
                                return index  # Retornar el índice de la opción seleccionada

    def save_custom_nonogram(self, grid, rows, cols):
        directory = "nonogramas_creados"
        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(directory, f"{timestamp}.pkl")

        data = {
            'grid': grid,
            'rows': rows,
            'cols': cols,
            'elapsed_time': 0
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        print(f"Nonograma guardado en: {filename}")

    def save_game(self, grid, rows, cols, elapsed_time, solution, cantidadPistas):
        """Guarda el estado de la partida en un archivo usando pickle."""
        directory = "partidas_guardadas"
        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        save_filename = f"{timestamp}.pkl"

        filepath = os.path.join(directory, save_filename)

        data = {
            'grid': grid,  # Estado actual del tablero
            'rows': rows,
            'cols': cols,
            'elapsed_time': elapsed_time,
            'solution': solution,  # Solución para verificar partidas cargadas
            'cantidadPistas' : cantidadPistas,
        }

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"Partida guardada en: {filepath}")

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"Partida guardada en: {filepath}")

    def load_game(self, load_filename):
        """Carga el estado de la partida desde un archivo usando pickle."""
        with open(load_filename, 'rb') as f:
            data = pickle.load(f)

        grid = data['grid']
        rows = data['rows']
        cols = data['cols']
        elapsed_time = data.get('elapsed_time', 0)  # Asegura que tenga un valor por defecto
        solution = data.get('solution', None)
        cantidadPistas = data.get('cantidadPistas', 0)

        return grid, rows, cols, elapsed_time, solution, cantidadPistas

    def load_custom_game(self, load_filename):
        """Carga el estado de una partida personalizada desde un archivo usando pickle."""
        with open(load_filename, 'rb') as f:
            data = pickle.load(f)

        solution = data['grid']  # En partidas personalizadas, el 'grid' es la solución
        rows = data['rows']
        cols = data['cols']
        elapsed_time = data.get('elapsed_time', 0)  # Asegúrate de manejar 'elapsed_time'

        return solution, rows, cols, elapsed_time

    def main_loop(self):
        while True:  # Bucle externo para reiniciar el juego
            # Restablecer el tamaño de la pantalla al tamaño del menú
            self.WIDTH = 800
            self.HEIGHT = 600
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            # Inicializar variables predeterminadas
            rows, cols = self.ROWS, self.COLS
            row_clues, col_clues = [], []
            grid = None
            solution = None  # Inicializamos solution como None
            cantidadPistas = 0

            # Mostrar menú inicial
            option = menu.show_menu(self.screen, self.WIDTH // 2, self.HEIGHT // 2)

            if option == "cargar_partida":
                selected_game = menu.show_saved_games(self.screen)

                if selected_game == "menu_principal":
                    continue  # Regresar al menú principal
                if selected_game:
                    game_filename = os.path.join("partidas_guardadas", selected_game)
                    try:
                        # Cargar datos de la partida
                        grid_data, rows, cols, elapsed_time, solution, cantidadPistas = self.load_game(game_filename)
                        start_time = pygame.time.get_ticks() - elapsed_time * 1000

                        # Generar pistas basadas en la solución cargada
                        row_clues, col_clues = utils.generate_clues(solution, rows, cols)

                        # Crear el grid con los datos cargados
                        grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen,
                                    grid_data)
                    except Exception as e:
                        print(f"Error al cargar la partida: {e}")
                        continue  # Regresar al menú principal


            elif option == "random":
                rows = random.randint(5, 10)
                cols = random.randint(5, 10)
                solution = self.generate_solution(rows, cols)
                row_clues, col_clues = utils.generate_clues(solution, rows, cols)
                grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)

            elif option == "choose_size":
                result = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)  # Llama a la función para obtener el tamaño
                if result is None:  # Si el usuario presionó Volver y no eligió tamaño
                    continue  # Regresar al menú principal

                rows, cols = result  # Desempaquetar las dimensiones
                solution = self.generate_solution(rows, cols)  # Generar una solución para el tablero
                row_clues, col_clues = utils.generate_clues(solution, rows,
                                                            cols)  # Generar pistas para las filas y columnas
                grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN,
                            self.screen)  # Crear el grid

            elif option == "tutorial":
                self.run_tutorial()
                continue  # Vuelve al menú después del tutorial


            elif option == "create_nonogram":
                self.create_nonogram()
                continue  # Regresar al menú principal después de guardar el nonograma


            elif option == "play_custom":
                selected_game = menu.show_created_games(self.screen)
                if selected_game == "menu_principal" or selected_game is None:
                    continue  # Regresar al menú principal si el usuario presiona ESC o selecciona "menu_principal"

                if selected_game:
                    created_game_filename = os.path.join("nonogramas_creados", selected_game)
                    solution, rows, cols, elapsed_time = self.load_custom_game(created_game_filename)
                    start_time = pygame.time.get_ticks() - elapsed_time * 1000
                    grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
                    row_clues, col_clues = utils.generate_clues(solution, rows, cols)
                else:
                    print("Error: No se pudo cargar el juego personalizado.")

            else:
                pygame.quit()
                sys.exit()

            # Validar que grid y solution se hayan inicializado
            if grid is None:
                grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
            if solution is None:
                solution = self.generate_solution(rows, cols)  # Generar solución por defecto
                row_clues, col_clues = utils.generate_clues(solution, rows, cols)

            # Ajustar tamaño de la pantalla según el tamaño del tablero
            self.adjust_screen_size(rows, cols)

            start_time = pygame.time.get_ticks()
            paused_time = 0  # Tiempo acumulado en pausa
            running = True

            while running:
                # Dibujar botones para "Menu" y "Ayuda"
                button_size = 30

                # Botón de menú
                menu_button_x = self.WIDTH - 40
                menu_button_y = 50
                menu_button_rect = pygame.Rect(menu_button_x, menu_button_y, button_size, button_size)

                # Botón de ayuda
                help_button_x =  self.WIDTH - 40
                help_button_y =  90
                help_button_rect = pygame.Rect(help_button_x, help_button_y, button_size, button_size)

                # Dibujar botones
                pygame.draw.rect(self.screen, DARK_GRAY, menu_button_rect)  # Botón gris para menú
                pygame.draw.rect(self.screen, BLACK, menu_button_rect, 2)  # Borde negro
                pygame.draw.rect(self.screen, DARK_GRAY, help_button_rect)  # Botón gris para ayuda
                pygame.draw.rect(self.screen, BLACK, help_button_rect, 2)  # Borde negro

                # Agregar texto a los botones
                menu_text = FONT.render("M", True, BLACK)  # "M" para menú
                help_text = FONT.render("?", True, BLACK)  # "?" para ayuda
                self.screen.blit(menu_text, (menu_button_x + (button_size - menu_text.get_width()) // 2, menu_button_y + (button_size - menu_text.get_height()) // 2))
                self.screen.blit(help_text, (help_button_x + (button_size - help_text.get_width()) // 2, help_button_y + (button_size - help_text.get_height()) // 2))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Detectar clic en el botón de menú
                        if menu_button_rect.collidepoint(event.pos):
                            pause_start_time = pygame.time.get_ticks()  # Tiempo al pausar
                            selected_option = self.show_pause_menu(self.screen, self.WIDTH, self.HEIGHT)

                            if selected_option == 0:  # Reanudar
                                paused_time += pygame.time.get_ticks() - pause_start_time  # Acumula tiempo pausado
                                continue
                            elif selected_option == 1:  # Guardar partida
                                self.save_game(grid.get_grid(), rows, cols, elapsed_time, solution, cantidadPistas)
                            elif selected_option == 2:  # Reiniciar
                                start_time = pygame.time.get_ticks()  # Reinicia el tiempo
                                paused_time = 0  # Reinicia el tiempo pausado
                                grid.reset()
                            elif selected_option == 3:  # Salir
                                running = False
                                break

                        # Detectar clic en el botón de ayuda
                        if help_button_rect.collidepoint(event.pos):
                            utils.mostrar_ayuda(grid.get_grid(), solution)
                            cantidadPistas += 1

                    if not grid.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            grid.handle_click(pygame.mouse.get_pos(), event.button)

                # Actualizar pantalla
                pygame.display.flip()

                elapsed_time = (pygame.time.get_ticks() - start_time - paused_time) // 1000

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
                    #Calcula el puntaje de la partida
                    puntajeBase = rows+cols
                    cantidadCeldasMarcadas = utils.contar_celdas_marcadas(solution) 
                    puntajeTiempo = puntajeBase - (elapsed_time // 6000)
                    puntajePistas = 0
                    if cantidadPistas > 0:
                        if puntajeTiempo < 0:
                            puntajePistas = (-puntajeTiempo + cantidadPistas)*(cantidadPistas/cantidadCeldasMarcadas)
                        elif puntajeTiempo > 0 :
                            puntajePistas = (puntajeTiempo + cantidadPistas)*(cantidadPistas/cantidadCeldasMarcadas)

                    if cantidadPistas < cantidadCeldasMarcadas :
                        puntajeTotal = puntajeBase + puntajeTiempo - puntajePistas
                    else :
                        puntajeTotal = 0     

                    # Llamamos a la función del menú para agregar el puntaje
                    menu.agregar_puntaje(puntajeTotal) 
                    
                    # Mostrar el puntaje en pantalla, en el mismo estilo que el tiempo
                    puntaje_texto = f"Puntaje: {int(puntajeTotal)}"  # Convertir el puntaje a entero
                    puntaje_surface = FONT.render(puntaje_texto, True, BLACK)  # Usamos la misma fuente

                    puntaje_x = 20  # Borde izquierdo
                    puntaje_y = self.HEIGHT - puntaje_surface.get_height() - 10  # Colocar el puntaje justo encima del borde inferior


                    self.screen.blit(puntaje_surface, (puntaje_x, puntaje_y))  # Dibujar el puntaje en pantalla

                    #Guarda una screenshot de la partida al ganar
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y%m%d_%H%M%S")
                    screenshot_filename = f"nonograma_ganado_{timestamp}.png"
                    directory = "partidas_ganadas"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    filepath = os.path.join(directory, screenshot_filename)
                    screenshot_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                    screenshot_surface.blit(self.screen, (0, 0))
                    pygame.image.save(screenshot_surface, filepath)
                    grid.display_win_message(self.WIDTH, self.HEIGHT)
                    pygame.display.flip()
                    pygame.time.delay(5000)
                    running = False

    def ask_nonogram_name(self):
        """Permite al usuario ingresar un nombre para el nonograma."""
        running = True
        input_text = ""
        error_message = ""  # Mensaje de error para mostrar en pantalla

        while running:
            self.screen.fill(WHITE)

            # Mensajes en pantalla
            title_surface = FONT.render("Nombre para el nonograma:", True, BLACK)
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 100))

            # Mostrar el texto ingresado por el usuario
            input_surface = FONT.render(input_text, True, BLACK)
            self.screen.blit(input_surface, (self.WIDTH // 2 - input_surface.get_width() // 2, 150))

            # Mostrar mensaje de error si existe
            if error_message:
                error_surface = FONT.render(error_message, True, RED)  # Color rojo para errores
                self.screen.blit(error_surface, (self.WIDTH // 2 - error_surface.get_width() // 2, 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Confirmar entrada con Enter
                        if input_text.strip():  # Validar que no esté vacío
                            return input_text.strip()  # Retornar el texto limpio
                        else:
                            error_message = "El nombre no puede estar vacío."
                    elif event.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        input_text = input_text[:-1]
                        error_message = ""  # Limpiar mensaje de error
                    elif event.unicode.isalnum() or event.unicode in "_-":  # Aceptar caracteres válidos
                        input_text += event.unicode
                        error_message = ""  # Limpiar mensaje de error

        return "nonograma_sin_nombre"  # Nombre por defecto si se cancela

    def create_nonogram(self):
        """Crea un nonograma personalizado permitiendo elegir el tamaño del tablero."""
        # Pedir al usuario el tamaño del tablero
        result = menu.get_board_size(self.screen, self.WIDTH, self.HEIGHT)
        if result is None:
            return

        rows, cols = result  # Desempaquetar las dimensiones
        self.adjust_screen_size(rows, cols)

        # Inicializar un tablero vacío
        grid = Grid(rows, cols, self.SQUARE_SIZE, self.TOP_MARGIN, self.LEFT_MARGIN, self.screen)
        editing = True

        while editing:
            self.screen.fill(WHITE)
            grid.draw([], [])  # Dibuja el tablero vacío

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grid.handle_click(pygame.mouse.get_pos(), event.button)  # Permitir clic para dibujar
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Finalizar creación
                        solution = grid.get_grid()
                        row_clues, col_clues = utils.generate_clues(solution, rows, cols)
                        nonogram_name = self.ask_nonogram_name()  # Pedir nombre para el nonograma
                        self.save_custom_nonogram(solution, rows, cols, nonogram_name)
                        editing = False
                    elif event.key == pygame.K_ESCAPE:  # Cancelar creación y regresar al menú principal
                        editing = False

            pygame.display.flip()

    def save_custom_nonogram(self, solution, rows, cols, name):
        """Guarda un nonograma personalizado con un nombre específico."""
        directory = "nonogramas_creados"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, f"{name}.pkl")

        data = {
            'grid': solution,
            'rows': rows,
            'cols': cols,
            'elapsed_time': 0
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

        print(f"Nonograma guardado en: {filename}")

    def run_tutorial(self):
        # Limpiar pantalla y mostrar fondo blanco
        self.screen.fill(WHITE)

        instructions = [
            "1. Las Reglas Básicas del Nonograma",
            "  - Debes marcar las celdas basándote en los números que aparecen en los bordes.",
            "  - Los números indican cuántas celdas consecutivas debes llenar en cada fila o columna.",
            "  - Si hay N cantidad de números, significa que hay N grupos de celdas correctas",
            "    y al menos una celda vacía entre cada grupo.",
            "2. Controles del Juego:",
            "  - Click izquierdo: Marcar celda correcta",
            "  - Click derecho: Marcar celda incorrecta",
            "  - Tecla H: Ayuda aleatoria"
        ]
        paso1 = [
            "Comienza por las",
            "filas o columnas completas."
        ]
        paso2 = [
            "Recuerda las reglas, ",
            "úsalas para completar las ",
            "filas o columnas casi llenas"
        ]
        paso3 = [
            "Sigue deduciendo hasta",
            "completar la imagen."
        ]

        rows, cols = 5, 5
        row_clues = [[2, 1], [1, 1, 1], [2], [3], [3, 1]]
        col_clues = [[1, 1], [1, 1], [2, 2], [2], [5]]

        grid2 = [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]]
        grid3 = [[0, 0, 1, 0, 1], [1, 0, 1, 0, 1], [0, 0, 0, 0, 1], [0, 0, 1, 0, 1], [1, 1, 1, 0, 1]]
        grid4 = [[0, 1, 1, 0, 1], [1, 0, 1, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [1, 1, 1, 0, 1]]

        waiting = True
        while waiting:
            self.screen.fill(WHITE)

            # Dibujar instrucciones
            for i, line in enumerate(instructions):
                instruction_surface = FONT.render(line, True, BLACK)
                self.screen.blit(instruction_surface, (20, 20 + i * 25))

            for i, line in enumerate(paso1):
                paso1_surface = FONT.render(line, True, BLACK)
                self.screen.blit(paso1_surface, (30, 300 + i * 25))

            for i, line in enumerate(paso2):
                paso2_surface = FONT.render(line, True, BLACK)
                self.screen.blit(paso2_surface, (295, 275 + i * 25))

            for i, line in enumerate(paso3):
                paso3_surface = FONT.render(line, True, BLACK)
                self.screen.blit(paso3_surface, (575, 550 + i * 25))

            # Dibujar pistas y cuadrículas
            left_margin_1 = 50
            left_margin_2 = 325
            left_margin_3 = 600
            top_margin_1 = 170
            top_margin_2 = 400

            for i, clues in enumerate(row_clues):
                text = ' '.join(map(str, clues))
                clue_surface = FONT.render(text, True, BLACK)
                self.screen.blit(clue_surface, (left_margin_3 - 40, top_margin_1 + i * SQUARE_SIZE))
                self.screen.blit(clue_surface, (left_margin_1 - 40, top_margin_2 + i * SQUARE_SIZE))
                self.screen.blit(clue_surface, (left_margin_2 - 40, top_margin_2 + i * SQUARE_SIZE))
                self.screen.blit(clue_surface, (left_margin_3 - 40, top_margin_2 + i * SQUARE_SIZE))

            for i, clues in enumerate(col_clues):
                for j, clue in enumerate(clues):
                    clue_surface = FONT.render(str(clue), True, BLACK)
                    self.screen.blit(clue_surface, (
                    left_margin_3 + i * SQUARE_SIZE + SQUARE_SIZE / 2 - 5, top_margin_1 - 45 + j * 15))
                    self.screen.blit(clue_surface, (
                    left_margin_1 + i * SQUARE_SIZE + SQUARE_SIZE / 2 - 5, top_margin_2 - 45 + j * 15))
                    self.screen.blit(clue_surface, (
                    left_margin_2 + i * SQUARE_SIZE + SQUARE_SIZE / 2 - 5, top_margin_2 - 45 + j * 15))
                    self.screen.blit(clue_surface, (
                    left_margin_3 + i * SQUARE_SIZE + SQUARE_SIZE / 2 - 5, top_margin_2 - 45 + j * 15))

            for row in range(rows):
                for col in range(cols):
                    rect1 = pygame.Rect(left_margin_3 + col * SQUARE_SIZE, top_margin_1 + row * SQUARE_SIZE,
                                        SQUARE_SIZE, SQUARE_SIZE)
                    rect2 = pygame.Rect(left_margin_1 + col * SQUARE_SIZE, top_margin_2 + row * SQUARE_SIZE,
                                        SQUARE_SIZE, SQUARE_SIZE)
                    rect3 = pygame.Rect(left_margin_2 + col * SQUARE_SIZE, top_margin_2 + row * SQUARE_SIZE,
                                        SQUARE_SIZE, SQUARE_SIZE)
                    rect4 = pygame.Rect(left_margin_3 + col * SQUARE_SIZE, top_margin_2 + row * SQUARE_SIZE,
                                        SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(self.screen, BLACK, rect1, 1)
                    if grid2[row][col] == 1:
                        pygame.draw.rect(self.screen, GRAY, rect2)
                    pygame.draw.rect(self.screen, BLACK, rect2, 1)
                    if grid3[row][col] == 1:
                        pygame.draw.rect(self.screen, GRAY, rect3)
                    pygame.draw.rect(self.screen, BLACK, rect3, 1)
                    if grid4[row][col] == 1:
                        pygame.draw.rect(self.screen, GRAY, rect4)
                    pygame.draw.rect(self.screen, BLACK, rect4, 1)

            # Dibujar el botón "Volver"
            button_size = 50
            button_x = self.WIDTH - button_size - 10
            button_y = 10
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = button_x <= mouse_x <= button_x + button_size and button_y <= mouse_y <= button_y + button_size
            button_color = DARK_RED if is_hovered else CHERRY
            pygame.draw.rect(self.screen, BLACK, (button_x - 3, button_y - 3, button_size + 6, button_size + 6))
            pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_size, button_size))
            button_text = FONT.render("Volver", True, WHITE)
            self.screen.blit(button_text, (button_x + (button_size - button_text.get_width()) // 2,
                                           button_y + (button_size - button_text.get_height()) // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if is_hovered:
                        waiting = False
