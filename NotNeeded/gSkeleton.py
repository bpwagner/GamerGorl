from gamerGorl import gamerGorl

import utime

def showBoard(gg):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html

    gg.display.fill(0)
    gg.display.rect(18,0,58,58,1)
    gg.display.text("Text", 82, 22)
    gg.display.text(str(1234), 82, 32)
    gg.display.show()

def main(gg):
    #put your game loop here

    while(True):
        JoyX = gg.getJoyStickX()
        JoyY = gg.getJoyStickY()
        APressed, BPressed = gg.getButtons()
        rnd = gg.randint(0, 1000) #here is how to make a random number

        showBoard(gg)
        utime.sleep_ms(200)


if __name__ == '__main__':
    #setup the variables
    gg = gamerGorl()
    main(gg)