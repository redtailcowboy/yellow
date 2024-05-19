import pygame
import sys
import random
import time
from card_loader import load_card_images, deal_card, check_winner, calculate_hand_value, CARD_WIDTH, CARD_HEIGHT
from learn import AIPlayer

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PAUSE_TIME = 0.001  # Pause for 1ms

# Initialize the AI player and win counters
ai_player = AIPlayer()
player_wins = 0
dealer_wins = 0
games_played = 0

# Function to represent the current game state
def get_game_state(player_hand, dealer_hand):
    return {
        'player_hand_value': calculate_hand_value(player_hand),
        'dealer_visible_card_value': calculate_hand_value([dealer_hand[1]]),
        'player_has_ace': any(card[1] == 'A' for card in player_hand),
    }

# Main game loop
def main():
    global player_wins, dealer_wins, games_played
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Blackjack')

    card_images = load_card_images()

    running = True
    while running:
        deck = [('Hearts', str(i)) for i in range(2, 11)] + \
               [('Hearts', j) for j in ['J', 'Q', 'K', 'A']] + \
               [('Diamonds', str(i)) for i in range(2, 11)] + \
               [('Diamonds', j) for j in ['J', 'Q', 'K', 'A']] + \
               [('Clubs', str(i)) for i in range(2, 11)] + \
               [('Clubs', j) for j in ['J', 'Q', 'K', 'A']] + \
               [('Spades', str(i)) for i in range(2, 11)] + \
               [('Spades', j) for j in ['J', 'Q', 'K', 'A']]
        random.shuffle(deck)

        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]

        game_round = True
        while game_round:
            game_state = get_game_state(player_hand, dealer_hand)
            action = ai_player.make_decision(game_state)
            if action == 'hit':
                player_hand.append(deal_card(deck))
                if calculate_hand_value(player_hand) > 21:
                    ai_player.record_decision(game_state, 'hit', 'lose')
                    dealer_wins += 1
                    print(f"Round {games_played + 1}: Dealer wins! Player busts with a hand value of {calculate_hand_value(player_hand)}.")
                    game_round = False
            elif action == 'stand':
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deal_card(deck))
                outcome = check_winner(player_hand, dealer_hand)
                ai_player.record_decision(game_state, 'stand', outcome)
                if outcome == 'win':
                    player_wins += 1
                    print(f"Round {games_played + 1}: Player wins with a hand value of {calculate_hand_value(player_hand)} against dealer's {calculate_hand_value(dealer_hand)}.")
                elif outcome == 'lose':
                    dealer_wins += 1
                    print(f"Round {games_played + 1}: Dealer wins with a hand value of {calculate_hand_value(dealer_hand)} against player's {calculate_hand_value(player_hand)}.")
                game_round = False

            screen.fill((0, 128, 0))

            for i, card in enumerate(player_hand):
                card_image = card_images[f'card{card[0]}{card[1]}']
                screen.blit(card_image, (50 + i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 10))

            for i, card in enumerate(dealer_hand):
                if i == 0:
                    screen.blit(card_images['card_back'], (50 + i * (CARD_WIDTH + 10), 10))
                else:
                    card_image = card_images[f'card{card[0]}{card[1]}']
                    screen.blit(card_image, (50 + i * (CARD_WIDTH + 10), 10))

            pygame.display.flip()

        # Update wins and games played
        games_played += 1

        # Pause for a short time
        time.sleep(PAUSE_TIME)

    pygame.quit()

if __name__ == '__main__':
    main()
