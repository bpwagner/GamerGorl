#import random
import utime

'''
def checkCollisions():
    # return true if you hit something
    # x component of head of snake
    if segments[0][0] < 0 or segments[0][0] > 128:
        return True
        # y component of head of snake
    if segments[0][1] < 0 or segments[0][1] > 64:
        return True
        # see if we bite ourselves
    for i in range(dots - 1, 1, -1):
        if segments[i][0] == segments[0][0] and segments[i][1] == segments[0][1]:
            return True
    return False
'''

def showBoard(gg, fruitPoint, segments, dots):
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
    gg.display.fill(0)
    gg.display.text("snake", 42, 28)
    gg.display.show()
    utime.sleep_ms(2000)
    # gg.display.draw_rect(2, 2, 124, 60)
    # gg.display.show()

    # put your game loop here
    # variables
    gameW = 128
    gameH = 64
    dotSize = 5
    score = 0
    totalDots = (gameW * gameH) / (dotSize * dotSize)
    loopDelay = 50
    dots = 3

    # snake directions
    leftDirection = False
    rightDirection = True
    upDirection = False
    downDirection = False

    # random fruit location
    fruitPoint = (gg.randint(1, 11) * 10, gg.randint(1, 5) * 10)
    # fruitPoint = (gg.randint(0, gameW / 10) * 10, gg.randint(0, gameH / 10) * 10)
    segments = []

    # add snake segments
    for i in range(0, dots):
        segments.append((50 - i * dotSize, 50))

    while True:

        # check apple
        if segments[0][0] == fruitPoint[0] and segments[0][1] == fruitPoint[1]:
            segments.append((0, 0))
            dots = dots + 1
            fruitPoint = (gg.randint(1, 11) * 10, gg.randint(1, 5) * 10)
            score += 1

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

        showBoard(gg, fruitPoint, segments, dots)
        utime.sleep_ms(50)

        if segments[0][0] == 0 or segments[0][0] == 120 or segments[0][1] == 0 or segments[0][1] == 60:
            break

    gg.display.fill(0)
    gg.display.text("game over", 28, 28)
    gg.display.show()
    utime.sleep_ms(3000)

'''
snake hits itself
        for i in range(dots - 1, 1, - 1):
            if segments[i][0] == segments[0][0] and segments[i][1] == segments[0][1]:
                break
                if snake[0] in snake[1:]: break
'''



if __name__ == '__main__':
    # setup the variables
    gg = gamerGorl()
    main(gg)