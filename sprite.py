import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_x, frame_y, width, height, scale):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (frame_x * width, frame_y * height, width, height))
        sprite = pygame.transform.scale(sprite, (width * scale, height * scale))
        sprite.set_colorkey((0, 0, 0))
        return sprite