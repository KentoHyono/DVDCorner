# Import and initialize the pygame library
import pygame
from random import choice
from constants import *

# Initiate pygame and accept multiple keydown
pygame.init()
pygame.key.set_repeat(1, 10)
# Set up the drawing window
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# Load dvd logo and player images
dvd_logo = pygame.image.load('DVD_logo.png')
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (PLAYER_WIDTH, PLAYER_HEIGHT))


def _handle_keydown(keys):
    """
    Handle keydown. Also handles oblique movement. (multiple keydown)
    Return corresponding movements.
    """
    x_move = y_move = 0
    if keys[pygame.K_RIGHT]:
        x_move += PLAYER_SPEED
    if keys[pygame.K_LEFT]:
        x_move += -PLAYER_SPEED
    if keys[pygame.K_UP]:
        y_move += -PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        y_move += PLAYER_SPEED
    return x_move, y_move

def _move_player(x, y, x_move, y_move):
    """
    Handle given x, y position and movements to avoid
    player to go out of the display.
    Return updated positions if moved.
    """
    # position: left, move: right, or position: right, move: left, or normal position
    if x < 0 and x_move > 0 or x > DISPLAY_WIDTH - PLAYER_WIDTH and x_move < 0 or 0 < x < DISPLAY_WIDTH - PLAYER_WIDTH: 
        x += x_move
    # position: top, move: down, or position: bottom, move up, or normal position
    if y < 0 and y_move > 0 or y > DISPLAY_WIDTH - PLAYER_WIDTH and y_move < 0 or 0 < y < DISPLAY_HEIGHT - PLAYER_HEIGHT: 
        y += y_move   
    return x, y

# Run until the user asks to quit
def run():
    dvd_x = (DISPLAY_WIDTH - LOGO_WIDTH) / 2
    dvd_y = (DISPLAY_HEIGHT - LOGO_HEIGHT) / 2
    player_x = (DISPLAY_WIDTH - LOGO_WIDTH) / 2
    player_y = 100
    # Get random speed between -0.2 to 0.2
    logo_x_move = choice([-0.2, 0.2])
    logo_y_move = choice([-0.2, 0.2])

    running = True
    while running:
        # Fill the background with white
        screen.fill(WHITE)

        # If user closes
        if pygame.event.get(pygame.QUIT):
            running = False

        # Detect players keydown and move 
        keys = pygame.key.get_pressed()
        player_x_move, player_y_move = _handle_keydown(keys)
        player_x, player_y = _move_player(player_x, player_y, player_x_move, player_y_move)

        # Locate logo and player
        screen.blit(dvd_logo, (dvd_x, dvd_y))
        screen.blit(player, (player_x, player_y))
        
        # Move logo
        dvd_x += logo_x_move
        dvd_y += logo_y_move
    

        # When logo collides wall
        if dvd_x > DISPLAY_WIDTH and dvd_y > DISPLAY_HEIGHT:
            print('Clear!')
            running = False
        if dvd_x > DISPLAY_WIDTH - LOGO_WIDTH or dvd_x < 0:
            logo_x_move *= -1
            dvd_x += logo_x_move
        if dvd_y > DISPLAY_HEIGHT - LOGO_HEIGHT or dvd_y < 0:
            logo_y_move *= -1
            dvd_y += logo_y_move


        # Flip the display
        pygame.display.flip()
        pygame.display.update()

    # Done! Time to quit.
    pygame.quit()


if __name__ == '__main__':
    run()