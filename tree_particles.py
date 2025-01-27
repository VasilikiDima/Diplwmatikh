import pygame
import random

#Τα φυλλαράκια που πέφτουν από τα δέντρα
class Leaf:
    def __init__(self,pos,velocity,size,speed,spawn_camera_pos):
        self.pos = pos
        self.size = size
        self.speed = speed
        self.lifetime = 100
        self.velocity = velocity
        self.leafs = [pygame.image.load('data/images/leaf/00.png').convert(),
                 pygame.image.load('data/images/leaf/01.png').convert(),
                 pygame.image.load('data/images/leaf/02.png').convert(),
                 pygame.image.load('data/images/leaf/03.png').convert(),
                 pygame.image.load('data/images/leaf/04.png').convert(),
                 pygame.image.load('data/images/leaf/05.png').convert(),
                 pygame.image.load('data/images/leaf/06.png').convert(),
                 pygame.image.load('data/images/leaf/07.png').convert(),
                 pygame.image.load('data/images/leaf/08.png').convert(),
                 pygame.image.load('data/images/leaf/09.png').convert(),
                 pygame.image.load('data/images/leaf/10.png').convert(),
                 pygame.image.load('data/images/leaf/11.png').convert(),
                 pygame.image.load('data/images/leaf/12.png').convert(),
                 pygame.image.load('data/images/leaf/13.png').convert(),
                 pygame.image.load('data/images/leaf/14.png').convert(),
                 pygame.image.load('data/images/leaf/15.png').convert(),
                 pygame.image.load('data/images/leaf/16.png').convert(),
                 pygame.image.load('data/images/leaf/17.png').convert()]
        for l in self.leafs:
            l.set_colorkey((0, 0, 0))
        self.count = 0
        self.spawn_camera_pos = list(spawn_camera_pos)

    def update(self,current_camera_x,current_camera_y):
        self.pos[0] -= self.velocity[0] * self.speed
        self.pos[1] -= self.velocity[1] * self.speed

        camera_dx = current_camera_x - self.spawn_camera_pos[0]
        camera_dy = current_camera_y - self.spawn_camera_pos[1]

        self.pos[0] += camera_dx
        self.pos[1] += camera_dy

        self.spawn_camera_pos[0] = current_camera_x
        self.spawn_camera_pos[1] = current_camera_y

        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            scaled_frame = pygame.transform.scale(self.leafs[self.count // 10], (int(self.size), int(self.size)))
            screen.blit(scaled_frame, (self.pos[0], self.pos[1]))
            self.count = (self.count + 1) % (10 * len(self.leafs))




