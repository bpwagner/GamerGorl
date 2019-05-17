import utime


def showHighscore(gg, score, highscore2):
    gg.display.fill(0)
    gg.display.text("SCORE: " + str(score), 0, 0)
    gg.display.text("HIGHSCORE: " + str(highscore2), 0, 10)
    gg.display.text("PLAY AGAIN?", 20, 30)
    gg.display.text("YES[A]", 10, 45)
    gg.display.text("NO[B]", 80, 45)
    gg.display.show()


def showBoard(gg, fruitPoint, segments, dots, score, highscore2):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html

    gg.display.fill(0)

    print(fruitPoint)
    gg.display.fill_rect(fruitPoint[0], fruitPoint[1], 5, 5, 1)
    gg.display.rect(0, 0, 126, 64, 1)

    for i in range(0, dots):
        gg.display.rect(segments[i][0], segments[i][1], 5, 5, 1)

    # gg.display.text(str(1234), 82, 32)
    gg.display.show()


def main(gg):
    playagain2 = True
    f = open("snakehighscore", "r")
    highscore2 = int(f.readline())
    f.close()
    playingagain2 = True

    while playagain2:
        # put your game loop here
        gg.fillLEDs((255, 0, 255), 1, 19)
        gg.display.fill(0)
        gg.display.text("snake", 42, 28)
        gg.display.show()
        utime.sleep_ms(1000)

        # put your game loop here
        # variables
        gameW = 128
        gameH = 64
        dotSize = 5
        score = 0
        gameOver = False
        totalDots = (gameW * gameH) / (dotSize * dotSize)
        loopDelay = 50
        dots = 3

        # random fruit location
        fruitPoint = (gg.randint(1, 11) * 10, gg.randint(1, 5) * 10)
        # fruitPoint = (gg.randint(0, gameW / 10) * 10, gg.randint(0, gameH / 10) * 10)
        segments = []

        # snake directions
        leftDirection = False
        rightDirection = True
        upDirection = False
        downDirection = False

        # add snake segments
        for i in range(0, dots):
            segments.append((50 - i * dotSize, 50))

        while not gameOver:
            # check apple
            if segments[0][0] == fruitPoint[0] and segments[0][1] == fruitPoint[1]:
                segments.append((0, 0))
                dots = dots + 1
                fruitPoint = (gg.randint(1, 11) * 10, gg.randint(1, 5) * 10)
                score += 1
                gg.beep()

            # wall collision
            if segments[0][0] == 0 or segments[0][0] == 115 or segments[0][1] == 0 or segments[0][1] == 60:
                gameOver = True

            # check snake

            joyX = gg.getJoyStickX()
            joyY = gg.getJoyStickY()
            aPressed, bPressed = gg.getButtons()
            # rnd = gg.randint(0, 1000)  # here is how to make a random number
            # fruitPoint = (gg.randint(2, 124), gg.randint(2, 60))


            if joyX < 200:
                leftDirection = True
                rightDirection = False
                upDirection = False
                downDirection = False

            elif joyX > 800:
                leftDirection = False
                rightDirection = True
                upDirection = False
                downDirection = False

            elif joyY < 200:
                leftDirection = False
                rightDirection = False
                upDirection = True
                downDirection = False

            elif joyY > 800:
                leftDirection = False
                rightDirection = False
                upDirection = False
                downDirection = True

            # the body
            for i in range(dots - 1, 0, -1):
                segments[i] = (segments[(i - 1)][0], segments[(i - 1)][1])

            # the head
            if leftDirection:
                segments[0] = (segments[0][0] - dotSize, segments[0][1])

            if rightDirection:
                segments[0] = (segments[0][0] + dotSize, segments[0][1])

            if upDirection:
                segments[0] = (segments[0][0], segments[0][1] - dotSize)

            if downDirection:
                segments[0] = (segments[0][0], segments[0][1] + dotSize)

            showBoard(gg, fruitPoint, segments, dots, score, highscore2)
            utime.sleep_ms(50)

            '''
            snake hits itself
                    for i in range(dots - 1, 1, - 1):
                        if segments[i][0] == segments[0][0] and segments[i][1] == segments[0][1]:
                            break
                            if snake[0] in snake[1:]: break
                    # see if we bite ourselves
                for i in range(dots - 1, 1, -1):
                    if segments[i][0] == segments[0][0] and segments[i][1] == segments[0][1]:
                        return True
            '''

        if score > highscore2:
            highscore2 = score
            f = open("snakehighscore", "w")
            f.write(str(highscore2))
            f.close()

        z = True
        showHighscore(gg, score, highscore2)
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