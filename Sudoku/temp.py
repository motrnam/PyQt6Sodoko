import pygame
import sys

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define the puzzle (0 represents empty cells)
puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 540, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku")

# Define cell dimensions
CELL_SIZE = 60
GRID_SIZE = CELL_SIZE * 9


# Function to draw the Sudoku grid
def draw_grid():
    for i in range(10):
        # Draw horizontal lines
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (GRID_SIZE, i * CELL_SIZE), 1)

        # Draw vertical lines
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE), 1)


# Function to draw the Sudoku puzzle
def draw_puzzle():
    font = pygame.font.SysFont("Arial", 30)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                text = font.render(str(puzzle[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)


# Main game loop
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_puzzle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
