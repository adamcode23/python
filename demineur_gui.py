import random
import tkinter as tk
from tkinter import messagebox
from functools import partial

DIFFICULTIES = {
    "Débutant": (9, 9, 10),
    "Intermédiaire": (16, 16, 40),
    "Expert": (16, 30, 99),
}


class DemineurGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Démineur")
        self.root.configure(bg="#eef2ff")
        self.root.resizable(False, False)

        self.top = tk.Frame(root, bg="#eef2ff")
        self.top.pack(pady=(10, 5))

        self.title = tk.Label(
            self.top,
            text="💣 DÉMINEUR",
            font=("Segoe UI", 14, "bold"),
            bg="#eef2ff",
            fg="#1f2937"
        )
        self.title.pack()

        self.controls = tk.Frame(self.top, bg="#eef2ff")
        self.controls.pack(pady=(0, 5))

        self.difficulty_var = tk.StringVar(value="Débutant")
        self.difficulty_menu = tk.OptionMenu(
            self.controls,
            self.difficulty_var,
            *DIFFICULTIES.keys(),
            command=lambda *_: self.setup_game()
        )
        self.difficulty_menu.config(
            bg="#dbeafe",
            fg="#111827",
            relief="raised",
            bd=1,
            font=("Segoe UI", 10)
        )
        self.difficulty_menu.pack(side=tk.LEFT)

        self.info = tk.Label(
            self.top,
            text="Clic gauche : ouvrir   Clic droit : drapeau",
            font=("Segoe UI", 9),
            bg="#eef2ff",
            fg="#4b5563"
        )
        self.info.pack()

        self.status = tk.Label(
            self.top,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#eef2ff",
            fg="#1f2937"
        )
        self.status.pack()

        self.frame = tk.Frame(root, bg="#eef2ff")
        self.frame.pack(pady=5)

        self.setup_game()

    def setup_game(self):
        self.rows, self.cols, self.bombs = DIFFICULTIES[self.difficulty_var.get()]
        self.board = self.init_board(self.rows, self.cols, self.bombs)
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for widget in self.frame.winfo_children():
            widget.destroy()

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    font=("Segoe UI", 10, "bold"),
                    bg="#dbeafe",
                    fg="#111827",
                    relief="raised",
                    bd=1,
                    command=partial(self.on_left_click, r, c)
                )
                btn.bind("<Button-3>", lambda event, rr=r, cc=c: self.on_right_click(rr, cc))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

        self.status.config(
            text=f"Niveau : {self.difficulty_var.get()}   Mines : {self.bombs}"
        )
        self.root.update_idletasks()
        self.root.geometry(f"{self.cols * 28 + 40}x{self.rows * 28 + 180}")

    def init_board(self, rows, cols, bombs):
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        positions = set()

        while len(positions) < bombs:
            r = random.randrange(rows)
            c = random.randrange(cols)
            positions.add((r, c))

        for r, c in positions:
            board[r][c] = -1
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != -1:
                        board[nr][nc] += 1

        return board

    def on_left_click(self, r, c):
        if self.flags[r][c] or self.revealed[r][c]:
            return

        if self.reveal(r, c):
            self.show_all_bombs()
            messagebox.showinfo("Perdu", "💥 Vous avez touché une mine !")
            self.setup_game()
            return

        if self.is_winner():
            messagebox.showinfo("Gagné", "🎉 Bravo, vous avez gagné !")
            self.setup_game()

    def on_right_click(self, r, c):
        if self.revealed[r][c]:
            return
        self.flags[r][c] = not self.flags[r][c]
        self.buttons[r][c].config(
            text="🚩" if self.flags[r][c] else "",
            bg="#fde68a" if self.flags[r][c] else "#dbeafe"
        )

    def reveal(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.revealed[r][c] or self.flags[r][c]:
            return False

        self.revealed[r][c] = True
        btn = self.buttons[r][c]

        if self.board[r][c] == -1:
            btn.config(text="💥", bg="#fca5a5", fg="#7f1d1d")
            return True

        if self.board[r][c] == 0:
            btn.config(text="", bg="#e5e7eb")
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal(r + dr, c + dc)
        else:
            colors = {
                1: "#bfdbfe",
                2: "#bbf7d0",
                3: "#fde68a",
                4: "#fca5a5",
                5: "#fda4af",
                6: "#c4b5fd",
                7: "#fdba74",
                8: "#a7f3d0",
            }
            btn.config(
                text=str(self.board[r][c]),
                bg=colors.get(self.board[r][c], "#f3f4f6"),
                fg="#111827"
            )

        return False

    def show_all_bombs(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text="💣", bg="#fecaca", fg="#7f1d1d")

    def is_winner(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    DemineurGUI(root)
    root.mainloop()
