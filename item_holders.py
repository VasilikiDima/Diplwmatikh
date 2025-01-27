import pygame
from utils import *

#το stash του παίκτη

class Item_holder:
    def __init__(self,center):
        self.item_holder = pygame.image.load('data/images/costumization/Design/Buttons & Holders/item_holder.png').convert_alpha()
        self.selected_item_holder = pygame.image.load('data/images/costumization/Design/Buttons & Holders/selected_item_holder.png').convert_alpha()

        self.active_image = self.item_holder

        self.center = list(center)
        holder_image_width, holder_image_height = self.item_holder.get_size()
        self.holder_x = center[0] - (holder_image_width // 2)
        self.holder_y = center[1] - (holder_image_height // 2)


        self.items = {'diamond': pygame.image.load('data/images/costumization/Design/icons/diamond.png').convert_alpha(),
                      'life' :pygame.image.load('data/images/costumization/Design/icons/life.png').convert_alpha(),
                      'empty' :pygame.image.load('data/images/costumization/Design/icons/empty.png').convert_alpha()}
        self.item = 'empty'
        self.info = {'diamond':['κρυσταλλοσ',"Οι κρύσταλλοι είναι μαγικά n αντικείμενα που έχουν μέσα n τους αποθηκευμένη μαγεία n ~ n Χρησιμοποιούνται για να n τροφοδοτούν τις ασπίδες n ~ n Τους έχουν πάνω τους τα n τέρατα του Χάκερον"],
                     'life':['φιλτρο ζωησ','αν το πιεισ σε κανει να νοιωθεισ καλητερα n n ~ n n σου δινει συν δεκα ζωη'],
                     'empty':['','']
                     }
        item_image_width, item_image_height = self.items.get('empty').get_size()
        self.item_x =center[0] - (item_image_width // 2)
        self.item_y = center[1] - (item_image_height // 2)

    def set_item(self,item):
        self.item = item
    def get_item(self):
        return self.item
    def select(self):
        self.active_image = self.selected_item_holder
    def unselect(self):
        self.active_image = self.item_holder
    def get_name(self):
        return self.info.get(self.item)[0]
    def get_description(self):
        return self.info.get(self.item)[1]
    def draw(self, screen):
        screen.blit(self.active_image, (self.holder_x, self.holder_y))
        screen.blit(self.items.get(self.item), (self.item_x, self.item_y))

