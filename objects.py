import pygame
from settings import *
import random

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED

    # ускорить платформу
    def speed_up(self):
        self.speed *= 1.02

    def reset_speed(self):
        self.speed = PADDLE_SPEED

    def move(self, dx):
        self.rect.x += dx * self.speed
        # ограничить движение в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = (255, 255, 255)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.particles = []  # список для хранения частиц

    # ускорить шарик
    def speed_up(self):
        self.speed_x *= 1.05
        self.speed_y *= 1.05

    def move(self, paddle1, paddle2):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # отскок от стен меняет горизонт. скорость на обратную
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1

        # отскок от клюшек меняет верт. скорость на обратную
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_y *= -1
            # частицы при столкновении
            self.generate_particles(paddle1 if self.rect.colliderect(paddle1.rect) else paddle2)

        # проверить на выход за верхнюю и нижнюю границы экрана (гол)
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            return True  # мяч вышел за пределы поля (гооооол)
        return False

    def generate_particles(self, paddle):
        for _ in range(20):  # создать 20 частиц
            particle = Particle(self.rect.centerx, self.rect.centery, paddle.color)
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles:
            particle.move()
        # удалить частицы, у которых закончилось время жизни
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)
        for particle in self.particles:
            particle.draw(screen)

# Класс частиц для эффектов
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.randint(-200, 200) / 100
        self.speed_y = random.randint(-200, 200) / 100
        self.lifetime = random.randint(10, 20)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)