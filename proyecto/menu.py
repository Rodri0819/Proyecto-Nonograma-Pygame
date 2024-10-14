import sys
from constants import *

def show_menu(screen, width, height):
    while True:
        screen.fill(WHITE)
        title_surface = MENU_FONT.render("Seleccione una opción:", True, BLACK)
        option1_surface = FONT.render("1. Tablero aleatorio de tamaño aleatorio", True, BLACK)
        option2_surface = FONT.render("2. Elegir tamaño del tablero", True, BLACK)
        option3_surface = FONT.render("3. Cerrar nonograma", True, BLACK)
        screen.blit(title_surface, (width - title_surface.get_width() // 2, height - 100))
        screen.blit(option1_surface, (width - option1_surface.get_width() // 2, height - 50))
        screen.blit(option2_surface, (width - option2_surface.get_width() // 2, height))
        screen.blit(option3_surface, (width - option3_surface.get_width() // 2, height + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "random"
                elif event.key == pygame.K_2:
                    return "choose_size"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def get_board_size(screen, width, height):
    input_active = True
    user_text = ''
    while input_active:
        screen.fill(WHITE)
        prompt_surface = FONT.render("Ingrese el tamaño del tablero (ejemplo: 5x5):", True, BLACK)
        input_surface = FONT.render(user_text, True, BLACK)
        screen.blit(prompt_surface, (width // 2 - prompt_surface.get_width() // 2, height // 2 - 50))
        screen.blit(input_surface, (width // 2 - input_surface.get_width() // 2, height // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        rows, cols = map(int, user_text.lower().split('x'))
                        return rows, cols
                    except:
                        user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
