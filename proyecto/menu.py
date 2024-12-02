import sys  # Módulo para controlar la salida del sistema y el cierre del programa.
from constants import *  # Importa las constantes (colores, fuentes, etc.) definidas en 'constants.py'.
import os
import datetime

top_scores = []  # Lista que almacenará los puntajes

# Función que muestra el menú principal
def show_menu(screen, width, height):
    options = [
        ("Cargar partida", "cargar_partida"),
        ("Tablero de tamaño aleatorio", "random"),
        ("Elegir tamaño del tablero", "choose_size"),
        ("Jugar Nonograma Personalizado", "play_custom"),
        ("Crear Nonograma", "create_nonogram"),
        ("¿Cómo Jugar?", "tutorial"),
        ("Cerrar nonograma", "exit")
    ]

    # Colores
    BUTTON_COLOR = (200, 200, 200)  # Color de fondo del botón
    HOVER_COLOR = (150, 150, 150)  # Color al pasar el mouse por encima
    TEXT_COLOR = BLACK
    BORDER_COLOR = BLACK
    TITLE_BG_COLOR = (173, 216, 230)  # Fondo del título

    # Posiciones y rectángulos para cada opción
    option_rects = []

    while True:
        screen.fill(WHITE)  # Rellena la pantalla con blanco

        # Dibujar título con fondo
        title_surface = MENU_FONT.render("Seleccione modo", True, BLACK)
        title_width, title_height = title_surface.get_width(), title_surface.get_height()
        title_x = width - title_width // 2
        title_y = height - 250

        # Dibujar fondo para el título
        title_bg_rect = pygame.Rect(title_x - 20, title_y - 10, title_width + 40, title_height + 20)
        pygame.draw.rect(screen, TITLE_BG_COLOR, title_bg_rect)
        pygame.draw.rect(screen, BORDER_COLOR, title_bg_rect, 2)  # Borde para el fondo del título
        screen.blit(title_surface, (title_x, title_y))  # Dibujar texto del título

        # Mostrar el top 10 de puntajes en el lado izquierdo
        mostrar_top_scores(screen, width, height)

        option_rects = []
        mouse_pos = pygame.mouse.get_pos()  # Obtener la posición actual del mouse

        for i, (text, action) in enumerate(options):
            option_surface = FONT.render(text, True, TEXT_COLOR)
            option_x = width  # Centrar botones horizontalmente
            option_y = height - 150 + i * 60  # Separación vertical entre botones
            button_width = 300
            button_height = 40

            # Crear un rectángulo para el botón
            button_rect = pygame.Rect(option_x - button_width // 2, option_y, button_width, button_height)

            # Cambiar color de fondo si el mouse está sobre el botón
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, button_rect)  # Color hover
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Color normal

            # Dibujar borde del botón
            pygame.draw.rect(screen, BORDER_COLOR, button_rect, 2)

            # Dibujar el texto de la opción centrado en el botón
            text_x = button_rect.centerx - option_surface.get_width() // 2
            text_y = button_rect.centery - option_surface.get_height() // 2
            screen.blit(option_surface, (text_x, text_y))

            # Guardar el rectángulo y la acción para manejar clics
            option_rects.append((button_rect, action))

        pygame.display.flip()  # Actualizar pantalla

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Cerrar juego
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                if event.button == 1:  # Solo manejar clic izquierdo
                    for button_rect, action in option_rects:
                        if button_rect.collidepoint(event.pos):  # Verificar clic en un botón
                            return action  # Retornar la acción correspondiente

# Función para agregar un puntaje al top 10
def agregar_puntaje(puntaje):
    global top_scores

    # Añadir el nuevo puntaje a la lista
    top_scores.append(puntaje)

    # Ordenar los puntajes de mayor a menor
    top_scores.sort(reverse=True)

    # Mantener solo los 10 mejores puntajes
    if len(top_scores) > 10:
        top_scores = top_scores[:10]

# Función para mostrar los puntajes en el menú
def mostrar_top_scores(screen, width, height):
    global top_scores

    # Posición de inicio para los puntajes (a la izquierda)
    x_offset = 50  # Límite izquierdo
    y_offset = 100  # Posición superior en el menú

    # Dibujar título "Top Puntajes"
    title_surface = FONT.render("Top Puntajes", True, BLACK)
    screen.blit(title_surface, (x_offset, y_offset - 30))  # Título arriba de la lista de puntajes

    # Mostrar los puntajes en el lado izquierdo
    if not top_scores:
        # Si no hay puntajes, mostrar "no hay registros"
        score_text = f"No hay registros"  
        score_surface = FONT.render(score_text, True, BLACK)
        screen.blit(score_surface, (x_offset, y_offset))  
    else:
        # Mostrar los puntajes en el lado izquierdo con su numeración
        for i, score in enumerate(top_scores):
            score_text = f"{i+1}. {score}"  # Texto con el índice y el puntaje
            score_surface = FONT.render(score_text, True, BLACK)  # Usamos la misma fuente
            screen.blit(score_surface, (x_offset, y_offset + i * 30))  # Dibujar cada puntaje

# Función que permite al jugador ingresar el tamaño del tablero
def get_board_size(screen, width, height):
    input_active = True  # Mantener el bucle de entrada activo
    user_text = ''  # Variable para almacenar el texto ingresado por el usuario
    error_message = ""  # Mensaje de error para entrada inválida

    while input_active:
        screen.fill(WHITE)  # Rellena la pantalla con el color blanco

        # Renderiza el mensaje para ingresar el tamaño del tablero
        prompt_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
        # Renderiza el texto ingresado por el usuario
        input_surface = FONT.render(user_text, True, BLACK)
        # Renderiza el mensaje de error si existe
        if error_message:
            error_surface = FONT.render(error_message, True, (255, 0, 0))  # Texto en rojo

        # Posiciona los textos en la pantalla
        screen.blit(prompt_surface, (width // 2 - prompt_surface.get_width() // 2, 100))
        screen.blit(input_surface, (width // 2 - input_surface.get_width() // 2, 150))
        if error_message:
            screen.blit(error_surface, (width // 2 - error_surface.get_width() // 2, height // 2 + 50))

        # Dibujar botón "Volver" en la esquina superior derecha
        button_size = 50
        back_button_x = width - button_size - 10
        back_button_y = 10

        # Detectar si el cursor está sobre el botón "Volver"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_back = back_button_x <= mouse_x <= back_button_x + button_size and \
                          back_button_y <= mouse_y <= back_button_y + button_size

        back_button_color = (150, 0, 0) if is_hovered_back else (200, 0, 0)

        # Dibujar el borde negro del botón "Volver"
        pygame.draw.rect(screen, BLACK, (back_button_x - 3, back_button_y - 3,
                                         button_size + 6, button_size + 6))
        pygame.draw.rect(screen, back_button_color, (back_button_x, back_button_y, button_size, button_size))
        back_button_text = FONT.render("Volver", True, WHITE)
        screen.blit(back_button_text, (back_button_x + (button_size - back_button_text.get_width()) // 2,
                                       back_button_y + (button_size - back_button_text.get_height()) // 2))

        # Dibujar botón "Confirmar" (Enter) debajo del input
        confirm_button_x = width // 2 - 150
        confirm_button_y = 300
        confirm_button_width = 300
        confirm_button_height = 50
        is_hovered_confirm = confirm_button_x <= mouse_x <= confirm_button_x + confirm_button_width and \
                             confirm_button_y <= mouse_y <= confirm_button_y + confirm_button_height

        confirm_button_color = (0, 150, 0) if is_hovered_confirm else (0, 200, 0)
        pygame.draw.rect(screen, confirm_button_color, (confirm_button_x, confirm_button_y,
                                                        confirm_button_width, confirm_button_height))
        pygame.draw.rect(screen, BLACK, (confirm_button_x, confirm_button_y,
                                         confirm_button_width, confirm_button_height), 2)
        confirm_button_text = FONT.render("Confirmar", True, WHITE)
        screen.blit(confirm_button_text, (confirm_button_x + (confirm_button_width - confirm_button_text.get_width()) // 2,
                                          confirm_button_y + (confirm_button_height - confirm_button_text.get_height()) // 2))

        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_RETURN:  # Si se presiona Enter
                    try:
                        rows, cols = map(int, user_text.lower().split('x'))
                        if 5 <= rows <= 20 and 5 <= cols <= 20:
                            return rows, cols
                        else:
                            error_message = "Tamaño inválido. Dimensiones entre 5x5 y 20x20."
                    except ValueError:
                        error_message = "Formato inválido. Use NxM (ejemplo: 10x10)."
                elif event.key == pygame.K_BACKSPACE:  # Si se presiona retroceso
                    user_text = user_text[:-1]
                    error_message = ""
                else:  # Agregar el texto ingresado
                    user_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clics del mouse
                if is_hovered_back:  # Si se hace clic en "Volver"
                    return None
                if is_hovered_confirm:  # Si se hace clic en "Confirmar"
                    try:
                        rows, cols = map(int, user_text.lower().split('x'))
                        if 5 <= rows <= 20 and 5 <= cols <= 20:
                            return rows, cols
                        else:
                            error_message = "Tamaño inválido. Dimensiones entre 5x5 y 20x20."
                    except ValueError:
                        error_message = "Formato inválido. Use NxM (ejemplo: 10x10)."


def get_saved_games():
    # Devuelve una lista de los archivos de partidas guardadas.
    directory = "partidas_guardadas"
    if not os.path.exists(directory):
        return []  # Devuelve una lista vacía si no existe la carpeta

    return [f for f in os.listdir(directory) if f.endswith('.pkl')]  # Filtra solo archivos .pkl

def show_saved_games(screen):
    saved_games = get_saved_games()

    # Ordenar las partidas guardadas del más reciente al más antiguo
    saved_games.sort(key=lambda x: datetime.datetime.strptime(x, "%Y%m%d_%H%M%S.pkl"), reverse=True)

    while True:
        screen.fill(WHITE)  # Rellena la pantalla con blanco

        # Renderiza el título
        title_surface = FONT.render("Partidas Guardadas:", True, BLACK)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20))

        # Mensaje instruccional
        instruction_surface = FONT.render("Haz clic en una partida para cargarla", True, BLACK)
        screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, 50))

        # Dibujar las partidas guardadas como botones
        game_buttons = []
        if saved_games:
            for i, game in enumerate(saved_games[:5]):  # Limitar a las primeras 5 partidas
                button_x = screen.get_width() // 2 - 150
                button_y = 100 + i * 50
                button_width, button_height = 300, 40

                # Detectar si el cursor está sobre el botón
                mouse_x, mouse_y = pygame.mouse.get_pos()
                is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

                # Cambiar el color del botón si está siendo "hovered"
                button_color = (150, 150, 150) if is_hovered else (200, 200, 200)

                # Dibujar el botón
                pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
                pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)  # Borde negro

                # Renderizar el texto de la partida
                game_text = FONT.render(game, True, BLACK)
                screen.blit(game_text, (button_x + (button_width - game_text.get_width()) // 2,
                                        button_y + (button_height - game_text.get_height()) // 2))

                # Guardar las coordenadas del botón
                game_buttons.append((button_x, button_y, button_width, button_height, game))
        else:
            empty_surface = FONT.render("No hay partidas guardadas", True, BLACK)
            screen.blit(empty_surface, (screen.get_width() // 2 - empty_surface.get_width() // 2, 100))

        # Dibujar el botón "Volver" en la esquina superior derecha
        button_size = 50  # Hacerlo casi cuadrado
        button_x = screen.get_width() - button_size - 10
        button_y = 10

        # Detectar si el cursor está sobre el botón "Volver"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_back = button_x <= mouse_x <= button_x + button_size and button_y <= mouse_y <= button_y + button_size

        # Cambiar el color del botón si está siendo "hovered"
        button_color_back = (150, 0, 0) if is_hovered_back else (200, 0, 0)

        # Dibujar el borde negro del botón "Volver"
        border_thickness = 3
        pygame.draw.rect(screen, BLACK, (button_x - border_thickness, button_y - border_thickness,
                                         button_size + 2 * border_thickness, button_size + 2 * border_thickness))

        # Dibujar el botón "Volver" dentro del borde
        pygame.draw.rect(screen, button_color_back, (button_x, button_y, button_size, button_size))

        # Agregar texto centrado dentro del botón "Volver"
        button_text = FONT.render("Volver", True, WHITE)
        screen.blit(button_text, (button_x + (button_size - button_text.get_width()) // 2,
                                  button_y + (button_size - button_text.get_height()) // 2))

        pygame.display.flip()  # Actualiza la pantalla

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Verificar si se hizo clic en el botón "Volver"
                if is_hovered_back:
                    return "menu_principal"

                # Verificar si se hizo clic en alguna partida
                for button in game_buttons:
                    button_x, button_y, button_width, button_height, game = button
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        return game  # Devuelve el nombre del archivo seleccionado

def show_created_games(screen):
    """Muestra una lista de nonogramas creados y permite al usuario seleccionar uno."""
    directory = "nonogramas_creados"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Obtener la lista de archivos en la carpeta
    created_games = [f for f in os.listdir(directory) if f.endswith(".pkl")]

    # Ordenar los archivos
    try:
        created_games.sort(
            key=lambda x: datetime.datetime.strptime(x, "%Y%m%d_%H%M%S.pkl"),
            reverse=True
        )
    except ValueError:
        created_games.sort()  # Orden alfabético si hay nombres personalizados

    while True:
        screen.fill(WHITE)

        # Título
        title_surface = FONT.render("Selecciona un nonograma para jugar:", True, BLACK)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20))

        # Dibujar los nonogramas creados como botones
        game_buttons = []
        if created_games:
            for i, game in enumerate(created_games[:5]):  # Limitar a las primeras 5 partidas
                button_x = screen.get_width() // 2 - 150
                button_y = 100 + i * 50
                button_width, button_height = 300, 40

                # Detectar si el cursor está sobre el botón
                mouse_x, mouse_y = pygame.mouse.get_pos()
                is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

                # Cambiar el color del botón si está siendo "hovered"
                button_color = (150, 150, 150) if is_hovered else (200, 200, 200)

                # Dibujar el botón
                pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
                pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 2)  # Borde negro

                # Renderizar el texto del nonograma
                game_text = FONT.render(game, True, BLACK)
                screen.blit(game_text, (button_x + (button_width - game_text.get_width()) // 2,
                                        button_y + (button_height - game_text.get_height()) // 2))

                # Guardar las coordenadas del botón
                game_buttons.append((button_x, button_y, button_width, button_height, game))
        else:
            empty_surface = FONT.render("No hay nonogramas creados", True, BLACK)
            screen.blit(empty_surface, (screen.get_width() // 2 - empty_surface.get_width() // 2, 100))

        # Dibujar el botón "Volver" en la esquina superior derecha
        button_size = 50  # Hacerlo casi cuadrado
        button_x = screen.get_width() - button_size - 10
        button_y = 10

        # Detectar si el cursor está sobre el botón "Volver"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_back = button_x <= mouse_x <= button_x + button_size and button_y <= mouse_y <= button_y + button_size

        # Cambiar el color del botón si está siendo "hovered"
        button_color_back = (150, 0, 0) if is_hovered_back else (200, 0, 0)

        # Dibujar el borde negro del botón "Volver"
        border_thickness = 3
        pygame.draw.rect(screen, BLACK, (button_x - border_thickness, button_y - border_thickness,
                                         button_size + 2 * border_thickness, button_size + 2 * border_thickness))

        # Dibujar el botón "Volver" dentro del borde
        pygame.draw.rect(screen, button_color_back, (button_x, button_y, button_size, button_size))

        # Agregar texto centrado dentro del botón "Volver"
        button_text = FONT.render("Volver", True, WHITE)
        screen.blit(button_text, (button_x + (button_size - button_text.get_width()) // 2,
                                  button_y + (button_size - button_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Verificar si se hizo clic en el botón "Volver"
                if is_hovered_back:
                    return "menu_principal"

                # Verificar si se hizo clic en algún nonograma
                for button in game_buttons:
                    button_x, button_y, button_width, button_height, game = button
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        return game  # Devuelve el nombre del archivo seleccionado
