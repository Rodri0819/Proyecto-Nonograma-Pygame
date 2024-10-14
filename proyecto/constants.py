import pygame

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (90, 140, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tamaño de cuadrícula por defecto
DEFAULT_ROWS = 5
DEFAULT_COLS = 5
SQUARE_SIZE = 30

# Márgenes base
TOP_MARGIN_BASE = 24
LEFT_MARGIN_BASE = 24

# Inicialización de fuentes
pygame.font.init()
FONT = pygame.font.SysFont(None, 24)
WIN_FONT = pygame.font.SysFont(None, 48)
MENU_FONT = pygame.font.SysFont(None, 36)
