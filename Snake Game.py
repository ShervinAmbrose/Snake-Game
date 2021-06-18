"""
Feel free to download and play the Game.
-Shervin W. Ambrose
"""
import pygame
import random
pygame.init()
screenL = 421
screenB = 421
padding = 21
squares = 20  # x by x
sqrSide = 20
screen = pygame.display.set_mode((screenL, screenB))
pygame.display.set_caption('Snake Game')


def direction(goLeft, goDown, goRight, goUp):
    global i, j
    if goLeft:
        i -= 1
        if i == -1:
            i = 19
    elif goRight:
        i += 1
        if i == 20:
            i = 0
    elif goUp:
        j -= 1
        if j == -1:
            j = 19
    elif goDown:
        j += 1
        if j == 20:
            j = 0


def apple(gridApple):
    return random.choice(random.choice(gridApple))


def endGame(score):

    running = True
    # print(pygame.font.get_fonts())
    titleFont = pygame.font.SysFont('applechancery', 50, 0, 1)
    yourScore = pygame.font.SysFont('comicsansms', 40, 0, 1)
    playAgain = pygame.font.SysFont('comicsansms', 30, 0, 1)
    leave = pygame.font.SysFont('comicsansms', 30, 0, 1)
    # digits = pygame.font.Font('freesansbold.tff', 40)
    while running:
        screen.fill((0, 0, 0))
        titleLabel = titleFont.render('GAME OVER', 1, (255, 255, 255))
        yourScoreLabel = yourScore.render('Your  Score: ' + str(score), 1, (255, 255, 255))
        playAgainLabel = playAgain.render('Press SPACE to Play Again', 1, (255, 255, 255), (0, 200, 0))
        leaveLabel = leave.render('Press ESC to Exit', 1, (255, 255, 255), (255, 0, 0))
        screen.blit(titleLabel, (int(screenL / 2 - titleLabel.get_width() / 2), int(screenB / 16)))
        screen.blit(yourScoreLabel, (int(screenL / 2 - yourScoreLabel.get_width() / 2), int(screenB / 2)))
        screen.blit(playAgainLabel, (int(screenL / 2 - playAgainLabel.get_width() / 2), int(screenB / 1.5)))
        screen.blit(leaveLabel, (int(screenL / 2 - leaveLabel.get_width() / 2), int(screenB / 1.25)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            main()
    pygame.quit()
    exit()


def main():
    running = True
    global i, j
    i = j = 10  # grid[i][j]
    goLeft = goUp = goDown = False
    goRight = True
    food = True
    headPath = []
    bodys = 0
    speed = 100
    score = 0
    collision = False
    while running:
        pygame.time.delay(speed)  # Controls the snake's speed
        grid = []
        gridApple = []
        screen.fill((0, 0, 0))  # black background
        # Check if the escape key or quit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Draws Grids
        # Change (0, 0, 0) to (255, 255, 255) to see the grid
        for row in range(squares):
            grid.append([])
            gridApple.append([])
            for column in range(squares):
                grid[row].append(
                    pygame.draw.rect(screen, (0, 0, 0), (row * padding + 1, column * padding + 1, sqrSide, sqrSide)))
                # gridApple stores the x and y coordinates of the 400 grid block
                gridApple[row].append((row * padding + 1, column * padding + 1))

            # Checks for key press and
            # Bars the snake from moving left to right or up to down
            if goRight:
                if keys[pygame.K_s]:  # down
                    goDown = True
                    goRight = goLeft = goUp = False
                elif keys[pygame.K_w]:  # up
                    goUp = True
                    goDown = goLeft = goRight = False
            if goUp:
                if keys[pygame.K_a]:  # left
                    goLeft = True
                    goRight = goUp = goDown = False
                if keys[pygame.K_d]:  # right
                    goRight = True
                    goLeft = goUp = goDown = False
            if goDown:
                if keys[pygame.K_a]:  # left
                    goLeft = True
                    goRight = goUp = goDown = False
                if keys[pygame.K_d]:  # right
                    goRight = True
                    goLeft = goUp = goDown = False
            if goLeft:
                if keys[pygame.K_s]:  # down
                    goDown = True
                    goRight = goLeft = goUp = False
                elif keys[pygame.K_w]:  # up
                    goUp = True
                    goDown = goLeft = goRight = False

        # Change the direction
        direction(goLeft, goDown, goRight, goUp)

        # Draws snake's head on the screen
        pygame.draw.rect(screen, (0, 255, 0), grid[i][j])
        # headPath stores the path which the snake's head treads
        headPath.append(gridApple[i][j])

        # add bodies to the head
        bodyIndex = 2
        for size in range(bodys):
            pygame.draw.rect(screen, (140, 26, 255), (headPath[len(headPath) - bodyIndex][0], headPath[len(headPath) - bodyIndex][1], sqrSide, sqrSide))
            bodyIndex += 1

        # Condition to detect if the head touches the body(collision detection)
        # this is done by checking if the (x,y) coordinates of the head is present in the list(headPath) of the bodys
        if gridApple[i][j] in headPath[-(bodys + 1): -1]:
            pygame.time.delay(2500)
            endGame(score)

        # draw the food at random location
        if food:
            foodPos = apple(gridApple)
            # Condition to check if the food is on the snake body.
            # if true, draw the apple at a new location.
            if foodPos in headPath[-(bodys + 1): -1]:
                foodPos = apple(gridApple)
                food = False
            else:
                food = False

        # Draws apple
        pygame.draw.rect(screen, (255, 0, 0), (foodPos[0], foodPos[1], sqrSide, sqrSide))

        # check if the snake has eaten the apple
        # if it true, then increment the body by 1 (add body at the tail end of the snake),
        # and draw the apple at another location
        if grid[i][j][0] == foodPos[0] and grid[i][j][1] == foodPos[1]:
            food = True
            bodys += 1
            score += 1
            # For every multiple of 5 bodies increase the speed
            if (bodys + 1) % 5 == 0:
                speed -= 5

        # Condition to detect if the head touches the body(collision detection)
        # this is done by checking if the (x,y) coordinates of the head is present in the list(headPath) of the bodys
        if gridApple[i][j] in headPath[-(bodys + 1): -1]:
            pygame.time.delay(2500)
            collision = True

        if collision:
            endGame(score)
            main()
        pygame.display.update()
    pygame.quit()
    exit()


def mainScreen():
    running = True
    titleFont = pygame.font.SysFont('comicsansms', 30, 0, 1)
    while running:
        screen.fill((0, 0, 0))
        titleLabel = titleFont.render('Press SPACE to Start...', 1, (255, 255, 255))
        screen.blit(titleLabel, (int(screenL / 2 - titleLabel.get_width() / 2), int(screenB / 2)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            main()
    pygame.quit()


mainScreen()
