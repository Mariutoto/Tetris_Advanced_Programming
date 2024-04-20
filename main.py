import pygame
import sys

# Import everything from the game mode files
from Tetris_Puzzle_Mode_Yann import main as puzzle_main
from Tetris_Color_Mode_Yann import main as color_main
from Tetris_Multiplayer_local_Mode_Yann import main as multiplayer_main


# Define the button class
class Button:
    def __init__(self, text, x, y, width, height, callback_function):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback_function = callback_function
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Draw the button text
        font = pygame.font.SysFont('Calibri', 30)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, position):
        # Check if the position is inside the button's rect
        if self.rect.collidepoint(position):
            self.callback_function()



# Define game mode functions
def run_puzzle_mode():
    puzzle_main()

def run_color_mode():
    color_main()

# Define game mode functions
def run_multiplayer_mode():
    multiplayer_main()

# Initialize Pygame
pygame.init()

# Set up the display
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Tetris Game Modes')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define font for the title
title_font = pygame.font.SysFont('Calibri', 40)

# Create buttons
puzzle_button = Button("Puzzle Mode", 100, 200, 200, 50, run_puzzle_mode)
color_button = Button("Color Mode", 500, 200, 200, 50, run_color_mode)
multiplayer_button = Button("Local Multiplayer Mode", 250, 300, 350, 50, run_multiplayer_mode)  

# Main loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen

        # Draw the title
    title_surface = title_font.render('Click on a Game Mode to play', True, BLACK)
    title_rect = title_surface.get_rect(center=(screen_size[0] // 2, 100))
    screen.blit(title_surface, title_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if puzzle_button.rect.collidepoint(event.pos):
                puzzle_button.check_click(event.pos)
            elif color_button.rect.collidepoint(event.pos):
                color_button.check_click(event.pos)
            elif multiplayer_button.rect.collidepoint(event.pos):  # Add this check for the multiplayer button
                multiplayer_button.check_click(event.pos)

    # Draw buttons
    puzzle_button.draw(screen)
    color_button.draw(screen)
    multiplayer_button.draw(screen)  # You need to draw the multiplayer button

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
