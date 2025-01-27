import random
from enemy import *

#Χειρίζεται το spawn των εχθρών

class SpawnManager:
    def __init__(self,tmx_data,camera_x,camera_y,player_pos):
        self.tmx_data = tmx_data
        self.atrux_region_name = 'atrux'
        self.atrux = []
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.player_pos = list(player_pos)
        # Ανάκτηση των επιτρεπτών θέσεων για spawn από το atrux layer του Tiled
        self.valid_spawn_positions_Atrux = self.get_valid_spawn_positions('spawn_Atrux')
        self.new_valid_positions_Atrux = []
        for position in self.valid_spawn_positions_Atrux:
            temp = position
            enemy = Atrux((position[0] * TILESET_SIZE - self.camera_x, position[1] * TILESET_SIZE - self.camera_y),temp)

            self.atrux.append(enemy)
            self.new_valid_positions_Atrux.append([position[0] * TILESET_SIZE - self.camera_x, position[1] * TILESET_SIZE - self.camera_y,-100,100])
        self.atrux = sorted(self.atrux, key=lambda obj: obj.position[1])

        self.larvea = []
        self.valid_spawn_positions_Larvea = self.get_valid_spawn_positions('spawn_Larvea')
        self.new_valid_positions_Larvea = []
        for position in self.valid_spawn_positions_Larvea:
            temp = position
            enemy = Larvea((position[0] * TILESET_SIZE - self.camera_x, position[1] * TILESET_SIZE - self.camera_y),temp)

            self.larvea.append(enemy)
            self.new_valid_positions_Larvea.append([position[0] * TILESET_SIZE - self.camera_x, position[1] * TILESET_SIZE - self.camera_y,-100,100])
        self.larvea = sorted(self.larvea, key=lambda obj: obj.position[1])

    def get_valid_spawn_positions(self,layer_name):
        layer =  self.tmx_data.get_layer_by_name(layer_name)
        valid_positions = []
        for x in range(100):
            for y in range(100):
                tile_id = layer.data[y][x]
                if tile_id != 0:
                    valid_positions.append((x, y))
        return valid_positions
    def get_monsters(self):
        temp = []
        for a in self.atrux:
            temp.append([a.position[0],a.position[1],a.life])
        return temp
    def update_spawns(self,player_position,player_rect,last_move,character_speed,camera_x,camera_y,object_layer_collidable,larvea_layer_collidable):
        #print(self.valid_spawn_positions)
        #print(camera_x,camera_y)

        for a in self.atrux:
            if a.life > 0:
                if a.check_proximity(player_position,player_rect):
                    a.start_attack()
                else:
                    a.stop_attack()

                a.move(last_move,character_speed)
                if a.walk_count == 3 and a.attack:
                    '''if 'right' in a.direction:
                        a.position[0] -= 60
                    else:
                        a.position[0] += 60'''
                    return [5,a.direction]
            else:
                a.respawn_counter -= 1
            if a.respawn_counter == 0:

                a.life = 100
                a.position = [a.starting_position[0] * TILESET_SIZE - camera_x, a.starting_position[1] * TILESET_SIZE - camera_y]

                a.respawn_counter = 1000
        for l in self.larvea:
            l.move(last_move,character_speed,object_layer_collidable,camera_x,camera_y,player_position,player_rect,larvea_layer_collidable)

        return [0,0]
    def return_larvea_attack(self):
        if self.larvea:
            attacks = []
            for l in self.larvea:
                attacks.append(l.return_larvea_attack())
            return attacks
    def player_knockback(self,direction):
        for a in self.atrux:
            a.position[0] -=10 * direction

    def check_projectile_collision(self,players_powers):
        for power in players_powers:
            if power.isActive:
                for a in self.atrux:
                    collition_rect = pygame.Rect(a.position[0] + 70, a.position[1] + 38, 70, 110)
                    power_rect = pygame.Rect(power.position[0], power.position[1],power.size, power.size)
                    if power_rect.colliderect(collition_rect):
                        a.take_damage(power.damage)
                        power.destroy()


    def draw_spawns(self, player_position,screen,camera_x,camera_y,last_move,character_speed):
        for a in self.atrux:
            a.atrux_render(screen,player_position,last_move,character_speed)

    def draw_spawns_before_player(self, player_position, screen, camera_x, camera_y, last_move, character_speed):
        #for l in self.larvea:
        #    l.render_attack(screen)
        for a in self.atrux:
            if a.position[1] + 60 <= player_position[1]:
                a.atrux_render(screen, player_position, last_move, character_speed)
        for l in self.larvea:
            if l.position[1] + 60 <= player_position[1]:
                l.larvea_render(screen, player_position, last_move, character_speed)

    def draw_spawns_after_player(self, player_position, screen, camera_x, camera_y, last_move, character_speed):
        for a in self.atrux:
            if a.position[1] + 60 > player_position[1]:
                a.atrux_render(screen, player_position, last_move, character_speed)
        for l in self.larvea:
            if l.position[1] + 60 > player_position[1]:
                l.larvea_render(screen, player_position, last_move, character_speed)
        #για κάθε τι στις active lists : update
        # σε αυτό το update, ρωτάει τον enemy που έιναι να πάει, κοιτάει τον χάρτη και του απαντάει, πήγαινε οπότε set, change direction and reasking
        #if get_attack_range < apo apostash me paikth, kai get_attack = Fale: attack, else update attack kai check attack with player colistion




