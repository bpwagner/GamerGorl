#sam adkins
#latest 5/16/19


from gamerGorl import gamerGorl

import utime
from machine import Pin
from neopixel import NeoPixel


def debugme(gg, str):
    gg.display.fill(0)
    gg.display.text(str, 40, 22)
    gg.display.show()


def help(gg):
    gg.display.fill(0)
    gg.display.text("Green", 47, 5)
    gg.display.text("Yellow      Red", 4, 27)
    gg.display.text("Blue", 47, 55)
    gg.display.show()


def showHighscore(gg, score, highscore2):
    gg.display.fill(0)
    gg.display.text("SCORE: " + str(score), 0, 0)
    gg.display.text("HIGHSCORE: " + str(highscore2), 0, 10)
    gg.display.text("PLAY AGAIN?", 20, 30)
    gg.display.text("YES[A]", 10, 45)
    gg.display.text("NO[B]", 80, 45)
    gg.display.show()


def main(gg):
    # put your game loop here
    f = open("HighscoreSimon", "r")
    highscore = int(f.readline())
    f.close()

    playagain2 = True

    while (playagain2):
        gg.clearLEDs()
        gg.display.fill(0)
        gg.display.text("Simon", 42, 22)
        gg.display.text("Highscore: " + str(highscore), 20, 48)
        gg.display.show()
        utime.sleep_ms(2000)

        score = 0
        colorList = []
        gameOver = False

        while (not gameOver):
            debugme(gg, 'Level: ' + str(score))
            utime.sleep_ms(650)

            rnd = gg.randint(1, 5)  # here is how to make a random number
            if rnd == 1:
                colorList.append(rnd)
            elif rnd == 2:
                colorList.append(rnd)
            elif rnd == 3:
                colorList.append(rnd)
            elif rnd == 4:
                colorList.append(rnd)

            for i in range(0, len(colorList)):
                if colorList[i] == 1:
                    debugme(gg, 'Red')
                    gg.flashRed(13, 16)
                elif colorList[i] == 2:
                    debugme(gg, 'Green')
                    gg.flashGreen(6, 13)
                elif colorList[i] == 3:
                    debugme(gg, 'Blue')
                    gg.flashBlue(0, 3, 16, 19)
                elif colorList[i] == 4:
                    debugme(gg, 'Yellow')
                    gg.flashYellow(3, 6)

            for i in range(0, len(colorList)):

                if colorList[i] == 1:
                    waiting = True
                    gameOver2 = False
                    while (waiting):
                        help(gg)
                        joyX = gg.getJoyStickX()
                        joyY = gg.getJoyStickY()
                        APressed, BPressed = gg.getButtons()
                        if joyX > 750 and (APressed or BPressed):
                            gg.beep()
                            debugme(gg, 'Correct')
                            break
                        elif (APressed or BPressed) and not (joyX > 750):
                            gg.lowBeep()
                            gameOver2 = True
                            break
                    if gameOver2:
                        gameOver = True
                        break


                elif colorList[i] == 2:
                    waiting = True
                    gameOver2 = False
                    while (waiting):
                        help(gg)
                        joyX = gg.getJoyStickX()
                        joyY = gg.getJoyStickY()
                        APressed, BPressed = gg.getButtons()

                        if joyY < 250 and (APressed or BPressed):
                            gg.beep()
                            debugme(gg, 'Correct')
                            break
                        elif (APressed or BPressed) and not (joyY < 250):
                            gg.lowBeep()
                            gameOver2 = True
                            break
                    if gameOver2:
                        gameOver = True
                        break


                elif colorList[i] == 3:
                    waiting = True
                    gameOver2 = False
                    while (waiting):
                        help(gg)
                        joyX = gg.getJoyStickX()
                        joyY = gg.getJoyStickY()
                        APressed, BPressed = gg.getButtons()

                        if joyY > 750 and (APressed or BPressed):
                            gg.beep()
                            debugme(gg, 'Correct')
                            break
                        elif (APressed or BPressed) and not (joyY > 750):
                            gg.lowBeep()
                            gameOver2 = True
                            break
                    if gameOver2:
                        gameOver = True
                        break


                elif colorList[i] == 4:
                    waiting = True
                    gameOver2 = False
                    while (waiting):
                        help(gg)
                        joyX = gg.getJoyStickX()
                        joyY = gg.getJoyStickY()
                        APressed, BPressed = gg.getButtons()

                        if joyX < 250 and (APressed or BPressed):
                            gg.beep()
                            debugme(gg, 'Correct')
                            break
                        elif (APressed or BPressed) and not (joyX < 250):
                            gg.lowBeep()
                            gameOver2 = True
                            break
                    if gameOver2:
                        gameOver = True
                        break

            score += 1

        if score > highscore:
            highscore = score
            f = open("HighscoreSimon", "w")
            f.write(str(highscore))
            f.close()

        z = True
        showHighscore(gg, score, highscore)
        utime.sleep_ms(200)
        while z:
            # gg.time.sleep_ms(gg.mstime)
            APressed, BPressed = gg.getButtons()
            if APressed:
                playagain2 = True
                z = False
            if BPressed:
                playagain2 = False
                z = False
                utime.sleep_ms(200)


'''
def showBoard(gg):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html

    gg.display.fill(0)
    gg.display.show()



leftDirection = False
rightDirection = False
upDirection = False
downDirection = False

if joyX < 250:
    leftDirection = True
    rightDirection = False
    upDirection = False
    downDirection = False

elif joyX > 750:
    leftDirection = False
    rightDirection = True
    upDirection = False
    downDirection = False

elif joyY < 250:
    leftDirection = False
    rightDirection = False
    upDirection = True
    downDirection = False

elif joyY > 750:
    leftDirection = False
    rightDirection = False
    upDirection = False
    downDirection = True

if leftDirection:
    print()
if rightDirection:
    print()
if upDirection:
    print()
if downDirection:
    print()
'''