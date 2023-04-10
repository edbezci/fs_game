import os
import random
import sys

import pygame
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
ASTROMINSIZE = 10
ASTROMAXSIZE = 40
ASTROMINSPEED = 1
ASTROMAXSPEED = 8
ADDNEWASTRORATE = 16
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # pressing escape quits
                    terminate()
                return


def playerHasHitAstro(playerRect, astros):
    for a in astros:
        if playerRect.colliderect(a["rect"]):
            return True
    return False


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode(
    [WINDOWWIDTH, WINDOWHEIGHT], pygame.FULLSCREEN
)
pygame.display.set_caption("Filling Space")
pygame.mouse.set_visible(False)

# set up paths
explosion_sound = os.path.abspath("assets/sound/explosion.ogg")
background_sound = os.path.abspath("assets/sound/background.ogg")

logo = os.path.abspath("assets/images/logo.png")
craft = os.path.abspath("assets/images/FS_Craft.png")
explosion = os.path.abspath("assets/images/explosion.png")
asteroid = os.path.abspath("assets/images/asteroid.png")
background_image = os.path.abspath("assets/images/background.png")


# set up fonts
font = pygame.font.SysFont("arial", 48)
font1 = pygame.font.SysFont("arial", 24)

# set up sounds
gameOverSound = pygame.mixer.Sound(explosion_sound)
pygame.mixer.music.load(background_sound)

# set up images
logoload = pygame.image.load(logo)
logoImage = pygame.transform.scale(logoload, (150, 150))
logoRect = logoImage.get_rect()
plload = pygame.image.load(craft)
expload = pygame.image.load(explosion)
explosionImage = pygame.transform.scale(expload, (70, 70))
playerImage = pygame.transform.scale(plload, (80, 80))
playerRect = playerImage.get_rect()
astroImage = pygame.image.load(asteroid)
bg_image = pygame.image.load(background_image)
bg = pygame.transform.scale(bg_image, (WINDOWWIDTH, WINDOWHEIGHT))
# show the "Start" screen

logoRect.topleft = (((WINDOWWIDTH / 2) - 75), (5))
windowSurface.blit(logoImage, logoRect)
drawText("Kapitän Erik", font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText(
    "Drücke eine beliebige Taste um zu starten!",
    font,
    windowSurface,
    15,
    (WINDOWHEIGHT / 3) + 50,
)
drawText(
    "Spiel für Erik - Vermeide die Meteoriten und rette die Menschen an Bord!",
    font1,
    windowSurface,
    10,
    (WINDOWHEIGHT / 3) + 100,
)
drawText(
    "Führe Die Menschheit im Universum...Die Menschheit vertraut dir!",
    font1,
    windowSurface,
    10,
    (WINDOWHEIGHT / 3) + 130,
)
drawText(
    "W= Geradeaus, A=Links, S=rückwärts, D=Recht, Z=Abbremsen, ESC=Quit",
    font1,
    windowSurface,
    10,
    (WINDOWHEIGHT / 3) + 180,
)

pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    astros = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    astroAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # the game loop runs while the game part is playing
        score += 1  # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord("z"):
                    reverseCheat = True
                if event.key == ord("x"):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord("a"):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord("d"):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord("w"):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord("s"):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord("z"):
                    reverseCheat = False
                    score = 0
                if event.key == ord("x"):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord("a"):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord("d"):
                    moveRight = False
                if event.key == K_UP or event.key == ord("w"):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord("s"):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(
                    event.pos[0] - playerRect.centerx,
                    event.pos[1] - playerRect.centery,
                )

        # Add new ASTROs at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            astroAddCounter += 1
        if astroAddCounter == ADDNEWASTRORATE:
            astroAddCounter = 0
            astroSize = random.randint(ASTROMINSIZE, ASTROMAXSIZE)
            newAstro = {
                "rect": pygame.Rect(
                    random.randint(0, WINDOWWIDTH - astroSize),
                    0 - astroSize,
                    astroSize,
                    astroSize,
                ),
                "speed": random.randint(ASTROMINSPEED, ASTROMAXSPEED),
                "surface": pygame.transform.scale(
                    astroImage, (astroSize, astroSize)
                ),
            }

            astros.append(newAstro)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the ASTROs down.
        for a in astros:
            if not reverseCheat and not slowCheat:
                a["rect"].move_ip(0, a["speed"])
            elif reverseCheat:
                a["rect"].move_ip(0, -5)
            elif slowCheat:
                a["rect"].move_ip(0, 1)

        # Delete ASTROs that have fallen past the bottom.
        for a in astros[:]:
            if a["rect"].top > WINDOWHEIGHT:
                astros.remove(a)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(bg, (0, 0))

        # Draw the score and top score.
        drawText("Score: %s" % (score), font, windowSurface, 10, 0)
        drawText("Top Score: %s" % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each ASTRO
        for a in astros:
            windowSurface.blit(a["surface"], a["rect"])

        pygame.display.update()

        # Check if any of the ASTROs have hit the player.
        if playerHasHitAstro(playerRect, astros):
            windowSurface.blit(explosionImage, playerRect)
            if score > topScore:
                topScore = score  # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText(
        "GAME OVER!",
        font,
        windowSurface,
        (WINDOWWIDTH / 3),
        (WINDOWHEIGHT / 3),
    )
    drawText(
        "Drücke eine beliebige Taste um noch einmal zu beginnen",
        font1,
        windowSurface,
        WINDOWWIDTH / 5,
        (WINDOWHEIGHT / 3) + 50,
    )
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
