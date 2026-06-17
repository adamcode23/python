import json
import os
import random
import tkinter as tk

WIDTH = 10
HEIGHT = 20
CELL_SIZE = 30
SIDE_PANEL = 180
SAVE_FILE = os.path.join(os.path.dirname(__file__), "tetris_save.json")
DIFFICULTIES = {
    "normal": "Normal",
    "rapid": "Rapide",
    "hard": "Difficile",
}

SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
    ],
}

COLORS = {
    "I": "#00f5ff",
    "O": "#ffd700",
    "T": "#b000ff",
    "S": "#00ff66",
    "Z": "#ff0040",
    "J": "#1e90ff",
    "L": "#ff8c00",
}


class Piece:
    def __init__(self, shape_key, x=WIDTH // 2 - 1, y=0):
        self.shape_key = shape_key
        self.shape = SHAPES[shape_key]
        self.rotation = 0
        self.x = x
        self.y = y

    def cells(self):
        return [(self.x + dx, self.y + dy) for dx, dy in self.shape[self.rotation]]

    def to_dict(self):
        return {
            "shape_key": self.shape_key,
            "rotation": self.rotation,
            "x": self.x,
            "y": self.y,
        }

    @classmethod
    def from_dict(cls, data):
        piece = cls(data["shape_key"], data["x"], data["y"])
        piece.rotation = data["rotation"]
        return piece


class PlayerGame:
    def __init__(self, name, canvas, difficulty="normal"):
        self.name = name
        self.canvas = canvas
        self.difficulty = difficulty
        self.opponent = None
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.current_piece = None
        self.next_piece = None
        self.has_started = False
        self.pending_garbage = 0

    def reset(self):
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.paused = False
        self.game_over = False
        self.current_piece = None
        self.next_piece = None
        self.has_started = True
        self.pending_garbage = 0

    def random_piece(self):
        return Piece(random.choice(list(SHAPES.keys())))

    def speed(self):
        if self.difficulty == "rapid":
            return max(80, 380 - (self.level - 1) * 35)
        if self.difficulty == "hard":
            return max(80, 250 - (self.level - 1) * 30)
        return max(80, 550 - (self.level - 1) * 40)

    def spawn_piece(self):
        self.current_piece = self.next_piece or self.random_piece()
        self.next_piece = self.random_piece()
        if not is_valid_position(self.current_piece, self.current_piece.x, self.current_piece.y, self.board):
            self.game_over = True

    def try_move(self, dx, dy):
        if self.current_piece is None:
            return False
        if is_valid_position(
            self.current_piece,
            self.current_piece.x + dx,
            self.current_piece.y + dy,
            self.board,
        ):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate(self):
        if self.current_piece is None:
            return
        old_rotation = self.current_piece.rotation
        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
        if not is_valid_position(self.current_piece, self.current_piece.x, self.current_piece.y, self.board):
            self.current_piece.rotation = old_rotation

    def hard_drop(self):
        while self.try_move(0, 1):
            self.score += 1

    def lock_piece(self):
        if self.current_piece is None:
            return
        for x, y in self.current_piece.cells():
            if y < 0:
                self.game_over = True
                return
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                self.board[y][x] = self.current_piece.shape_key
        self.clear_lines()
        self.current_piece = None

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = HEIGHT - len(new_board)
        while len(new_board) < HEIGHT:
            new_board.insert(0, [0 for _ in range(WIDTH)])
        self.board = new_board
        if cleared:
            self.lines += cleared
            self.level = 1 + self.lines // 10
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(cleared, 0) * self.level
            if self.opponent is not None:
                self.opponent.add_garbage(cleared)

    def add_garbage(self, count):
        self.pending_garbage += count

    def apply_garbage(self):
        if self.pending_garbage <= 0:
            return
        self.pending_garbage -= 1
        row = [random.choice(list(COLORS.keys())) for _ in range(WIDTH)]
        row[random.randint(0, WIDTH - 1)] = 0
        self.board = self.board[1:] + [row]

    def tick(self):
        if self.paused or self.game_over or not self.has_started:
            return
        if self.pending_garbage > 0:
            self.apply_garbage()
            self.draw()
            return
        if self.current_piece is None:
            self.spawn_piece()
            if self.game_over:
                self.draw()
                return
        elif not self.try_move(0, 1):
            self.lock_piece()
            if self.current_piece is None:
                self.spawn_piece()
                if self.game_over:
                    self.draw()
                    return
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    self.draw_cell(x, y, self.board[y][x])
        if self.current_piece:
            for x, y in self.current_piece.cells():
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    self.draw_cell(x, y, self.current_piece.shape_key)
        self.draw_sidebar()

        if self.paused:
            self.canvas.create_text(
                WIDTH * CELL_SIZE // 2,
                HEIGHT * CELL_SIZE // 2,
                text="PAUSE",
                font=("Arial", 22, "bold"),
                fill="white",
                tags="overlay",
            )
        elif self.game_over:
            self.canvas.create_text(
                WIDTH * CELL_SIZE // 2,
                HEIGHT * CELL_SIZE // 2,
                text="GAME OVER\nR pour rejouer",
                font=("Arial", 18, "bold"),
                fill="white",
                justify="center",
                tags="overlay",
            )

    def draw_grid(self):
        self.canvas.create_rectangle(
            0,
            0,
            WIDTH * CELL_SIZE,
            HEIGHT * CELL_SIZE,
            fill="#0b1020",
            outline="#1f2a44",
        )
        for x in range(WIDTH + 1):
            self.canvas.create_line(
                x * CELL_SIZE,
                0,
                x * CELL_SIZE,
                HEIGHT * CELL_SIZE,
                fill="#1f2a44",
            )
        for y in range(HEIGHT + 1):
            self.canvas.create_line(
                0,
                y * CELL_SIZE,
                WIDTH * CELL_SIZE,
                y * CELL_SIZE,
                fill="#1f2a44",
            )

    def draw_sidebar(self):
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            30,
            text=self.name,
            font=("Arial", 14, "bold"),
            fill="white",
            anchor="n",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            70,
            text="Score",
            font=("Arial", 12, "bold"),
            fill="#c7d2fe",
            anchor="n",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            95,
            text=str(self.score),
            font=("Arial", 18, "bold"),
            fill="white",
            anchor="n",
            tags="score",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            140,
            text="Lignes",
            font=("Arial", 12, "bold"),
            fill="#c7d2fe",
            anchor="n",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            165,
            text=str(self.lines),
            font=("Arial", 18, "bold"),
            fill="white",
            anchor="n",
            tags="lines",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            210,
            text="Niveau",
            font=("Arial", 12, "bold"),
            fill="#c7d2fe",
            anchor="n",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            235,
            text=str(self.level),
            font=("Arial", 18, "bold"),
            fill="white",
            anchor="n",
            tags="level",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            300,
            text="Malus",
            font=("Arial", 12, "bold"),
            fill="#c7d2fe",
            anchor="n",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            325,
            text=str(self.pending_garbage),
            font=("Arial", 16, "bold"),
            fill="white",
            anchor="n",
            tags="garbage",
        )
        self.canvas.create_text(
            WIDTH * CELL_SIZE + 90,
            360,
            text="Next",
            font=("Arial", 12, "bold"),
            fill="#c7d2fe",
            anchor="n",
        )
        if self.next_piece:
            for dx, dy in self.next_piece.shape[0]:
                px = WIDTH * CELL_SIZE + 50 + dx * CELL_SIZE * 0.8
                py = 390 + dy * CELL_SIZE * 0.8
                self.canvas.create_rectangle(
                    px,
                    py,
                    px + CELL_SIZE * 0.8,
                    py + CELL_SIZE * 0.8,
                    fill=COLORS[self.next_piece.shape_key],
                    outline="#0b1020",
                )

    def draw_cell(self, x, y, key):
        px = x * CELL_SIZE
        py = y * CELL_SIZE
        self.canvas.create_rectangle(
            px,
            py,
            px + CELL_SIZE,
            py + CELL_SIZE,
            fill=COLORS[key],
            outline="#0b1020",
            width=2,
        )

    def to_dict(self):
        return {
            "name": self.name,
            "difficulty": self.difficulty,
            "board": self.board,
            "score": self.score,
            "lines": self.lines,
            "level": self.level,
            "paused": self.paused,
            "game_over": self.game_over,
            "has_started": self.has_started,
            "pending_garbage": self.pending_garbage,
            "current_piece": self.current_piece.to_dict() if self.current_piece else None,
            "next_piece": self.next_piece.to_dict() if self.next_piece else None,
        }

    @classmethod
    def from_dict(cls, data, canvas):
        player = cls(data["name"], canvas, data.get("difficulty", "normal"))
        player.board = data["board"]
        player.score = data["score"]
        player.lines = data["lines"]
        player.level = data["level"]
        player.paused = data["paused"]
        player.game_over = data["game_over"]
        player.has_started = data["has_started"]
        player.pending_garbage = data.get("pending_garbage", 0)
        player.current_piece = Piece.from_dict(data["current_piece"]) if data.get("current_piece") else None
        player.next_piece = Piece.from_dict(data["next_piece"]) if data.get("next_piece") else None
        return player


class TetrisApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b1020")
        self.root.bind_all("<KeyPress>", self.key_press)
        self.root.focus_force()

        self.mode = None
        self.difficulty = "normal"
        self.menu_visible = True
        self.players = []
        self.canvas = tk.Canvas(self.root, width=0, height=0, bg="#0b1020", highlightthickness=0)
        self.canvas.pack()

        self.show_menu()

    def show_menu(self):
        self.menu_visible = True
        self.mode = None
        self.canvas.config(width=WIDTH * CELL_SIZE + SIDE_PANEL, height=HEIGHT * CELL_SIZE)
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0,
            0,
            self.canvas.winfo_reqwidth(),
            self.canvas.winfo_reqheight(),
            fill="#0b1020",
            outline="",
        )
        self.canvas.create_text(
            (WIDTH * CELL_SIZE + SIDE_PANEL) // 2,
            80,
            text="TETRIS",
            font=("Arial", 24, "bold"),
            fill="white",
        )
        self.canvas.create_text(
            (WIDTH * CELL_SIZE + SIDE_PANEL) // 2,
            150,
            text="1 - Solo normal\n2 - Solo rapide\n3 - Solo difficile\n4 - Deux joueurs\nP - Pause\nS - Sauvegarder\nL - Charger\nM - Menu",
            font=("Arial", 12),
            fill="#dbeafe",
            justify="center",
        )
        self.root.focus_force()

    def start_single(self, difficulty="normal"):
        self.mode = "single"
        self.difficulty = difficulty
        self.menu_visible = False
        self.players = []
        self.canvas.config(width=WIDTH * CELL_SIZE + SIDE_PANEL, height=HEIGHT * CELL_SIZE)
        self.canvas.delete("all")
        player = PlayerGame("Joueur 1", tk.Canvas(self.root, width=WIDTH * CELL_SIZE + SIDE_PANEL, height=HEIGHT * CELL_SIZE, bg="#0b1020", highlightthickness=0), difficulty=self.difficulty)
        player.reset()
        player.spawn_piece()
        player.next_piece = player.random_piece()
        player.draw()
        self.players = [player]
        self.canvas.pack_forget()
        player.canvas.pack(side=tk.LEFT)
        self.canvas = player.canvas
        self.root.after(0, self.schedule_tick)

    def start_two_players(self):
        self.mode = "two"
        self.menu_visible = False
        self.players = []
        board_width = (WIDTH * CELL_SIZE + SIDE_PANEL) * 2 + 40
        self.canvas.config(width=board_width, height=HEIGHT * CELL_SIZE)
        self.canvas.delete("all")
        self.canvas.pack_forget()
        self.canvas = tk.Canvas(self.root, width=board_width, height=HEIGHT * CELL_SIZE, bg="#0b1020", highlightthickness=0)
        self.canvas.pack()
        left = PlayerGame("Joueur 1", tk.Canvas(self.canvas, width=WIDTH * CELL_SIZE + SIDE_PANEL, height=HEIGHT * CELL_SIZE, bg="#0b1020", highlightthickness=0), difficulty=self.difficulty)
        right = PlayerGame("Joueur 2", tk.Canvas(self.canvas, width=WIDTH * CELL_SIZE + SIDE_PANEL, height=HEIGHT * CELL_SIZE, bg="#0b1020", highlightthickness=0), difficulty=self.difficulty)
        left.opponent = right
        right.opponent = left
        for player in (left, right):
            player.reset()
            player.spawn_piece()
            player.next_piece = player.random_piece()
            player.draw()
        left.canvas.place(x=0, y=0)
        right.canvas.place(x=WIDTH * CELL_SIZE + SIDE_PANEL + 40, y=0)
        self.players = [left, right]
        self.root.after(0, self.schedule_tick)

    def schedule_tick(self):
        for player in self.players:
            if player.has_started and not player.paused and not player.game_over:
                player.tick()
        active_players = [player for player in self.players if player.has_started and not player.paused and not player.game_over]
        if active_players:
            delay = min(player.speed() for player in active_players)
            self.root.after(delay, self.schedule_tick)

    def key_press(self, event):
        if self.menu_visible:
            if event.keysym == "1":
                self.start_single("normal")
            elif event.keysym == "2":
                self.start_single("rapid")
            elif event.keysym == "3":
                self.start_single("hard")
            elif event.keysym == "4":
                self.start_two_players()
            elif event.keysym in ("l", "L"):
                self.load_game()
            return

        if event.keysym in ("m", "M", "Escape"):
            self.show_menu()
            return
        if event.keysym in ("s", "S"):
            self.save_game()
            return
        if event.keysym in ("l", "L"):
            self.load_game()
            return
        if event.keysym in ("p", "P"):
            for player in self.players:
                player.paused = not player.paused
            for player in self.players:
                player.draw()
            return
        if event.keysym == "r" or event.keysym == "R":
            for player in self.players:
                player.reset()
                player.spawn_piece()
                player.next_piece = player.random_piece()
            for player in self.players:
                player.draw()
            return

        if self.mode == "single":
            player = self.players[0]
            if event.keysym == "Left":
                player.try_move(-1, 0)
            elif event.keysym == "Right":
                player.try_move(1, 0)
            elif event.keysym == "Down":
                player.try_move(0, 1)
            elif event.keysym == "Up":
                player.rotate()
            elif event.keysym == "space":
                player.hard_drop()
            player.draw()
        elif self.mode == "two":
            left, right = self.players
            controls = {
                "Left": (-1, 0),
                "Right": (1, 0),
                "Down": (0, 1),
                "Up": "rotate",
                "space": "hard",
                "a": (-1, 0),
                "d": (1, 0),
                "s": (0, 1),
                "w": "rotate",
                "q": "hard",
            }
            if event.keysym in controls:
                if event.keysym in ("Left", "Right", "Down", "Up", "space"):
                    if event.keysym == "Left":
                        left.try_move(-1, 0)
                    elif event.keysym == "Right":
                        left.try_move(1, 0)
                    elif event.keysym == "Down":
                        left.try_move(0, 1)
                    elif event.keysym == "Up":
                        left.rotate()
                    elif event.keysym == "space":
                        left.hard_drop()
                    left.draw()
                elif event.keysym in ("a", "d", "s", "w", "q"):
                    if event.keysym == "a":
                        right.try_move(-1, 0)
                    elif event.keysym == "d":
                        right.try_move(1, 0)
                    elif event.keysym == "s":
                        right.try_move(0, 1)
                    elif event.keysym == "w":
                        right.rotate()
                    elif event.keysym == "q":
                        right.hard_drop()
                    right.draw()

    def save_game(self):
        data = {
            "mode": self.mode,
            "players": [player.to_dict() for player in self.players],
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.mode = data.get("mode")
        if self.mode == "single":
            difficulty = data["players"][0].get("difficulty", "normal")
            self.start_single(difficulty)
            self.players[0] = PlayerGame.from_dict(data["players"][0], self.canvas)
            self.players[0].draw()
        elif self.mode == "two":
            self.start_two_players()
            self.players[0] = PlayerGame.from_dict(data["players"][0], self.players[0].canvas)
            self.players[1] = PlayerGame.from_dict(data["players"][1], self.players[1].canvas)
            for player in self.players:
                player.draw()


def is_valid_position(piece, x, y, board):
    for dx, dy in piece.shape[piece.rotation]:
        nx = x + dx
        ny = y + dy
        if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
            return False
        if ny >= 0 and board[ny][nx] != 0:
            return False
    return True


if __name__ == "__main__":
    app = TetrisApp()
    app.root.mainloop()
