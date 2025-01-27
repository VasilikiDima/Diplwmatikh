import pygame
import sys
import random
import math

#Διάφορα τεστ για να βάλω εφέ όταν συμπληρώνεται επιτυχώς ο κώδικας

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Transition Effect")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGIC_COLORS = [(161, 147, 90), (148, 136, 87), (140, 131, 94), (120, 111, 73), (148, 142, 117), (117, 112, 90)]

font = pygame.font.Font(None, 48)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.max_size = random.randint(15, 30)
        self.color = random.choice(MAGIC_COLORS)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 5)
        self.lifetime = 255

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if self.size < self.max_size:
            self.size += 0.1
        self.lifetime -= 2
        if self.lifetime <= 0:
            self.lifetime = 0

    def draw(self, surface):
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, (*self.color, self.lifetime), (self.size, self.size), self.size)
        surface.blit(particle_surface, (self.x - self.size, self.y - self.size))

def magic_transition(screen, duration=1.5):
    clock = pygame.time.Clock()
    particles = []
    alpha = 0
    max_alpha = 255
    fade_speed = max_alpha / (duration * 60)

    for _ in range(250):
        particles.append(Particle(WIDTH // 2, HEIGHT // 2))

    while alpha < max_alpha:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.update()
        alpha += fade_speed
        clock.tick(60)


    while alpha > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        pygame.display.update()
        alpha -= fade_speed
        clock.tick(60)


def scene_1():
    screen.fill(BLACK)
    text = font.render("Scene 1: Welcome to the Game!", True, WHITE)
    screen.blit(text, (150, 250))
    pygame.display.update()


def scene_2():
    screen.fill(BLACK)
    text = font.render("Scene 2: Now Playing!", True, WHITE)
    screen.blit(text, (200, 250))
    pygame.display.update()


def main():
    running = True
    in_scene_1 = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_scene_1 = not in_scene_1
                    magic_transition(screen)

        if in_scene_1:
            scene_1()
        else:
            scene_2()

        pygame.display.update()

# Run the game
if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
