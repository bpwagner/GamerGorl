from gamerGorl import gamerGorl

import utime
import framebuf
from machine import I2C, Pin, PWM
from neopixel import NeoPixel


def randColor(gg):
    r = gg.randint(0, 255)
    g = gg.randint(0, 255)
    b = gg.randint(0, 255)
    return (r, g, b)


def showHighscore(gg, score, highscore2):
    gg.display.fill(0)
    gg.display.text("SCORE: " + str(score), 0, 0)
    gg.display.text("HIGHSCORE: " + str(highscore2), 0, 10)
    gg.display.text("PLAY AGAIN?", 20, 30)
    gg.display.text("YES[A]", 10, 45)
    gg.display.text("NO[B]", 80, 45)
    gg.display.show()

def showBoard(gg, birdx, birdy, cntr, a, b, c, d, r1, r2, r3, r4, score, highscore2):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html
    gg.display.fill(0)
    gg.display.rect(birdx, birdy, 5, 5, 1)
    # gg.display.text("Text", 82, 22)
    # gg.display.text(str(1234), 82, 32)
    # for i in range(numOfPipes):
    gg.display.fill_rect(a - cntr, 0, 8, r1, 1)
    gg.display.fill_rect(a - cntr, r1 + 15, 8, 64 - r1 - 15, 1)
    gg.display.fill_rect(b - cntr, 0, 8, r2, 1)
    gg.display.fill_rect(b - cntr, r2 + 15, 8, 64 - r2 - 15, 1)
    gg.display.fill_rect(c - cntr, 0, 8, r3, 1)
    gg.display.fill_rect(c - cntr, r3 + 15, 8, 64 - r3 - 15, 1)
    gg.display.fill_rect(d - cntr, 0, 8, r4, 1)
    gg.display.fill_rect(d - cntr, r4 + 15, 8, 64 - r4 - 15, 1)
    gg.display.text(str(score), 0, 0)
    gg.display.show()


def main(gg):
    playagain2 = True
    f = open("Highscore", "r")
    highscore2 = int(f.readline())
    f.close()
    while playagain2:
        playing = True
        #put your game loop here
        birdx = 20
        birdy = 20
        gravity = 0
        cntr = 0
        a = 120
        b = 150
        c = 180
        d = 210
        a2 = 0
        b2 = 0
        c2 = 0
        d2 = 0
        r1 = gg.randint(14, 40)
        r2 = gg.randint(14, 40)
        r3 = gg.randint(14, 40)
        r4 = gg.randint(14, 40)
        score = 0
        gg.fillLEDs((255, 0, 128), 0, 19)
        while playing:
            JoyX = gg.getJoyStickX()
            JoyY = gg.getJoyStickY()
            APressed, BPressed = gg.getButtons()
            #else:
            if APressed:
                birdy -= 5
                gravity = 0
                gg.beep()
            elif birdy - 5 >= 64:
                birdy = 59
                gravity =0
            else:
                birdy += gravity
                gravity += 1

            if cntr % 120 == 0:
                if a2 >= 1:
                    a += 120
                    r1 = gg.randint(14, 40)  # here is how to make a random number
                    score += 1
                    gg.fillLEDs(randColor(gg),0,19)
                a2 += 1
            if cntr % 120 == 30:
                if b2 >= 1:
                    b += 120
                    r2 = gg.randint(14, 40)
                    score += 1
                    gg.fillLEDs(randColor(gg), 0, 19)
                b2 += 1
            if cntr % 120 == 60:
                if c2 >= 1:
                    c += 120
                    r3 = gg.randint(14, 40)
                    score += 1
                    gg.fillLEDs(randColor(gg), 0, 19)
                c2 += 1
            if cntr % 120 == 90:
                if d2 >= 1:
                    d += 120
                    r4 = gg.randint(14, 40)
                    score += 1
                    gg.fillLEDs(randColor(gg), 0, 19)
                d2 += 1

            showBoard(gg, birdx, birdy, cntr, a, b, c, d, r1, r2, r3, r4, score, highscore2)
            utime.sleep_ms(15)
            cntr += 2
            for k in range(4):
                for t in range(5):
                    num = 0
                    num2 = 0
                    num3 = 0
                    num4 = 0
                    for i in range(8):
                        if birdx+k == a - cntr + i:
                            for j in range(15):
                                if birdy+t != r1+j:
                                    num += 1
                    for i in range(8):
                        if birdx+k == b - cntr + i:
                            for j in range(15):
                                if birdy+t != r2+j:
                                    num2 += 1
                    for i in range(8):
                        if birdx+k == c - cntr + i:
                            for j in range(15):
                                if birdy+t != r3+j:
                                    num3 += 1
                    for i in range(8):
                        if birdx+k == d - cntr + i:
                            for j in range(15):
                                if birdy+t != r4+j:
                                    num4 += 1
                    if num == 15 or num2 == 15 or num3 == 15 or num4 == 15:
                        if score > highscore2:
                            highscore2 = score
                            f = open("Highscore", "w")

                            f.write(str(highscore2))
                            f.close()
                        playing = False
        z = True
        showHighscore(gg, score, highscore2)
        utime.sleep_ms(200)
        while z:
            #gg.time.sleep_ms(gg.mstime)
            APressed, BPressed = gg.getButtons()
            if APressed:
                playagain2 = True
                z = False
            if BPressed:
                playagain2 = False
                z = False
                utime.sleep_ms(200)