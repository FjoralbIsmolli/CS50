"""
Tic Tac Toe Player
"""

import math

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
    xs = sum(row.count(X) for row in board)
    os = sum(row.count(O) for row in board)

    return X if xs == os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.append((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy
    new_board = copy.deepcopy(board)
    
    curr_player = player(new_board)
    # print(f"Initial: {board}, action: {action}, player: {curr_player}")
    valid_actions = actions(new_board)
    if action not in valid_actions:
        raise ValueError("Invalid Move ...")
    new_board[action[0]][action[1]] = curr_player
    # print(f"Resultant board:   {board}\n")
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    n = len(board)
    for pl in [X, O]: 
        # horizonal
        for i in range(n):
            if all([x == pl for x in board[i]]):
                return pl
        # vertical
        for j in range(n):
            col = [board[i][j] for i in range(n)]
            if all([x == pl for x in col]):
                return pl
        # main diagonal
        if all([board[i][i] == pl for i in range(n)]):
            return pl
        # other diagonal
        if all([board[i][n-i-1] == pl for i in range(n)]):
            return pl

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] is EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_pl = winner(board)
    if winner_pl == X:
        return 1
    if winner_pl == O:
        return -1
    return 0


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = - math.inf
    best_act = None
    for action in actions(board):
        min_val, _ =  min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_act = action
    return v, best_act


def min_value(board):
    if terminal(board):
        return utility(board), None
    
    v = math.inf
    best_act = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_act = action
    return v, best_act


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    curr_player = player(board)
    if curr_player == X:
        _, best_act = max_value(board)
    elif curr_player == O:
        _, best_act = min_value(board)
    return best_act
