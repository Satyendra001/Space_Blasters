import pygame
import random as rd
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("bg.png")

mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Fighters")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImage = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImage.append(pygame.image.load("alien.png"))
    enemyX.append(rd.randint(0, 735))
    enemyY.append(rd.randint(50, 150))
    enemyX_change.append(10)
    enemyY_change.append(50)

# Bullet
# Ready -> You can't see the bullet on the screen
# Fire -> The bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# score

score_value = 0
# get extra fonts from dafont.com and extract the zip file to get ttf file, then write the name of the font.
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 100)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    game_text = game_over_font.render("GAME OVER! ", True, (255, 255, 255))
    screen.blit(game_text, (100, 250))


def player(x, y):
    screen.blit(playerImage, (playerX, playerY))  # blit method draws our character on the screen.


def enemy(x, y):
    screen.blit(enemyImage[i], (enemyX[i], enemyY[i]))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # print("space")
    screen.blit(bulletImage, (x + 16, y + 10))


def is_collision(enemyX, bulletX, enemyY, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # print(distance)
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    # Get the current x coordinate of the space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Defining position setting for the player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Defining enemy position
    for i in range(no_of_enemies):

        # Game over
        if enemyY[i] > 400:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = rd.randint(0, 735)
            enemyY[i] = rd.randint(50, 150)
        enemy(enemyX[i], enemyY[i])

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
