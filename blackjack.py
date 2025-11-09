import pygame
import random
import copy

# ----------------------------------
# Global Variables
# ----------------------------------
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
game_deck_count = 4
records = [0, 0, 0]  # [Wins, Losses, Ties]


# GUI Initialization

pygame.init()
WIDTH, HEIGHT = 600, 900
FPS = 60
timer = pygame.time.Clock()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('BlackJack')
font = pygame.font.Font('freesansbold.ttf', 44)
small_font = pygame.font.Font('freesansbold.ttf', 28)
tiny_font = pygame.font.Font('freesansbold.ttf', 20)

# Game Functions

def card_value(card):
    """Return numerical value of a card."""
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)


def calculate_score(hand):
    """Calculates the best score for a hand (handles Ace as 1 or 11)."""
    total = sum([card_value(c) for c in hand])
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def deal_cards(current_hand, current_deck):
    """Deals a random card from deck to hand."""
    if len(current_deck) > 0:
        card = random.randint(0, len(current_deck) - 1)
        current_hand.append(current_deck[card])
        current_deck.pop(card)
    return current_hand, current_deck


def draw_button(color, border_color, rect, text, text_color='black', border_width=3, corner_radius=5):
    """Draws a button with text."""
    button = pygame.draw.rect(screen, color, rect, 0, corner_radius)
    pygame.draw.rect(screen, border_color, rect, border_width, corner_radius)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    screen.blit(text_surf, text_rect)
    return button


def draw_game_buttons(active, game_over):
    """Draws appropriate buttons depending on game state."""
    buttons = []
    if not active:
        deal = draw_button('white', 'green', [150, 20, 300, 100], 'Deal Hand')
        buttons.append(deal)
    elif not game_over:
        hit = draw_button('white', 'green', [20, 700, 250, 90], 'HIT')
        stand = draw_button('white', 'red', [330, 700, 250, 90], 'STAND')
        buttons.extend([hit, stand])
    else:
        new_round = draw_button('white', 'blue', [150, 700, 300, 90], 'Next Round')
        buttons.append(new_round)
    return buttons


def draw_scoreboard():
    """Displays win/loss/tie counter."""
    text = font.render(f"Win : {records[0]}  Loss : {records[1]}  Tie : {records[2]}", True, "white")
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(text, rect)


def draw_card(x, y, value, hidden=False):
    """Draws a single card with a rectangle background."""
    card_width, card_height = 70, 100
    rect = pygame.Rect(x, y, card_width, card_height)

    if hidden:
        pygame.draw.rect(screen, 'darkred', rect, border_radius=8)
        pygame.draw.rect(screen, 'black', rect, 2, border_radius=8)
        text = tiny_font.render("🂠", True, "white")
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    else:
        pygame.draw.rect(screen, 'white', rect, border_radius=8)
        pygame.draw.rect(screen, 'black', rect, 2, border_radius=8)
        text = small_font.render(value, True, "black")
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


def draw_hands(player, dealer, reveal=False):
    """Displays cards as rectangles with values."""
    start_x = 60
    spacing = 80

    # Dealer
    dealer_label = small_font.render("Dealer", True, "white")
    screen.blit(dealer_label, (start_x, 130))
    for i, card in enumerate(dealer):
        hidden = (i != 0 and not reveal)
        draw_card(start_x + i * spacing, 180, card, hidden)
    if reveal:
        score = calculate_score(dealer)
        dealer_score_text = small_font.render(f"Score: {score}", True, "yellow")
        screen.blit(dealer_score_text, (start_x, 290))

    # Player
    player_label = small_font.render("You", True, "white")
    screen.blit(player_label, (start_x, 380))
    for i, card in enumerate(player):
        draw_card(start_x + i * spacing, 430, card)
    score = calculate_score(player)
    player_score_text = small_font.render(f"Score: {score}", True, "cyan")
    screen.blit(player_score_text, (start_x, 540))


def check_winner(player, dealer):
    """Determines round result."""
    p_score = calculate_score(player)
    d_score = calculate_score(dealer)

    if p_score > 21:
        return "Bust! Dealer Wins"
    elif d_score > 21:
        return "Dealer Busts! You Win"
    elif p_score == d_score:
        return "Tie Game"
    elif p_score > d_score:
        return "You Win!"
    else:
        return "Dealer Wins"

# Main Game Loop
def main():
    run = True
    active = False
    initial_deal = False
    game_over = False
    message = ""
    game_deck = copy.deepcopy(one_deck) * game_deck_count
    my_hand = []
    dealer_hand = []

    while run:
        timer.tick(FPS)
        screen.fill((0, 100, 0))  # green felt background

        if initial_deal:
            my_hand, game_deck = deal_cards([], game_deck)
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards([], game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False

        draw_hands(my_hand, dealer_hand, reveal=game_over)
        draw_scoreboard()
        buttons = draw_game_buttons(active, game_over)

        if message:
            text = font.render(message, True, "white")
            rect = text.get_rect(center=(WIDTH // 2, 620))
            screen.blit(text, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                if not active and buttons and buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_over = False
                    message = ""
                    game_deck = copy.deepcopy(one_deck) * game_deck_count
                    my_hand = []
                    dealer_hand = []

                elif active and not game_over:
                    # HIT button
                    if buttons[0].collidepoint(event.pos):
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                        if calculate_score(my_hand) > 21:
                            message = "Bust! Dealer Wins"
                            records[1] += 1
                            game_over = True

                    # STAND button
                    elif buttons[1].collidepoint(event.pos):
                        while calculate_score(dealer_hand) < 17:
                            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                        result = check_winner(my_hand, dealer_hand)
                        message = result
                        if "You Win" in result:
                            records[0] += 1
                        elif "Tie" in result:
                            records[2] += 1
                        else:
                            records[1] += 1
                        game_over = True

                elif game_over and buttons and buttons[0].collidepoint(event.pos):
                    # Next Round
                    active = False
                    game_over = False
                    message = ""
                    my_hand = []
                    dealer_hand = []

        pygame.display.flip()

    pygame.quit()


# ----------------------------------
# Run Game
# ----------------------------------
if __name__ == "__main__":
    main()

