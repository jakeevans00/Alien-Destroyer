from numpy import true_divide
import pygame
import random
import math
from pygame import mixer

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.init()

#create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#background
background = pygame.image.load('background.jpg')

#background sounds
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Alien Slayer")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


#Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy List
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
num_of_monsters = 6

for i in range(num_of_monsters):
    monsterImg.append(pygame.image.load('monster.png'))
    monsterX.append(random.randint(0,735))
    monsterY.append(random.randint(50,150))
    monsterX_change.append(1)
    monsterY_change.append(40)

#Bullet
#ready - state means you can't see the bullet on the screen
#Fire - the bullet is curently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('typewriter.ttf', 35)
over_font = pygame.font.Font("typewriter.ttf", 300)

textX = 10
textY = 10


def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))


def monster(x,y, i):
    screen.blit(monsterImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

#calculating collision condition
def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt((math.pow(monsterX-bulletX,2)) + (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else: 
        return False



#Game Loop (infinite)

running = True
while running:
    #RGB code
    screen.fill((45,50,73))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #if keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("Laser.wav")
                    bullet_sound.play()
                    #get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0

    
    #player movement       
    playerX += playerX_change
    #limits
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736


    #enemy movement  
    for i in range(num_of_monsters):

        #Game over
        if monsterY[i] > 440:
            for j in range(num_of_monsters):
                monsterY[j] = 2000
            game_over_text()
            break

        monsterX[i] += monsterX_change[i]
        if monsterX[i] <= 0:
            monsterX_change[i] = 1.5
            monsterY[i] += monsterY_change[i]
        elif monsterX[i] >= 736:
            monsterX_change[i] = -1.5
            monsterY[i] += monsterY_change[i]

        #collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            monsterX[i] = random.randint(0,735)
            monsterY[i] = random.randint(50,150)

        monster(monsterX[i],monsterY[i], i)
            
    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()