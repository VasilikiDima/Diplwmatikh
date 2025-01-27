import pygame
from sprite import SpriteSheet
from utils import *
from projectile import *
# Constants
SPRITE_SIZE = 32
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 53
ANIMATION_DURATION = 7
SPEED = 3

collition_bounds= {'house_small':[40,0,-80,-70],
                   'house_big':[30,0,-70,-110],
                   'shop':[64,0,-140,-60],
                   'lamp':[50,0,-100,-50],
                   'tree':[48,0,-96,-84],
                   'rock8_down':[55,0,-105,-64],
                   'rock8_up':[0,0,-50,0],
                   'water':[45,20,-90,-100],
                   'col_dirt_wall':[12,0,-22,-60],
                   'tall_dirt':[12,0,-22,-100],
                   'fence':[20,0,-40,-60],
                   'well':[60,0,-120,-90],
                   'chest':[0,0,0,-60],
                   'campfire':[15,10,-30,-40]
                   }

class Direction:
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'
    UP = 'up'
OFFSET = 8

class Player:
    def __init__(self, starting_pos, camera_x, camera_y):

        self.speed = 3
        self.player_pos = list(starting_pos)
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.rect = pygame.Rect(self.player_pos[0]-OFFSET, self.player_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)

        self.image = pygame.image.load('data/images/character.png').convert_alpha()
        self.image = pygame.image.load('data/images/character5.png').convert_alpha()

        sprite_sheet = SpriteSheet(self.image)
        self.animations = self.load_animations(sprite_sheet)

        self.direction = Direction.DOWN
        self.animate = False
        self.walk_count = 0
        self.monsters = []

        self.health = 50
        self.max_health = 50
        self.health_bar = 50
        self.alive = True
        #self.knockback = False
        #self.knockback_direction = 0
        #self.knockbakck_distance = 150
        self.damage_countdown = 10


        #plhktro, isActive, color, damage, cooldown isws
        self.powers = [Projectile(0, self.player_pos,1, 5,50,(255,0,0), 1000,10),Projectile(1, self.player_pos,10, 5,15,(255,0,0), 50,30)]
        #self.rect1 = self.image.get_rect(topleft=(self.player_pos[0], self.player_pos[1]))

    def load_animations(self, sprite_sheet):
        '''animations = {
            Direction.DOWN: [sprite_sheet.get_image(i, 0, SPRITE_SIZE, SPRITE_SIZE, 3) for i in [2, 1, 3, 1]],
            Direction.RIGHT: [sprite_sheet.get_image(i, 2, SPRITE_SIZE, SPRITE_SIZE, 3) for i in range(4)],
            Direction.LEFT: [sprite_sheet.get_image(i, 6, SPRITE_SIZE, SPRITE_SIZE, 3) for i in range(4)],
            Direction.UP: [sprite_sheet.get_image(i, 4, SPRITE_SIZE, SPRITE_SIZE, 3) for i in [2, 1, 3, 1]]
        }'''
        animations = {
            Direction.DOWN: [sprite_sheet.get_image(i, 0, 128, 128, 0.5) for i in range(4)],
            Direction.RIGHT: [sprite_sheet.get_image(i, 2, 128, 128, 0.5) for i in range(4)],
            Direction.LEFT: [sprite_sheet.get_image(i, 1, 128, 128, 0.5) for i in range(4)],
            Direction.UP: [sprite_sheet.get_image(i, 3, 128, 128, 0.5) for i in range(4)]
        }
        return animations

    def update_rect(self):
        self.rect.topleft = (self.player_pos[0]-OFFSET, self.player_pos[1])
    def get_rect(self):
        return self.rect
    def render(self, screen,monsters):
        #print(self.camera_x, self.camera_y)
        self.update_rect()

        current_animation = self.animations[self.direction]
        if self.animate:
            frame = current_animation[self.walk_count // ANIMATION_DURATION]
            self.walk_count = (self.walk_count + 1) % (ANIMATION_DURATION * len(current_animation))
        else:
            frame = current_animation[2]

        screen.blit(frame, (self.player_pos[0] - 18, self.player_pos[1] - 8))
        #players rect, i want it when making the collisions
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

        for power in self.powers:
            if power.isActive:
                power.draw(screen)

        health_ratio = self.health / self.max_health
        current_bar_length = int(self.health_bar * health_ratio)

        pygame.draw.rect(screen, (255, 0, 0), (self.player_pos[0]-10, self.player_pos[1]-20, self.health_bar, 10))

        pygame.draw.rect(screen, (0, 255, 255), (self.player_pos[0]-10, self.player_pos[1]-20, current_bar_length, 10))


    def checkCollistion(self, newPosx, newPosy, object_layer,object_layer_collidable,monsters):
        #new_player_rect = pygame.Rect(newPosx+3, newPosy+4, self.rect.width-6, self.rect.height-5)
        new_player_rect = pygame.Rect(newPosx, newPosy,self.rect.width, self.rect.height)
        #print(self.getClusterRects(object_layer))

        tile_x1 = new_player_rect.left // TILESET_SIZE
        tile_y1 = new_player_rect.top // TILESET_SIZE
        tile_x2 = new_player_rect.right // TILESET_SIZE
        tile_y2 = new_player_rect.bottom // TILESET_SIZE

        for test in object_layer_collidable:
            collition_rect = pygame.Rect(test.x, test.y, test.width, test.height)
            if new_player_rect.colliderect(collition_rect):
                # print("Collision detected from object!")
                return True
        monster_player_rect = pygame.Rect(newPosx - self.camera_x, newPosy - self.camera_y, self.rect.width,
                                          self.rect.height)
        return False

    def player_monster_collision(self,newPosx,newPosy,monsters):
        monster_player_rect = pygame.Rect(newPosx - self.camera_x, newPosy - self.camera_y, self.rect.width,
                                          self.rect.height)
        # print(self.getClusterRects(object_layer))
        for monster in monsters:
            if monster[2] > 0:
                collition_rect = pygame.Rect(monster[0]+60, monster[1]+45, 80, 60)
                if monster_player_rect.colliderect(collition_rect):
                    #print("Collision detected with monster from player!")
                    return True

    def check_larvea_collision(self,attack):
        collision_player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], self.rect.width, self.rect.height)
        collition_attack = pygame.Rect(attack[0], attack[1], 80, 80)
        if collision_player_rect.colliderect(collition_attack):
            self.health -= 5

    def attack(self,key):
        if not self.powers[key].isActive:
            self.powers[key].set_active(self.player_pos,self.direction)
    def update(self, keys, map_width, map_height, object_layer, keys_released,object_layer_collidable,monsters):
        if self.camera_x < 3895 and self.camera_y <700:
            if self.health < 50:
                self.health += 1
        if self.damage_countdown == 0:
            self.damage_countdown = 10
            #print(self.damage_countdown)
        elif self.damage_countdown < 10:
            self.damage_countdown -= 1
            self.collisiton_damage()
        to_be_returned = [None,None]
        if keys[pygame.K_LEFT]:
            self.direction = 'left'
            self.animate = True

            if not self.checkCollistion(self.player_pos[0] - SPEED + self.camera_x, self.player_pos[1] + self.camera_y,
                                        object_layer,object_layer_collidable,monsters):
                if self.player_monster_collision(self.player_pos[0] - SPEED + self.camera_x,
                                                 self.player_pos[1] + self.camera_y, monsters):
                    to_be_returned = ['left', True]
                    self.damage_countdown -= 1
                    self.collisiton_damage()
                else:
                    to_be_returned = ['left', False]
                if self.player_pos[0] > WINDOW_WIDTH // 2:
                    self.player_pos[0] -= SPEED
                else:
                    if self.camera_x - SPEED > 0:
                        self.camera_x -= SPEED
                    else:
                        self.camera_x = 0
                        if self.player_pos[0] - SPEED > 0:
                            self.player_pos[0] -= SPEED
                        else:
                            self.player_pos[0] = 0
        elif keys[pygame.K_RIGHT]:
            self.direction = 'right'

            self.animate = True


            if not self.checkCollistion(self.player_pos[0] + SPEED + self.camera_x, self.player_pos[1] + self.camera_y,
                                        object_layer,object_layer_collidable,monsters):
                if self.player_monster_collision(self.player_pos[0] + SPEED + self.camera_x,
                                                 self.player_pos[1] + self.camera_y, monsters):
                    to_be_returned = ['right', True]
                    self.damage_countdown -= 1
                    self.collisiton_damage()

                else:
                    to_be_returned = ['right', False]
                if self.player_pos[0] < WINDOW_WIDTH // 2:
                    self.player_pos[0] += SPEED
                else:
                    if self.camera_x + SPEED < map_width - WINDOW_WIDTH:
                        self.camera_x += SPEED
                    else:
                        self.camera_x = map_width - WINDOW_WIDTH
                        if self.player_pos[0] + SPEED > WINDOW_WIDTH - 30:
                            self.player_pos[0] = WINDOW_WIDTH - 30
                        else:
                            self.player_pos[0] += SPEED
        elif keys[pygame.K_UP]:
            self.direction = 'up'
            self.animate = True

            if not self.checkCollistion(self.player_pos[0] + self.camera_x, self.player_pos[1] + self.camera_y - SPEED,
                                        object_layer,object_layer_collidable,monsters):
                if self.player_monster_collision(self.player_pos[0] + self.camera_x,
                                                 self.player_pos[1] + self.camera_y - SPEED, monsters):
                    to_be_returned = ['up', True]
                    self.damage_countdown -= 1
                    self.collisiton_damage()
                else:
                    to_be_returned = ['up', False]
                if self.player_pos[1] > WINDOW_HEIGHT // 2:
                    self.player_pos[1] -= SPEED
                else:
                    if self.camera_y - SPEED > 0:
                        self.camera_y -= SPEED
                    else:
                        self.camera_y = 0
                        if self.player_pos[1] - SPEED > 0:
                            self.player_pos[1] -= SPEED
                        else:
                            self.player_pos[1] = 0
        elif keys[pygame.K_DOWN]:
            self.direction = 'down'
            self.animate = True
            if not self.checkCollistion(self.player_pos[0] + self.camera_x, self.player_pos[1] + self.camera_y + SPEED,
                                        object_layer,object_layer_collidable,monsters) :
                if self.player_monster_collision(self.player_pos[0] + self.camera_x, self.player_pos[1] + self.camera_y + SPEED, monsters):
                    to_be_returned = ['down', True]
                    self.damage_countdown -= 1
                    self.collisiton_damage()
                else:
                    to_be_returned = ['down', False]
                if self.player_pos[1] < WINDOW_HEIGHT // 2:
                    self.player_pos[1] += SPEED
                else:
                    if self.camera_y + SPEED < map_height - WINDOW_HEIGHT:
                        self.camera_y += SPEED
                    else:
                        camera_y = map_height - WINDOW_HEIGHT
                        if self.player_pos[1] + SPEED > WINDOW_HEIGHT - 40:
                            self.player_pos[1] = WINDOW_HEIGHT - 40
                        else:
                            self.player_pos[1] += SPEED
        if keys_released[pygame.K_DOWN] or keys_released[pygame.K_UP] or keys_released[pygame.K_RIGHT] or keys_released[pygame.K_LEFT]:
            self.animate = False
        for power in self.powers:
            #if power.isActive:
            power.update(to_be_returned[0],self.speed)
        return to_be_returned
    def collisiton_damage(self):
        if self.damage_countdown == 0:
            self.health -= 1
            self.damage_countdown = 10

    def get_position(self):
        return self.player_pos
    def do_knockback(self,monsters):
        if self.knockbakck_distance > 0:
            if not self.player_monster_collision(self.player_pos[0]+ self.knockback_direction*10 + self.camera_x,self.player_pos[1] + self.camera_y + SPEED, monsters):
                self.camera_x += self.knockback_direction*10
                self.knockbakck_distance -=10

            else:
                self.knockbakck_distance -= 10
        else:
            self.knockback = False
            self.knockback_direction = 0
            self.knockbakck_distance = 150
    def take_damage(self,damage):
        self.health -= damage[0]

'''if self.direction == 'up':
    if new_player_rect.top <= new_cluster.bottom:
        print("collide_bottom")
        return True
if self.direction == 'down':
    if new_player_rect.bottom >= new_cluster.top:
        print("collide_top")
        return True
if self.direction == 'right':
    if new_player_rect.right >= new_cluster.left :  # +30
        print("collide_right")
        return True
if self.direction == 'left':
    if new_player_rect.left <= new_cluster.right:
        print("collide_left")
        return True'''