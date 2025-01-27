import random

import pygame
from sprite import SpriteSheet
from utils import *

#Εδώ είναι τα δύο είδη εχθρών που έχω βάλει στο παιχνίδι.
#Στις αποστολές τελικά δεν χρησιμοποιήθηκαν, αλλά τα είχα φτιάξει.
#Αν φτάσετε και ολοκληρώσετε την τελευταία αποστολή, και ακολουθήσετε το μονοπάτι έξω από την πόλη θα τα βρείτε.
#Τα χτυπάτε με το πλήκτρο 1
class Direction:
    ATTACK_RIGHT = 'attack right'
    RIGHT = 'right'
    LEFT = 'left'
    ATTTACK_LEFT = 'attack left'

class Enemy:
    def __init__(self, position,starting_posistion):
        self.position = list(position)

        self.starting_position = list(starting_posistion)


        self.attack_range = 50

    def load_animations(self,sprite_sheet1,sprite_sheet2,ratio):
        animations = {
            Direction.RIGHT: [sprite_sheet2.get_image(i, 0, 192, 192, ratio) for i in range(4)],
            Direction.LEFT: [sprite_sheet1.get_image(i, 0, 192, 192, ratio) for i in range(4)],
            Direction.ATTACK_RIGHT: [sprite_sheet2.get_image(i, 1, 192, 192, ratio) for i in range(4)],
            Direction.ATTTACK_LEFT: [sprite_sheet1.get_image(i, 1, 192, 192, ratio) for i in range(4)]
        }
        return animations


    def render(self, screen,collision_rect,x,y,animations,direction,walk_count,animation_duration,new_player_position,last_move,character_speed):

        current_animation = animations[direction]

        frame = current_animation[walk_count // animation_duration]
        screen.blit(frame, (self.position[0],self.position[1]))
        walk_count = (walk_count + 1) % (animation_duration * len(current_animation))

        #pygame.draw.rect(screen,(255, 0, 0),(self.position[0]+50, self.position[1]+38, 90, 110),2)
        #pygame.draw.rect(screen, (255,0,0), (self.position[0]+60, self.position[1]+45, 80, 60),2)

        return walk_count
    def take_damage(self,damage):
        self.life -= damage

class Atrux(Enemy):
    def __init__(self, position,starting_posistion):
        super().__init__(position,starting_posistion)
        self.collision_rect = 1
        self.speed = 1
        self.attack = False
        self.attack_speed = 10
        self.damage = 1
        self.walk_count = 0
        self.count_moves = 200
        self.animation_duration = 10
        self.max_health = 100
        self.health_bar = 100
        self.temp_timer = 0
        self.attack_direction = 0
        self.life = 100
        self.respawn_counter = 1000
        self.image1 = pygame.image.load('data/images/enemies/Atrox.png').convert_alpha()
        sprite_sheet1 = SpriteSheet(self.image1)
        self.image2= pygame.image.load('data/images/enemies/Atrox2.png').convert_alpha()
        sprite_sheet2 = SpriteSheet(self.image2)

        self.animations = self.load_animations(sprite_sheet1,sprite_sheet2,1)
        self.direction  = self.random_direction()
        self.direction_changed = False

    def random_direction(self):
        r = random.randint(0,1)
        if r == 0:
            self.speed = abs(self.speed)
            return Direction.RIGHT
        else:
            self.speed = -abs(self.speed)
            return Direction.LEFT
    def will_move(self):
        if self.direction == 'left' or self.direction == 'attack left':
            return self.position[0] - self.speed,self.position[1]
        elif self.direction == 'right' or self.direction == 'attack right':
            return self.position[0] + self.speed,self.position[1]

    def charge_direction(self):
        if self.direction == 'left':
            self.direction = 'right'
        elif self.direction == 'right':
            self.direction = 'left'
        if self.direction == 'attack left':
            self.direction = 'attack right'
        elif self.direction == 'attack right':
            self.direction = 'attack left'

    def atrux_render(self,screen,player_position,last_move,character_speed):
        if self.life >0:
            self.walk_count = self.render(screen,self.collision_rect,self.position[0],self.position[1],self.animations,self.direction,self.walk_count,self.animation_duration,player_position,last_move,character_speed)
            health_ratio = self.life / self.max_health
            current_bar_length = int(self.health_bar * health_ratio)
            pygame.draw.rect(screen, (255,0,0), (self.position[0]+45, self.position[1]+30, self.health_bar, 8))
            pygame.draw.rect(screen, (0,255,255), (self.position[0]+45, self.position[1]+30, current_bar_length, 8))

    def move(self,last_move,character_speed):
        if last_move == 'right':
            self.position[0] -= character_speed
        elif last_move == 'left':
            self.position[0] += character_speed
        elif last_move == 'up':
            self.position[1] += character_speed
        elif last_move == 'down':
            self.position[1] -= character_speed
        if not self.attack:
            if self.count_moves > 0:
                self.count_moves -= 1
                self.position[0] += self.speed
            else:
                self.charge_direction()
                self.count_moves = 200
                self.speed *= -1
    def check_proximity(self,player_position,player_rect):
        player_rect = pygame.Rect(player_position[0], player_position[1], player_rect.width,player_rect.height)
        collition_rect = pygame.Rect(self.position[0], self.position[1]+50, 192, 80)
        if player_rect.colliderect(collition_rect):
            if player_position[0] < self.position[0] and self.direction == 'right':
                self.charge_direction()
                self.direction_changed = True
            elif player_position[0] > self.position[0] and self.direction == 'left':
                self.charge_direction()
                self.direction_changed = True
            return True
    def check_collision(self,player_position,player_rect):
        player_rect = pygame.Rect(player_position[0], player_position[1], player_rect.width,player_rect.height)
        collition_rect = pygame.Rect(self.position[0]+50, self.position[1]+38, 145, 110)
        if player_rect.colliderect(collition_rect):
            return True

    def start_attack(self):
        if self.direction == 'left':
            self.direction = 'attack left'
        elif self.direction == 'right':
            self.direction = 'attack right'
        self.attack = True
    def stop_attack(self):
        if self.direction_changed:
            self.charge_direction()
            self.direction_changed = False
        if self.direction == 'attack left':
            self.direction = 'left'
        elif self.direction == 'attack right':
            self.direction = 'right'
        self.attack = False


class Larvea(Enemy):
    def __init__(self, position,starting_posistion):
        super().__init__(position,starting_posistion)
        self.collision_rect = 1
        self.normal_speed = 8
        self.speed_x = 4
        self.speed_y = 4
        self.attack = False
        self.attack_speed = 10
        self.attack_cooldown = 500
        self.attack_x = 0
        self.attack_y = 0
        self.attack_duration = 500

        self.damage = 1
        self.walk_count = 0
        self.count_moves = 200
        self.animation_duration = 10
        self.max_health = 2
        self.health_bar = 2
        self.temp_timer = 0

        self.life = 2
        self.respawn_counter = 1000
        self.image1 = pygame.image.load('data/images/enemies/Larvea.png').convert_alpha()
        sprite_sheet1 = SpriteSheet(self.image1)
        self.image2= pygame.image.load('data/images/enemies/Larvea2.png').convert_alpha()
        sprite_sheet2 = SpriteSheet(self.image2)
        self.animations = self.load_animations(sprite_sheet1,sprite_sheet2,0.5)

        self.explosion_image = pygame.image.load('data/images/enemies/explosion.png').convert_alpha()
        sprite_sheet3 = SpriteSheet(self.explosion_image)
        self.explosion = [sprite_sheet3.get_image(i, 7, 64, 64, 1.25) for i in range(12)]
        self.explosion_duration = 3
        self.explosion_count = 0

        self.direction = Direction.RIGHT
        self.direction  = self.random_direction([1,2,3,4,5,6,7,8])
        self.direction_changed = False
    def random_direction(self,numbers):
        r = random.choice(numbers)

        if r == 1:
            self.speed_x = 0
            self.speed_y = - abs(self.normal_speed)
            return self.direction
        elif r == 2:
            self.speed_x = abs(self.normal_speed/2)
            self.speed_y = - abs(self.normal_speed/2)
            return Direction.RIGHT
        elif r == 3:
            self.speed_x = abs(self.normal_speed)
            self.speed_y = 0
            return Direction.RIGHT
        elif r == 4:
            self.speed_x = abs(self.normal_speed/2)
            self.speed_y = abs(self.normal_speed/2)
            return Direction.RIGHT
        elif r == 5:
            self.speed_x = 0
            self.speed_y = abs(self.normal_speed)
            return self.direction
        elif r == 6:
            self.speed_x = - abs(self.normal_speed/2)
            self.speed_y = abs(self.normal_speed/2)
            return Direction.LEFT
        elif r == 7:
            self.speed_x = - abs(self.normal_speed)
            self.speed_y = 0
            return Direction.LEFT
        elif r == 8:
            self.speed_x = - abs(self.normal_speed/2)
            self.speed_y = - abs(self.normal_speed/2)
            return Direction.LEFT
        #return Direction.LEFT
    def larvea_render(self,screen,player_position,last_move,character_speed):
        #pygame.draw.rect(screen, (255,0,0), (self.position[0]+30, self.position[1]+20, 35, 45),2)
        if self.life >0:
            self.walk_count = self.render(screen,self.collision_rect,self.position[0],self.position[1],self.animations,self.direction,self.walk_count,self.animation_duration,player_position,last_move,character_speed)
        if self.attack and self.attack_cooldown >= 464:
            screen.blit(self.explosion[int(self.explosion_count / self.explosion_duration)], (self.attack_x,self.attack_y))
            self.explosion_count = (self.explosion_count + 1) % (self.explosion_duration * len(self.explosion))
    def render_attack(self,screen):
        if self.attack and self.attack_cooldown >= 464:
            pygame.draw.rect(screen, (180,26,68), (self.attack_x, self.attack_y, 80, 80),2)
    def return_larvea_attack(self):
        if self.attack_cooldown == 464:
            return [self.attack_x, self.attack_y]
    def checkCollistion(self, newPosx, newPosy,object_layer_collidable,larvea_layer_collidable):
        new_rect = pygame.Rect(newPosx+10, newPosy,55, 65)
        for test in  larvea_layer_collidable:
            collition_rect = pygame.Rect(test.x, test.y, test.width, test.height)
            if new_rect.colliderect(collition_rect):
                if self.speed_x > 0 and self.speed_y > 0:
                    return [8,1,2]
                if self.speed_x < 0 and self.speed_y < 0:
                    return [3,4,5]
                if self.speed_x > 0 and self.speed_y < 0:
                    return [5,6,7]
                if self.speed_x < 0 and self.speed_y > 0:
                    return [1,2,3]
                if self.speed_x > 0:
                    return [6,7,8]
                if self.speed_x < 0:
                    return [2,3,4]
                if self.speed_y > 0:
                    return [8,1,2]
                else:
                    return [4,5,6]
        return None

    def check_proximity(self,player_position,player_rect):
        player_rect = pygame.Rect(player_position[0]-200, player_position[1]-200, player_rect.width+400,player_rect.height+400)
        collition_rect = pygame.Rect(self.position[0]+30, self.position[1]+20, 35, 45)
        if player_rect.colliderect(collition_rect):  # Check for collision
            if self.attack == False and self.attack_cooldown == 500:
                self.attack_cooldown -= 1
                self.attack = True
                self.attack_x = player_position[0]-20
                self.attack_y = player_position[1]-20
                self.explosion_count = 0
            if player_position[0] <= self.position[0] and player_position[1] <= self.position[1]:
                #self.direction = self.random_direction([3,5,4])
                return [3,5,4]
            elif player_position[0] <= self.position[0] and player_position[1] >= self.position[1]:
                #self.direction = self.random_direction([1,3,2])
                return [1,3,2]
            elif player_position[0] >= self.position[0] and player_position[1] <= self.position[1]:
                #self.direction = self.random_direction([7,5,6])
                return [7,5,6]
            elif player_position[0] >= self.position[0] and player_position[1] >= self.position[1]:
                #self.direction = self.random_direction([7,1,8])
                return [7,1,8]

        return None

    def move(self,last_move,character_speed,object_layer_collidable,camera_x,camera_y,player_position,player_rect,larvea_layer_collidable):
        if last_move == 'right':
            self.position[0] -= character_speed
            if self.attack and self.attack_cooldown >= 464:
                self.attack_x -= character_speed
        elif last_move == 'left':
            self.position[0] += character_speed
            if self.attack and self.attack_cooldown >= 464:
                self.attack_x += character_speed
        elif last_move == 'up':
            self.position[1] += character_speed
            if self.attack and self.attack_cooldown >= 464:
                self.attack_y += character_speed
        elif last_move == 'down':
            self.position[1] -= character_speed
            if self.attack and self.attack_cooldown >= 464:
                self.attack_y -= character_speed

        if self.attack_cooldown < 500:
            if self.attack_cooldown < 0:
                self.attack_cooldown = 500
                self.attack = False
            else:
                self.attack_cooldown -= 1

        new_direction = self.checkCollistion(self.position[0] + self.speed_x + camera_x, self.position[1] + self.speed_y + camera_y,object_layer_collidable,larvea_layer_collidable)
        #print(new_direction)
        proximity = self.check_proximity(player_position, player_rect)

        if  proximity is not None:
            self.direction = self.random_direction(proximity)

        if new_direction is not None:
            self.direction = self.random_direction(new_direction)

        self.position[0] += self.speed_x
        self.position[1] += self.speed_y
