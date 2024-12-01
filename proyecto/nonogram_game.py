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
                    sys.Salir()
                elif event.type == pygame.KEYDOWN:
                    waiting = False  # Salir de las instrucciones al presionar cualquier tecla

    def show_pause_menu(self, screen, width, height):
        options = ["Reanudar", "Guardar partida", "Reiniciar", "Salir"]
        TEXT_COLOR = BLACK
        HOVER_TEXT_COLOR = (150, 150, 150)  # Color de las letras al pasar el mouse por encima

        while True:
            screen.fill(WHITE)  # Rellena la pantalla con blanco

            # Obtener la posición actual del mouse
            mouse_pos = pygame.mouse.get_pos()

            # Lista para guardar los rectángulos de las opciones
            option_rects = []

            # Dibujar opciones
            for i, option in enumerate(options):
                # Definir posición del texto
                text_x = width // 2
                text_y = height // 2 - 80 + i * 60

                # Renderizar texto
                if pygame.Rect(text_x - 100, text_y - 20, 200, 40).collidepoint(mouse_pos):
                    text_surface = FONT.render(option, True, HOVER_TEXT_COLOR)  # Color de hover
                else:
                    text_surface = FONT.render(option, True, TEXT_COLOR)  # Color normal

                # Centrar texto
                text_rect = text_surface.get_rect(center=(text_x, text_y))
                screen.blit(text_surface, text_rect)

                # Guardar el rectángulo del texto para manejar clics
                option_rects.append(text_rect)

            pygame.display.flip()  # Actualizar pantalla

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Cerrar juego
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                    if event.button == 1:  # Solo manejar clic izquierdo
                        for i, rect in enumerate(option_rects):
                            if rect.collidepoint(event.pos):  # Verificar si el clic fue en el texto
                                return i  # Retornar el índice de la opción seleccionada


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
                result = menu.get_board_size(self.screen, self.WIDTH,
                                             self.HEIGHT)  # Llama a la función para obtener el tamaño
                if result is None:  # Si el usuario presionó ESC y no eligió tamaño
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

                    # Comenzar a jugar el tablero personalizado
                    playing = True
                    while playing:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    playing = False  # Salir del tablero personalizado y volver al menú principal
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                grid.handle_click(pygame.mouse.get_pos(), event.button)

                        # Dibujar el tablero y manejar el juego
                        self.screen.fill(WHITE)
                        grid.draw(row_clues, col_clues)
                        pygame.display.flip()
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
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
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
                        elif event.key == pygame.K_h:  # Ayuda
                            utils.mostrar_ayuda(grid.get_grid(), solution)
                            cantidadPistas +=1 

                    if not grid.win:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            grid.handle_click(pygame.mouse.get_pos(), event.button)

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

                     # Posicionar el puntaje en el centro de la parte inferior
                    puntaje_x = self.WIDTH // 2 - puntaje_surface.get_width() // 2  # Centrar el texto horizontalmente
                    puntaje_y = self.HEIGHT - puntaje_surface.get_height() - 10  # Colocar el puntaje justo encima del borde inferior


                    self.screen.blit(puntaje_surface, (puntaje_x, puntaje_y))  # Dibujar el puntaje en pantalla

                    #Guarda una screenshot de la partida al ganar
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
                    pygame.time.delay(5000)
                    running = False

                pygame.display.flip()




    def ask_board_size(self):
        """Permite al usuario ingresar el tamaño del tablero en formato NxM."""
        running = True
        input_text = ""
        error_message = ""  # Mensaje de error para mostrar en pantalla

        while running:
            self.screen.fill(WHITE)

            # Mensajes en pantalla
            title_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 100))

            # Mostrar el texto ingresado por el usuario
            input_surface = FONT.render(input_text, True, BLACK)
            self.screen.blit(input_surface, (self.WIDTH // 2 - input_surface.get_width() // 2, 200))

            # Mostrar mensaje de error si existe
            if error_message:
                error_surface = FONT.render(error_message, True, (255, 0, 0))  # Color rojo para errores
                self.screen.blit(error_surface, (self.WIDTH // 2 - error_surface.get_width() // 2, 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Si se presiona ESC, regresar al menú principal
                        return None
                    elif event.key == pygame.K_RETURN:  # Confirmar entrada con Enter
                        if "x" in input_text:
                            parts = input_text.split("x")
                            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                                rows, cols = map(int, parts)
                                if 5 <= rows <= 20 and 5 <= cols <= 20:  # Validar límites
                                    return rows, cols
                                else:
                                    error_message = "Tamaño inválido. Elija dimensiones entre 5 y 20."
                            else:
                                error_message = "Formato inválido. Use NxM (ejemplo: 10x10)."
                        else:
                            error_message = "Formato inválido. Use NxM (ejemplo: 10x10)."
                        input_text = ""  # Limpiar entrada después de un error
                    elif event.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        input_text = input_text[:-1]
                        error_message = ""  # Limpiar mensaje de error
                    elif event.unicode.isdigit() or event.unicode == "x":  # Aceptar números y "x"
                        input_text += event.unicode
                        error_message = ""  # Limpiar mensaje de error

        return None  # Valor por defecto si se cancela

    def ask_nonogram_name(self):
        """Permite al usuario ingresar un nombre para el nonograma."""
        running = True
        input_text = ""
        error_message = ""  # Mensaje de error para mostrar en pantalla

        while running:
            self.screen.fill(WHITE)

            # Mensajes en pantalla
            title_surface = FONT.render("Ingrese un nombre para el nonograma:", True, BLACK)
            self.screen.blit(title_surface, (self.WIDTH // 2 - title_surface.get_width() // 2, 100))

            # Mostrar el texto ingresado por el usuario
            input_surface = FONT.render(input_text, True, BLACK)
            self.screen.blit(input_surface, (self.WIDTH // 2 - input_surface.get_width() // 2, 200))

            # Mostrar mensaje de error si existe
            if error_message:
                error_surface = FONT.render(error_message, True, (255, 0, 0))  # Color rojo para errores
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
        result = self.ask_board_size()
        if result is None:  # Si el usuario presionó ESC, salir del método
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
