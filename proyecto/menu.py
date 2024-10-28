import sys  # Módulo para controlar la salida del sistema y el cierre del programa.
from constants import *  # Importa las constantes (colores, fuentes, etc.) definidas en 'constants.py'.

#Función que muestra el menú principal
def show_menu(screen, width, height):
    #Bucle principal del menú
    while True:
        #Rellena la pantalla con el color blanco
        screen.fill(WHITE)

        #Renderizado de textos del título y las opciones del menú
        title_surface = MENU_FONT.render("Seleccione modo:", True, BLACK)
        option1_surface = FONT.render("1. Tablero de tamaño aleatorio", True, BLACK)
        option2_surface = FONT.render("2. Elegir tamaño del tablero", True, BLACK)
        option3_surface = FONT.render("3. Cómo Jugar", True, BLACK)
        option4_surface = FONT.render("4. Cerrar nonograma", True, BLACK)

        #Centra los textos
        screen.blit(title_surface, (width - title_surface.get_width() // 2, height - 125))
        screen.blit(option1_surface, (width - option1_surface.get_width() // 2, height - 50))
        screen.blit(option2_surface, (width - option2_surface.get_width() // 2, height))
        screen.blit(option3_surface, (width - option3_surface.get_width() // 2, height + 50))
        screen.blit(option4_surface, (width - option4_surface.get_width() // 2, height + 100))

        #Actualiza la pantalla para que se muestre lo que se a renderizado
        pygame.display.flip()

        #Captura de los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Si se cierra la ventana
                pygame.quit()  #Cierra Pygame
                sys.exit()  #Sale del programa
            if event.type == pygame.KEYDOWN:  #Si se presiona una tecla
                if event.key == pygame.K_1:  #Si se presiona '1'
                    return "random"  #Devuelve la opción de tablero aleatorio
                elif event.key == pygame.K_2:  #Si se presiona '2'
                    return "choose_size"  #Devuelve la opción para elegir el tamaño del tablero
                elif event.key == pygame.K_3:
                    return "tutorial"
                elif event.key == pygame.K_4:  # Si se presiona '3'
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
