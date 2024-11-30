import sys  # Módulo para controlar la salida del sistema y el cierre del programa.
from constants import *  # Importa las constantes (colores, fuentes, etc.) definidas en 'constants.py'.
import os
import datetime


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


# Función que permite al jugador ingresar el tamaño del tablero
def get_board_size(screen, width, height):
    input_active = True  # Mantener el bucle de entrada activo
    user_text = ''  # Variable para almacenar el texto ingresado por el usuario

    # Bucle para capturar la entrada del usuario
    while input_active:
        screen.fill(WHITE)  # Rellena la pantalla con el color blanco

        # Renderiza el mensaje para ingresar el tamaño del tablero
        prompt_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
        # Renderiza el texto ingresado por el usuario
        input_surface = FONT.render(user_text, True, BLACK)

        # Posiciona ambos textos en el centro
        screen.blit(prompt_surface, (width // 2 - prompt_surface.get_width() // 2, height // 2 - 50))
        screen.blit(input_surface, (width // 2 - input_surface.get_width() // 2, height // 2))

        # Actualiza la pantalla para que se muestren los cambios
        pygame.display.flip()

        # Captura los eventos del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()  # Cierra Pygame
                sys.exit()  # Sale del programa
            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_RETURN:  # Si se presiona Enter
                    try:
                        # Intenta convertir el texto ingresado en el formato filas x columnas
                        rows, cols = map(int, user_text.lower().split('x'))
                        return rows, cols  # Devuelve el número de filas y columnas ingresadas
                    except:  # Si el formato es incorrecto
                        user_text = ''  # Borra el texto ingresado para que el usuario intente nuevamente
                elif event.key == pygame.K_BACKSPACE:  # Si se presiona la tecla de retroceso
                    user_text = user_text[:-1]  # Borra el último caracter del texto ingresado
                else:
                    user_text += event.unicode  # Agrega el carácter ingresado al texto


def get_saved_games():
    # Devuelve una lista de los archivos de partidas guardadas.
    directory = "partidas_guardadas"
    if not os.path.exists(directory):
        return []  # Devuelve una lista vacía si no existe la carpeta

    return [f for f in os.listdir(directory) if f.endswith('.pkl')]  # Filtra solo archivos .pkl


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

    selected_game = None
    running = True

    while running:
        screen.fill(WHITE)

        # Título
        title_surface = FONT.render("Selecciona un nonograma para jugar:", True, BLACK)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        # Obtener la posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Calcular posición inicial para centrar verticalmente
        total_height = len(created_games) * 40
        start_y = screen.get_height() // 2 - total_height // 2

        # Mostrar la lista de nonogramas
        for i, game in enumerate(created_games):
            text_color = BLACK
            # Detectar si el mouse está sobre una opción
            text_surface = FONT.render(game, True, text_color)
            text_x = screen.get_width() // 2 - text_surface.get_width() // 2
            text_y = start_y + i * 40

            # Detectar si el cursor está sobre el texto
            if pygame.Rect(text_x, text_y, text_surface.get_width(), text_surface.get_height()).collidepoint(mouse_pos):
                text_color = (150, 150, 150)  # Cambiar el color al pasar el cursor
                text_surface = FONT.render(game, True, text_color)

            screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    for i, game in enumerate(created_games):
                        text_surface = FONT.render(game, True, BLACK)
                        text_x = screen.get_width() // 2 - text_surface.get_width() // 2
                        text_y = start_y + i * 40
                        if pygame.Rect(text_x, text_y, text_surface.get_width(), text_surface.get_height()).collidepoint(mouse_pos):
                            selected_game = game
                            running = False
                            break

    if selected_game:
        return selected_game  # Retornar el archivo seleccionado
    return "menu_principal"  # Si no selecciona nada, regresar al menú principal
