import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion, Particle

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    dt = 0
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable) 
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        lives_text = font.render(f"{player.get_lives()} lives left", False, (255,255,255))
        score_text = font.render(f"Score: {score}", False, (255, 255, 255))

        screen.fill("black")
        screen.blit(lives_text, (SCREEN_WIDTH - 110, 5))
        screen.blit(score_text, (5, 5))
        for obj in drawable:
            obj.draw(screen)

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                asteroid.kill()
                player.get_hit()

                if player.get_lives() == 0:
                    log_event("player_dead")
                    print(f"Game over! Score: {score}")
                    sys.exit()

            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += asteroid.radius * 5

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
