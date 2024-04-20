#Tetris Puzzle 1

import pygame
import random

# Define color constants for easy reference
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

#So here we are choosing the colors for our game

colors = [
    (0, 0, 0),        # Black, typically unused or for background
    (0, 0, 0),        # Black, typically unused or for background
]

class Figure:
    x = 0
    y = 0

    #The first block is one rotation and the other another, so for I there is only 2 possibilities but for there are multiple
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # I shape
        [[4, 5, 9, 10], [2, 6, 5, 9]], #J shape
        [[6, 7, 9, 10], [1, 5, 6, 10]],# L shape
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # T shape
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #S shape
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], #Z shape
        [[1, 2, 5, 6]], # O shape
    ]

    def __init__(self, x, y, type=None, rotation=0, color=None):
        self.x = x
        self.y = y
        self.type = type if type is not None else random.randint(0, len(self.figures) - 1)
        self.color = color if color is not None else random.randint(1, len(colors) - 1)
        self.rotation = rotation

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
        self.y = 50   # To center the grid on the y-axis on the Pygame window
        self.zoom = 20
        self.figure = None
        self.height = height  # The number of rows in the Tetris field
        self.width = width    # The number of columns in the Tetris field
        self.field = [[0 for _ in range(width)] for _ in range(height)]  # Initialize the playing field
        self.static_piece_color = colors[0]  # Color for the static piece (Black)

        # Attributes for the target grid
        self.target_grid_x = self.x + self.width * self.zoom + 200  # 200 pixels to the right of the main grid
        self.target_grid_y = self.y
        self.target_grid_width = 10  # Width of the target grid in blocks
        self.target_grid_height = 20  # Height of the target grid in blocks

        self.level_configurations = {
            1: {'pieces': [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)], 'target_pattern': self.generate_target_pattern(1)}, #Here we generate the square figure
            2: {'pieces': [(6, 0), (6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0),(6, 0)], 'target_pattern': self.generate_target_pattern(2)}, #The Chirstimas Tree
            3: {'pieces': [(5, 0),(2, 0),(1, 0),(5, 0),(5, 0),(4, 0),(3, 0),(4, 0),(3, 0)], 'target_pattern': self.generate_target_pattern(3)}, #Heart pattern
            4: {'pieces': [(3, 0),(4, 0),(3, 0),(4, 0),(3, 0),(4, 0),(3,0)], 'target_pattern': self.generate_target_pattern(4)}, 
            5: {'pieces': [(3, 0),(4, 0),(3, 0),(4, 0),(3, 0),(4, 0),(3,0)], 'target_pattern': self.generate_target_pattern(5)}, 
        }
        self.load_level(self.level)

# 0 I (0, 0) |  J (3, 0)|  L (4, 0)|  T (5, 0)|  S (2, 0) | Z (1, 0) | 0 (6, 0)|

    def load_level(self, level):
        # Reset the playing field
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        
        config = self.level_configurations[level]
        self.next_figures = [Figure(3, 0, type=p[0], rotation=p[1]) for p in config['pieces']]
        self.target_pattern = config['target_pattern']
        self.figure = None


    def generate_target_pattern(self, level):
        # Start with a base pattern of zeros
        pattern = [[0] * self.target_grid_width for _ in range(self.target_grid_height)]
        
        if level == 1:
            # Simple vertical line at column 4
                pattern = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
            ]
                
        elif level == 2:
                # Simple vertical line at column 4
                pattern = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
        
        elif level == 3:
            # Simple vertical line at column 4
                pattern = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            ]
                
        elif level == 4:
            # Simple vertical line at column 4
                pattern = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1], #L shape
            ]

        elif level == 5:
            # If you ve come to here and if you enjoyed the game feel free to give me a 6 :)
                pattern = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
            ]
        else:
            self.state == "game_over"

        return pattern


    def new_figure(self):
        if self.next_figures:
            self.figure = self.next_figures.pop(0)
        else:
            self.figure = None
            self.check_end_game()

    def draw_target_grid(self, screen):
        # Update the title to include the level number
        title = f"Level {self.level}"
        # Draw the title "Target Grid"
        font = pygame.font.SysFont('Calibri', 20, True, False)
        text_surface = font.render(title, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.target_grid_x + self.target_grid_width * self.zoom // 2, self.target_grid_y - 30))
        screen.blit(text_surface, text_rect)

        # Retrieve the current level's target pattern
        pattern = self.generate_target_pattern(self.level)

        # Draw the outline of the target grid and fill according to the pattern
        for i in range(self.target_grid_height):
            for j in range(self.target_grid_width):
                # Outline each cell
                pygame.draw.rect(screen, GRAY, [
                    self.target_grid_x + j * self.zoom,
                    self.target_grid_y + i * self.zoom,
                    self.zoom, self.zoom], 1)
                # Fill the cell if the pattern indicates a block should be there
                if pattern[i][j] == 1:
                    pygame.draw.rect(screen, self.static_piece_color, [
                        self.target_grid_x + j * self.zoom + 1,
                        self.target_grid_y + i * self.zoom + 1,
                        self.zoom - 2, self.zoom - 2])

            
    def check_end_game(self):
        if not self.next_figures and self.figure is None: # I think here we are checking if online there is no more pieces
            # Perform the comparison with the target pattern
            for y in range(self.height):
                for x in range(self.width):
                    if (self.field[y][x] > 0) != (self.target_pattern[y][x] > 0):
                        self.state = "gameover"
                        return
            self.score += 1
            self.level += 1
            if self.level <= len(self.level_configurations):
                self.load_level(self.level)
            else:
                self.state = "completed"



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
        for next_piece in self.next_figures[:3]:
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
        # Lock the tetromino in place, check lines, and load new piece
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[self.figure.y + i][self.figure.x + j] = self.figure.color
        self.break_lines()

        self.new_figure()  # Now checks if it should end the game after last piece


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


# Define a main function that will run the game
def main():

    # Import necessary Pygame library
    import pygame

    # Initialize the Pygame engine
    pygame.init()

    # Define color constants for easy reference
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    # Set the size of the window or screen for the game
    screen_size = (800, 600)
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
        text = font.render("Level: " + str(game.score), True, BLACK)
        screen.blit(text, [0, 0])

        if game.state == "gameover":
            font1 = pygame.font.SysFont('Calibri', 60, True, BLACK,)
            text_game_over = font1.render("Game Over", True, BLACK, )
            text_game_over1 = font1.render("Press esc & restart", True, BLACK,)
            screen.blit(text_game_over, [20, 100])
            screen.blit(text_game_over1, [25, 265])

        # Draw the target grid
        game.draw_target_grid(screen)

        # Update the display and maintain frame rate
        pygame.display.flip()
        clock.tick(fps)

    # Quit Pygame
    pygame.quit()

# This allows the script to be run as a standalone game as well
if __name__ == "__main__":
    main()