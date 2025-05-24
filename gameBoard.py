from hadleOverflow import overflow
from dataInput import Queue

"""
Definition: A function that clones a given board and returns a new board.

Parameters:
board: The board to clone. A two-dimensional list where each row is represented as a list.

Returns:
list of lists: A deep clone of the given board. A new two-dimensional list with the same structure as the original board.
"""
def copy_board(board):
    # Create an empty list to store the cloned boards.
    current_board = []
    
    # Find the height (number of rows) of the board.
    height = len(board)

    # Duplicate each row and add it to current_board.
    for i in range(height):
        current_board.append(board[i].copy())

    # return duplicate board
    return current_board

"""
Definition: A function that evaluates a given board and returns the current player's score.

Parameters:
board : A two-dimensional list representing the board state. The value of each cell represents a player's score.
current_player (int): An integer representing the current player. It can be 1 or -1.

Return Value:
float: The current player's score.
"""
def evaluate_board(board, current_player) -> float:    
    # Initialize initial score and vertical bonus point 
    player1_score = 0  # player1 score
    player2_score = 0  # player2 score
    player1_vertical_bonus = 0  # Vertical bonus points for player 1
    player2_vertical_bonus = 0  # Vertical bonus points for player 1

    num_rows = len(board)  # row num of board 
    num_cols = len(board[0])  # col num of board

    # Calculate player score based on the each cell
    for row in board:  
        for cell in row:  
            if cell > 0: # if cell value is positive, add player1 score
                player1_score += cell  
            elif cell < 0: # if cell value is negative, add player2 score
                player2_score -= cell  

    # Check three consecutive vertical cells and calculate bonus points
    for col in range(num_cols):  
        consecutive_player1 = 0  # Player 1 consecutive cell counter
        consecutive_player2 = 0  # Player 2 consecutive cell counter
        for row in range(num_rows): 
            cell = board[row][col]  
            if cell > 0:
                consecutive_player1 += 1 # Player 1 cell consecutive counter increases
                consecutive_player2 = 0  # Player 2 cell consecutive counter reset
            elif cell < 0:
                consecutive_player2 += 1 # Player 2 cell consecutive counter increases
                consecutive_player1 = 0  # Player 2 cell consecutive counter reset
            else:                        # Reset counter if cell is empty      
                consecutive_player1 = 0  
                consecutive_player2 = 0  

            # Bonus points added when there are 3 or more consecutive cells
            if consecutive_player1 >= 3:
                player1_vertical_bonus += 100  # Add bonus 100 to player 1
                consecutive_player1 = 0  # Counter reset after bonus
            if consecutive_player2 >= 3:
                player2_vertical_bonus += 100  # Add bonus 100 to player 2
                consecutive_player2 = 0  # Counter reset after bonus

    # Calculate the total value of non-empty cells
    total_value = player1_score + player2_score  

    # Calculating each player's weighted score on a non-empty board
    if total_value != 0:
        player1_score = (player1_score / total_value) + player1_vertical_bonus  
        player2_score = (player2_score / total_value) + player2_vertical_bonus  

    # Returns the current player's score
    return player1_score if current_player == 1 else player2_score  

class GameTree:
    """
    Definition: A constructor function that initializes a node.

    Parameters:
    board (list): A two-dimensional list representing the board state represented by the node.
    depth (int): An integer representing the depth or level of the node.
    player (int): An integer representing the player currently playing at the node. Typically 1 or -1.
    tree_height (int): An integer representing the maximum height of the tree. The default value is 4.
    """
    class Node:
        #initialize the node
        def __init__(self, board, depth, player, tree_height = 4):
            self.board = board
            self.depth = depth
            self.player = player
            self.tree_height = tree_height
            self.children = []

    """
    Definition: A constructor function that initializes the root node of the game tree and sets the initial game state.

    Parameters:
    board (lists): A two-dimensional list representing the initial board state.
    player (int): An integer representing the current player. Typically 1 or -1.
    tree_height (int): An integer that sets the maximum depth of the tree. The default is 4.
    """
    def __init__(self, board, player, tree_height = 4):
        self.player = player            # current player.
        self.board = copy_board(board)  # initial board state
        self.tree_height = tree_height  # maximum depth of the tree
        self.root = self.Node(self.board, 0, self.player, self.tree_height) #Creates and stores the root node of the tree
        self.board_list = [self.root] # A list that stores all the nodes of the tree
        self.winning_row = None       # index of the winning row
        self.winning_col = None       # index of the winning_col row
        self.initialize_tree(self.root) # index of the winning_col row
        self.grid_move = []             # list of possible moves
        self.counter = 0                # counter variable

    """
    Definition: initializes a game tree from a given node. creates child nodes and recursively initializes the tree for the child nodes.

    Parameters:
    node:Start node from which to initialize the tree. 
    This node contains information such as the current game state, the player, and the depth of the tree.
    """
    def initialize_tree(self, node):    
        active_player = node.player
        opponent_player = -active_player

        # End when the game is over or the depth of the node is greater than or equal to the tree height.
        if self.is_game_over(node.board, active_player) or node.tree_height <= node.depth:
            return

        # Find possible moves on the current board
        possible_moves = self.find_adjacent_neighbors(node.board, node.player)
        # Sets the first element in the possible moves to be a child node.
        node.children = possible_moves[0]
                
        i = 0
        # Initialize the tree recursively on all child nodes
        while i < len(node.children):
            move = node.children[i]
            # Creates a new child node based on the current movement.
            child_node = self.Node(move, node.depth + 1, opponent_player, self.tree_height)
            
            # Adds a new child node to the board list.
            self.board_list.append(child_node)
            # Initializes the tree for child nodes.
            self.initialize_tree(child_node)
            i += 1
            
    """
    Definition: Find possible moves for a player on a given board and checks whether there is a move that the player can win.

    Parameters:
    board (list): A two-dimensional list representing the current game board. 
    player (int): An integer representing the current player. Positive for player 1, negative for player 2.

    Return Values:
    valid_move_list (list): A list containing the board state after performing a valid move. 
    winning_row (int): The row index of a move that the current player can win. 
    winning_col (int): The column index of a move that the current player can win. 
    move_position_list (list of tuples): positions of valid moves. (row index, column index).
    """
    def find_adjacent_neighbors(self, board, player):
        # size of the rows and columns on the board
        rows, cols = len(self.board), len(self.board[0])

        def count_adjacent_cell(row, col):
            # Define the directions
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
            neighbor_cell = 0

            for dr, dc in directions:
                r, c = row + dr, col + dc
                # Check if given coordinates are within the board's bounds
                if 0 <= r < rows and 0 <= c < cols:
                    neighbor_cell += 1

            return neighbor_cell

        def can_player_play_here(board, row, col, player):
            # Specific cell values ​​on the board
            board_row = board[row]
            board_cell = board_row[col]

            # Counts the number of adjacent cells for a given cell.
            adjacent_cell_count = count_adjacent_cell(row, col)

            # Player1 positive, Player2 negative
            if player > 0:
                player_sign = 1
            else:
                player_sign = -1

            # If the cell is empty, move it
            if board_cell == 0:
                return True

            # If the player's symbol and the cell's symbol are different, movement is not possible.
            if (player > 0 and board_cell < 0) or (player < 0 and board_cell > 0):
                return False

            # If the symbol in the cell is the same as the player symbol and there are enough adjacent cells, you can move.
            if board_cell * player_sign > 0 and abs(board_cell) < adjacent_cell_count:
                return True

            return False

        valid_move_list = []
        winning_row = None
        winning_col = None
        move_position_list = []

        # Iterate through each cell on the board to see if the player has a valid move.
        i = 0
        while i < rows and winning_row is None:
            for j in range(cols):
                # Check if the player can make a move at position
                if can_player_play_here(board, i, j, player):
                    # Copy the current board state to make changes
                    new_board = copy_board(board)

                    # Update the board with the player's move
                    new_board[i][j] += player

                    # Record the position of the move
                    move_position_list.append((i, j))

                    # Apply overflow logic to the board
                    self.overflow_board(new_board)

                    # Add the valid move to the list
                    valid_move_list.append(copy_board(new_board))

                    # Check if the move resulted in a game win condition
                    if self.is_game_over(new_board, player):
                        # Record the win move
                        winning_row, winning_col = i, j
                        # Exit the loop as a win move
                        break
            i += 1

        return valid_move_list, winning_row, winning_col, move_position_list

    """
    Definition: Determines and returns the optimal move from the current state. It uses an alpha-beta pruning algorithm to find the optimal number.

    Parameters:
    None

    Return Value:
    tuple or None:
    - (int, int): A tuple representing the optimal move location. It is in the format (row index, column index).
    - None: Returns if the optimal move is not found.
    """
    def get_move(self):        
        # Initial values ​​for alpha-beta pruning
        alpha = -float('inf')
        beta = float('inf')
        result_move = None

        # Initialize player optimal values
        if self.player == 1:
            best_value = -float('inf')
        else:
            best_value = float('inf')
                    
        # set current node is root node
        curr_node = self.root

        # Find adjacent cells, get the winning row and column, and move position
        result = self.find_adjacent_neighbors(self.board, self.player)
        winning_row = result[1]
        winning_col = result[2]
        move_position = result[3]

        # Returns the cell position where a win is possible
        if winning_row is not None:
            return winning_row, winning_col

        # Get the list of children of the current node
        children_list = list(curr_node.children)
        index = 0

        while index < len(children_list):
            child = children_list[index]
            # Calculate the moving value by evaluating the Min-Max algorithm
            move_value = self.min_max_evaluation(child, alpha, beta, self.player * -1, 1)
            
            # Update optimal movement values ​​based on the current player's maximization/minimization criteria.
            if (self.player == 1 and move_value > best_value) or (self.player == -1 and move_value < best_value):
                best_value = move_value
                result_move = child

            index += 1

        # If the optimal move is found, return the move location.
        if result_move is not None:
            counter = 0
            for child in curr_node.children:
                if result_move == child:
                    break
                counter += 1

            # Return the move position
            return_row, return_col = move_position[counter]

            return return_row, return_col

        # return None if there is no optimal move
        return None

    """
    Definition: Computes the optimal evaluation value for the current board state using the Min-Max algorithm. 

    Parameters:
    board (list): A two-dimensional list representing the current game board state.
    alpha (float): The maximum optimized value so far. The initial value is negative infinity.
    beta (float): The minimum optimized value so far. The initial value is positive infinity.
    player (int): A value representing the current player. Player 1 is represented as 1, and Player 2 is represented as -1.
    depth (int): The depth in the current tree.

    Return Value:
    float: The optimal evaluation value for the current board state.
    """
    def min_max_evaluation(self, board, alpha, beta, player, depth):
        # Returns the evaluation value (tree maximum height or current depth = tree maximum height or game end)
        if self.tree_height == 0 or depth >= self.tree_height or self.is_game_over(board, player):
            return self.evaluate_min_max(board, player)

        # Check if the current player is a maximized player or a minimized player
        is_maximizing_player = self.check_player(player)

        # Player1 initialized to negative infinity, Player2 initialized to positive infinity
        best_value = -float('inf') if is_maximizing_player else float('inf')

        # Find possible moves given the current board state
        possible_moves = self.find_adjacent_neighbors(board, player)[0]

        # Sort possible moves by evaluation value
        possible_moves.sort(key=lambda move: self.evaluate_move(move, player), reverse=is_maximizing_player)

        # Repeat for possible moves
        for move in possible_moves:
            # Recursively calculate the evaluation values ​​of child nodes
            eval = self.min_max_evaluation(move, alpha, beta, -player, depth + 1)
            if is_maximizing_player:
                # If maximizing player, update best_value
                best_value = max(best_value, eval)
                # update alpha
                alpha = max(alpha, best_value)
            else:
                # If minimizing player, update best_value
                best_value = min(best_value, eval)
                # update alpha
                beta = min(beta, best_value)

            # Pruning is performed if the alpha value is greater than or equal to the beta value.
            if beta <= alpha:
                break

        return best_value
    
    """
    Definition: Estimates the value of a given move. 

    Parameters:
    move (list): A two-dimensional list of board states after the move to be evaluated.
    player (int): An integer representing the current player (1 or -1).

    Return Value:
    float: A floating-point value representing the value of a given move.
    """
    def evaluate_move(self, move, player):       
        # Value estimation function
        return self.evaluate_min_max(move, player)

    """
    Definition: Create a queue to process the board state, and pass the current board state and the queue to the overflow function to process the board.

    Parameters:
    board (list): A two-dimensional list representing the current game board state.

    Return Value:
    None
    """
    def overflow_board(self, board):
        # Create a queue to process board states.
        overflow_queue = Queue()
        # Call the verflow function to process the queue and board state.
        overflow(board, overflow_queue)

    """
    Definition: Returns a boolean value, evaluating whether the game is over based on the given board state and players.

    Parameters:
    board (list): A two-dimensional list representing the current game board state.
    player (int): An integer representing the current player. Usually 1 or -1.

    Return Value:
    bool: Returns True if the game is over, False otherwise.
    """
    def is_game_over(self, board, player) -> bool:
        # Returns whether the game ends by evaluating whether the player won.
        return evaluate_board(board, player) == 1

    """
    Definition: Returns a boolean value, checking if the given player is player 1.

    Parameters:
    player (int): An integer representing the player to check. Usually expressed as 1 or -1.

    Return Value:
    bool: Returns True if the given player is 1, otherwise False.
    """
    def check_player(self, player: int) -> bool:
       return player == 1

    """
    Definition: Computes an evaluation value for a given board state and player, and returns it multiplied by the player's preference.

    Parameters:
    board (list): A two-dimensional list representing the board states to evaluate.
    player (int): An integer representing the current player. Typically expressed as 1 or -1.

    Return Value:
    float: Returns the result of multiplying the evaluated board state by the current player's preference. 
    """
    def evaluate_min_max(self, board: list, player: int) -> float:
        return evaluate_board(board, player) * player

    """
    Definition: A function that prints a given board state to the console.

    Parameters:
    board (list): A two-dimensional list representing the board states to print.

    Return Value:
    None:
    """
    def display_board(self, board):       
        for row in board:
            print(' '.join(map(str, row)))
        print()

    """
    Definition: A function that outputs a tree structure with a given node and its children.

    Parameters:
    node (Node): The node of the tree to output. Each node contains a depth, a player, a board state, and children.
    indent (str): A string to add indentation according to the depth of the node when outputting. The default is an empty string.

    Return Value:
    None
    """
    def display_tree(self, node, indent=""):
        # print depth and player information of the current node.
        print("Depth: {}, Player: {}".format(node.depth, node.player))

        # Print the board status of the current node
        self.display_board(node.board)

        # Recursively print child nodes
        for child in node.children:
            self.display_tree(child, indent + "    ")
        
    """
    Definition: A function that recursively cleans up all nodes in a tree. 
                This function frees up the memory by freeing resources including the node's child nodes and the board.

    Parameters:
    None

    Return Value:
    None
    """
    def clear_tree(self):
        # helper method
        def clear_node(node):
            stack = [node]
            
            while stack:
                current = stack.pop()
                # Process by adding the children of the current node to the stack.
                stack.extend(current.children)
                # Initialize properties of current node
                current.children = []
                current.board = None
        
        # Root node clear
        if self.root:
            clear_node(self.root)
        
        # Initialize root and board_list
        self.root = None
        self.board_list = []    