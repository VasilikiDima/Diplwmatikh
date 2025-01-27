import pygame
import random

#μικρά κυκλάκια για εφέ γύρω από την φωτιά
class Particle:
    def __init__(self, pos, velocity, size, color,spawn_camera_pos):
        self.pos = pos
        self.velocity = velocity
        self.size = size
        self.color = color
        self.spawn_camera_pos = list(spawn_camera_pos)
        self.lifetime = 100

    def update(self,current_camera_x, current_camera_y):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        camera_dx = current_camera_x - self.spawn_camera_pos[0]
        camera_dy = current_camera_y - self.spawn_camera_pos[1]

        #print(f"Camera dx: {camera_dx}, camera dy: {camera_dy}")
        self.pos[0] += camera_dx
        self.pos[1] += camera_dy

        self.spawn_camera_pos[0] = current_camera_x
        self.spawn_camera_pos[1] = current_camera_y

        self.lifetime -= 1
        self.size *= 0.98

    def draw(self, screen,camera_position_x, camera_position_y):
        if self.lifetime > 0:
            screen_pos = (int(self.pos[0] - camera_position_x), int(self.pos[1] - camera_position_y))
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.size))

particles = []


