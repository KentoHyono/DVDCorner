# Written by Kento Hyono

import pygame
from random import choice

from functions import *
from constants import *

# Run until the user asks to quit
def run():

    # Initiate pygame and accept multiple keydown, set title
    pygame.init()
    pygame.key.set_repeat(1, 10)
    pygame.display.set_caption('DVD Corner Game')
    # Set up the drawing window
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    # Clock for controlling fps
    clock = pygame.time.Clock()
    # Load dvd logo and player images
    dvd_logo = pygame.image.load('Resource/DVD_logo.png')
    player = pygame.image.load('Resource/player.png')
    player = pygame.transform.scale(player, (PLAYER_WIDTH, PLAYER_HEIGHT))
    # Load Sound effects
    hit_sound = pygame.mixer.Sound('Resource/hit.wav')

    collideCount = 0
    dvd_x = (DISPLAY_WIDTH - LOGO_WIDTH) / 2
    dvd_y = (DISPLAY_HEIGHT - LOGO_HEIGHT) / 2
    player_x = (DISPLAY_WIDTH - LOGO_WIDTH) / 2
    player_y = 100
    # Get random speed between -LOGO_SPEED to LOGO_SPEED
    logo_x_move = choice([-LOGO_SPEED, LOGO_SPEED])
    logo_y_move = choice([-LOGO_SPEED, LOGO_SPEED])
    # Change color of images
    fill(dvd_logo, WHITE)
    fill(player, WHITE)

    running = True

    while running:

        clock.tick(FPS)
        # Fill the background with white
        screen.fill(BG_COLOR)

        # Detect players keydown and move 
        keys = pygame.key.get_pressed()
        # When player and logo collide
        if collision_detect(dvd_x, dvd_y, LOGO_WIDTH, LOGO_HEIGHT, player_x + PLAYER_WIDTH / 2, player_y + PLAYER_HEIGHT / 2, 20):
            logo_x_move, logo_y_move = handle_collision(dvd_x, dvd_y, logo_x_move, logo_y_move, LOGO_WIDTH, LOGO_HEIGHT, player_x + PLAYER_WIDTH / 2, player_y + PLAYER_HEIGHT / 2)

            # TODO: if dvd logo gets stuck on edge by being pushed by player, 
            # both player and logo cannot move.
            
        # player cannot move if collided
        else:
            player_x_move, player_y_move = handle_keydown(keys)
            player_x, player_y = move_player(player_x, player_y, player_x_move, player_y_move)

        # Locate collision count, logo and player
        coll_msg = create_text(str(collideCount), 50, GRAY)
        screen.blit(coll_msg, (20, DISPLAY_HEIGHT - 60))
        screen.blit(dvd_logo, (dvd_x, dvd_y))
        screen.blit(player, (player_x, player_y))
        
        # Move logo
        dvd_x += logo_x_move
        dvd_y += logo_y_move
    
        # Check corners 
        running = not hit_corner(dvd_x, dvd_y, LOGO_WIDTH, LOGO_HEIGHT)

        # When logo collides wall
        if dvd_x > DISPLAY_WIDTH - LOGO_WIDTH or dvd_x < 0:
            pygame.mixer.Sound.play(hit_sound)
            logo_x_move *= -1
            dvd_x += logo_x_move
            collideCount += 1
            fill(dvd_logo, COLORS[collideCount % len(COLORS)][1])
        if dvd_y > DISPLAY_HEIGHT - LOGO_HEIGHT or dvd_y < 0:
            pygame.mixer.Sound.play(hit_sound)
            logo_y_move *= -1
            dvd_y += logo_y_move
            collideCount += 1
            fill(dvd_logo, COLORS[collideCount % len(COLORS)][1])

        # If user closes
        if pygame.event.get(pygame.QUIT):
            pygame.quit()


        # Flip the display
        pygame.display.flip()
        pygame.display.update()

    # Done! Display collision count and ask replay
    if play_again(screen, collideCount, clock, dvd_logo):
        run()
    else:
        pygame.quit()

if __name__ == '__main__':
    run()