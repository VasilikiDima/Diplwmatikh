import pygame
from utils import *
from letters import *
class Start_menu():
    def __init__(self):
        self.button = pygame.image.load('data/images/costumization/Design/Buttons & Holders/start_screen_button.png').convert_alpha()
        self.selected_button = pygame.image.load('data/images/costumization/Design/Buttons & Holders/start_screen_button_selected.png').convert_alpha()
        self.active_image = self.button
        self.image_width, self.image_height = self.button.get_size()
        #self.x = (WINDOW_WIDTH//2) - (self.image_width // 2)
        #self.y = 200 - (self.image_height // 2)
        self.letters = Letter()
        self.buttons = [[(WINDOW_WIDTH//2) - (self.image_width // 2),100,self.letters.render_text_simple('ξεκινα το παιχνιδι', 130, 8)],
                        [(WINDOW_WIDTH//2) - (self.image_width // 2),200,self.letters.render_text_simple('οδηγιες', 50, 8)],
                        [(WINDOW_WIDTH//2) - (self.image_width // 2),300,self.letters.render_text_simple('πληροφοριες', 80, 8)],
                        [(WINDOW_WIDTH//2) - (self.image_width // 2),400,self.letters.render_text_simple('εξοδος', 50, 8)]]
        self.active_button = 0
    def move_down(self):
        self.active_button += 1
        if self.active_button >= len(self.buttons):
            self.active_button = 0
    def move_up(self):
        self.active_button -= 1
        if self.active_button < 0:
            self.active_button = len(self.buttons) - 1
    def draw(self, screen):
        for index, button in enumerate(self.buttons):
            if index == self.active_button:
                screen.blit(self.selected_button, (button[0], button[1]))
            else:
                screen.blit(self.button, (button[0], button[1]))
            screen.blit(button[2], (button[0]+ (self.image_width - button[2].get_width()) // 2, button[1]+ (self.image_height - button[2].get_height()) // 2))
            #pygame.draw.rect(screen, (255, 0, 0), (button[0]+ (self.image_width - button[2].get_width()) // 2, button[1]+ (self.image_height - button[2].get_height()) // 2, button[2].get_width(), button[2].get_height()), 2)
        #screen.blit(self.text_surface, (self.x + (self.image_width - self.text_surface.get_width()) // 2, self.y + (self.image_height - self.text_surface.get_height()) // 2))