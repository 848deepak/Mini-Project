import random
import tkinter as tk
from tkinter import messagebox, simpledialog  


board = [' ' for _ in range(9)]

def is_winner(player):
    """Check if the current player has won the game."""
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                      (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                      (0, 4, 8), (2, 4, 6)]            
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def is_draw():
    """Check if the game is a draw."""
    return ' ' not in board

def minimax(is_maximizing):
    """Minimax algorithm to find the best move for the AI."""
    if is_winner('O'):
        return 1  # AI wins
    elif is_winner('X'):
        return -1  # Human wins
    elif is_draw():
        return 0  # Draw

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'  
                score = minimax(False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'  
                score = minimax(True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def get_ai_move(difficulty):
    """Determine AI's move based on the selected difficulty."""
    if difficulty == 'easy':
       
        available_moves = [i for i in range(9) if board[i] == ' ']
        return random.choice(available_moves)
    else:
    
        best_move = None
        best_score = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(False)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

def make_move(position, player):
    """Make a move on the board and update the GUI."""
    if board[position] == ' ':
        board[position] = player
        buttons[position].config(text=player, state="disabled",
                                 disabledforeground='blue' if player == 'X' else 'red')
        return True
    return False

def check_game_over():
    """Check if the game is over and display the result."""
    if is_winner('X'):
        messagebox.showinfo("Result", "Congratulations! You win!")
        window.destroy()
    elif is_winner('O'):
        messagebox.showinfo("Result", "AI wins! Better luck next time.")
        window.destroy()
    elif is_draw():
        messagebox.showinfo("Result", "It's a draw!")
        window.destroy()

def player_move(position):
    """Handle player's move and trigger AI's move."""
    if make_move(position, 'X'):
        check_game_over()
        window.update() 
        ai_move = get_ai_move(difficulty)
        make_move(ai_move, 'O')
        check_game_over()

def start_game():
    """Start the Tic-Tac-Toe game with GUI."""
    global difficulty, window, buttons
    window = tk.Tk()
    window.title("Tic-Tac-Toe with AI")

   
    window.configure(bg='lightblue')

    
    difficulty = simpledialog.askstring("Input", "Choose difficulty level (easy/hard):").lower()
    while difficulty not in ['easy', 'hard']:
        difficulty = simpledialog.askstring("Input", "Invalid choice. Choose difficulty level (easy/hard):").lower()

 
    title_label = tk.Label(window, text="Welcome to Tic-Tac-Toe!", font=('Arial', 24, 'bold'), bg='lightblue')
    title_label.grid(row=0, column=0, columnspan=3, pady=10)

    instruction_label = tk.Label(window, text="You are 'X'. The AI is 'O'. Click a button to make your move.", 
                                 font=('Arial', 14), bg='lightblue')
    instruction_label.grid(row=1, column=0, columnspan=3, pady=5)


    buttons = []
    for i in range(9):
        button = tk.Button(window, text=' ', width=10, height=3, font=('Arial', 24),
                           bg='white', activebackground='lightgreen', command=lambda i=i: player_move(i))
        button.grid(row=(i // 3) + 2, column=i % 3, padx=5, pady=5)
        buttons.append(button)

    window.mainloop()

if __name__ == "__main__":
    start_game()