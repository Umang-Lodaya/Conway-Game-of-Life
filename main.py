# IMPORTING LIBRARIES
import time
import pygame
import numpy as np

# PYGAME CONSTANTS
SCREEN_SIZE = WIDTH, HEIGHT = 1200, 700
CELL_SIZE = 20
CELLS_SHAPE = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# DEFINING COLORS
COLOR_BG = (10, 10, 10)
COLOR_GRID = (50, 50, 50)
# COLOR_DIE_NEXT = (170, 170, 170) # COLOR OF CELL IF ITS GONNA DIE IN NEXT GENERATION
COLOR_DIE_NEXT = (240, 180, 190) # COLOR OF CELL IF ITS GONNA DIE IN NEXT GENERATION
# COLOR_ALIVE_NEXT = (255, 255, 255) # COLOR OF CELL IF ITS GONNA LIVE IN NEXT GENERATION
COLOR_ALIVE_NEXT = (180, 240, 190) # COLOR OF CELL IF ITS GONNA LIVE IN NEXT GENERATION

# PYGAME UPDATE FUNCTION
def update(SCREEN, CELLS, SIZE, with_progress = False):
    updatedCells = np.zeros(CELLS.shape)
    for row, col in np.ndindex(CELLS.shape):
        # COUNT OF NEIGHBORS THAT ARE ALIVE
        alive = np.sum(CELLS[row-1:row+2, col-1:col+2]) - CELLS[row, col]
        color = COLOR_BG if CELLS[row, col] == 0 else COLOR_ALIVE_NEXT

        # IF CURRENTLY CELL IS ALIVE
        if CELLS[row, col] == 1:
            # CHECKING IF CELL WOULD BE ALIVE
            if 2 <= alive <= 3:
                updatedCells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
            else:
                if with_progress:
                    color = COLOR_DIE_NEXT

        # IF CURRENTLY CELL IS DEAD
        else:
            # CHECKING IF CELL WOULD BE ALIVE
            if alive == 3:
                updatedCells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # DISPLAYING THE CELL ON SCREEN
        pygame.draw.rect(SCREEN, color, (col * SIZE, row * SIZE, SIZE - 1, SIZE - 1))
    
    return updatedCells

# MAIN FUNCTION
def main():
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Conway's Game of Life")
    SCREEN.fill(COLOR_GRID)

    CELLS = np.zeros(CELLS_SHAPE)
    update(SCREEN, CELLS, CELL_SIZE)

    pygame.display.flip()
    pygame.display.update()

    runningProgress = False

    # GAME LOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # PAUSING GAME AFTER PRESSING SPACE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    runningProgress = not runningProgress
                    update(SCREEN, CELLS, CELL_SIZE)
                    pygame.display.update()
            
            # DRAWING NEW CELLS
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                CELLS[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
                update(SCREEN, CELLS, CELL_SIZE)
                pygame.display.update()
        
        SCREEN.fill(COLOR_GRID)
        
        if runningProgress:
            CELLS = update(SCREEN, CELLS, CELL_SIZE, with_progress = True)
            pygame.display.update()
        
        time.sleep(0.001)

if __name__ == "__main__":
    print("\nSTARTING ...")
    main()
    print("ENDED!\n")