import pygame
import sys
import math

from hadleOverflow import overflow
from dataInput import Queue
from player1 import PlayerOne
from player2 import PlayerTwo

class Dropdown:
    def __init__(self, x, y, width, height, options):
        """
        Creates a dropdown menu for selecting options.
        Purpose: Allows the user to select player type and board size.
        Impact: The handle_event method updates the dropdown selection on mouse clicks,
                and get_choice returns the index of the currently selected option.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        """
        Draws the dropdown box and displays the currently selected option.
        """
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], True, BLACK)
        window.blit(text, (self.x + 5, self.y + 5))

    def handle_event(self, event):
        """
        Changes the dropdown menu selection on mouse clicks.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        """
        Returns the index of the currently selected option.
        Return: Index of the currently selected option in the dropdown menu.
        """
        return self.current_option

class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        """
        Manages the game board including its size and state.
        Purpose: Sets the board size and initializes its state, including player sprites.
        Impact: Prepares the board with initial values and player sprites.
        """
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height - 1][self.width - 1] = -1
        self.turn = 0

    def get_board(self):
        """
        Returns a copy of the current board state.
        Return: A copy of the board state.
        """
        return [row.copy() for row in self.board]

    def valid_move(self, row, col, player):
        """
        Checks if a move is valid for a given position and player.
        Return: True if the move is valid, False otherwise.
        """
        if 0 <= row < self.height and 0 <= col < self.width and (
                self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        """
        Adds a piece to the board if the move is valid.
        Return: True if the piece was added successfully, False otherwise.
        """
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            self.turn += 1
            return True
        return False

    def check_win(self):
        """
        Checks for win conditions and returns the winner.
        Return: 1 if player 1 wins, -1 if player 2 wins, 0 if no winner yet.
        """
        if self.turn > 0:
            num_p1 = num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif self.board[i][j] < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        """
        Handles overflow and reverts to a previous state if necessary.
        Return: Number of handled overflow steps.
        """
        oldboard = [row.copy() for row in self.board]
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps

    def set(self, newboard):
        """
        Sets the board to a new state.
        """
        self.board = [row.copy() for row in newboard]

    def draw(self, window, frame):
        """
        Draws the board and pieces on the screen.
        """
        for row in range(self.height):
            for col in range(self.width):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(window, BLACK, rect, 1)
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    sprite = self.p1_sprites if self.board[row][col] > 0 else self.p2_sprites
                    if abs(self.board[row][col]) == 1:
                        # Draw a single piece.
                        cpos += CELL_SIZE // 2 - 16
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        # Draw two pieces.
                        cpos += CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 3:
                        # Draw three pieces.
                        cpos += CELL_SIZE // 2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE // 2 - 32
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        # Draw four pieces.
                        cpos += CELL_SIZE // 2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE // 2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

# Constants
CELL_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_OFFSET = 0
Y_OFFSET = 100
FULL_DELAY = 5

def get_grid_size(choice):
    """
    Returns the board size based on the selected choice. => added feature we can select grid size as drowpdown menu selection
    Purpose: Allows the user to select the board size through the dropdown menu.
    Impact: Dynamically changes the board size by recreating the Board object based on the selected size.
    Return: A tuple representing the board size (rows, columns).
    """
    sizes = [(3, 4), (4, 5), (5, 6)]  # List of board sizes based on selection
    # sizes[0] = 3*4 board, sizes[1] = 4*5 board.... saved to matched later
    # should be continuously verified size matching : If not => result : forcely initialized every player turn
    return sizes[choice]

# Pygame initialization
pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.font.init()
font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 108)

# Initialize dropdown menus
player1_dropdown = Dropdown(900, 50, 200, 50, ['Human', 'AI'])
player2_dropdown = Dropdown(900, 110, 200, 50, ['Human', 'AI'])

"""
Purpose: Provide UI for defining board size drop-down menu and match grid.size selection
Shows the user a UI for selection and retrieves options for the grid associated with each selection from the Drawdown array.
"""
board_size_dropdown = Dropdown(900, 170, 200, 50, ['3x4', '4x5', '5x6'])
# added part of dropdown menu
# 3 part of selection : size 3*4 4*5 5*6 saved to array
# 3x4 UI selection automatically selected grid of size[0] so 3*4 board 
# returning board_size_dropdown which matching with GRID_SIZE later

# Initialize sprites, setting colour
p1spritesheet = pygame.image.load('img/green.png')
p2spritesheet = pygame.image.load('img/pink.png')
p1_sprites = [p1spritesheet.subsurface(pygame.Rect(32 * i, 0, 32, 32)) for i in range(8)]
p2_sprites = [p2spritesheet.subsurface(pygame.Rect(32 * i, 0, 32, 32)) for i in range(8)]

# Initialize board
grid_size_choice = 0
GRID_SIZE = get_grid_size(grid_size_choice)
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

# Initialize game variables
frame = 0
current_player = 0
status = ["", ""]
overflow_boards = Queue()
overflowing = False
numsteps = 0
has_winner = False
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]
player_id = [1, -1]  # Ensure player_id is defined here (player 1 = 1,2 = -1)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            player1_dropdown.handle_event(event)  # Handles (player 1's) dropdown menu events
            player2_dropdown.handle_event(event)  # Handles (player 2's) dropdown menu events
            board_size_dropdown.handle_event(event)  # Handles board size dropdown menu events
            choice[0] = player1_dropdown.get_choice()  # Gets (player 1's) choice
            choice[1] = player2_dropdown.get_choice()  # Gets (player 2's) choice
            new_grid_size_choice = board_size_dropdown.get_choice()  # Gets the selected board size
            new_grid_size = get_grid_size(new_grid_size_choice) # added Feature 2: To optimize drop-down menu options to selected items

            """
            Purpose: Check the selected board size through two-stage verification
            Functionalities: Adding this prevents inconsistencies with the temp grid in the function flow when initializing the grid.
            """
            if GRID_SIZE != new_grid_size: # added feature for fix error 1: If you match the size of the newly selected grid to put the game [row, col] into the grid, if it's the same, if it's returned, it's spires
            # draw grid size of drop down menu after player dropdown draw : configure repeatable iteration
            # matching new size = grid size selection
                GRID_SIZE = new_grid_size
                # Creates a new board with the selected size
                # New board matching with additional temp grid if it doesn't matched already
                board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y - Y_OFFSET
                col = x - X_OFFSET
                grid_row, grid_col = row // CELL_SIZE, col // CELL_SIZE

    # Check for win conditions
    win = board.check_win()
    if win != 0:
        has_winner = True
        winner = 1 if win == 1 else 2

    if not has_winner:
        if overflowing:
            status[0] = "Overflowing"
            if not overflow_boards.is_empty():
                if numsteps == FULL_DELAY:
                    next_board = overflow_boards.dequeue()
                    board.set(next_board)
                    numsteps = 0
                else:
                    numsteps += 1
            else:
                overflowing = False
                current_player = (current_player + 1) % 2
        else:
            status[0] = f"Player {current_player + 1}'s turn"
            make_move = False
            if choice[current_player] == 1:  # AI player
                grid_row, grid_col = bots[current_player].get_play(board.get_board())
                status[1] = f"Bot chose row {grid_row}, col {grid_col}"
                if not board.valid_move(grid_row, grid_col, player_id[current_player]):
                    has_winner = True
                    winner = ((current_player + 1) % 2) + 1
                else:
                    make_move = True
            else:  # Human player
                if board.valid_move(grid_row, grid_col, player_id[current_player]):
                    make_move = True

            if make_move:
                board.add_piece(grid_row, grid_col, player_id[current_player])
                numsteps = board.do_overflow(overflow_boards)
                if numsteps != 0:
                    overflowing = True
                    numsteps = 0
                else:
                    current_player = (current_player + 1) % 2
                grid_row = -1
                grid_col = -1

    # Draw all elements on the screen
    window.fill(WHITE)
    board.draw(window, frame)
    window.blit(p1_sprites[math.floor(frame)], (850, 60))
    window.blit(p2_sprites[math.floor(frame)], (850, 120))
    frame = (frame + 0.5) % 8
    player1_dropdown.draw(window)  # Draws the (player 1) dropdown menu 
    player2_dropdown.draw(window)  # Draws the (player 2) dropdown menu
    
    """
    Purpose: Call the dropdown menu with a player size draw followed by a board size draw.
    Functioalities: By adding this, grid size discrepancy is prevented after gem selection each player turn.
    """
    board_size_dropdown.draw(window)  # Draws the board size dropdown menu => 
    #added feature for fix error 2 : there was Fixed an issue that disappeared immediately after the player entered the gem because the grid size was inconsistent
    #draw grid size of drop down menu after player dropdown draw : configure repeatable iteration
    #matching new size = grid size selection

    if not has_winner:
        text = font.render(status[0], True, BLACK)
        window.blit(text, (X_OFFSET, 750))
        text = font.render(status[1], True, BLACK)
        window.blit(text, (X_OFFSET, 700))
    else:
        text = bigfont.render(f"Player {winner} wins!", True, BLACK)
        window.blit(text, (300, 250))

    pygame.display.update()
    pygame.time.delay(100)

pygame.quit()
sys.exit()
