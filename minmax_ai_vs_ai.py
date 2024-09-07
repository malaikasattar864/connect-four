# -*- coding: utf-8 -*-
"""MINMAX- AI Vs AI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pjo-KDfXX0PER7LrP4zOkvlh1xdxvdiT

#Introduction to Artificial Intellingence - Lab MidTerm

###Malaika Sattar FA22-BAI-021
###Sheeza Tanveer FA22-BAI-037

The game we chose is Connect-Four. Connect Four is a two-player, abstract strategy game that is played on a grid. The objective of the game is to be the first player to connect four of their own discs in a row, either horizontally, vertically, or diagonally, within the grid.

##Alpha-Beta Pruning (Min-Max) on Connect-Four - AI VS AI

Firstly, import the necessary libraries required for the implementation. Numpy for mathematical opertaion involving arrays, random for generating random numbers and math for mathematical function
"""

import numpy as np
import math
import random

"""The rows and coulmns of the board are initialized to with values 6 and 7 respectively, since connect four is played on a 6X7 board."""

ROWS = 6
COLS = 7

"""Some other variables are initialized, AI X is given the value 0 and AI O turn is given the value 1. AI X game piece is given the value 1 and AI O's game piece is given the value 2."""

AIX_TURN = 0
AIO_TURN = 1
AIX_PIECE = 1
AIO_PIECE = 2

"""Using the above defined variables ROWS and COL an empty game board is created using the numpy library with the data type integer."""

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

"""This is the function for placing a game piece on the board. The function takes four parameters:
*   board: represents the game board
*   row: specifies the row where the piece should be placed on the board
*   col: specifies the column where the piece should be placed on the board
*   piece: represents the game piece that will be placed on the board
"""

def drop_piece(board, row, col, piece):
    board[row][col] = piece

"""This function is used to check if it's valid to place a game piece in a specific column on the game board. The function takes two parameters:
*   board: represents the game board
*   col: specifies the column that you want to check for validity

It checks if the value in the first row (row 0) of the specified column on the game board is equal to 0. If the value is 0, it means that the column is not yet full, and it is valid to place a game piece in that column.


"""

def is_valid_location(board, col):
    return (board[:, col] == 0).any()

""" This function is used to find the next available row in a specific column on a game board where you can place a game piece. it takes board and col again as parameters. The loop iterates through each rown and as soon as an empty row is found it returns the value of that row."""

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

"""This function is used to check if a particular game piece has formed a winning combination on the game board. The code checks for four different ways to win:
 horizontally, vertically, and diagonally up right and down right.
"""

def winning_move(board, piece):
    for c in range(COLS - 3): #checks for horizontal winning combinations
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLS):
        for r in range(ROWS - 3): #checks for vertical winning combinations
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLS - 3):
        for r in range(3, ROWS): #checks for diagonal winning combinations from the bottom left to the top right
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    for c in range(3, COLS):
        for r in range(3, ROWS): #checks for diagonal winning combinations from the bottom right to the top left
            if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece:
                return True

"""This function is used to evaluate a window or subset of a game board for a specific game piece. It assigns a score to the window based on the presence of pieces and empty spaces. The function takes two parameters window and the piece."""

def evaluate_window(window, piece):
    opponent_piece = AIX_PIECE if piece == AIO_PIECE else AIO_PIECE #determines the opponent's game piece based on the provided piece
    score = 0 #score initialized to zero
    if window.count(piece) == 4: #if four consecutive game pieces, 100 is added tos score
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1: #if three consecutive game pieces and 1 empty it adds 5 to score
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2: #if two consecutive game pieces and 2 empty it adds 2 to score
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1: #if three consecutive opponent's game pieces and 1 empty it subtracts 4 from score
        score -= 4
    return score

"""This function is used to evaluate the overall score of a game board position for a specific game piece. It starts by examining the central column to determine the presence of the specified piece and rewards the particular AI for having more of its pieces in the center. Next, it evaluates the board in all directions, including rows, columns, and diagonals, by creating 4-cell "windows" and passing them to the evaluate_window function. The evaluate_window function assesses each window, considering the number of consecutive pieces of the specified type and empty spaces, and adjusts the score accordingly."""

def score_position(board, piece):
    score = 0 #initializes score to zero
    center_array = [int(i) for i in list(board[:,COLS//2])] #extracts the central column of the game board and converts it into a list of integers
    center_count = center_array.count(piece)
    score += center_count * 6 #updates score
    for r in range(ROWS): #iteratates through each row
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    for c in range(COLS): #iteratates through each column
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS): #iteratates through up-right diagonal
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(3, COLS): #iteratates through down-right diagonal
            window = [board[r - i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

"""This is used to determine whether the terminal state of the game is reached or not."""

def is_terminal_node(board):
    return winning_move(board, AIX_PIECE) or winning_move(board, AIO_PIECE) or len(get_valid_locations(board)) == 0
     #checks if the player has made a winning move on the game board
     #checks if the AI has made a winning move on the game board
     #checks if there are no valid locations left on the game board to make a move

"""This is the chunk of code where the main alpha-beta pruning algorithm is implemented. The algorithm helps the AI choose it's best move so that it wins the game.The function takes several parameters including the board, depth (current depth or level of the search tree), alpha (the best score that the (AI) can guarantee from the explored options), beta (the best score that the opponenet can guarantee from the explored options), and the maximizing_player (indicates whther AI is opponent or is the human)."""

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board) #calls the is_terminal_move function
    if depth == 0 or is_terminal: #checks if depth is zero or is terminal state reached
        if is_terminal:
            if winning_move(board, AIO_PIECE): #if the game is won by AI, it returns a high positive score
                return (None, 10000000)
            elif winning_move(board, AIX_PIECE): #f the game is won by the opponent, it returns a high negative score
                return (None, -10000000)
            else: #if no one has won it returns zero
                return (None, 0)
        else:
            return (None, score_position(board, AIO_PIECE))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations: #explores possible moves
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AIO_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value: #evaluates them
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value #returns the column index and the maximum score
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AIX_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value

"""The function checks and returns the valid oves an AI can do on the game board. The working of the function is easy."""

def get_valid_locations(board):
    valid_locations = [] #initializes an empty list to estore the locations
    for column in range(COLS): #iterates through each row and column
        if is_valid_location(board, column):
            valid_locations.append(column)
    return valid_locations

"""This method prints the current state of the game board using dashes. X'S and O's. It also prints the column number making it easier to understand the game."""

def print_board(board): #displays the current state of the game board
    for r in range(ROWS): #iterates thorugh each row
        for c in range(COLS): #iterates thorugh each column
            if board[r][c] == 0:
                print(" - ", end="")
            elif board[r][c] == AIX_PIECE:
                print(" X ", end="")
            else:
                print(" O ", end="")
        print("")
    print(" 0  1  2  3  4  5  6 ")
    print("\n")

"""This is the function whether the game is over or not."""

def end_game():
    global game_over #a global variable game_over is initialized
    game_over = True #the value is set to true

"""This piexe of code initializes several variables to set up the initial state of a game."""

board = create_board() #calls the create_board function to set up the baord
game_over = False #the game_over variable is set to false
not_over = True #this mean that the game is started
turn = random.randint(AIX_TURN, AIO_TURN) #randomly selects who will do the first move

"""This code first has print statements that print the prompt explaining the game rules. It then has main loop that allows players  to take turns in a game. The game loop continues until the game_over is set to True, indicating that the game has ended."""

print("Welcome to Connect 4!")
print("The goal of the game is to connect four of your pieces either horizontally, vertically, or diagonally.")
print("You will play as 'X', and the AI will play as 'O'.")
print("To make a move, enter the column number (0-6) where you want to drop your piece.")
print("Let's start the game!")
while not game_over: #loop that continues as long as the game_over variable is False
    if turn == AIX_TURN and not_over: #AI X'ss turn
        print("AI X's Turn")
        colX, minimax_scoreX = minimax(board, 5, -math.inf, math.inf, True) #gets the AI X's move using the alpa-beta pruning function
        if is_valid_location(board, colX).any(): #if it is a valid move
            rowX = get_next_open_row(board, colX)
            drop_piece(board, rowX, colX, AIX_PIECE) #it places the move on the game board
            if winning_move(board, AIX_PIECE): #checks if winning move is reached
                print("AI X WINS!")
                print_board(board)
                game_over = True
                not_over = False
                break
            print_board(board)
            turn = AIO_TURN #switches turn to AI O
    elif turn == AIO_TURN and not game_over and not_over: #AI O's turn
        print("AI O's Turn")
        colO, minimax_scoreO = minimax(board, 5, -math.inf, math.inf, True) #gets the AI's move using the alpa-beta pruning function
        if is_valid_location(board, col).any(): #if it is a valid move
            rowO = get_next_open_row(board, colO)
            drop_piece(board, rowO, colO, AIO_PIECE) #it places the move on the game board
            if winning_move(board, AIO_PIECE): #checks if winning move is reached
                print("AI O WINS!")
                print_board(board)
                game_over = True
                not_over = False
                break
            print_board(board)
            turn = AIX_TURN #switches turn to AI X