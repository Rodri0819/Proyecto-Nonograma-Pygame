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


def show_saved_games(screen):
    saved_games = get_saved_games()

    # Ordenar las partidas guardadas del más reciente al más antiguo
    saved_games.sort(key=lambda x: datetime.datetime.strptime(x, "%Y%m%d_%H%M%S.pkl"), reverse=True)

    TEXT_COLOR = BLACK
    HOVER_TEXT_COLOR = (150, 150, 150)  # Color al pasar el mouse por encima
    TITLE_FONT = MENU_FONT
    OPTION_FONT = FONT

    while True:
        screen.fill(WHITE)  # Rellena la pantalla con blanco

        # Renderiza el título
        title_surface = TITLE_FONT.render("Partidas Guardadas", True, TEXT_COLOR)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20))

        # Mensaje instruccional
        instruction_surface = OPTION_FONT.render("Haz clic en una partida para cargarla", True, TEXT_COLOR)
        screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, 70))

        # Dibujar las opciones de partidas guardadas
        mouse_pos = pygame.mouse.get_pos()  # Obtener la posición del mouse
        option_rects = []  # Lista para guardar los rectángulos de cada opción

        if saved_games:
            for i, game in enumerate(saved_games[:5]):  # Limitar a las primeras 5 partidas
                option_surface = OPTION_FONT.render(f"{i + 1}. {game}", True, TEXT_COLOR)

                # Determinar posición del texto
                text_x = screen.get_width() // 2 - option_surface.get_width() // 2
                text_y = 120 + i * 50  # Espaciado entre opciones

                # Crear un rectángulo para la opción
                option_rect = pygame.Rect(text_x, text_y, option_surface.get_width(), option_surface.get_height())

                # Cambiar color al pasar el mouse por encima
                if option_rect.collidepoint(mouse_pos):
                    option_surface = OPTION_FONT.render(f"{i + 1}. {game}", True, HOVER_TEXT_COLOR)

                # Dibujar el texto
                screen.blit(option_surface, (text_x, text_y))

                # Guardar el rectángulo de la opción
                option_rects.append((option_rect, game))
        else:
            empty_surface = OPTION_FONT.render("No hay partidas guardadas", True, TEXT_COLOR)
            screen.blit(empty_surface, (screen.get_width() // 2 - empty_surface.get_width() // 2, 120))

        pygame.display.flip()  # Actualizar la pantalla

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                if event.button == 1:  # Solo clic izquierdo
                    for rect, game in option_rects:
                        if rect.collidepoint(event.pos):  # Verificar si el clic fue en una opción
                            if os.path.exists(os.path.join("partidas_guardadas", game)):
                                return game  # Retorna el nombre del archivo seleccionado
                            else:
                                print(f"El archivo {game} no existe.")
                                break  # Salir del bucle si el archivo no existe
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Salir al menú principal
                return "menu_principal"

def get_created_games():
    # Devuelve una lista de los archivos de partidas guardadas.
    directory = "nonogramas_creados"
    if not os.path.exists(directory):
        return []  # Devuelve una lista vacía si no existe la carpeta

    return [f for f in os.listdir(directory) if f.endswith('.pkl')]  # Filtra solo archivos .pkl

def show_created_games(screen):
    created_games = get_created_games()

    # Ordenar los nonogramas creados del más reciente al más antiguo
    created_games.sort(key=lambda x: datetime.datetime.strptime(x, "%Y%m%d_%H%M%S.pkl"), reverse=True)

    TEXT_COLOR = BLACK
    HOVER_TEXT_COLOR = (150, 150, 150)  # Color al pasar el mouse por encima
    TITLE_FONT = MENU_FONT
    OPTION_FONT = FONT

    while True:
        screen.fill(WHITE)  # Rellena la pantalla con blanco

        # Renderiza el título
        title_surface = TITLE_FONT.render("Nonogramas Creados:", True, TEXT_COLOR)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 20))

        # Mensaje instruccional
        instruction_surface = OPTION_FONT.render("Haz clic en un nonograma para cargarlo", True, TEXT_COLOR)
        screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, 70))

        # Dibujar las opciones de nonogramas creados
        mouse_pos = pygame.mouse.get_pos()  # Obtener la posición del mouse
        option_rects = []  # Lista para guardar los rectángulos de cada opción

        if created_games:
            for i, game in enumerate(created_games[:5]):  # Limitar a los primeros 5 nonogramas
                option_surface = OPTION_FONT.render(f"{i + 1}. {game}", True, TEXT_COLOR)

                # Determinar posición del texto
                text_x = screen.get_width() // 2 - option_surface.get_width() // 2
                text_y = 120 + i * 50  # Espaciado entre opciones

                # Crear un rectángulo para la opción
                option_rect = pygame.Rect(text_x, text_y, option_surface.get_width(), option_surface.get_height())

                # Cambiar color al pasar el mouse por encima
                if option_rect.collidepoint(mouse_pos):
                    option_surface = OPTION_FONT.render(f"{i + 1}. {game}", True, HOVER_TEXT_COLOR)

                # Dibujar el texto
                screen.blit(option_surface, (text_x, text_y))

                # Guardar el rectángulo de la opción
                option_rects.append((option_rect, game))
        else:
            empty_surface = OPTION_FONT.render("No hay nonogramas creados", True, TEXT_COLOR)
            screen.blit(empty_surface, (screen.get_width() // 2 - empty_surface.get_width() // 2, 120))

        pygame.display.flip()  # Actualizar la pantalla

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic
                if event.button == 1:  # Solo clic izquierdo
                    for rect, game in option_rects:
                        if rect.collidepoint(event.pos):  # Verificar si el clic fue en una opción
                            if os.path.exists(os.path.join("nonogramas_creados", game)):
                                return game  # Retorna el nombre del archivo seleccionado
                            else:
                                print(f"El archivo {game} no existe.")
                                break  # Salir del bucle si el archivo no existe
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Salir al menú principal
                return "menu_principal"