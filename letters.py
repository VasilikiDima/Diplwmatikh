import pygame
import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (105,105,105)
BLUE = (0, 0, 255)
BORDO= (150, 49, 38)
RED = (255, 0,0)
GREEN = (34, 117, 81)
pygame.font.init()
FONT = pygame.font.Font(None, 20)

#Η γενική της χρήση είναι για να παίρνει τα κείμενα που θέλω να γράψω στην οθόνη, και τον χώρο του "τετραγώνου" που θα εκτυπωθούν, και να σπάει τις λέξεις όπου χρειάζεται με -
#Αρχικά το χρησιμοποιούσα παντού γιατί στην αρχή αντί για έτοιμο font, έκατσα και ζωγράφισα τα γράμματα στο pixilart και φόρτωνα εικόνες.
#Τελικά τα πρώτα τεστ (αυτά που αναφέρω στο κεφάλαιο της υλοποίησης) έδειξαν ότι ήταν λίγο δυσανάγνωστα οπότε έβαλα font.
#Αυτή την στιγμή χρησιμοποιούνται μόνο στο loading screen με το που φορτώνει το παιχνίδι
class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ""
        self.active = False
    def set_text(self,t):
        self.text = t
    def change_active(self):
        self.active =  not self.active
        self.color = BLUE if self.active else GRAY
    def set_active(self, status: bool):
        self.active = status
        self.color = BLUE if self.active else GRAY
    def set_wrong(self):
        self.color = RED
    def reset_color(self):
        self.color = BLUE if self.active else GRAY
    def handle_event(self, event):
        if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
            return False
        if self.active:
            self.color = BLUE if self.active else GRAY
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_BACKSPACE:
                    self.text = ""
                else:
                    char = event.unicode
                    if len(char) == 1:
                        self.text = char
                        self.change_active()
                        return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = FONT.render(self.text, True, BLACK)
        screen.blit(
            text_surface,
            (
                self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                self.rect.y + (self.rect.height - text_surface.get_height()) // 2,
            ),
        )

class Letter:

    def __init__(self):
        self.letter_images = {}
        self.vowels = "αεηιουωaeiouy"
        self.consonants = "βγδζθκλμνξπρσςτφχψbcdfghjklmnpqrstvwxz!&;=']_0123456789()"
        self.decorations = '^~'
        #self.text_boxes = []
        for letter in self.vowels + self.consonants + "-" + self.decorations:
            self.letter_images[letter] = pygame.image.load(f'data/images/letter/{letter}.png')


        self.letter_images[' '] = pygame.Surface((3, 5), pygame.SRCALPHA)
        self.font_path = "fonts\\Play-Regular.ttf"
        # self.font_path = "fonts\\PressStart2P-Regular.ttf"
        # self.font_path = "fonts\\Play-Regular.ttf"
        self.color = BLACK
        self.font_size = 15
        try:
            self.font = pygame.font.Font(self.font_path, self.font_size)
        except FileNotFoundError:
            print("Font file not found!")

    def change_color(self,letter):
        if letter == 'c':
            if self.color == BLACK:
                self.color = BORDO
            else:
                self.color = BLACK
        if letter == 'p':
            if self.color == BLACK:
                self.color = GREEN
            else:
                self.color = BLACK
    def render_text_with_font(self, text, box_width, box_height):
        text_boxes = []
        surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        x, y = 0, 0
        words = text.split(' ')
        letter_height = 8
        for word in words:
            if word == 'n':
                y += self.font.get_height() + 3
                x = 0
                continue
            if word == 't':
                x += 50
                continue
            if word in ['^', '~']:
                image_width = self.letter_images[word].get_width()
                surface.blit(self.letter_images[word], ((box_width//2) - (image_width //2), y))
                y += letter_height + 3
                continue

            if word == '_':
                text_boxes.append([x, y])
                x += 18
                continue
            if word == 'c':
                self.change_color('c')
                continue
            if word == 'p':
                self.change_color('p')
                continue
            word_width = sum([self.font.size(char)[0] for char in word])

            if x + word_width > box_width:
                split_point = len(word) - 1
                for i in range(1, len(word)):
                    if word[i] in self.consonants and word[i - 1] in self.vowels:
                        split_point = i
                        break
                first_part = word[:split_point] + '-'
                second_part = word[split_point:]

                for char in first_part:
                    char_surface = self.font.render(char, True, self.color)
                    surface.blit(char_surface, (x, y))
                    x += char_surface.get_width()

                y += self.font.get_height() + 3
                x = 0

                for char in second_part:
                    char_surface = self.font.render(char, True, self.color)
                    surface.blit(char_surface, (x, y))
                    x += char_surface.get_width()
            else:
                for char in word:
                    char_surface = self.font.render(char, True, self.color)
                    surface.blit(char_surface, (x, y))
                    x += char_surface.get_width()

                x += self.font.size(' ')[0]

            if x >= box_width:
                x = 0
                y += self.font.get_height() + 3

            if y + self.font.get_height() > box_height:
                break

        return surface, text_boxes

    def render_text(self, text, box_width, box_height):
        text_boxes = []
        hyphen_image = self.letter_images['-']
        letter_height = 8

        surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        x, y = 0, 0

        words = text.split(' ')

        for word in words:
            if word == 'n':
                y += letter_height + 3
                x = 0
                continue
            if word == 't':
                y += letter_height + 3
                x = 50
                continue
            if word == '^' or word == '~':
                image_width = self.letter_images[word].get_width()
                surface.blit(self.letter_images[word], ((box_width//2) - (image_width //2), y))
                y += letter_height + 3
                continue
            if word == '_':
                text_boxes.append([x, y])
                x = x + 18
                continue

            word_width = sum([self.letter_images[char].get_width() for char in word])

            if x + word_width > box_width:
                split_point = len(word) - 1
                for i in range(1, len(word)):
                    if word[i] in self.consonants and word[i - 1] in self.vowels:
                        split_point = i
                        break

                first_part = word[:split_point] + '-'
                second_part = word[split_point:]


                first_part_width = sum([self.letter_images[char].get_width() for char in first_part])

                if x + first_part_width <= box_width:
                    for char in first_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1

                    y += letter_height + 3
                    x = 0

                    for char in second_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1
                    x+=6
                else:
                    y += letter_height + 3
                    x = 0

                    for char in first_part:
                        if char != '-':
                            surface.blit(self.letter_images[char], (x, y))
                            x += self.letter_images[char].get_width()+1

                    second_part = second_part+' '
                    for char in second_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1
            else:
                for char in word:
                    surface.blit(self.letter_images[char], (x, y))
                    x += self.letter_images[char].get_width()+1

                x += self.letter_images[' '].get_width()+1

            if x >= box_width:
                x = 0
                y += letter_height + 3

            if y + letter_height > box_height:
                break
        return surface,text_boxes
    def render_text_simple(self, text, box_width, box_height):
        text_boxes = []
        hyphen_image = self.letter_images['-']
        letter_height = 8

        surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        x, y = 0, 0

        words = text.split(' ')

        for word in words:
            if word == 'n':
                y += letter_height + 3
                x = 0
                continue
            if word == 't':
                y += letter_height + 3
                x = 50
                continue
            if word == '^' or word == '~':
                image_width = self.letter_images[word].get_width()
                surface.blit(self.letter_images[word], ((box_width//2) - (image_width //2), y))
                y += letter_height + 3
                continue
            if word == '_':
                text_boxes.append([x, y])
                x = x + 18
                continue

            word_width = sum([self.letter_images[char].get_width() for char in word])

            if x + word_width > box_width:
                split_point = len(word) - 1
                for i in range(1, len(word)):
                    if word[i] in self.consonants and word[i - 1] in self.vowels:
                        split_point = i
                        break

                first_part = word[:split_point] + '-'
                second_part = word[split_point:]

                first_part_width = sum([self.letter_images[char].get_width() for char in first_part])

                if x + first_part_width <= box_width:
                    for char in first_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1

                    y += letter_height + 3
                    x = 0

                    for char in second_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1
                    x+=6
                else:
                    y += letter_height + 3
                    x = 0

                    for char in first_part:
                        if char != '-':
                            surface.blit(self.letter_images[char], (x, y))
                            x += self.letter_images[char].get_width()+1

                    second_part = second_part+' '
                    for char in second_part:
                        surface.blit(self.letter_images[char], (x, y))
                        x += self.letter_images[char].get_width()+1
            else:
                for char in word:
                    surface.blit(self.letter_images[char], (x, y))
                    x += self.letter_images[char].get_width()+1

                x += self.letter_images[' '].get_width()+1

            if x >= box_width:
                x = 0
                y += letter_height + 3

            if y + letter_height > box_height:
                break
        return surface