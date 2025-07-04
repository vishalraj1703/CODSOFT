import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")


FONT = pygame.font.SysFont("Comic Sans MS", 36)
SMALL_FONT = pygame.font.SysFont("Comic Sans MS", 24)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
GREEN, RED = (0, 200, 0), (200, 0, 0)

class Button:
    def __init__(self, text, x, y, w, h, action=None, color=LIGHT_BLUE):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        txt = SMALL_FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def winner(p1, p2):
    if p1 == p2: return "Tie"
    if (p1, p2) in [("rock","scissors"), ("paper","rock"), ("scissors","paper")]: return "Player"
    return "Opponent"

game_state = "home"
mode = "computer"
win_limit = None
player_score = 0
opponent_score = 0
round_result = ""
player_choice = ""
opponent_choice = ""
waiting_for_p2 = False
player1_selected = False

home_buttons = [
    Button("Play", 260, 130, 180, 50, action="mode_select"),
    Button("2 Player", 260, 200, 180, 50, action="2player"),
    Button("Instructions", 260, 270, 180, 50, action="instructions"),
    Button("Quit", 260, 340, 180, 50, action="quit")
]

mode_buttons = [
    Button("1 Win", 260, 100, 180, 50, action=1),
    Button("2 Wins", 260, 160, 180, 50, action=2),
    Button("3 Wins", 260, 220, 180, 50, action=3),
    Button("5 Wins", 260, 280, 180, 50, action=5),
    Button("Endless", 260, 340, 180, 50, action=None)
]

back_button = Button("Main Menu", 20, 20, 140, 40, action="home")
choices = [Button("Rock", 100, 350, 140, 50, "rock", YELLOW), Button("Paper", 280, 350, 140, 50, "paper", YELLOW), Button("Scissors", 460, 350, 140, 50, "scissors", YELLOW)]
result_buttons = [Button("Play Again", 200, 300, 140, 50, "game", LIGHT_BLUE), Button("Main Menu", 380, 300, 140, 50, "home", LIGHT_BLUE)]
endless_exit_button = Button("End Game", 280, 420, 140, 40, "result", LIGHT_BLUE)

def main():
    global game_state, mode, win_limit, player_score, opponent_score
    global round_result, player_choice, opponent_choice, waiting_for_p2, player1_selected

    clock = pygame.time.Clock()

    while True:
        screen.fill((230, 230, 250))
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "home":
                    for btn in home_buttons:
                        if btn.is_clicked(pos):
                            if btn.action == "quit":
                                pygame.quit(); sys.exit()
                            elif btn.action == "2player":
                                mode = "2player"
                                game_state = "mode_select"
                            else:
                                mode = "computer"
                                game_state = btn.action

                elif game_state == "mode_select":
                    for btn in mode_buttons:
                        if btn.is_clicked(pos):
                            win_limit = btn.action
                            round_result = ""
                            game_state = "game"
                            if mode != "2player":
                                player_score = opponent_score = 0
                            waiting_for_p2 = mode == "2player"
                            player1_selected = False

                elif game_state == "instructions":
                    if back_button.is_clicked(pos):
                        game_state = "home"

                elif game_state == "game":
                    if win_limit is None and endless_exit_button.is_clicked(pos):
                        game_state = "result"
                    else:
                        for btn in choices:
                            if btn.is_clicked(pos):
                                if mode == "computer":
                                    player_choice = btn.action
                                    opponent_choice = random.choice(["rock", "paper", "scissors"])
                                    outcome = winner(player_choice, opponent_choice)
                                else:
                                    if not player1_selected:
                                        player_choice = btn.action
                                        round_result = "Player 1 selected. Now Player 2."
                                        player1_selected = True
                                        continue
                                    else:
                                        opponent_choice = btn.action
                                        outcome = winner(player_choice, opponent_choice)
                                        player1_selected = False

                                if mode == "computer" or outcome:
                                    if outcome == "Player":
                                        player_score += 1
                                        round_result = f"You Win! ({player_choice} vs {opponent_choice})"
                                    elif outcome == "Opponent":
                                        opponent_score += 1
                                        round_result = f"You Lose! ({player_choice} vs {opponent_choice})"
                                    else:
                                        round_result = f"It's a Tie! ({player_choice} vs {opponent_choice})"

                                    if win_limit and (player_score == win_limit or opponent_score == win_limit):
                                        game_state = "result"

                elif game_state == "result":
                    for btn in result_buttons:
                        if btn.is_clicked(pos):
                            if btn.action == "game":
                                round_result = ""
                                waiting_for_p2 = mode == "2player"
                                player1_selected = False
                                if mode != "2player":
                                    player_score = opponent_score = 0
                                game_state = "game"
                            elif btn.action == "home":
                                player_score = opponent_score = 0
                                game_state = "home"

        if game_state == "home":
            screen.blit(FONT.render("Rock Paper Scissors", True, PURPLE), (180, 50))
            for b in home_buttons: b.draw()

        elif game_state == "mode_select":
            screen.blit(FONT.render("Select Game Mode", True, PURPLE), (180, 30))
            for b in mode_buttons: b.draw()

        elif game_state == "instructions":
            screen.blit(FONT.render("Instructions", True, PURPLE), (200, 50))
            for i, line in enumerate([
                "Choose Rock, Paper, or Scissors.",
                "Rock beats Scissors, Scissors beats Paper, Paper beats Rock.",
                "Score a certain number of wins to finish the game.",
                "Endless mode continues until you exit manually.",
                "2 Player mode: each player selects in turn."
            ]):
                screen.blit(SMALL_FONT.render(line, True, BLACK), (60, 130 + i*40))
            back_button.draw()

        elif game_state == "game":
            s = SMALL_FONT.render(f"Player: {player_score}   Opponent: {opponent_score}", True, BLACK)
            screen.blit(s, (220, 40))
            screen.blit(SMALL_FONT.render(round_result, True, PURPLE), (50, 120))
            for b in choices: b.draw()
            if win_limit is None:
                endless_exit_button.draw()

        elif game_state == "result":
            final = "You Win!" if player_score > opponent_score else "You Lose!"
            screen.blit(FONT.render(final, True, GREEN if player_score > opponent_score else RED), (250, 100))
            screen.blit(SMALL_FONT.render(f"Final Score: You {player_score} - {opponent_score} Opponent", True, BLACK), (180, 180))
            for b in result_buttons: b.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
