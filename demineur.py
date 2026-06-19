import random
import time

DIFFICULTIES = {
    "Débutant": (9, 9, 10),
    "Intermédiaire": (16, 16, 40),
    "Expert": (16, 30, 99),
}
BEST_TIMES = {}


def init_board(rows, cols, bombs):
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


def format_time(seconds):
    if seconds is None:
        return "--:--"
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def display_board(board, revealed, flagged, elapsed, difficulty):
    best = BEST_TIMES.get(difficulty)
    print(f"\nNiveau : {difficulty} | Temps : {format_time(elapsed)} | Meilleur : {format_time(best)}")
    print("   " + " ".join(str(i) for i in range(len(board[0]))))
    print("  " + "-" * (len(board[0]) * 2 + 1))
    for r in range(len(board)):
        row = [f"{r:2} |"]
        for c in range(len(board[r])):
            if flagged[r][c]:
                row.append("F")
            elif revealed[r][c]:
                if board[r][c] == -1:
                    row.append("*")
                elif board[r][c] == 0:
                    row.append(".")
                else:
                    row.append(str(board[r][c]))
            else:
                row.append("#")
        print(" ".join(row))


def reveal(board, revealed, r, c):
    if not (0 <= r < len(board) and 0 <= c < len(board[0])):
        return False
    if revealed[r][c]:
        return False

    revealed[r][c] = True

    if board[r][c] == -1:
        return True

    if board[r][c] == 0:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                reveal(board, revealed, r + dr, c + dc)

    return False


def is_winner(revealed, board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != -1 and not revealed[r][c]:
                return False
    return True


def choose_difficulty():
    print("Choisissez un niveau :")
    for name in DIFFICULTIES:
        print(f"- {name}")

    while True:
        choice = input("Votre niveau : ").strip()
        if choice in DIFFICULTIES:
            return choice
        print("Choix invalide. Essayez Débutant, Intermédiaire ou Expert.")


def main():
    difficulty = choose_difficulty()
    rows, cols, bombs = DIFFICULTIES[difficulty]

    def new_game():
        return init_board(rows, cols, bombs), [[False for _ in range(cols)] for _ in range(rows)], [[False for _ in range(cols)] for _ in range(rows)]

    board, revealed, flagged = new_game()
    start_time = time.time()

    print(f"Démineur (console) - {difficulty}")
    print("Commandes :")
    print("- ligne colonne      : ouvrir une case")
    print("- f ligne colonne    : poser ou retirer un drapeau")
    print("- r                  : recommencer")
    print("- q                  : quitter")

    while True:
        elapsed = time.time() - start_time
        display_board(board, revealed, flagged, elapsed, difficulty)
        command = input("Votre choix : ").strip().lower()

        if command == "q":
            print("Partie abandonnée.")
            break

        if command == "r":
            board, revealed, flagged = new_game()
            start_time = time.time()
            print("Nouvelle partie lancée.")
            continue

        parts = command.split()
        if len(parts) == 3 and parts[0] == "f":
            try:
                r, c = int(parts[1]), int(parts[2])
                if 0 <= r < rows and 0 <= c < cols:
                    flagged[r][c] = not flagged[r][c]
                else:
                    print("Coordonnées invalides.")
            except ValueError:
                print("Utilisez : f ligne colonne")
            continue

        if len(parts) != 2:
            print("Utilisez : ligne colonne ou f ligne colonne")
            continue

        try:
            r, c = int(parts[0]), int(parts[1])
        except ValueError:
            print("Les coordonnées doivent être des nombres.")
            continue

        if not (0 <= r < rows and 0 <= c < cols):
            print("Coordonnées invalides.")
            continue

        if flagged[r][c]:
            print("Cette case est marquée d'un drapeau.")
            continue

        if reveal(board, revealed, r, c):
            display_board(board, revealed, flagged, time.time() - start_time, difficulty)
            print("Boom ! Vous avez perdu.")
            break

        if is_winner(revealed, board):
            elapsed = time.time() - start_time
            display_board(board, revealed, flagged, elapsed, difficulty)
            print(f"Bravo, vous avez gagné ! Temps : {format_time(elapsed)}")
            previous = BEST_TIMES.get(difficulty)
            if previous is None or elapsed < previous:
                BEST_TIMES[difficulty] = elapsed
                print(f"Nouveau record pour {difficulty} !")
            else:
                print(f"Record actuel pour {difficulty} : {format_time(previous)}")
            break


if __name__ == "__main__":
    main()
