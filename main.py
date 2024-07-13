import pygame
import time
import random

pygame.font.init()  # Importing it to add text to the game

WIDTH, HEIGHT = 900, 650
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)  # To add font as time

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Button colors
color_light = (180, 180, 170)
color_dark = (100, 100, 100)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, WHITE)
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, RED, player)
    for star in stars:
        pygame.draw.rect(WIN, WHITE, star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)  # FPS
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)  # Making the stars faster
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:  # Not to go out of the screen
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:  # Not to go out of the screen
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, BLACK)
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))  # Centering the text
            pygame.display.update()
            run = False
            time.sleep(2)  # Delay for 2 seconds before showing the quit button

        draw(player, elapsed_time, stars)

    show_buttons()

def show_buttons():
    small_font = pygame.font.SysFont('Corbel', 35)
    button_text_quit = small_font.render('Quit', True, WHITE)
    button_text_restart = small_font.render('Restart', True, WHITE)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
                    pygame.quit()
                    return
                elif WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 50 <= mouse[1] <= HEIGHT / 2 + 90:
                    main()
                    return

        mouse = pygame.mouse.get_pos()

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
            pygame.draw.rect(WIN, color_light, [WIDTH / 2, HEIGHT / 2, 140, 40])
        else:
            pygame.draw.rect(WIN, color_dark, [WIDTH / 2, HEIGHT / 2, 140, 40])

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 50 <= mouse[1] <= HEIGHT / 2 + 90:
            pygame.draw.rect(WIN, color_light, [WIDTH / 2, HEIGHT / 2 + 50, 140, 40])
        else:
            pygame.draw.rect(WIN, color_dark, [WIDTH / 2, HEIGHT / 2 + 50, 140, 40])

        WIN.blit(button_text_quit, (WIDTH / 2 + 50, HEIGHT / 2))
        WIN.blit(button_text_restart, (WIDTH / 2 + 50, HEIGHT / 2 + 50))
        pygame.display.update()

if __name__ == "__main__":
    main()
