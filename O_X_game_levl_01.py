import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.player_scores = {"X": 0, "O": 0}
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.colors = [
            "white", "light blue", "light green", "light yellow", "light gray",
            "red", "orange", "purple", "pink", "brown", "cyan", "magenta",
            "dark blue", "dark green", "gold", "silver", "maroon", "navy",
            "olive", "teal", "lime", "indigo", "violet", "black"
        ]
        self.current_bg_color = "white"
        self.is_single_player = False
        self.difficulty = "Medium"  # Default difficulty level
        self.create_menu()
        self.create_score_labels()
        self.create_board()
        self.create_color_buttons()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Single Player (Easy)", command=lambda: self.start_single_player("Easy"))
        game_menu.add_command(label="Single Player (Medium)", command=lambda: self.start_single_player("Medium"))
        game_menu.add_command(label="Single Player (Hard)", command=lambda: self.start_single_player("Hard"))
        game_menu.add_command(label="Two Players", command=self.start_two_players)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)

    def start_single_player(self, difficulty):
        self.is_single_player = True
        self.difficulty = difficulty
        self.reset_board()

    def start_two_players(self):
        self.is_single_player = False
        self.reset_board()

    def create_score_labels(self):
        self.score_label_X = tk.Label(self.root, text="Player X: 0", font=("Arial", 8))
        self.score_label_X.grid(row=1, column=0, columnspan=3, sticky="we")
        self.score_label_O = tk.Label(self.root, text="Player O: 0", font=("Arial", 8))
        self.score_label_O.grid(row=2, column=0, columnspan=3, sticky="we")

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font=("Arial", 40, "bold"), width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c), bg=self.current_bg_color)
                button.grid(row=row + 4, column=col, padx=0, pady=0, sticky="nsew")
                self.buttons[row][col] = button

        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i + 4, weight=1)

    def create_color_buttons(self):
        for index, color in enumerate(self.colors):
            button = tk.Button(self.root, bg=color, width=5, height=2,
                               command=lambda c=color: self.change_bg_color(c))
            button.grid(row=7 + index // 3, column=index % 3, padx=0, pady=0, sticky="we")

    def change_bg_color(self, color):
        self.current_bg_color = color
        self.root.configure(bg=color)
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]:
                    self.buttons[row][col].configure(bg=color)

    def on_button_click(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.update_button_text(self.buttons[row][col], self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.update_score(self.current_player)
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Tic Tac Toe", "The game is a draw!")
                self.reset_board()
            else:
                if self.is_single_player and self.current_player == "X":
                    self.current_player = "O"
                    self.computer_move()
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"

    def computer_move(self):
        if self.difficulty == "Easy":
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.board[row][col] = self.current_player
                self.update_button_text(self.buttons[row][col], self.current_player)
        else:
            best_score = -float('inf')
            best_move = None
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == "":
                        self.board[row][col] = "O"
                        if self.difficulty == "Medium":
                            score = self.minimax(self.board, 0, False, 3)  # Depth limit for Medium
                        else:
                            score = self.minimax(self.board, 0, False)
                        self.board[row][col] = ""
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
            if best_move:
                row, col = best_move
                self.board[row][col] = self.current_player
                self.update_button_text(self.buttons[row][col], self.current_player)

        if self.check_winner(self.current_player):
            messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
            self.update_score(self.current_player)
            self.reset_board()
        elif self.is_board_full():
            messagebox.showinfo("Tic Tac Toe", "The game is a draw!")
            self.reset_board()
        else:
            self.current_player = "X"

    def minimax(self, board, depth, is_maximizing, max_depth=float('inf')):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.is_board_full():
            return 0
        if depth >= max_depth:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "O"
                        score = self.minimax(board, depth + 1, False, max_depth)
                        board[row][col] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "X"
                        score = self.minimax(board, depth + 1, True, max_depth)
                        board[row][col] = ""
                        best_score = min(score, best_score)
            return best_score

    def update_button_text(self, button, text):
        button.config(text=text, compound="center", padx=1, pady=1, fg="black")

    def check_winner(self, player):
        for row in self.board:
            if row.count(player) == 3:
                return True

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True

        return False

    def is_board_full(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def update_score(self, player):
        self.player_scores[player] += 1
        if player == "X":
            self.score_label_X.config(text=f"Player X: {self.player_scores['X']}")
        else:
            self.score_label_O.config(text=f"Player O: {self.player_scores['O']}")

    def reset_board(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", bg=self.current_bg_color)


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

