## base game
from board import board
import pygame

pygame.init()

WIDTH = 840
HEIGHT = 890

# Getting the height of every square from the board 
# Removing 50px from the bottom allowing score and powerUps to be displayed, 30 is height of board
height = ((HEIGHT - 50) // 30) 

# Getting the width of every square from the board, 28 is width of board 
width = ((WIDTH // 28)) 

# Setting size of screen
screen = pygame.display.set_mode([WIDTH, HEIGHT]) 

# Setting Font
font = pygame.font.SysFont("freesansbold.tff", 20)

# Tracking time
timer = pygame.time.Clock()

# FPS for amount of executions per second ############
fps = 60

# Counter used to change pacman images to appear to animate as well as flicking of the powerUps
counter = 0
pacmanImages = []

# Setting initial postion of player
playerX = 10 # 10 13 453
playerY = 395 # 395 (scaling changed) 646

# Starting direction of player
direction = 0 

# Starting direction of 
directionChoice = 0 # pressing a key before pacman can move makes pacman turn in that direction when next available
padding = 0

flickering = True # allows the powerUps to appear to "flicker" so they are seperate from pellets
speed = 3 # speed that pacman moves (can be changed with a possible option menu)

# R, L, U, D
possibleDirections = [False, False, False, False]

score = 0
powerUps = 0
powerUpCounter = 0
powerUpActive = False

moving = False # stops everything from moving in the beginning of the game
startUpCounter = 0


# displays each pacman image in order
for i in range(1, 4): 
    pacmanImages.append(pygame.transform.scale(pygame.image.load(f"images//pacman/P{i}.png"), (24, 24)))

def drawBoard(board):
    for i in range(len(board)): # each row
        for j in range(len(board[i])): # each column in row

            circle = (j * width + (0.5 * width), i * height + (0.5 * height))
            x = width * j
            y = height * i

            # Draw pellets
            if board[i][j] == 1:
                pygame.draw.circle(screen, "white", circle, 4) 
            
            # Draw powerUps
            if board[i][j] == 2 and flickering == True:
                pygame.draw.circle(screen, "white", circle, 8)

            # Draw rectangle
            if board[i][j] == 3:
                pygame.draw.rect(screen, "red", (x, y, width + 2, height + 2)) # Outline of walls/squares
                pygame.draw.rect(screen, "blue", (x, y, width, height)) # Walls/squares
            
            # Draw line
            if board[i][j] == 4: 
                lineStart = (x, y + (0.5 * height)) # Start X and Y
                lineEnd = (x + width, y + (0.5 * height)) # End X and Y coordinates
                pygame.draw.line(screen, "white", lineStart, lineEnd, 3)

def drawScoreboardAndPowerUps(powerUps, padding, test):
    # Display score
    scoreText = font.render(f'Score: {score}', True, "white")
    screen.blit(scoreText, (10, 500)) # // 870 maybe (change Y)

    # Display PowerUps
    powerUpsText = font.render('PowerUps: ', True, "white")
    screen.blit(powerUpsText, (700, 500)) # // shift X to fit all powerUps

    # For every powerUp gained, the powerUp is drawn next to the diplay text, showing how many powerUps are available
    for i in range(powerUps):
        pygame.draw.circle(screen, "white", (780 + padding, 506), 8)
        padding += 20

    # Testing
    testText = font.render(f'PowerUps: {powerUps} and {test}', True, "white")
    screen.blit(testText, (300, 500))

def drawTrademark():
    # Displaying creators of game
    createdByText = font.render('Created By: ', True, "white")
    nameOneText = font.render('Harrison Tween & ', True, "white")
    nameTwoText = font.render('Aaron Temiwoluwa', True, "white")

    screen.blit(createdByText, (345, 385))
    screen.blit(nameOneText, (360, 400))
    screen.blit(nameTwoText, (375, 415))

def drawPacman(playerX, playerY):
    # Right, left, up, down
    imageCounter = counter // 8

    # Change direction pacman faces

    # If facing right
    if direction == 0:
        screen.blit(pacmanImages[imageCounter], (playerX, playerY)) 

    # If facing left
    elif direction == 1:
        screen.blit(pygame.transform.flip(pacmanImages[imageCounter], True, False), (playerX, playerY))

    # If facing up
    elif direction == 2:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], 90), (playerX, playerY))

    # If facing down
    elif direction == 3:
        screen.blit(pygame.transform.rotate(pacmanImages[imageCounter], -90), (playerX, playerY))

## def getPlayerCenter():
##    return [(playerX + 13), (playerY + 13)]

def positionCheck(playerCenterX, playerCenterY):
    # R, L, U, D
    # Set all available directions to False, and the function changes possible directions to true
    possibleDirections = [False, False, False, False]

    factor = 15 # Checking a wall will check from center, 15px allows checks before colliding with wall

    # Each square middle 
    gridCenter = [12, 18] # in px

    # Checking if player hasn't exceeded the board. If player has, they can go left or right
    if (playerCenterX // 28) < 29:

        # Checking collision for up and down

        if direction == 2 or direction == 3: # if going up or down
            if gridCenter[0] <= playerCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(playerCenterY + factor) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[3] = True # opposite direction

                if board[(playerCenterY - factor) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[2] = True # opposite direction
            
            if gridCenter[0] <= playerCenterY % height <= gridCenter[1]:
                if board[playerCenterY // height][(playerCenterX - width) // width] < 3: # if square next to is free 
                    possibleDirections[1] = True # opposite direction
               
                if board[playerCenterY // height][(playerCenterX + width) // width] < 3: # if square next to is free 
                    possibleDirections[0] = True # opposite direction

        # Checking collision for left and right

        if direction == 0 or direction == 1: # if going right or left
            if gridCenter[0] <= playerCenterX % width <= gridCenter[1]: # roughly center of square (width is 30px)
                if board[(playerCenterY + height) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[3] = True # opposite direction

                if board[(playerCenterY - height) // height][playerCenterX // width] < 3: # if square below/above is free 
                    possibleDirections[2] = True # opposite direction
            
            if gridCenter[0] <= playerCenterY % height <= gridCenter[1]:
                if board[playerCenterY // height][(playerCenterX - factor) // width] < 3: # if square next to is free 
                    possibleDirections[1] = True # opposite direction
               
                if board[playerCenterY // height][(playerCenterX + factor) // width] < 3: # if square next to is free 
                    possibleDirections[0] = True # opposite direction
    
    else:
        possibleDirections[0] = True
        possibleDirections[1] = True

    return possibleDirections

def checkPelletsAndPowerUps(score, powerUps, powerUpActive):
    if 0 < playerX < 810: # only do check if inside the board otherwise an error is thrown as it cannot check for squares outside the board
        if board[playerCenterY // height][playerCenterX // width] == 1: # If player is on a pellet
            board[playerCenterY // height][playerCenterX // width] = 0 # Remove pellet
            score += 10
        if board[playerCenterY // height][playerCenterX // width] == 2: # If player is on a powerUp
            board[playerCenterY // height][playerCenterX // width] = 0 # Remove powerUp
            score += 50
            powerUps += 1

    return score, powerUps, powerUpActive

def movePlayer(playerX, playerY):
    # R, L, U, D

    # Move player
    if direction == 0 and possibleDirection[0] == True:
        playerX += speed
    elif direction == 1 and possibleDirection[1] == True:
        playerX -= speed
    elif direction == 2 and possibleDirection[2] == True:
        playerY -= speed
    elif direction == 3 and possibleDirection[3] == True:
        playerY += speed
    return playerX, playerY

def activatePowerUp(powerUps):
    powerUpActive = True
    powerUps -= 1
    powerUpCounter = 0

    return powerUps, powerUpActive, powerUpCounter


run = True

while run:
    timer.tick(fps)

    # For iterating though pacman images and flickering of powerUps
    if counter < 23:
        counter += 1
        if counter > 12:
            flickering = True

    else:
        counter = 0 # Reset counter to start at first pacman image
        flickering = False # Turning flickering off to make powerUp disappear briefly to simulate flickering

    # Game Start Up
    if startUpCounter < 180:
        moving = False
        startUpCounter += 1
    else:
        moving = True


    if powerUpActive == True and powerUpCounter < 600: # If powerUp is active and has been active for less than 10 seconds
        powerUpCounter += 1
    elif powerUpActive == True and powerUpCounter >= 600: # If powerUp is active but has been active for 10 or more seconds
        powerUpCounter = 0
        powerUpActive = False


    screen.fill("black")
    drawBoard(board)
    drawPacman(playerX, playerY)
    drawScoreboardAndPowerUps(powerUps, padding, powerUpCounter)
    drawTrademark()

    playerCenterX = playerX + 13 # Center x coordinate of player
    playerCenterY = playerY + 13 # Center y coordinate of player

    pygame.draw.circle(screen, "white", (playerCenterX, playerCenterY), 2)

    possibleDirection = positionCheck(playerCenterX, playerCenterY)
    # ghostPossibleDirection = positionCheck(ghostCenterX, ghostCenterY) // x 4

    if moving == True:
        playerX, playerY = movePlayer(playerX, playerY)
        # ghostX, ghostY = moveGhost(ghostX, ghostY) // x 4

    score, powerUps, powerUpActive = checkPelletsAndPowerUps(score, powerUps, powerUpActive)

    for event in pygame.event.get(): # gets the input of keyboard
        if event.type == pygame.QUIT: # if the user quits
            run = False

        if event.type == pygame.KEYDOWN: # If the user presses a key
            if event.key == pygame.K_d:
                directionChoice = 0 
            if event.key == pygame.K_a:
                directionChoice = 1
            if event.key == pygame.K_w:
                directionChoice = 2
            if event.key == pygame.K_s:
                directionChoice = 3

            # activate powerUp

            if event.key == pygame.K_e:
                if powerUps >= 1: # if there is a powerUp available
                    powerUps, powerUpActive, powerUpCounter = activatePowerUp(powerUps)

        if event.type == pygame.KEYUP: # if the user holds down a key and is in the previous direction
            if event.key == pygame.K_d and directionChoice == 0:
                directionChoice == direction
            if event.key == pygame.K_a and directionChoice == 1:
                directionChoice == direction
            if event.key == pygame.K_w and directionChoice == 2:
                directionChoice == direction
            if event.key == pygame.K_s and directionChoice == 3:
                directionChoice == direction

    for i in range(len(possibleDirection)): # for each direction, if the user chooses a direction that they can go in, that direction is now the new direction
        if directionChoice == i and possibleDirection[i] == True:
            direction = i

    # if directionChoice == 0 and possibleDirection[0] == True:
    #     direction = 0
    # if directionChoice == 1 and possibleDirection[1] == True:
    #     direction = 1
    # if directionChoice == 2 and possibleDirection[2] == True:
    #     direction = 2
    # if directionChoice == 3 and possibleDirection[3] == True:
    #     direction = 3

    # check if player has gone through tunnel to other side of map
    if playerX > WIDTH:
        playerX = -45 # -50 is off board, -45 is slightly on board so pacman doesn't appear to disappear
    elif playerX < -50: # -50 is off board
        playerX = (WIDTH - 5) # WIDTH is off the board, -5 puts pacman slightly back on the board

    pygame.display.flip() # updates screen

pygame.quit()