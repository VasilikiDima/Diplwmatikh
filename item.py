import pygame

class Item():
    def __init__(self,position,name):
        self.item_image = {'diamond': pygame.image.load('data/images/costumization/Design/icons/diamond.png').convert_alpha(),
            'life': pygame.image.load('data/images/costumization/Design/icons/life.png').convert_alpha()}
        self.name = name
        self.position = list(position)
        self.rect = pygame.Rect(self.position[0],self.position[1],15,15)
    def update(self,players_last_move,players_speed):
        if players_last_move == 'right':
            self.position[0] -= players_speed
            self.rect.x = self.position[0]
        elif players_last_move == 'left':
            self.position[0] += players_speed
            self.rect.x = self.position[0]
        elif players_last_move == 'up':
            self.position[1] += players_speed
            self.rect.y = self.position[1]
        elif players_last_move == 'down':
            self.position[1] -= players_speed
            self.rect.y = self.position[1]
    def render(self,screen):
        screen.blit(self.item_image.get(self.name), (self.position[0], self.position[1]))
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
