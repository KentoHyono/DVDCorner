from pygame.sprite import Sprite
from enum import Enum

# UI element that works with mouseover. 
# Referenced from 'https://www.youtube.com/watch?v=zFBQJ9bU5kQ'
class UIElement(Sprite):

    def __init__(self, center_p, text, font_size, text_color, action=None):
        super().__init__()
        self.mouse_over = False

        from functions import create_text
        default_image = create_text(text, font_size, text_color)
        high_image = create_text(text, int(font_size * 1.1), text_color)

        self.images = [default_image, high_image]
        self.rects = [default_image.get_rect(center=center_p), high_image.get_rect(center=center_p)]
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]
    
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameAction(Enum):
    QUIT = 1
    REPLAY = 1