# Written by Kento Hyono

# Import and initialize the pygame library
import pygame
from constants import *
from math import sqrt
from UIElement import *


def handle_keydown(keys):
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

def move_player(x, y, x_move, y_move):
    """
    Handle given x, y position and movements to avoid
    player to go out of the display.
    Return updated positions if moved.
    """
    # position: left, move: right, or position: right, move: left, or normal position
    if x < 1 and x_move > 0 or x > DISPLAY_WIDTH - PLAYER_WIDTH - 1 and x_move < 0 or 0 < x < DISPLAY_WIDTH - PLAYER_WIDTH: 
        x += x_move
    # position: top, move: down, or position: bottom, move up, or normal position
    if y < 1 and y_move > 0 or y > DISPLAY_WIDTH - PLAYER_WIDTH - 1 and y_move < 0 or 0 < y < DISPLAY_HEIGHT - PLAYER_HEIGHT: 
        y += y_move   
    return x, y

def collision_detect(rec_left, rec_top, rec_width, rec_height, cir_center_x, cir_center_y, radius):
    """
    Check whether rectangle (dvd logo) and circle (player) collide
    Return true if they collide; false otherwise.
    """
    rec_right = rec_left + rec_width
    rec_bottom = rec_top + rec_height
    cir_right = cir_center_x + radius
    cir_left = cir_center_x - radius
    cir_top = cir_center_y - radius
    cir_bottom = cir_center_y + radius

    # if don't collide at all
    if rec_right < cir_left or cir_right < rec_left or rec_bottom < cir_top or cir_bottom < rec_top:
        return False

    # Calculate the closest point on the rectangle to the circle
    closest_x = max(rec_left, min(cir_center_x, rec_right))
    closest_y = max(rec_top, min(cir_center_y, rec_bottom))

    # Calculate the distance between the closest point and the circle's center
    distance_x = closest_x - cir_center_x
    distance_y = closest_y - cir_center_y
    distance = sqrt(distance_x ** 2 + distance_y ** 2)

    # Check if the distance is less than or equal to the circle's radius
    if distance <= radius:
        return True

    return False  # no collision detected

def handle_collision(rec_x, rec_y, old_x_move, old_y_move, rec_width, rec_height, circle_center_x, circle_center_y):
    """
    Handle how the collided rectangle bounces by comparing position of each center points.
    Returns corresponding movement after the collision
    """
    x_move = old_x_move
    y_move = old_y_move
    if circle_center_x < rec_x:
        x_move = LOGO_SPEED
    if rec_x + rec_width < circle_center_x:
        x_move = -LOGO_SPEED
    if circle_center_y < rec_y:
        y_move = LOGO_SPEED
    if rec_y + rec_height < circle_center_y:
        y_move = -LOGO_SPEED

    return x_move, y_move


def fill(image, color):
    """
    Fill all pixels of the image with color, preserve transparency.
    """
    w, h = image.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = image.get_at((x, y))[3]
            image.set_at((x, y), pygame.Color(r, g, b, a))

def hit_corner(x, y, width, height):
    """
    Return true if dvd logo hits corner.
    """
    left, right = x, x + width
    top, bottom = y, y + height

    if left <= 0 and top <= 0:
        return True
    if right >= DISPLAY_WIDTH and top <= 0:
        return True
    if left <= 0 and bottom >= DISPLAY_HEIGHT:
        return True
    if right >= DISPLAY_WIDTH and bottom >= DISPLAY_HEIGHT:
        return True
    
    return False

def create_text(text, font_size, color):
    """
    Get text, apply font and size, then return it as a surface.
    """
    font = pygame.font.Font('Resource/ARCADECLASSIC.TTF', font_size)
    msg = font.render(text, 1, color)
    return msg.convert_alpha()

def play_again(screen: pygame.Surface, count, clock, dvd_logo):
    running = True
    replay_prompt = UIElement((350, 550), 'Play Again', 80, GRAY, GameAction.REPLAY)
    quit_prompt = UIElement((350, 650), 'Quit', 80, GRAY, GameAction.QUIT)

    while running:

        clock.tick(FPS)
        screen.fill(BG_COLOR)
        mouse_up = False
        # If user closes
        for event in pygame.event.get():
            if event == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

        screen.blit(dvd_logo, ((DISPLAY_WIDTH - LOGO_WIDTH) / 2, 200))
        result_msg = create_text(f'{count} hits', 100, GRAY)
        screen.blit(result_msg, (140, 380))

        if replay_prompt.update(pygame.mouse.get_pos(), mouse_up) is not None:
            return True
        if quit_prompt.update(pygame.mouse.get_pos(), mouse_up) is not None:
            return False        

        replay_prompt.draw(screen)
        quit_prompt.draw(screen)
        # Flip the display
        pygame.display.flip()
        pygame.display.update()
    return False