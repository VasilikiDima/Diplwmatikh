import pygame
import sys
from pytmx.util_pygame import load_pygame
import pytmx
from player import Player
from utils import *
from sprite import SpriteSheet
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from particles import *
from tree_particles import *
#from Torch import *
import random
from item_holders import *
from letters import *
from SpawnManager import *
from item import *
from Mission import *
from start_menu import *


#έχει όλο το game logic, collitions, render για τα πάντα κλπ

DEBAG = 0

collidable_layers_names = ['water','tree','campfire','lamp']

water_variants = {'0111':'center',
                  '0011':'left',
                  '0101':'right'}
WAVES_ANIMATION_DURATION = 120
LAMP_ANIMATION_DURATION = 10

MENU_CLOSE_DURATION = 5
MENU_CLOSE_OPTIONS_DURATION = 5
MENU_OPEN_DURATION = 5
MENU_OPEN_OPTIONS_DURATION = 5


class Game():
    def __init__(self):
        pygame.init()


        #self.font_path = "fonts\\basis33.ttf"
        #self.font_path = "fonts\\PressStart2P-Regular.ttf"
        self.font_path = "fonts\\Play-Regular.ttf"
        self.font_size = 15
        try:
            self.new_font = pygame.font.Font(self.font_path, self.font_size)
        except FileNotFoundError:
            print("Font file not found!")
        self.my_mission = Mission()


        self.game = 0
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        self.tmx_data = load_pygame('data\\tiled\\bigmap\\tmx\\big_map.tmx')
        self.background_image = pygame.image.load('data/map/background.png').convert_alpha()
        self.dummy_image = pygame.image.load('data/map/dummy with.png').convert_alpha()
        self.foreground_image = pygame.image.load('data/map/foreground.png').convert_alpha()


        pygame.display.set_caption("Κώδικοντ: Το Ξόρκι της Python")

        pygame.mixer.music.load('data/music/background.mp3')
        self.sound_completed = pygame.mixer.Sound('data/music/completed.wav')
        self.sound_coin = pygame.mixer.Sound('data/music/coin.wav')
        self.sound_click = pygame.mixer.Sound('data/music/click.wav')
        self.sound_click2 = pygame.mixer.Sound('data/music/click2.wav')
        self.sound_enemy = pygame.mixer.Sound('data/music/enemy.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)


        self.map_width = self.tmx_data.width * TILESET_SIZE
        self.map_height = self.tmx_data.height * TILESET_SIZE

        self.sprite_group = pygame.sprite.Group()

        self.transition = -50
        self.story = 0

        self.object_layer = []

        for name in collidable_layers_names:
            self.object_layer.append(self.tmx_data.get_layer_by_name(name))

        self.object_layer_waypoint = self.tmx_data.get_layer_by_name('waypoint')


        self.object_layer_collidable = self.tmx_data.get_layer_by_name('collidable')
        self.enemies_collision_layer = self.tmx_data.get_layer_by_name('larvea_collide')
        self.water_images = {'center':[pygame.image.load(f'data/images/water/center{str(i)}.png').convert_alpha() for i in range(1,9)],
                             'right': [pygame.image.load(f'data/images/water/right{str(i)}.png').convert_alpha() for i in range(1, 9)],
                             'left': [pygame.image.load(f'data/images/water/left{str(i)}.png').convert_alpha() for i in range(1, 9)],
                             'singleleft': [pygame.image.load(f'data/images/water/singleleft{str(i)}.png').convert_alpha() for i in range(1, 9)],
                             'singleright': [pygame.image.load(f'data/images/water/singleright{str(i)}.png').convert_alpha() for i in range(1, 9)]
                             }


        self.water_center = [pygame.image.load('data/images/water/center1.png').convert_alpha(),
                             pygame.image.load('data/images/water/center2.png').convert_alpha(),
                             pygame.image.load('data/images/water/center3.png').convert_alpha(),
                             pygame.image.load('data/images/water/center4.png').convert_alpha(),
                             pygame.image.load('data/images/water/center5.png').convert_alpha(),
                             pygame.image.load('data/images/water/center6.png').convert_alpha(),
                             pygame.image.load('data/images/water/center7.png').convert_alpha(),
                             pygame.image.load('data/images/water/center8.png').convert_alpha(),
                             pygame.image.load('data/images/water/center9.png').convert_alpha()
                             ]

        self.count_waves = 0
        self.water = []

        self.lamp_images = [pygame.image.load(f'data/images/lamp/lamp1.png').convert_alpha(),
                            pygame.image.load(f'data/images/lamp/lamp2.png').convert_alpha(),
                            pygame.image.load(f'data/images/lamp/lamp3.png').convert_alpha(),
                            pygame.image.load(f'data/images/lamp/lamp4.png').convert_alpha(),
                            pygame.image.load(f'data/images/lamp/lamp3.png').convert_alpha(),
                            pygame.image.load(f'data/images/lamp/lamp2.png').convert_alpha()]
        self.lamp_count = 0
        self.lamps = []

        self.campfire_image = pygame.image.load('data/images/Fire.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(self.campfire_image)
        self.campfire = [self.sprite_sheet.get_image(i, 0, 128,128, 0.5) for i in range(6)]
        self.fire_count = 0

        self.fire_particles = []
        self.tree_particles = []
        self.torches = []

        self.banner = pygame.image.load('data/images/banner.png').convert_alpha()

        self.menu_static = pygame.transform.scale(pygame.image.load('data/images/menu/Map Static/new.png').convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.menu_open = [pygame.transform.scale(pygame.image.load(f'data/images/menu/Map Open/{i}.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT))for i in range(0, 7)]
        self.menu_close = [pygame.transform.scale(pygame.image.load(f'data/images/menu/Map Close/{i}.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)) for i in range(0, 8)]
        self.menu_icons_open = [pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/open/{i}.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)) for i in range(0, 14)]
        self.menu_icons_close = [pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/close/{i}.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)) for i in range(0, 14)]
        self.menu_icons_change = [pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/change/{i}.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)) for i in range(1, 7)]
        self.inventory = {'diamond':pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/change/diamond.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)),
                          'empty':pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/change/empty.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT)),
                          'life':pygame.transform.scale(pygame.image.load(f'data/images/menu/With icons/change/life.png').convert_alpha(),(WINDOW_WIDTH, WINDOW_HEIGHT))}
        self.code_image = pygame.transform.scale(pygame.image.load('data/images/menu/With icons/change/code.png').convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dialog_image = pygame.transform.scale(pygame.image.load('data/images/menu/With icons/change/dialog.png').convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.menu_open_animation_count = 0
        self.menu_open_icons_animation_count = 0
        self.menu_close_animation_count = 0
        self.menu_close_icons_animation_count = 0
        self.letters = Letter()
        self.info,text_boxes = self.letters.render_text_with_font('Πάτα M για το Μενού',150,20)


        image_width, image_height = self.banner.get_size()

        self.max_stash_items = 19
        self.stash_current_draw = 1
        '''if self.mission <= 3:
            self.stash_current_draw = 0
        elif self.mission < 6:
            self.stash_current_draw = 4
        else: #isws 5 tha doume
            self.stash_current_draw = self.max_stash_items'''
        #ftiaxnw to poso einai to megethos tou stash analoga ta missions
        if self.my_mission.get_mission_id() <= 5:
            self.stash_current_draw = 0
        elif self.my_mission.get_mission_id() <= 7:
            self.stash_current_draw = 1
        elif self.my_mission.get_mission_id() <= 9:
            self.stash_current_draw = 3
        else:
            self.stash_current_draw = self.max_stash_items
        spacing = 34

        self.stash = [Item_holder(((WINDOW_WIDTH // 2) + ((i - (self.max_stash_items // 2)) * spacing), WINDOW_HEIGHT - 55)) for i in range(self.max_stash_items)]
        s = open('stash.txt', 'r')
        for i in range (19):
            self.stash[i].set_item(s.readline().replace('\n', ''))
        s.close()


        self.selected_item = 0
        self.stash[self.selected_item].select()

        self.info_images = [pygame.image.load('data/images/banner/left.png').convert_alpha(),
                            pygame.image.load('data/images/banner/center.png').convert_alpha(),
                            pygame.image.load('data/images/banner/right.png').convert_alpha()]

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Monotype Corsiva', 20)
        self.spawn_manager = None

        self.drops = []
        self.possible_drops = ["diamond", "life"]

        # gia drop chance, to megalitero einai pio pithano
        self.drop_weights = [10, 5]

        self.active_text_boxes = []
        self.active_text_boxes_index = 0
        self.code_instruction_textbox = []
        self.code_instruction_textbox_index = 0
        self.mission_drops = []

        self.start_menu = Start_menu()
        self.selected_button_big = pygame.image.load('data/images/costumization/Design/Buttons & Holders/start_screen_button_selected.png').convert_alpha()

        self.scriptio = pygame.image.load('data/images/scriptio.png').convert_alpha()
        self.hero = pygame.image.load('data/images/hero.png').convert_alpha()

        self.intro_char_index = 0
        self.intr = open('intro.txt', 'r',encoding="utf-8")


    def print_de(self,rect):
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
    def update(self, camera_x, camera_y, px, py, character,last_move):
        if not self.spawn_manager and self.my_mission.get_current_mission()["id"] >= 10:
            self.spawn_manager = SpawnManager(self.tmx_data,character.camera_x,character.camera_y,character.player_pos)
        self.sprite_group.empty()
        tempRect = []
        campfire_location = []
        if not self.mission_drops and self.my_mission.get_current_mission()["id"] in [3, 4, 5, 6, 7,8,9,10]:
            layer_mission =  self.tmx_data.get_layer_by_name('mission_drops')
            #print(layer_mission)

            for x in range(150):
                for y in range(100):
                    tile_id = layer_mission.data[y][x]
                    if tile_id != 0: # Αν το κελί είναι άδειο (0 = empty)
                        self.mission_drops.append(Item((x *TILESET_SIZE - camera_x,y *TILESET_SIZE - camera_y), 'diamond'))
            #print(len(self.mission_drops))
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'name') and hasattr(layer, 'data'):
                layer_name = layer.name
                #print(layer_name)
                if layer_name in collidable_layers_names:
                    for x in range(((px + camera_x) // TILESET_SIZE) - (WINDOW_WIDTH // 50),((px + camera_x) // TILESET_SIZE) + (WINDOW_WIDTH // 50)):
                        for y in range(((py + camera_y) // TILESET_SIZE) - (WINDOW_HEIGHT // 50),((py + camera_y) // TILESET_SIZE) + (WINDOW_HEIGHT // 50)):
                            if 0 <= x < layer.width and 0 <= y < layer.height:
                                tile_id = layer.data[y][x]
                                if tile_id != 0:

                                    if layer_name in collidable_layers_names:
                                        tempRect.append(pygame.Rect(x *TILESET_SIZE - camera_x, y *TILESET_SIZE - camera_y,64,64))

                                    if layer_name == 'campfire':
                                        campfire_location.append([x *TILESET_SIZE - camera_x, y *TILESET_SIZE - camera_y])
                                        if random.random() < 0.1:
                                            self.fire_particles.append(Particle([x *TILESET_SIZE - camera_x+random.randint(16,48), y *TILESET_SIZE - camera_y+random.randint(16,48)],
                                                         [random.uniform(-1, 1), random.uniform(-2, -0.5)],
                                                         random.randint(2, 4),
                                                         (random.randint(200,255), random.randint(50,100), 0),
                                                         (character.player_pos[0]*TILESET_SIZE-character.camera_x,character.player_pos[1]*TILESET_SIZE-character.camera_y)))
                                    if layer_name == 'tree':
                                        if layer.data[y][x-1] != 0 and layer.data[y][x-2] != 0 and layer.data[y][x-3] == 0 and layer.data[y+1][x] != 0:
                                            if random.random() < 0.15:
                                                self.tree_particles.append(Leaf(
                                                    [x * TILESET_SIZE - camera_x + random.randint(-64, 64),
                                                     y * TILESET_SIZE - camera_y + random.randint(-64, 0)],
                                                    [random.uniform(-1, 1), random.uniform(-2, -0.5)],
                                                    random.randint(1, 15),
                                                    random.uniform(0.1, 1.5),
                                                    (character.player_pos[0] * TILESET_SIZE - character.camera_x,
                                                     character.player_pos[1] * TILESET_SIZE - character.camera_y)
                                                ))
                                    if layer_name == 'water':
                                        up = '1' if layer.data[y-1][x]!=0 else '0'
                                        left = '1' if layer.data[y][x-1]!=0 else '0'
                                        right = '1' if layer.data[y][x+1] != 0 else '0'
                                        down = '1' if layer.data[y+1][x] != 0 else '0'
                                        variant = self.water_images.get(water_variants.get(up+left+right+down))
                                        if up+left+right+down in water_variants:
                                            self.water.append([variant, x * TILESET_SIZE - camera_x, y * TILESET_SIZE - camera_y])
                                        elif up+left == '11' and layer.data[y-1][x-1]==0 and layer.data[y][x+1]!=0 and layer.data[y+1][x]!=0:
                                            variant = self.water_images.get('singleright')
                                            self.water.append([variant, x * TILESET_SIZE - camera_x, y * TILESET_SIZE - camera_y])
                                        elif up+left+right+down == '1111' and layer.data[y-1][x+1]==0:
                                            variant = self.water_images.get('singleleft')
                                            self.water.append([variant, x * TILESET_SIZE - camera_x, y * TILESET_SIZE - camera_y])
                                        if x == 0 and layer.data[y - 1][x] == 0:
                                            variant = self.water_images.get(water_variants.get('0111'))
                                            self.water.append(
                                                [variant, x * TILESET_SIZE - camera_x, y * TILESET_SIZE - camera_y])
                                    if layer_name == 'lamp':
                                        self.lamps.append([x * TILESET_SIZE - camera_x, y * TILESET_SIZE - camera_y])
        if self.my_mission.get_current_mission()["id"] >= 10:
            damage = self.spawn_manager.update_spawns(character.player_pos,character.get_rect(),last_move,character.speed,character.camera_x, character.camera_y,self.enemies_collision_layer,self.enemies_collision_layer)
            if damage[0] > 0:
                character.take_damage(damage)

        if self.my_mission.get_current_mission()["id"] >= 10:
            larvea_attacks = self.spawn_manager.return_larvea_attack()
            for attack in larvea_attacks:
                if attack is not None:
                    self.sound_enemy.play()
                    character.check_larvea_collision(attack)
            self.spawn_manager.check_projectile_collision(character.powers)
        for drop in self.drops:
            drop.update(last_move,character.speed)
        if self.my_mission.get_current_mission()["id"] in [3,4,5,6,7,8,9,10]:
            for drop in self.mission_drops:
                drop.update(last_move,character.speed)
        if self.my_mission.get_current_mission()["id"] >= 10:
            for monster in self.spawn_manager.atrux:
                if monster.respawn_counter == 1000 and monster.life == 0:
                    random_drop = random.choices(self.possible_drops, weights=self.drop_weights, k=1)[0]
                    self.drops.append(Item((monster.position[0]+50,monster.position[1]+100),random_drop))

        self.draw_map(character.camera_x, character.camera_y, character.player_pos[0], character.player_pos[1], character, campfire_location,tempRect,last_move)
        self.draw_menu()

    #todo na to allaksw gia na koitaei to active stash
    def item_pickup(self,keys,character):
        if keys[pygame.K_z]:
            if self.my_mission.get_mission_id()>=10:
                for drop in self.drops:
                    if drop.rect.colliderect(character.get_rect()):
                        for s in self.stash:
                            if s.get_item() == 'empty':
                                s.set_item(drop.name)
                                self.sound_coin.play()
                                self.drops.remove(drop)
                                break
            if  self.my_mission.get_current_mission()["id"] in [6, 7, 8,9,10]:
                for drop in self.mission_drops:
                    if drop.rect.colliderect(character.get_rect()):
                        for s in range(self.stash_current_draw):
                            if self.stash[s].get_item() == 'empty':
                                self.stash[s].set_item(drop.name)
                                self.sound_coin.play()
                                self.mission_drops.remove(drop)
                                break


    def draw_map(self, camera_x, camera_y, px, py, character,campfire_location,tempRect,last_move):
        self.screen.blit(self.background_image, (-character.camera_x, -character.camera_y))

        for w in self.water:
            frame = w[0][self.count_waves // WAVES_ANIMATION_DURATION]
            self.count_waves = (self.count_waves + 1) % (WAVES_ANIMATION_DURATION * len(w[0]))
            self.screen.blit(frame, (w[1], w[2]))
        self.water.clear()

        self.screen.blit(self.dummy_image, (-character.camera_x, -character.camera_y))

        self.sprite_group.draw(self.screen)
        # to be remover
        if DEBAG == 1:
            for r in tempRect:
                pygame.draw.rect(self.screen, (255, 0, 0), r, 2)
                for i in [0, 12, 24, 36, 48]:
                    for j in [0, 12, 24, 36, 48]:
                        pygame.draw.rect(self.screen, (0, 250, 0), pygame.Rect(r.x + i, r.y + j, 12, 12), 1)

        for drop in self.drops:
            drop.render(self.screen)
        if self.my_mission.get_current_mission()["id"] in [3, 4, 5, 6, 7,8,9,10]:
            for drop in self.mission_drops:
                #print(f'draw drops {drop.position}')
                drop.render(self.screen)
        if self.my_mission.get_current_mission()["id"] >= 10:
            self.spawn_manager.draw_spawns_before_player(character.player_pos,self.screen,character.player_pos[0] * TILESET_SIZE - character.camera_x,
                     character.player_pos[1] * TILESET_SIZE - character.camera_y,last_move,character.speed)
        #TODO gia otan einai collided
        if character.damage_countdown == 10 or character.damage_countdown == 9 or character.damage_countdown == 5 or character.damage_countdown == 3:
            character.render(self.screen, self.get_monsters())
        if self.my_mission.get_current_mission()["id"] >= 10:
            self.spawn_manager.draw_spawns_after_player(character.player_pos,self.screen,character.player_pos[0] * TILESET_SIZE - character.camera_x,
                     character.player_pos[1] * TILESET_SIZE - character.camera_y,last_move,character.speed)

        for f in campfire_location:
            self.screen.blit(self.campfire[int(self.fire_count / 20)], (f[0], f[1] - 20))
            self.fire_count = (self.fire_count + 1) % (20 * len(self.campfire))

        self.sprite_group.empty()

        for p in self.fire_particles[:]:
            p.update(character.player_pos[0] * TILESET_SIZE - character.camera_x,
                     character.player_pos[1] * TILESET_SIZE - character.camera_y)
            if p.lifetime <= 0:
                self.fire_particles.remove(p)
        for p in self.fire_particles:
            p.draw(self.screen, character.player_pos[0] * TILESET_SIZE - character.camera_x,
                   character.player_pos[1] * TILESET_SIZE - character.camera_y)

        for l in self.tree_particles[:]:
            l.update(character.player_pos[0] * TILESET_SIZE - character.camera_x,
                     character.player_pos[1] * TILESET_SIZE - character.camera_y)
            if l.lifetime <= 0:
                self.tree_particles.remove(l)
        for l in self.tree_particles:
            l.draw(self.screen)

        for lamp in self.lamps:
            self.lamp_count = (self.lamp_count + 1) % (LAMP_ANIMATION_DURATION * len(self.lamp_images))
            self.screen.blit(self.lamp_images[self.lamp_count // LAMP_ANIMATION_DURATION], (lamp[0], lamp[1] - 128))
        self.lamps.clear()

        #print(character.player_pos,character.camera_x)

        self.screen.blit(self.foreground_image, (-character.camera_x, -character.camera_y))

    def get_monsters(self):
        try:
            return self.spawn_manager.get_monsters()
        except Exception as e:
            print(f"Error getting monsters: {e}")
            return []

    def draw_menu(self):
        pygame.draw.rect(self.screen, (89, 74, 33), pygame.Rect(0, WINDOW_HEIGHT-90, WINDOW_WIDTH, 100))

        image_width, image_height = self.banner.get_size()
        x = (WINDOW_WIDTH // 2) - (image_width // 2)
        y = WINDOW_HEIGHT-90
        self.screen.blit(self.banner, (x,y))

        font = pygame.font.SysFont(None, 20)
        text = font.render('Press S to save and M to open menu', True, (0, 0, 0))
        self.screen.blit(self.info, ((WINDOW_WIDTH // 2)-self.info.width//2, WINDOW_HEIGHT - 20))
        if self.my_mission.get_mission_id() <= 5:
            self.stash_current_draw = 0
        elif self.my_mission.get_mission_id() <= 7:
            self.stash_current_draw = 1
        elif self.my_mission.get_mission_id() <= 9:
            self.stash_current_draw = 3
        else:
            self.stash_current_draw = self.max_stash_items
        for s in range(self.stash_current_draw):
            self.stash[s].draw(self.screen)

    def select_item_right(self):
        self.stash[self.selected_item].unselect()
        self.selected_item = min(self.selected_item + 1, self.stash_current_draw - 1)
        self.stash[self.selected_item].select()
    def select_item_left(self):
        self.stash[self.selected_item].unselect()
        self.selected_item = max(self.selected_item - 1, 0)
        self.stash[self.selected_item].select()

    def open_options_panel(self,character,last_move):
        self.update(character.camera_x, character.camera_y,character.player_pos[0], character.player_pos[1],character,last_move)
        if  self.menu_open_animation_count // MENU_OPEN_DURATION !=6:
            self.menu_open_animation_count = (self.menu_open_animation_count + 1) % (MENU_OPEN_DURATION * len(self.menu_open))
            self.screen.blit(self.menu_open[self.menu_open_animation_count // MENU_OPEN_DURATION], (0,0))
        elif self.menu_open_icons_animation_count // MENU_OPEN_OPTIONS_DURATION !=13:
            self.menu_open_icons_animation_count = (self.menu_open_icons_animation_count + 1) % (MENU_OPEN_OPTIONS_DURATION * len(self.menu_icons_open))
            self.screen.blit(self.menu_icons_open[self.menu_open_icons_animation_count // MENU_OPEN_OPTIONS_DURATION], (0, 0))
        else:
            return False
        return True

    def reset_animation_counter(self):
        self.menu_open_animation_count = 0
        self.menu_open_icons_animation_count = 0
        self.menu_close_animation_count = 0
        self.menu_close_icons_animation_count = 0
    def draw_dialog_start(self,dialog_index):
        pygame.draw.rect(self.screen, (216,196,148), (0,450,800,400))
        if self.my_mission.get_current_mission()["dialogs"].get("start")[dialog_index].get('character') == 'scriptio':
            self.screen.blit(self.scriptio,(500,450))
        elif self.my_mission.get_current_mission()["dialogs"].get("start")[dialog_index].get('character') == 'hero':
            self.screen.blit(self.hero,(50,450))
        self.screen.blit(self.dialog_image, (0, 10))

        text = self.my_mission.get_current_mission()["dialogs"].get("start")[dialog_index].get('text')

        text_surface, text_boxes = self.letters.render_text_with_font(text, 700, 130)
        #text_surface,text_boxes = self.letters.render_text(text, 700, 130)
        self.screen.blit(text_surface, (50, 560))
        #pygame.draw.rect(self.screen, (255, 0, 0), (50, 550, 700, 120), 2)
    def start_menu_info(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))
        text = "Αυτό το παιχνίδι αναπτύχθηκε ως μέρος διπλωματικής εργασίας για το πρόγραμμα n n Πληροφοριακά Συστήματα και Ψηφιακή Καινοτομία του Πανεπιστημίου Νεάπολης n n Πάφου με στόχο να εισάγει μαθητές Γυμνασίου στον προγραμματισμό με την γλώσσα n n Python μέσα από μια διασκεδαστική ιστορία."
        text_surface, text_boxes = self.letters.render_text_with_font(text, 600, 300)
        self.screen.blit(text_surface, (100, 200))
        self.screen.blit(self.selected_button_big, (300, 600))
        text_surface, text_boxes = self.letters.render_text_with_font('Πίσω', 40, 16)
        image_width,image_height = self.selected_button_big.get_size()
        self.screen.blit(text_surface, (300+ (image_width - text_surface.get_width()) // 2, 600+ (image_height - text_surface.get_height()) // 2))
    def start_menu_directions(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))
        text = "Χρησιμοποίησε τα βελάκια για να κινηθείς n ^ n Πάτα Σ για αποθήκευση n ^ n"
        text_surface, text_boxes = self.letters.render_text_with_font(text, 300, 300)
        self.screen.blit(text_surface, (250, 200))
        self.screen.blit(self.selected_button_big, (300, 600))
        text_surface, text_boxes = self.letters.render_text_with_font('Πίσω', 40, 16)
        image_width,image_height = self.selected_button_big.get_size()
        self.screen.blit(text_surface, (300+ (image_width - text_surface.get_width()) // 2, 600+ (image_height - text_surface.get_height()) // 2))

    def draw_dialog_end(self,dialog_index):
        pygame.draw.rect(self.screen, (216, 196, 148), (0, 450, 800, 400))
        if self.my_mission.get_current_mission()["dialogs"].get("end")[dialog_index].get('character') == 'scriptio':
            self.screen.blit(self.scriptio,(600,450))
        elif self.my_mission.get_current_mission()["dialogs"].get("end")[dialog_index].get('character') == 'hero':
            self.screen.blit(self.hero,(50,450))
        self.screen.blit(self.dialog_image, (0, 10))
        text = self.my_mission.get_current_mission()["dialogs"].get("end")[dialog_index].get('text')

        text_surface,text_boxes = self.letters.render_text_with_font(text, 700, 130)
        self.screen.blit(text_surface, (50, 560))
        #pygame.draw.rect(self.screen, (255, 0, 0), (50, 550, 700, 120), 2)
    def draw_starting_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))
        self.start_menu.draw(self.screen)
    def draw_code(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))
        #pygame.draw.rect(self.screen, (255, 0, 0), (50, 50, 700, 600), 2)
        text_surface, text_boxes = self.letters.render_text_with_font(self.my_mission.get_current_mission()["code_task"].get("code_snippet"), 700,600)
        self.screen.blit(text_surface, (50,50))
        if  not self.active_text_boxes:
            for t in text_boxes:
                self.active_text_boxes.append(TextBox(t[0]+50,t[1]+55,15,15))
            self.active_text_boxes[0].change_active()
        for t in self.active_text_boxes:
            #print(t.rect)
            t.draw(self.screen)

        text_surface, text_boxes = self.letters.render_text_with_font("Πάτα F1 για να δεις τις οδηγίες και Εnter για να ελέγξεις τον κώδικά σου.", 700, 600)
        self.screen.blit(text_surface, (50, 650))
        #print(self.my_mission.get_current_mission()["code_task"].get("code_snippet"))
    def draw_code_mission_completed(self):
        self.screen.blit(self.dialog_image, (0, 10))
        text = self.my_mission.get_current_mission()["code_instuctions_2"]
        text_surface,text_boxes = self.letters.render_text_with_font(text, 700, 130)
        self.screen.blit(text_surface, (50, 560))
    def intro(self,):
        self.screen.blit(self.code_image, (0, 0))

        try:
            line = self.intr.readline()
        except:
            self.intr.close()
            return False
        if line == '':
            self.intr.close()
            return False

        current_text = ""
        char_delay = 5
        for char in line:
            current_text += char
            self.screen.blit(self.code_image, (0, 0))

            lines = current_text.split('`')
            y_offset = 250

            for i, text_line in enumerate(lines):
                text_surface = self.new_font.render(text_line, True, BLACK)
                self.screen.blit(text_surface, (50, y_offset + i * 60))

            pygame.display.flip()
            pygame.time.delay(char_delay)

            pygame.time.delay(char_delay)
        return True
        #completed_text, completed_intro
    def code_general(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))
        text = self.my_mission.get_current_mission()["code_general"]
        text_surface,text_boxes = self.letters.render_text_with_font(text, 700, 600)
        self.screen.blit(text_surface, (50, 50))
    def draw_code_instructions(self,index_instructions,completed):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.code_image, (0, 0))

        #self.screen.blit(self.dialog_image, (0, 10))
        text = self.my_mission.get_current_mission()["code_instuctions_1"][index_instructions]
        text_surface,text_boxes = self.letters.render_text_with_font(text, 700, 600)
        self.screen.blit(text_surface, (50, 50))

        if not self.code_instruction_textbox and text_boxes:
            self.code_instruction_textbox = []
            for t in text_boxes:
                self.code_instruction_textbox.append(TextBox(t[0]+50,t[1]+55,15,15))
                #print(t[0], t[1])
            self.code_instruction_textbox[0].change_active()
        if completed and text_boxes:
            for index,t in enumerate(self.my_mission.get_current_mission()["code_instuctions_1"][index_instructions+1]):
                #print(index)
                self.code_instruction_textbox[index].set_text(t)
        if text_boxes:
            for t in self.code_instruction_textbox:
                #print(t.rect)
                t.draw(self.screen)
        else:
            self.code_instruction_textbox.clear()
        return self.code_instruction_textbox
    def check_code(self):
        i = 0
        all_correct = True
        for answer in self.my_mission.get_current_mission()["code_task"].get("correct_answers"):
            if answer != self.active_text_boxes[i].text:
                all_correct = False
                self.active_text_boxes[i].set_wrong()
            i += 1
        return all_correct
    def check_code_instruction_answer(self,index_instructions):
        temp = ''
        for count,test in enumerate(self.code_instruction_textbox):
            temp  = temp + test.text
            if str(test.text) != str(self.my_mission.get_current_mission()["code_instuctions_1"][index_instructions + 1][count]):
                test.set_wrong()
        return str(temp) == str(self.my_mission.get_current_mission()["code_instuctions_1"][index_instructions + 1])


    def draw_options(self,character,page,last_move):
        self.update(character.camera_x, character.camera_y,character.player_pos[0], character.player_pos[1],character,last_move)
        self.screen.blit(self.menu_icons_change[page], (0, 0))
        if page == 0:
            text_surface,text_boxes = self.letters.render_text_with_font('ΠΛΗΚΤΡΑ', 80, 20)
            self.screen.blit(text_surface, ((WINDOW_WIDTH // 2) - 40, WINDOW_HEIGHT // 2 - 165))
            info = 'Πάτα Σ για αποθήκευση n ^ n Πάτα Α και Δ για να μετακινηθείς n ανάμεσα στα αντικείμενα n ^ n Πάτα Μ για να ανοίξεις n ή να κλείσεις το Μενού'
            text_surface,text_boxes = self.letters.render_text_with_font(info, 200, 270)
            self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT // 2 - 135))
        if page == 1:
            self.screen.blit(self.inventory.get(self.stash[self.selected_item].get_item()), (0, 0))
            text_surface,text_boxes = self.letters.render_text_with_font('Πληροφορίες', 150, 20)
            self.screen.blit(text_surface, ((WINDOW_WIDTH // 2) - 55, WINDOW_HEIGHT // 2 - 110))
            if self.stash[self.selected_item].get_item() != 'empty':
                text_surface,text_boxes = self.letters.render_text_with_font(self.stash[self.selected_item].get_description(), 200,230)
                self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT // 2 - 75))
                text_surface,text_boxes = self.letters.render_text_with_font(self.stash[self.selected_item].get_name(), 150,8)
                self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 77, WINDOW_HEIGHT // 2 - 170))
        if page == 3:
            text_surface,text_boxes = self.letters.render_text_with_font(self.my_mission.get_current_mission()["title"], 270,400)
            self.screen.blit(text_surface, (250, WINDOW_HEIGHT // 2 - 145))
            #pygame.draw.rect(self.screen, (255, 0, 0),(250, WINDOW_HEIGHT // 2 - 145, 270,400), 2)
            text_surface, text_boxes = self.letters.render_text_with_font(self.my_mission.get_current_mission()["description"], 270,500)
            self.screen.blit(text_surface, (250, WINDOW_HEIGHT // 2-100))
            #pygame.draw.rect(self.screen, (255, 0, 0),(250, WINDOW_HEIGHT // 2-100, 270,500), 2)
        if page == 4:
            info = 'Πάτα space ή enter για να ξεκινήσεις να προγραμματίζεις.'
            text_surface,text_boxes = self.letters.render_text_with_font(info, 270,500)
            self.screen.blit(text_surface, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 145))

    def close_options_panel(self,character,last_move):
        self.update(character.camera_x, character.camera_y,character.player_pos[0], character.player_pos[1],character,last_move)
        if self.menu_close_icons_animation_count // MENU_CLOSE_OPTIONS_DURATION !=13:
            self.menu_close_icons_animation_count = (self.menu_close_icons_animation_count + 1) % (MENU_CLOSE_OPTIONS_DURATION * len(self.menu_icons_close))
            self.screen.blit(self.menu_icons_close[self.menu_close_icons_animation_count // MENU_CLOSE_OPTIONS_DURATION], (0, 0))
        elif  self.menu_close_animation_count // MENU_CLOSE_DURATION !=7:
            self.menu_close_animation_count = (self.menu_close_animation_count + 1) % (MENU_CLOSE_DURATION * len(self.menu_close))
            self.screen.blit(self.menu_close[self.menu_close_animation_count // MENU_CLOSE_DURATION], (0,0))
        else:
            return False
        return True

    def use_item(self,character):
        if self.stash[self.selected_item].get_item() == 'life':
            character.health +=10
            self.stash[self.selected_item].set_item('empty')
    def all_diamonds(self):
        for item in self.stash:
            #print(item.get_name())
            if item.get_name() != 'κρυσταλλοσ':
                return False
        return True

    def save(self,character):
        try:
            with open('location.txt', 'w') as location:
                location.write(str(character.player_pos[0]) + '\n')
                location.write(str(character.player_pos[1]) + '\n')
                location.write(str(character.camera_x) + '\n')
                location.write(str(character.camera_y) + '\n')
                location.write(str(character.health) + '\n')
            print("Location saved successfully.")

            with open('stash.txt', 'w') as stash:
                for s in self.stash:
                    stash.write(str(s.item) + '\n')
            print("Stash saved successfully.")

            with open('mission.txt', 'w') as stash:
                stash.write(str(self.mission) + '\n')
            print("Mission saved successfully.")

            #font = pygame.font.SysFont(None, 35)
            #text = font.render('Game saved successfully', True, (0, 0, 0))
            text_surface,text_boxes = self.letters.render_text_with_font("To παιχνίδι αποθηκεύτηκε επιτυχώς!", 255, 35)
            self.screen.blit(self.info_images[0], ((WINDOW_WIDTH // 2) - 224, 28))
            self.screen.blit(self.info_images[1], ((WINDOW_WIDTH // 2) - 112, 28))
            self.screen.blit(self.info_images[1], ((WINDOW_WIDTH // 2), 28))
            self.screen.blit(self.info_images[2],((WINDOW_WIDTH // 2) + 112,28))
            #self.screen.blit(text, ((WINDOW_WIDTH // 2) - (text.get_width() // 2),50))
            self.screen.blit(text_surface,((WINDOW_WIDTH // 2) - (text_surface.get_width() // 2),57))
            #pygame.draw.rect(self.screen, (255, 0, 0), ((WINDOW_WIDTH // 2) - (text_surface.get_width() // 2),60, 255, 35), 2)
            self.my_mission.save_missions()
            pygame.display.update()

            pygame.time.delay(1500)


        except Exception as e:
            print(f"An error occurred: {e}")