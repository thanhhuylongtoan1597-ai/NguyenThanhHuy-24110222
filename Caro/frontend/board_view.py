import tkinter as tk
from .styles import BG_MAIN, BG_BTN, BG_BTN_HOVER, FG_DARK, COLOR_WIN, COLOR_TEXT_WIN

class BoardView(tk.Frame):
    def __init__(self, parent, on_cell_click_callback):
        super().__init__(parent, bg=BG_MAIN)
        self.on_cell_click_callback = on_cell_click_callback
        self.buttons = []
        self.build_board()

    def build_board(self):
        self.board_inner_frame = tk.Frame(self, bg='#dee2e6')
        self.board_inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        for r in range(3):
            row_buttons = []
            for c in range(3):
                cell_frame = tk.Frame(self.board_inner_frame, width=135, height=135, bg='#dee2e6')
                cell_frame.grid(row=r, column=c, padx=3, pady=3)
                cell_frame.grid_propagate(False)

                btn = tk.Button(
                    cell_frame,
                    text="",
                    font=("Arial", 40, "bold"),
                    bg=BG_BTN,
                    fg=FG_DARK,
                    activebackground=BG_BTN_HOVER,
                    activeforeground=FG_DARK,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda row=r, col=c: self.on_cell_click_callback(row, col)
                )
                btn.pack(fill="both", expand=True)
                
                btn.bind("<Enter>", lambda e, b=btn: self.on_btn_enter(b))
                btn.bind("<Leave>", lambda e, b=btn: self.on_btn_leave(b))

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def on_btn_enter(self, btn):
        if btn.cget("text") == "" and btn.cget("state") != "disabled":
            btn.config(bg=BG_BTN_HOVER)

    def on_btn_leave(self, btn):
        if btn.cget("text") == "" and btn.cget("state") != "disabled":
            btn.config(bg=BG_BTN)

    def update_cell(self, r, c, symbol, color):
        btn = self.buttons[r][c]
        btn.config(text=symbol, fg=color)

    def highlight_winning_line(self, winning_line):
        for r, c in winning_line:
            self.buttons[r][c].config(bg=COLOR_WIN, fg=COLOR_TEXT_WIN)

    def reset_grid(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", bg=BG_BTN, state="normal")

    def set_interactive(self, enabled):
        state = "normal" if enabled else "disabled"
        for r in range(3):
            for c in range(3):
                if self.buttons[r][c].cget("text") == "":
                    self.buttons[r][c].config(state=state)
