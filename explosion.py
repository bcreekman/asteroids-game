import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH


class Particle(CircleShape):
    def __init__(self, x, y, radius, lifetime=0.5):
        super().__init__(x, y, radius)
        self.lifetime = lifetime

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

class Explosion():
    def __init__(self, x, y, count=36, size=2):
        self.x = x
        self.y = y
        self.count = count
        self.size = size
        self.particles = []

        self.create_particles()
    
    def create_particles(self):
        angle = 0
        
        for _ in range(self.count):
            particle = Particle(self.x, self.y, self.size, random.uniform(0.2, 1.2))

            angle_offset = random.uniform(-5, 5)
            speed = random.uniform(50, 150)
            particle.velocity = pygame.Vector2(0,1).rotate(angle + angle_offset) * speed

            self.particles.append(particle)
            angle += 360 / self.count
