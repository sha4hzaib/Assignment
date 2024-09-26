import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")

# Fonts for displaying text
font = pygame.font.SysFont(None, 36)

# Function to draw the Tic-Tac-Toe grid
def draw_grid():
    screen.fill(BG_COLOR)
    # Horizontal lines
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw the X and O symbols on the board
def draw_symbols(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                         int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

# Function to check for a winner or if the game is a draw
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    if all(cell != " " for row in board for cell in row):
        return "Draw"

    return None

# Function to get the available moves on the board
def available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move[0]][move[1]] = "X"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move[0]][move[1]] = " "
            best_score = max(score, best_score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move[0]][move[1]] = "O"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move[0]][move[1]] = " "
            best_score = min(score, best_score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

# Function for the AI to find the best move
def best_move(board):
    best_score = -math.inf
    move = None
    for i, j in available_moves(board):
        board[i][j] = "X"
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[i][j] = " "
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

start_time = time.perf_counter()
end_time = time.perf_counter()

# Main function to play the game
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    running = True
    player_turn = True

    draw_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE

                if board[clicked_row][clicked_col] == " ":
                    board[clicked_row][clicked_col] = "O"
                    player_turn = False
                    draw_symbols(board)
                    pygame.display.update()

                    if check_winner(board):
                        draw_symbols(board)
                        pygame.display.update()
                        pygame.time.delay(500)
                        running = False
                        break

        if not player_turn and running:
            ai_move = best_move(board)
            if ai_move:
                board[ai_move[0]][ai_move[1]] = "X"
                player_turn = True
                draw_symbols(board)
                pygame.display.update()

                if check_winner(board):
                    draw_symbols(board)
                    pygame.display.update()
                    pygame.time.delay(500)
                    running = False
                    break

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    play_game()
    pygame.quit()
    print(f"Time taken: {end_time - start_time:.10f} seconds")
