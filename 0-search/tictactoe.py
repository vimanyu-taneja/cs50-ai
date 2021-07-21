"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0

    for row in board:
        X_count += row.count(X)
        O_count += row.count(O)

    if X_count <= O_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row_index, row in enumerate(board):
        for column_index, item in enumerate(row):
            if item == None:
                possible_actions.add((row_index, column_index))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    player_move = player(board)

    new_board = copy.deepcopy(board)
    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player_move

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):

        # Check vertical columns for three in a row
        for row in board:
            if row == [player] * 3:
                return player

        # Check horizontal rows for three in a row
        for i in range(3):
            column = [board[x][i] for x in range(3)]
            if column == [player] * 3:
                return player
        
        # Check diagonals for three in a row
        if [board[i][i] for i in range(0, 3)] == [player] * 3:
            return player

        elif [board[i][~i] for i in range(0, 3)] == [player] * 3:
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If a player has won the game, then return True
    if winner(board) != None:
        return True

    # If there are any moves still possible, then return False 
    for row in board:
        if EMPTY in row:
            return False

    # If there are no more possible moves, then return True
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    player_who_won = winner(board)
    if player_who_won == X:
        return 1
    if player_who_won == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def calculate_max_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = -100
            for action in actions(board):
                min_value = calculate_min_value(result(board, action))[0]
                if min_value > v:
                    v = min_value
                    optimal_move = action
            return v, optimal_move

    def calculate_min_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = 100
            for action in actions(board):
                max_value = calculate_max_value(result(board, action))[0]
                if max_value < v:
                    v = max_value
                    optimal_move = action
            return v, optimal_move

    current_player = player(board)

    if terminal(board):
        return None
    if current_player == X:
        return calculate_max_value(board)[1]
    else:
        return calculate_min_value(board)[1]
