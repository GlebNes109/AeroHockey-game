import pygame
from settings import *
from objects import Paddle, Ball

# обработка событий на неигровых экранах
def process_events():
    global running, show_menu

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #
            running = False
        if event.type == pygame.KEYDOWN:
            if show_menu and event.key == pygame.K_SPACE:
                show_menu = False  # убрать меню, старт игры
            if game_over and event.key == pygame.K_r:
                reset_game()  # перезапуск игры

def update():
    global show_menu, game_over, score1, score2, ball, game_timer

    if not show_menu and not game_over: # если игра идет, следить за кнопками
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle1.move(-1)
        if keys[pygame.K_RIGHT]:
            paddle1.move(1)
        if keys[pygame.K_a]:
            paddle2.move(-1)
        if keys[pygame.K_d]:
            paddle2.move(1)

        if ball.move(paddle1, paddle2): # двигать мяч и проверять, забит ли гол
            goal_sound.play()  # звук "гоооол!"

            if ball.rect.top <= 0: # начислить очки
                score1 += 1
            else:
                score2 += 1

            ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # мяч на центр поля

            print(f"Счет: {score1} : {score2}")

        # проверить столкновение мяча с клюшками
        if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
            hit_sound.play()  # Воспроизводим звук удара

        # обновить частицы
        ball.update_particles()

        # завершить игру при достижении счета 5
        if score1 >= 5 or score2 >= 5:
            game_over = True

        game_timer += 1 # увеличить игровое время
        if game_timer % 60 * 3 == 0: # ускорять шарик и клюшки каждые 3 сек
            ball.speed_up()
            paddle1.speed_up()
            paddle2.speed_up()


def reset_game():
    global score1, score2, game_over, ball
    score1 = 0
    score2 = 0
    game_over = False
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # мяч на центр поля
    paddle1.reset_speed()
    paddle2.reset_speed()

def draw_start_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    title_text = font.render("Аэрохоккей", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 3))

    font = pygame.font.Font(None, 36)
    start_text = font.render("Нажмите пробел для старта", True, (255, 255, 255))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

def draw_game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    winner = "Игрок 1" if score1 >= 5 else "Игрок 2"
    game_over_text = font.render(f"{winner} победил!", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Нажмите R для рестарта", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

def draw():
    if show_menu:
        draw_start_menu()
    elif game_over:
        draw_game_over()
    else:
        screen.fill((0, 0, 0))
        paddle1.draw(screen)
        paddle2.draw(screen)
        ball.draw(screen)

        # отрисовать счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{score1} : {score2}", True, (0, 255, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 30, 10))

    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Аэрохоккей")
    clock = pygame.time.Clock()
    running = True
    game_over = False
    show_menu = True
    fps = 60
    game_timer = 0 # таймер тиков от старта раунда

    # загрузить звуки в миксер
    hit_sound = pygame.mixer.Sound(HIT_SOUND)
    goal_sound = pygame.mixer.Sound(GOAL_SOUND)

    # создать объекты клюшки и мяча
    paddle1 = Paddle(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50, (255, 0, 0))
    paddle2 = Paddle(SCREEN_WIDTH // 4, 50, (0, 0, 255))
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # обнуляем счет обоих игроков
    score1, score2 = 0, 0

    while running:
        process_events()
        update()
        draw()
        clock.tick(fps)
        print(game_timer)
    pygame.quit()