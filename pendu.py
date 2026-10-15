import random
import string

import pygame


WIDTH = 900
HEIGHT = 650
FPS = 60
MAX_ERRORS = 7

WORDS = (
    "PYTHON",
    "SOLEIL",
    "CHOCOLAT",
    "ORDINATEUR",
    "MUSIQUE",
    "BANANE",
    "ETOILE",
    "RENARD",
    "PAPILLON",
    "MONTAGNE",
)

BACKGROUND = (15, 23, 42)
PANEL = (30, 41, 59)
PANEL_LIGHT = (51, 65, 85)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)
ACCENT = (56, 189, 248)
GREEN = (74, 222, 128)
RED = (248, 113, 113)


def draw_text(surface, font, text, color, position, center=False):
    image = font.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    surface.blit(image, rect)


class HangmanGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Le Pendu")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("dejavusans", 20)
        self.small_font = pygame.font.SysFont("dejavusans", 15)
        self.title_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        self.word_font = pygame.font.SysFont("dejavusans", 36, bold=True)
        self.button_font = pygame.font.SysFont("dejavusans", 18, bold=True)
        self.restart_rect = pygame.Rect(690, 39, 165, 44)
        self.new_game()

    def new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.errors = 0
        self.finished = False
        self.won = False

    def guess(self, letter):
        if self.finished or letter in self.guessed:
            return

        self.guessed.add(letter)
        if letter not in self.word:
            self.errors += 1

        if all(letter in self.guessed for letter in self.word):
            self.finished = True
            self.won = True
        elif self.errors >= MAX_ERRORS:
            self.finished = True

    def letter_rect(self, index):
        columns = 7
        button_width = 44
        button_height = 40
        gap = 8
        left = 457
        top = 300
        row, column = divmod(index, columns)
        return pygame.Rect(
            left + column * (button_width + gap),
            top + row * (button_height + gap),
            button_width,
            button_height,
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key in (pygame.K_r, pygame.K_SPACE) and self.finished:
                self.new_game()
            elif event.unicode.upper() in string.ascii_uppercase:
                self.guess(event.unicode.upper())

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.restart_rect.collidepoint(event.pos):
                self.new_game()
            else:
                for index, letter in enumerate(string.ascii_uppercase):
                    if self.letter_rect(index).collidepoint(event.pos):
                        self.guess(letter)
                        break

        return True

    def draw_hangman(self):
        pygame.draw.rect(self.screen, PANEL, (40, 140, 390, 390), border_radius=18)

        draw_text(self.screen, self.small_font, "TES ESSAIS", MUTED, (68, 165))
        draw_text(
            self.screen,
            self.font,
            f"{MAX_ERRORS - self.errors} / {MAX_ERRORS}",
            ACCENT,
            (68, 188),
        )

        color = (203, 213, 225)
        width = 6
        # Le gibet reste visible ; les erreurs ajoutent progressivement le personnage.
        pygame.draw.line(self.screen, color, (110, 465), (320, 465), width)
        pygame.draw.line(self.screen, color, (160, 465), (160, 215), width)
        pygame.draw.line(self.screen, color, (160, 215), (285, 215), width)
        pygame.draw.line(self.screen, color, (285, 215), (285, 250), width)

        person_color = RED if self.finished and not self.won else ACCENT
        if self.errors >= 1:
            pygame.draw.circle(self.screen, person_color, (285, 273), 23, width)
        if self.errors >= 2:
            pygame.draw.line(self.screen, person_color, (285, 296), (285, 365), width)
        if self.errors >= 3:
            pygame.draw.line(self.screen, person_color, (285, 310), (255, 340), width)
        if self.errors >= 4:
            pygame.draw.line(self.screen, person_color, (285, 310), (315, 340), width)
        if self.errors >= 5:
            pygame.draw.line(self.screen, person_color, (285, 365), (257, 410), width)
        if self.errors >= 6:
            pygame.draw.line(self.screen, person_color, (285, 365), (313, 410), width)
        if self.errors >= 7:
            pygame.draw.circle(self.screen, person_color, (278, 269), 2)
            pygame.draw.circle(self.screen, person_color, (292, 269), 2)
            pygame.draw.arc(self.screen, person_color, (276, 277, 18, 12), 0, 3.14, 2)

    def draw_word(self):
        draw_text(self.screen, self.small_font, "MOT À DEVINER", MUTED, (470, 170))
        gap = 6
        letter_width = min(43, (365 - (len(self.word) - 1) * gap) // len(self.word))
        total_width = len(self.word) * letter_width + (len(self.word) - 1) * gap
        start_x = 470 + max(0, (365 - total_width) // 2)

        for index, letter in enumerate(self.word):
            x = start_x + index * (letter_width + gap)
            pygame.draw.line(
                self.screen,
                PANEL_LIGHT,
                (x, 262),
                (x + letter_width - 5, 262),
                3,
            )
            shown = letter in self.guessed or (self.finished and not self.won)
            if shown:
                color = GREEN if self.won else TEXT
                draw_text(
                    self.screen,
                    self.word_font,
                    letter,
                    color,
                    (x + (letter_width - 5) // 2, 238),
                    center=True,
                )

    def draw_keyboard(self):
        for index, letter in enumerate(string.ascii_uppercase):
            rect = self.letter_rect(index)
            if letter not in self.guessed and not self.finished:
                color = PANEL_LIGHT
                text_color = TEXT
            elif letter in self.word:
                color = (22, 101, 75)
                text_color = GREEN
            else:
                color = (127, 49, 57)
                text_color = (254, 202, 202)

            pygame.draw.rect(self.screen, color, rect, border_radius=9)
            draw_text(
                self.screen,
                self.button_font,
                letter,
                text_color,
                rect.center,
                center=True,
            )

    def draw(self):
        self.screen.fill(BACKGROUND)
        draw_text(self.screen, self.title_font, "LE PENDU", TEXT, (45, 34))
        draw_text(
            self.screen,
            self.small_font,
            "Devine le mot, une lettre à la fois !",
            MUTED,
            (48, 82),
        )

        pygame.draw.rect(self.screen, PANEL_LIGHT, self.restart_rect, border_radius=12)
        draw_text(
            self.screen,
            self.button_font,
            "NOUVELLE PARTIE",
            TEXT,
            self.restart_rect.center,
            center=True,
        )

        self.draw_hangman()
        pygame.draw.rect(self.screen, PANEL, (445, 140, 410, 390), border_radius=18)
        self.draw_word()
        self.draw_keyboard()

        if self.won:
            message = "Bravo, tu as trouvé le mot !"
            message_color = GREEN
        elif self.finished:
            message = f"Perdu ! Le mot était {self.word}."
            message_color = RED
        else:
            message = "Clique sur une lettre ou tape-la au clavier."
            message_color = MUTED
        draw_text(self.screen, self.font, message, message_color, (450, 548))
        draw_text(
            self.screen,
            self.small_font,
            "Échap : quitter",
            MUTED,
            (48, 603),
        )
        if self.finished:
            draw_text(
                self.screen,
                self.small_font,
                "Espace ou R : rejouer",
                MUTED,
                (450, 603),
            )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event) and running
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    HangmanGame().run()
