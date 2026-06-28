import tkinter as tk
from backend import CaroBoard, CaroAI
from .styles import setup_styles, BG_MAIN, COLOR_X, COLOR_O, COLOR_WIN, COLOR_ACCENT
from .board_view import BoardView
from .panel_view import PanelView

class CaroGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro 3x3 AI")
        self.root.geometry("950x650")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(False, False)

        self.board = CaroBoard()
        self.ai_symbol = 'O'
        self.human_symbol = 'X'
        self.current_turn = 'Human'
        self.game_over = False

        setup_styles(self.root)
        self.build_ui()
        self.reset_game()

    def build_ui(self):
        title_label = tk.Label(
            self.root,
            text="CARO 3x3",
            font=("Helvetica", 20, "bold"),
            bg=BG_MAIN,
            fg=COLOR_ACCENT,
            pady=15
        )
        title_label.pack(side="top", fill="x")

        main_frame = tk.Frame(self.root, bg=BG_MAIN)
        main_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.board_view = BoardView(main_frame, self.on_cell_click)
        self.board_view.pack(side="left", fill="both", expand=True)

        self.panel_view = PanelView(main_frame, self.reset_game, self.on_setting_change)
        self.panel_view.pack(side="right", fill="both", padx=(10, 0), pady=6)

    def on_setting_change(self, event=None):
        self.reset_game()

    def reset_game(self):
        self.board = CaroBoard()
        self.game_over = False
        
        ai_choice = self.panel_view.ai_sym_var.get()
        if "O" in ai_choice:
            self.ai_symbol = 'O'
            self.human_symbol = 'X'
        else:
            self.ai_symbol = 'X'
            self.human_symbol = 'O'

        self.board_view.reset_grid()
        self.panel_view.reset_stats()

        starter = self.panel_view.starter_var.get()
        if starter == "AI":
            self.current_turn = 'AI'
            self.panel_view.set_status("AI đang suy nghĩ...", COLOR_O)
            self.board_view.set_interactive(False)
            self.root.after(300, self.make_ai_move)
        else:
            self.current_turn = 'Human'
            self.panel_view.set_status("Lượt chơi: Người chơi (" + self.human_symbol + ")", COLOR_X)
            self.board_view.set_interactive(True)

    def on_cell_click(self, r, c):
        if self.game_over or self.current_turn != 'Human':
            return

        if self.board.make_move(r, c, self.human_symbol):
            color = COLOR_X if self.human_symbol == 'X' else COLOR_O
            self.board_view.update_cell(r, c, self.human_symbol, color)

            winner, winning_line = self.board.check_winner()
            if winner is not None:
                self.handle_game_end(winner, winning_line)
                return

            self.current_turn = 'AI'
            self.panel_view.set_status("AI đang suy nghĩ...", COLOR_O)
            self.board_view.set_interactive(False)
            self.root.after(300, self.make_ai_move)

    def make_ai_move(self):
        if self.game_over:
            return

        algorithm = self.panel_view.algo_var.get()
        max_depth = int(self.panel_view.depth_slider.get())

        best_move, nodes, elapsed = CaroAI.get_best_move(self.board, algorithm, max_depth, self.ai_symbol)

        if best_move is not None:
            r, c = best_move
            self.board.make_move(r, c, self.ai_symbol)

            color = COLOR_X if self.ai_symbol == 'X' else COLOR_O
            self.board_view.update_cell(r, c, self.ai_symbol, color)
            self.panel_view.update_stats(algorithm, elapsed, nodes, r, c)

            winner, winning_line = self.board.check_winner()
            if winner is not None:
                self.handle_game_end(winner, winning_line)
                return

            self.current_turn = 'Human'
            self.panel_view.set_status("Lượt chơi: Người chơi (" + self.human_symbol + ")", COLOR_X)
            self.board_view.set_interactive(True)

    def handle_game_end(self, winner, winning_line):
        self.game_over = True
        self.board_view.set_interactive(False)

        if winner == 'Draw':
            self.panel_view.set_status("Kết quả: HÒA NHAU!", COLOR_ACCENT)
        else:
            is_ai_won = (winner == self.ai_symbol)
            winner_text = "AI thắng!" if is_ai_won else "Bạn thắng!"
            color = COLOR_O if is_ai_won else COLOR_WIN
            self.panel_view.set_status(f"Kết quả: {winner_text} ({winner} thắng)", color)
            self.board_view.highlight_winning_line(winning_line)
