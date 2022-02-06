import pygame
import random
import time
import math
from pygame import mixer

# initialize the screen
pygame.init()

# creating the window params -> width,height
screen = pygame.display.set_mode((800,600))

# creating the background image
BACKGROUND_IMAGE = pygame.image.load("images/backgroundImage.jpg")



# tittle and icon
pygame.display.set_caption("DumbGame")
ICON = pygame.image.load("images/icon.png")
pygame.display.set_icon(ICON)

# font
FONT = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
scoreValue = 0



# creating a new player
playerImage = pygame.image.load("images/shipOne.png")
playerX = 370
playerY = 480
playerX_change = 0

# creating a new enemy list
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
NUMBER_OF_ENEMIES = 10
for i in range(NUMBER_OF_ENEMIES):
    enemyImage.append(pygame.image.load("images/enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# creating bullet the state determine whether the bullet will be firing or in a state of rest
bulletImage = pygame.image.load("images/bullet.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 3
# True bulletState means that the bullet is in fire condition , if it is in False state then its not firing 
bulletState = False

SCORE = 0

# adding background music on loop
mixer.init()
mixer.music.load("sounds/BackgroundMusic.mp3")
mixer.music.play()


# creating player function
def player(x,y):
    # blit means to draw something on to the screen, drawing the spaceship on to the screen,params-> image and coordinates inside a tuple
    screen.blit(playerImage,(x,y))
    
# creating enemy function
def enemy(x,y,i):
    # drawing the enemy in certain coordinates in the screen
    screen.blit(enemyImage[i],(x,y))
    
# creating function for firing bullets
def fireBullet(x,y):
    global bulletState
    bulletState = True
    screen.blit(bulletImage,(x+16,y+10))
    
# detect collision between bullet and the enemy
def DetectCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
#  rendering the score to the screen, incase of font it has to be rendered first then blit on the screen    
def ShowScore(x,y,scoreValue):
    SCORE = FONT.render("Score: ", str(scoreValue), True, (255,255,255))
    screen.blit(SCORE,(x,y))
    
def GameOver(enemyY):
    if enemyY >= 440:
        return True
    
def PlayFiringSound():
    firingSound = mixer.Sound("sounds/bulletSound.wav")
    # -1 means that this plays the sound in loop
    firingSound.play()    
    
    
    

running = True
while running:
    # setting the background color inside a tuple (RGB values)
    screen.fill((0,0,0))
    # drawing the background image , params -> image and the starting coordinates
    screen.blit(BACKGROUND_IMAGE,(0,0))
    
    # loop through all the events that is going on in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # setting the running value to false to break the loop
            running = False
        # handling keyboard events -> key pressed , KEYDOWN means key pressed , KEYDOWN represents any keyboard stroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            # checking if spacebar is pressed
            if event.key == pygame.K_SPACE:
                # allow the player to fire bullet only when the state is False(FIRE)
                if bulletState is False: 
                    bulletX = playerX
                    fireBullet(bulletX,bulletY)
                    PlayFiringSound()
                    
        # handling key release , KEYUP means key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # looping through the event and searching for any change in keystroke and adding the coordinates         
    playerX += playerX_change
    
    # checking if the x coordinate is outside the boundary or not subtracting 64 pixels as 64 pixel is the size
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
        
        
    for i in range(NUMBER_OF_ENEMIES):
        # looping through event to find enemy coordinates
        enemyX[i] += enemyX_change[i]  
        # checking if the enemy is out of bounds or not, if it is out of bounds then it should change the direction
        if enemyX[i] <= 0:
            time.sleep(0.01)
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            time.sleep(0.01)
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # detect collision
        collision = DetectCollision(enemyX[i],enemyY[i],bulletX,bulletY) 
        if collision:
            bulletY = 480
            bulletState = False 
            scoreValue += 1
            #  respawning the enemy to its new position
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        # calling the enemy function
        enemy(enemyX[i],enemyY[i],i)
        if GameOver(enemyY[i]) == True:
            running = False
            break
        
    # creating multiple bullets by reseting the bullet postion
    if bulletY <= 0:
        bulletY = 480
        bulletState = False
    # creating the bullet movement
    if bulletState is True:
        fireBullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    # calling the player function
    player(playerX, playerY)
   
    ShowScore(textX,textY,scoreValue)
    
    # update method to keep updating the screen
    pygame.display.update()