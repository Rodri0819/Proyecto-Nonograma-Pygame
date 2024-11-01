import sys  # Módulo para controlar la salida del sistema y el cierre del programa.
from constants import *  # Importa las constantes (colores, fuentes, etc.) definidas en 'constants.py'.
import os
import datetime

#Función que muestra el menú principal
def show_menu(screen, width, height):
    #Bucle principal del menú
    while True:
        #Rellena la pantalla con el color blanco
        screen.fill(WHITE)

        #Renderizado de textos del título y las opciones del menú
        title_surface = MENU_FONT.render("Seleccione modo:", True, BLACK)
        option1_surface = FONT.render("1. Cargar partida", True, BLACK)
        option2_surface = FONT.render("2. Tablero de tamaño aleatorio", True, BLACK)
        option3_surface = FONT.render("3. Elegir tamaño del tablero", True, BLACK)
        option4_surface = FONT.render("4. Cómo Jugar", True, BLACK)
        option5_surface = FONT.render("5. Cerrar nonograma", True, BLACK)

        #Centra los textos
        screen.blit(title_surface, (width - title_surface.get_width() // 2, height - 125))
        screen.blit(option1_surface, (width - option1_surface.get_width() // 2, height - 50))
        screen.blit(option2_surface, (width - option2_surface.get_width() // 2, height))
        screen.blit(option3_surface, (width - option3_surface.get_width() // 2, height + 50))
        screen.blit(option4_surface, (width - option4_surface.get_width() // 2, height + 100))
        screen.blit(option5_surface, (width - option5_surface.get_width() // 2, height + 150))

        #Actualiza la pantalla para que se muestre lo que se a renderizado
        pygame.display.flip()

        #Captura de los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Si se cierra la ventana
                pygame.quit()  #Cierra Pygame
                sys.exit()  #Sale del programa
            if event.type == pygame.KEYDOWN:  #Si se presiona una tecla
                if event.key == pygame.K_1:
                    return "cargar_partida"
                elif event.key == pygame.K_2:  #Si se presiona '1'
                    return "random"  #Devuelve la opción de tablero aleatorio
                elif event.key == pygame.K_3:  #Si se presiona '2'
                    return "choose_size"  #Devuelve la opción para elegir el tamaño del tablero
                elif event.key == pygame.K_4:
                    return "tutorial"
                elif event.key == pygame.K_5:  # Si se presiona '3'
                    pygame.quit()  #Cierra Pygame
                    sys.exit()  #Sale del programa



#Función que permite al jugador ingresar el tamaño del tablero
def get_board_size(screen, width, height):
    input_active = True  #Mantener el bucle de entrada activo
    user_text = ''  #Variable para almacenar el texto ingresado por el usuario

    #Bucle para capturar la entrada del usuario
    while input_active:
        screen.fill(WHITE)  #Rellena la pantalla con el color blanco

        #Renderiza el mensaje para ingresar el tamaño del tablero
        prompt_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
        #Renderiza el texto ingresado por el usuario
        input_surface = FONT.render(user_text, True, BLACK)

        #Posiciona ambos textos en el centro
        screen.blit(prompt_surface, (width // 2 - prompt_surface.get_width() // 2, height // 2 - 50))
        screen.blit(input_surface, (width // 2 - input_surface.get_width() // 2, height // 2))

        #Actualiza la pantalla para que se muestren los cambios
        pygame.display.flip()

        #Captura los eventos del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Si se cierra la ventana
                pygame.quit()  #Cierra Pygame
                sys.exit()  #Sale del programa
            if event.type == pygame.KEYDOWN:  #Si se presiona una tecla
                if event.key == pygame.K_RETURN:  #Si se presiona Enter
                    try:
                        #Intenta convertir el texto ingresado en el formato filas x columnas
                        rows, cols = map(int, user_text.lower().split('x'))
                        return rows, cols  #Devuelve el número de filas y columnas ingresadas
                    except:  #Si el formato es incorrecto
                        user_text = ''  #Borra el texto ingresado para que el usuario intente nuevamente
                elif event.key == pygame.K_BACKSPACE:  #Si se presiona la tecla de retroceso
                    user_text = user_text[:-1]  #Borra el último caracter del texto ingresado
                else:
                    user_text += event.unicode  #Agrega el carácter ingresado al texto

def get_saved_games():
        #Devuelve una lista de los archivos de partidas guardadas.
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
        instruction_surface = FONT.render("Presiona un número (1-5) para cargar una partida", True, BLACK)
        screen.blit(instruction_surface, (screen.get_width() // 2 - instruction_surface.get_width() // 2, 50))

        # Renderiza la lista de partidas guardadas, limitando a 5
        if saved_games:
            for i, game in enumerate(saved_games[:5]):  # Limitar a las primeras 5 partidas
                game_surface = FONT.render(f"{i + 1}. {game}", True, BLACK)  # Mostrar el índice (1, 2, 3...)
                screen.blit(game_surface, (screen.get_width() // 2 - game_surface.get_width() // 2, 100 + i * 30))    
        else:
            empty_surface = FONT.render("No hay partidas guardadas", True, BLACK)
            screen.blit(empty_surface, (screen.get_width() // 2 - empty_surface.get_width() // 2, 100))

        pygame.display.flip()  # Actualiza la pantalla
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Regresar con Escape
                    return "menu_principal"  # Indica que debe regresar al menú principal
                
                # Verificar si se presionó un número del 1 al 5
                if pygame.K_1 <= event.key <= pygame.K_5:
                    index = event.key - pygame.K_1  # Obtener el índice basado en la tecla presionada
                    if 0 <= index < len(saved_games[:5]):
                        return saved_games[index]  # Devuelve el nombre del archivo seleccionado

