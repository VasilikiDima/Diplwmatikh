import pygame
from sprite import SpriteSheet

class Projectile:
    def __init__(self, projectile_type, position,speed, damage,range,color, cooldown,size):
        self.projectile_type = projectile_type
        self.position = list(position)
        self.damage = damage
        self.range = range
        self.range_counter = range
        self.cooldown = cooldown
        self.cooldown_counter = cooldown
        self.speed = speed
        self.isActive = False
        self.color = color
        self.size = size
        self.projectile_image = pygame.image.load('data/images/projectiles/ice.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(self.projectile_image)
        self.projectile_animations = [self.sprite_sheet.get_image(0, 0, 192,192, 0.2),
                                      self.sprite_sheet.get_image(1, 0, 192,192, 0.2),
                                      self.sprite_sheet.get_image(2, 0, 192,192, 0.2),
                                      self.sprite_sheet.get_image(3, 0, 192,192, 0.2)]

    def set_active(self,position,last_move):
        #print(self.cooldown_counter)
        if (last_move == 'left' or last_move == 'right') and self.cooldown_counter == self.cooldown:
            self.isActive = True
            self.position = list(position)
            self.range_counter = self.range
            self.cooldown_counter -=1
            if last_move == 'left':
                self.speed = -abs(self.speed)
            else:
                self.speed = abs(self.speed)

    def destroy(self):
        self.isActive = False
        self.range_counter = 0
    def isActive(self):
        return self.isActive
    def update(self, players_last_move,players_speed):
        if self.isActive:
            if players_last_move == 'right':
                self.position[0] -= players_speed
            elif players_last_move == 'left':
                self.position[0] += players_speed
            elif players_last_move == 'up':
                self.position[1] += players_speed
            elif players_last_move == 'down':
                self.position[1] -= players_speed
            self.position[0] += self.speed
            self.range_counter -=1
            if self.range_counter <= 0:
                self.isActive = False
        if self.cooldown_counter < self.cooldown:
            self.cooldown_counter -= 1
        if self.cooldown_counter <= 0:
            self.cooldown_counter = self.cooldown
    def draw(self,screen):
        #έσπασα το range του attack σε ποσοστα για να έχω άλλη εικάνα ανά απόσταση
        percentage = self.range_counter / self.range

        if percentage >= 0.75:
            if self.speed > 0:
                screen.blit(self.projectile_animations[0], (self.position[0], self.position[1]))
            else:
                flipped_image = pygame.transform.flip(self.projectile_animations[0], True, False)
                screen.blit(flipped_image, (self.position[0], self.position[1]))
        elif percentage >=0.5:
            if self.speed > 0:
                screen.blit(self.projectile_animations[1], (self.position[0], self.position[1]))
            else:
                flipped_image = pygame.transform.flip(self.projectile_animations[1], True, False)
                screen.blit(flipped_image, (self.position[0], self.position[1]))
        elif percentage >=0.25:
            if self.speed > 0:
                screen.blit(self.projectile_animations[2], (self.position[0], self.position[1]))
            else:
                flipped_image = pygame.transform.flip(self.projectile_animations[2], True, False)
                screen.blit(flipped_image, (self.position[0], self.position[1]))
        else:
            if self.speed > 0:
                screen.blit(self.projectile_animations[3], (self.position[0], self.position[1]))
            else:
                flipped_image = pygame.transform.flip(self.projectile_animations[3], True, False)
                screen.blit(flipped_image, (self.position[0], self.position[1]))
        #pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size),2)




