import pygame
import random

# Constants
CARD_WIDTH = 140
CARD_HEIGHT = 190
CARD_BACK = 'cards/cardBack_red3.png'

# Initialize Pygame
pygame.init()

# Load card images
def load_card_images():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_images = {}
    for suit in suits:
        for value in values:
            card_name = f'card{suit}{value}'
            card_images[card_name] = pygame.image.load(f'cards/{card_name}.png').convert()
    card_images['card_back'] = pygame.image.load(CARD_BACK).convert()
    return card_images

# Game logic functions
def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        if card[1] == 'A':
            ace_count += 1
            value += 11
        elif card[1] in ['J', 'Q', 'K']:
            value += 10
        else:
            value += int(card[1])
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1
    return value

def check_winner(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)
    
    if player_value > 21:
        return 'Dealer Wins'
    elif dealer_value > 21 or player_value > dealer_value:
        return 'Player Wins'
    elif player_value < dealer_value:
        return 'Dealer Wins'
    else:
        return 'Tie'
