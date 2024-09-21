"""
Tic Tac Toe Player
"""
import copy
import math
import sys

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
    count_x, count_o = 0, 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == X:
                count_x += 1
            if board[row][col] == O:
                count_o += 1
    return O if count_x > count_o else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_pos = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                actions_pos.append((row, col))
    return actions_pos


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    move = player(board)
    row = action[0]
    col = action[1]
    # row, col = action
    new_board = copy.deepcopy(board)
    if new_board[row][col] != EMPTY:
        raise Exception("infeasible move")
    new_board[row][col] = move
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return board[2][0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0


def max_choice(v):
    return v.index(max(v))


def min_choice(v):
    return v.index(min(v))


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)
    # all possible action this player can take
    actions_pos = actions(board)
    v = []
    if turn == X:
        for action in actions_pos:
            # all min value choices opponent would take
            v.append(min_value(result(board, action)))
        # print("v = ", v)
        # return the best choice I would take
        return actions_pos[max_choice(v)]
    if turn == O:
        for action in actions_pos:
            v.append(max_value(result(board, action)))
        # print("v = ", v)
        return actions_pos[min_choice(v)]


def min_value(board):
    # print(f"min_value = {board}")
    if terminal(board):
        return utility(board)
    v = sys.maxsize
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    # print(f"max_value = {board}")
    if terminal(board):
        return utility(board)
    v = -sys.maxsize - 1
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
