import pygame
class DirtBall:
    def __init__(self, x, y, dir_x, dir_y, speed=20, damage=30):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = speed
        self.damage = damage
        self.radius = 50  

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (139, 69, 19), (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
