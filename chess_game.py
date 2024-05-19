import pygame
import chess
import os

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

# Constants for the board size
BOARD_SIZE = 8
SQUARE_SIZE = 80
BOARD_WIDTH = BOARD_HEIGHT = SQUARE_SIZE * BOARD_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
pygame.display.set_caption('Chess Assistant')

# Load images
pieces = {}
for piece in chess.PIECE_TYPES:
    for color in (chess.WHITE, chess.BLACK):
        piece_name = chess.piece_name(piece)
        color_prefix = 'w' if color == chess.WHITE else 'b'
        filename = f'{color_prefix}_{piece_name}.png'
        pieces[f'{color_prefix}_{piece_name}'] = pygame.transform.scale(
            pygame.image.load(os.path.join('images', filename)),
            (SQUARE_SIZE, SQUARE_SIZE)
        )

# Draw the board
def draw_board(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            color = colors[((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw the pieces on the board
def draw_pieces(screen, board):
    for i in range(BOARD_SIZE**2):
        piece = board.piece_at(i)
        if piece:
            color_prefix = 'w' if piece.color == chess.WHITE else 'b'
            piece_name = chess.piece_name(piece.piece_type)
            screen.blit(pieces[f'{color_prefix}_{piece_name}'], pygame.Rect((i % BOARD_SIZE) * SQUARE_SIZE, (i // BOARD_SIZE) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Main game loop
def main():
    clock = pygame.time.Clock()
    board = chess.Board()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
