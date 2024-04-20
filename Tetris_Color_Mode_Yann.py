#Tetris game

import pygame
import random

# Define color constants for easy reference
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
#So here we are choosing the colors for our game

colors = [
    (180, 34, 22),    # Red
    (180, 34, 122),   # Pink
    (0, 0, 0),        # Black (generally used for background or empty spaces)
    (80, 34, 22),     # Brown
    (120, 37, 179),   # Purple
    (100, 179, 179),  # Cyan
    (80, 134, 22),    # Green
    (255, 165, 0),    # Orange (Distinct from red and brown)
    (255, 255, 0),    # Yellow (Bright and highly visible)
    (0, 128, 128),    # Teal (Contrasts well with cyan and blue)
    (255, 20, 147),   # Deep Pink (Stands out from purple and red)
    (75, 0, 130)      # Indigo (Different enough from deep blues and purples)
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
        self.level = 1
        self.score = 0
        self.state = "start"
        self.x = 100  # To center the grid on the x-axis on the Pygame window
        self.y = 30   # To center the grid on the y-axis on the Pygame window
        self.zoom = 20  # The size of each Tetris block
        self.figure = None
        self.next_figures = [Figure(3, 0) for _ in range(3)]  # Initialize list of next pieces
        self.height = height  # The number of rows in the Tetris field
        self.width = width    # The number of columns in the Tetris field
        self.field = [[0 for _ in range(width)] for _ in range(height)]  # Initialize the playing field

    def new_figure(self):
        self.figure = self.next_figures.pop(0)  # Get the next piece from the list
        self.next_figures.append(Figure(3, 0))  # Add a new piece to the list

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
            # Check if all blocks in the row are filled (none are zero)
            if all(self.field[row][col] != 0 for col in range(self.width)):
                # Increment the count of lines cleared
                lines_cleared += 1
                
                # Move all rows above this one down by one
                for move_row in range(row, 0, -1):
                    self.field[move_row] = self.field[move_row - 1]
                
                # Reset the topmost row to all zeros because there's no row above it
                self.field[0] = [0] * self.width
        
        # Update the score based on the number of lines cleared
        # The scoring is quadratic, emphasizing clearing multiple lines at once
        self.score += lines_cleared ** 2


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

#problem avec bottom grid pui comment savoir si c est les meme couleurs

    def freeze(self):
        touching_same_color = False
        positions_to_clear = []  # Store positions of the tetromino to be cleared

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    grid_x = j + self.figure.x
                    grid_y = i + self.figure.y
                    # Check if block is within grid bounds
                    if 0 <= grid_y < self.height and 0 <= grid_x < self.width:
                        positions_to_clear.append((grid_x, grid_y))  # Collect position to potentially clear
                        # Check adjacent cells for color match
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = grid_x + dx, grid_y + dy
                            # Make sure the neighbor is within bounds
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                # Check for same color and that the position is not empty
                                if self.field[ny][nx] != 0 and self.field[ny][nx] == self.figure.color:
                                    touching_same_color = True
                                    break
                        if touching_same_color:
                            break
                if touching_same_color:
                    break

        # If any part of the tetromino touched another block of the same color, clear all positions
        if touching_same_color:
            for x, y in positions_to_clear:
                self.field[y][x] = 0  # Clear the position
        else:
            # Otherwise, lock the tetromino in place
            for x, y in positions_to_clear:
                self.field[y][x] = self.figure.color
            self.break_lines()  # Check and clear any full lines if needed

        # Spawn a new tetromino
        self.new_figure()
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
# Define a main function that will run the game
def main():
    # Initialize the Pygame engine
    pygame.init()

    # Define color constants for easy reference
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    # Set the size of the window or screen for the game
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)

    # Set the title of the window
    pygame.display.set_caption("Tetris")

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
                if event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_DOWN:
                    pressing_down = True
                elif event.key == pygame.K_LEFT:
                    game.go_side(-1)
                elif event.key == pygame.K_RIGHT:
                    game.go_side(1)
                elif event.key == pygame.K_SPACE:
                    game.go_space()
                elif event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)  # Reset game

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

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
        # Display score and game over messages
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        screen.blit(text, [0, 0])

        if game.state == "gameover":
            font1 = pygame.font.SysFont('Calibri', 60, True, BLACK,)
            text_game_over = font1.render("Game Over", True, BLACK, )
            text_game_over1 = font1.render("Press esc & restart", True, BLACK,)
            screen.blit(text_game_over, [20, 100])
            screen.blit(text_game_over1, [25, 265])

        # Update the display and maintain frame rate
        pygame.display.flip()
        clock.tick(fps)

    # Quit Pygame
    pygame.quit()

# This allows the script to be run as a standalone game as well
if __name__ == "__main__":
    main()