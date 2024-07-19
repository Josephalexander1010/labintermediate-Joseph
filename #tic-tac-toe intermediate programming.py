"""A tic-tac-toe game built with Python and Tkinter."""

from math import comb
import tkinter as tk
from tkinter import simpledialog, messagebox
from itertools import cycle
from tkinter import font
from typing import NamedTuple


class Player(NamedTuple):
    label:str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str=""

DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players, board_size, win_condition):
        self._players = cycle(players)
        self.board_size = board_size
        self.win_condition = win_condition
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row,col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):
        combos = []
        for row in range(self.board_size):
            for col in range(self.board_size - self.win_condition + 1):
                combo = [(row, col + i) for i in range(self.win_condition)]
                combos.append(combo)
        for col in range(self.board_size):
            for row in range(self.board_size - self.win_condition + 1):
                combo = [(row + i, col) for i in range(self.win_condition)]
                combos.append(combo)
        for row in range(self.board_size - self.win_condition + 1):
            for col in range(self.board_size - self.win_condition + 1):
                combo = [(row + i, col + i) for i in range(self.win_condition)]
                combos.append(combo)
        for row in range(self.win_condition - 1, self.board_size):
            for col in range(self.board_size - self.win_condition + 1):
                combo = [(row - i, col + i) for i in range(self.win_condition)]
                combos.append(combo)
        return combos
    
    def is_valid_move(self,move):
        """Return True if move is valid, and false otherwise"""
        row,col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self,move):
        """Process the current move and check if it's a win"""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    def has_winner(self):
        """Return True if the game has winner, and False otherwise"""
        return self._has_winner
    
    def is_tied(self):
        """Return true if the game is tied, and false otherwise"""
        no_winner = not self._has_winner
        played_moves= (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        """return a toggled player."""
        self.current_player = next(self._players)
    
    def reset_game(self):
        """reset the game state to play again"""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play again",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font= font.Font(size=28, weight="bold"),
        )
        self.display.pack()
    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range (self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font= font.Font(size=36,weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
               )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
               )
    def play(self, event):
        """handle a players move"""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
    
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)
    
    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")
    
    def reset_board(self):
        """reset the game's board to play again"""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
        

def main():
    """Create the game's board and run its main loop."""
    root =  tk.Tk() 
    root.withdraw()

    board_size = simpledialog.askinteger ("Board Size", "Enter the board size:", minvalue=3)
    if not board_size:
        messagebox.showerror("input error", "board size is required")
        return
    
    win_condition = simpledialog.askinteger ("win condition", "enter the number of symbols needed to win:", minvalue=3)
    if not win_condition:
        messagebox.showerror("input error","win condition is required")
        return
    
    game = TicTacToeGame(players=DEFAULT_PLAYERS, board_size=board_size, win_condition=win_condition)
    board=TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()