import pygame
import sys
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (90, 140, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ROWS = 5
COLS = 5
SQUARE_SIZE = 30
TOP_MARGIN = 24 + 7 * ROWS
LEFT_MARGIN = 24 + 7 * COLS

WIDTH = 50 + LEFT_MARGIN + COLS * SQUARE_SIZE
HEIGHT = 50 + TOP_MARGIN + ROWS * SQUARE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Nonogram")

solution = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont(None, 24)
win_font = pygame.font.SysFont(None, 48)

def generate_clues():
    row_clues = []
    col_clues = []
    for row in solution:
        clues = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        row_clues.append(clues or [0])
    for col in range(COLS):
        clues = []
        count = 0
        for row in range(ROWS):
            if solution[row][col] == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues or [0])
    return row_clues, col_clues

row_clues, col_clues = generate_clues()

def check_win():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 1 and solution[row][col] != 1:
                return False
            if grid[row][col] == 0 and solution[row][col] == 1:
                return False
    return True


def draw_grid():
    for i, clues in enumerate(row_clues):
        text = ' '.join(map(str, clues))
        clue_surface = font.render(text, True, BLACK)
        screen.blit(clue_surface, (10, TOP_MARGIN + i * SQUARE_SIZE))

    for i, clues in enumerate(col_clues):
        for j, clue in enumerate(clues):
            clue_surface = font.render(str(clue), True, BLACK)
            screen.blit(clue_surface, (LEFT_MARGIN + i * SQUARE_SIZE + SQUARE_SIZE / 2 -10, 10 + j * 15))  # Espaciado vertical

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(LEFT_MARGIN + col * SQUARE_SIZE, TOP_MARGIN + row * SQUARE_SIZE, SQUARE_SIZE,
                               SQUARE_SIZE)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GRAY, rect)
            elif grid[row][col] == -1:
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


def handle_click(pos, button):
    x, y = pos
    row = (y - TOP_MARGIN) // SQUARE_SIZE
    col = (x - LEFT_MARGIN) // SQUARE_SIZE
    if 0 <= row < ROWS and 0 <= col < COLS:
        if button == 1:
            if grid[row][col] == 0:
                grid[row][col] = 1
            elif grid[row][col] == 1:
                grid[row][col] = -1
            else:
                grid[row][col] = 0
        elif button == 3:
            if grid[row][col] == 0:
                grid[row][col] = -1
            elif grid[row][col] == -1:
                grid[row][col] = 1
            else:
                grid[row][col] = 0

win = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not win:
            handle_click(pygame.mouse.get_pos(), event.button)
    screen.fill(WHITE)
    draw_grid()
    if check_win():
        win = True
        win_message = win_font.render("Ganaste", True, GREEN)
        screen.blit(win_message, (WIDTH // 2 - win_message.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
