# game.py

import pygame
from settings import *
from objects import Paddle, Ball

class Game:
    """Класс для управления игрой."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Аэрохоккей")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.show_menu = True

        # Загрузка звуков
        self.hit_sound = pygame.mixer.Sound(HIT_SOUND)
        self.goal_sound = pygame.mixer.Sound(GOAL_SOUND)

        # Создаем объекты
        self.paddle1 = Paddle(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50, RED)
        self.paddle2 = Paddle(SCREEN_WIDTH // 4, 50, BLUE)
        self.puck = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Счет
        self.score1 = 0
        self.score2 = 0

    def handle_events(self):
        """Обрабатывает события."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.show_menu and event.key == pygame.K_SPACE:
                    self.show_menu = False  # Начинаем игру
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()  # Перезапуск игры

    def update(self):
        """Обновляет состояние игры."""
        if not self.show_menu and not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle1.move(-1)
            if keys[pygame.K_RIGHT]:
                self.paddle1.move(1)
            if keys[pygame.K_a]:
                self.paddle2.move(-1)
            if keys[pygame.K_d]:
                self.paddle2.move(1)

            # Двигаем шайбу и проверяем, забит ли гол
            if self.puck.move(self.paddle1, self.paddle2):
                self.goal_sound.play()  # Воспроизводим звук гола
                self.reset_puck()
                # Определяем, кто забил гол
                if self.puck.rect.top <= 0:
                    self.score1 += 1
                else:
                    self.score2 += 1
                print(f"Счет: {self.score1} - {self.score2}")

            # Проверяем столкновение шайбы с клюшками
            if self.puck.rect.colliderect(self.paddle1.rect) or self.puck.rect.colliderect(self.paddle2.rect):
                self.hit_sound.play()  # Воспроизводим звук удара

            # Обновляем частицы
            self.puck.update_particles()

            # Завершение игры при достижении счета 5
            if self.score1 >= 5 or self.score2 >= 5:
                self.game_over = True

    def reset_puck(self):
        """Сбрасывает шайбу в центр поля."""
        self.puck = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def reset_game(self):
        """Сбрасывает игру в начальное состояние."""
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        self.reset_puck()

    def draw_menu(self):
        """Отрисовывает меню старта."""
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        title_text = font.render("Аэрохоккей", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 3))

        font = pygame.font.Font(None, 36)
        start_text = font.render("Нажмите SPACE для старта", True, WHITE)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    def draw_game_over(self):
        """Отрисовывает экран завершения игры."""
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        winner = "Игрок 1" if self.score1 >= 5 else "Игрок 2"
        game_over_text = font.render(f"{winner} победил!", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Нажмите R для рестарта", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    def draw(self):
        """Отрисовывает все объекты на экране."""
        if self.show_menu:
            self.draw_menu()
        elif self.game_over:
            self.draw_game_over()
        else:
            self.screen.fill(BLACK)
            self.paddle1.draw(self.screen)
            self.paddle2.draw(self.screen)
            self.puck.draw(self.screen)

            # Отрисовка счета
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"{self.score1} - {self.score2}", True, WHITE)
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 30, 10))

        pygame.display.flip()

    def run(self):
        """Основной цикл игры."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()