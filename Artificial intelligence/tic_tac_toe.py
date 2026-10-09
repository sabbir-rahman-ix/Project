import math


def print_board(board):
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")
        if i < 6:
            print("--+---+--")
    print()


def check_winner(board, player):

    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[pos] == player for pos in combo) for combo in winning_combinations)


def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == " "]


def is_board_full(board):
    return " " not in board


def evaluate_board(board):

    if check_winner(board, "O"):
        return 10
    if check_winner(board, "X"):
        return -10
    return 0


def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate_board(board)
    if score != 0:
        return score - depth if score > 0 else score + depth

    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = " "
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score

    best_score = math.inf
    for move in get_available_moves(board):
        board[move] = "X"
        score = minimax(board, depth + 1, True, alpha, beta)
        board[move] = " "
        best_score = min(best_score, score)
        beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_score


def get_best_move(board):
    best_score = -math.inf
    best_move = None

    for move in get_available_moves(board):
        board[move] = "O"
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = " "

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def play_game():
    board = [" "] * 9
    current_player = "X"

    print("Welcome to Tic-Tac-Toe")
    print("You are X. The computer is O.")
    print("Choose a number from 1 to 9 based on the board positions below:")
    print("1 | 2 | 3")
    print("--+---+--")
    print("4 | 5 | 6")
    print("--+---+--")
    print("7 | 8 | 9")
    print()

    while True:
        print_board(board)

        if current_player == "X":
            try:
                move = int(input("Your turn. Enter a position (1-9): ")) - 1
            except ValueError:
                print("Please enter a valid number.")
                continue

            if move not in range(9) or board[move] != " ":
                print("That position is not available. Try again.")
                continue

            board[move] = "X"
        else:
            print("Computer is thinking...")
            move = get_best_move(board)
            board[move] = "O"
            print(f"Computer chose position {move + 1}")

        if check_winner(board, "X"):
            print_board(board)
            print("You win!")
            break

        if check_winner(board, "O"):
            print_board(board)
            print("Computer wins!")
            break

        if is_board_full(board):
            print_board(board)
            print("It is a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    play_game()