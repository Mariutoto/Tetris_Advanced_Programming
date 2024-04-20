#Multiplayer local mode Yann

import pygame
import random

# Define color constants for easy reference
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
#So here we are choosing the colors for our game

# Define controls for two players
player_controls = {
    1: {'rotate': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'drop': pygame.K_SPACE},
    2: {'rotate': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'drop': pygame.K_q}  # Using 'q' for drop as an example
}


colors = [ 
    (180, 34, 22),    # Red
    (180, 34, 122),   # Pink
    (0, 0, 0),        # Black
    (80, 34, 22),     # Brown
    (120, 37, 179),   # Purple
    (100, 179, 179),  # Cyan
    (80, 134, 22),    # Green
]

class Figure:
    x = 0
    y = 0

    #The first block is one rotation and the other another, so for I there is only 2 possibilities but for there are multiple
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], #I shape
        [[4, 5, 9, 10], [2, 6, 5, 9]], #J shape
        [[6, 7, 9, 10], [1, 5, 6, 10]],# L #shape
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # T shape
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #S shape
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], #Z shape
        [[1, 2, 5, 6]], #O shape
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)  # Chooses a random tetromino type
        self.color = random.randint(1, len(colors) - 1)       # Chooses a random color (excluding the first one, typically black)
        self.rotation = 0                                     # Starts without any rotation

    #This method returns the current rotation of the tetromino. This is used to render the tetromino on the game board.
    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation += 1
        if self.rotation >= len(self.figures[self.type]):
            self.rotation = 0

class Tetris:
    def __init__(self, height, width):
        self.current_player = 1 # Start with player 1
        self.level = 1
        self.score = 0
        self.state = "start"
        self.x = 100  # To center the grid on the x-axis on the Pygame window
        self.y = 100   # To center the grid on the y-axis on the Pygame window
        self.zoom = 20  # The size of each Tetris block
        self.figure = None
        self.next_figures = [Figure(3, 0) for _ in range(3)]  # Initialize list of next pieces
        self.height = height  # The number of rows in the Tetris field
        self.width = width    # The number of columns in the Tetris field
        self.field = [[0 for _ in range(width)] for _ in range(height)]  # Initialize the playing field
        self.scores = {1: 0, 2: 0}  # Dictionary to hold scores for each player

    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2

    def new_figure(self):
        self.figure = self.next_figures.pop(0)  # Get the next piece from the list
        self.next_figures.append(Figure(3, 0))  # Add a new piece to the list
        self.switch_player()  # Switch player after a new figure is spawned


    def process_key(self, key):
        controls = player_controls[self.current_player]
        if key == controls['rotate']:
            self.rotate()
        elif key == controls['down']:
            self.go_down()
        elif key == controls['left']:
            self.go_side(-1)
        elif key == controls['right']:
            self.go_side(1)

    def draw_next_pieces(self, screen):
        # Calculate the position and size of the box for next pieces
        box_width = 6 * self.zoom  # Adjust as needed
        box_height = 16 * self.zoom  # Adjust as needed
        box_x = self.x + self.width * self.zoom + 20  # Adjust as needed
        box_y = self.y  # Adjust as needed

        # Draw the box for next pieces
        pygame.draw.rect(screen, GRAY, [box_x, box_y, box_width, box_height], 1)

        # Draw the title
        font = pygame.font.SysFont('Calibri', 20, True, False)
        text_surface = font.render('Next Pieces', True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x + box_width // 2, box_y + 20)  # Adjust position as needed
        screen.blit(text_surface, text_rect)

        # Draw each next piece vertically stacked
        next_pieces_y = box_y + 40  # Adjust spacing from the top of the box
        for next_piece in self.next_figures:
            # Find the min and max x indices of the blocks for the current piece to center it
            block_indices = [index % 4 for index in next_piece.image()]  # Get only the x indices of blocks
            min_x = min(block_indices)
            max_x = max(block_indices)
            piece_width = (max_x - min_x + 1) * self.zoom
            start_x = box_x + (box_width - piece_width) // 2 - min_x * self.zoom  # Calculate start x to center the piece

            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in next_piece.image():
                        pygame.draw.rect(screen, colors[next_piece.color],
                                     [start_x + self.zoom * j + 1,
                                      next_pieces_y + self.zoom * i + 1,
                                      self.zoom - 2, self.zoom - 2])
            next_pieces_y += 5 * self.zoom  # Adjust spacing between pieces
                            
    def intersects(self):
        for i in range(4):  # Iterate over each row in the 4x4 matrix
            for j in range(4):  # Iterate over each column in the 4x4 matrix
                # Check if the position in the 4x4 matrix corresponds to a block in the tetromino
                if i * 4 + j in self.figure.image():
                    # Calculate the absolute x and y positions on the grid
                    grid_x = j + self.figure.x
                    grid_y = i + self.figure.y

                    # Check for boundary conditions and block collisions
                    if self.is_out_of_bounds(grid_x, grid_y) or self.is_collision(grid_x, grid_y):
                        return True
        return False

    def is_out_of_bounds(self, grid_x, grid_y):
        # Check if the block is outside the left, right, or bottom boundaries of the grid
        return grid_x < 0 or grid_x >= self.width or grid_y >= self.height

    def is_collision(self, grid_x, grid_y):
        # Check if the block position on the grid is already occupied
        return self.field[grid_y][grid_x] > 0

    def break_lines(self):
        # Initialize a counter for the number of lines cleared
        lines_cleared = 0
        
        # Iterate through each row in the game field
        for row in range(self.height):
            if all(self.field[row][col] != 0 for col in range(self.width)):  # Check if row is completely filled
                lines_cleared += 1
                # Move all rows above this one down by one
                for move_row in range(row, 0, -1):
                    self.field[move_row] = self.field[move_row - 1]
                self.field[0] = [0] * self.width  # Reset the topmost row

        # Update the score of the current player based on the number of lines cleared
        # Increment score quadratically to emphasize clearing multiple lines at once
        if lines_cleared > 0:
            self.scores[self.current_player] += lines_cleared ** 2


    def go_space(self):
        # Drop the tetromino down until it intersects with another block or the bottom of the grid
        while not self.intersects():
            self.figure.y += 1  # Incrementally move the tetromino down by one row
    
        # Move the tetromino back up by one row to its last valid position
        self.figure.y -= 1
    
        # Lock the tetromino in place and handle any full lines created
        self.freeze()


    def go_down(self):
        # Attempt to move the tetromino down by one unit
        self.figure.y += 1
    
        # Check if the tetromino intersects with anything after moving down
        if self.intersects():
            # Move back up if there's an intersection
            self.figure.y -= 1

            # Lock the tetromino in place since it cannot move further
            self.freeze()


    def freeze(self):
        # Embed the tetromino into the field
        for i in range(4):  # Tetromino fits within a 4x4 matrix
            for j in range(4):
                # Check if the cell is part of the tetromino image
                if i * 4 + j in self.figure.image():
                    # Set the color of the grid cell to match the tetromino's color
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
    
        # Check and clear any full lines
        self.break_lines()
    
        # Spawn a new tetromino
        self.new_figure()
    
        # Check if the new figure intersects immediately (game over condition)
        if self.intersects():
            self.state = "gameover"


    def go_side(self, dx):
        # Store the current x position before moving
        old_x = self.figure.x
    
        # Try to move the tetromino horizontally by dx units
        self.figure.x += dx
    
        # Check for any intersections after moving
        if self.intersects():
            # Revert to the original position if there is an intersection
            self.figure.x = old_x


    def rotate(self):
        # Store the current rotation before attempting to rotate
        old_rotation = self.figure.rotation
    
        # Rotate the tetromino
        self.figure.rotate()
    
        # Check for intersections after rotation
        if self.intersects():
            # If there's an intersection, revert to the previous rotation
            self.figure.rotation = old_rotation



# Import necessary Pygame library
import pygame

# Define color constants for easy reference
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define a main function that will run the game
def main():
    # Initialize the Pygame engine
    pygame.init()

    # Define color constants for easy reference
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)


    # Set the size of the window or screen for the game
    screen_size = (600, 600)
    screen = pygame.display.set_mode(screen_size)

    # Set the title of the window
    pygame.display.set_caption("Tetris Muliplayer")

    # Flag to keep track of whether the game loop should continue
    done = False

    # Create a clock object to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Define frames per second: how many times the game updates per second
    fps = 30

    game = Tetris(20, 10)
    counter = 0

    # Boolean to check if the down key is being pressed
    pressing_down = False

    # Main game loop
    while not done:
        # Check and create a new tetromino if needed
        if game.figure is None:
            game.new_figure()

        # Manage the frame counter for timing events
        counter += 1
        if counter > 100000:  # Prevent overflow for performance
            counter = 0

        # Calculate how frequently the tetromino should move down based on game level
        movement_frequency = fps // game.level // 2

        # Move the tetromino down based on timing or player action
        if counter % movement_frequency == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Fetch the control set for the current player
                controls = player_controls[game.current_player]

                if event.key == controls['rotate']:
                    game.rotate()
                elif event.key == controls['down']:
                    pressing_down = True  # Allow the player to hold down to accelerate the piece
                elif event.key == controls['left']:
                    game.go_side(-1)
                elif event.key == controls['right']:
                    game.go_side(1)
                elif event.key == controls['drop']:  # Assuming you map a key for drop like 'space' for both
                    game.go_space()
                    game.switch_player()  # Switch the turn after dropping the piece

                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)  # Reset the game

            elif event.type == pygame.KEYUP:
                if event.key == controls['down']:
                    pressing_down = False  # Stop the fast drop when the key is released


        # Draw the game board
        screen.fill(WHITE)
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        # Draw the active tetromino
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.zoom * (j + game.figure.x) + 1,
                                        game.y + game.zoom * (i + game.figure.y) + 1,
                                        game.zoom - 2, game.zoom - 2])

        game.draw_next_pieces(screen)

        # Display scores for both players
        font = pygame.font.SysFont('Calibri', 25, True, False)
        padding = 20
        score1_text = font.render(f"Player 1 Score: {game.scores[1]}", True, BLACK)
        score2_text = font.render(f"Player 2 Score: {game.scores[2]}", True, BLACK)
        # Calculate positions for the scores so they are not right against the screen edges
        score1_pos = (padding, padding)  # Add some padding from the top left corner
        score2_pos = (screen.get_width() - score2_text.get_width() - padding, padding)  # Add some padding from the top right corner

        screen.blit(score1_text, (10, 10))  # Player 1 score on the left
        screen.blit(score2_text, (screen.get_width() - score2_text.get_width() - 10, 10))  # Player 2 score on the right

        if game.state == "gameover":
            font1 = pygame.font.SysFont('Calibri', 65, True, False)
            text_game_over = font1.render("Game Over", True, (255, 125, 0))
            text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))
            screen.blit(text_game_over, [20, 100])
            screen.blit(text_game_over1, [25, 265])

        # Update the display and maintain frame rate
        pygame.display.flip()
        clock.tick(fps)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()