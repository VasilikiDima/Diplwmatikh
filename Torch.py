import random
import pygame

class Torch:
    def __init__(self, pos, base_color, base_radius,spawn_camera_pos):
        self.pos = list(pos)
        self.base_color = base_color
        self.base_radius = base_radius
        self.current_radius = base_radius
        self.brightness_variation = 0
        self.count = 0
        self.lifetime = 100
        self.spawn_camera_pos = list(spawn_camera_pos)
        self.count = 0

    def update(self,current_camera_x, current_camera_y):
        if self.count %10==0:
            self.brightness_variation = random.uniform(-20, 20)
            flicker_radius = random.uniform(-5, 5)
            self.current_radius = self.base_radius + flicker_radius

        self.count +=1
        self.lifetime -= 1

        camera_dx = current_camera_x - self.spawn_camera_pos[0]
        camera_dy = current_camera_y - self.spawn_camera_pos[1]

        self.pos[0] += camera_dx
        self.pos[1] += camera_dy

        self.spawn_camera_pos[0] = current_camera_x
        self.spawn_camera_pos[1] = current_camera_y

    def draw(self, screen):
        flicker_color = (
            max(0, min(255, self.base_color[0] + self.brightness_variation)),
            max(0, min(255, self.base_color[1] + self.brightness_variation)),
            max(0, min(255, self.base_color[2] + self.brightness_variation)),
            255
        )

        pygame.draw.circle(screen, flicker_color, (int(self.pos[0]), int(self.pos[1])), int(self.current_radius))
