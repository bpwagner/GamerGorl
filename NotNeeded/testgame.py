from gamerGorl import gamerGorl

import utime

def showBoard(gg, joy):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html

    gg.display.fill(0)
    gg.display.line(64,32,joy[0],joy[1],1)
    #gg.display.text("Text", 82, 22)
    gg.display.text(str(joy[0]) + ", " + str(joy[1]), 0, 55)
    print(str(joy[0]) + ", " + str(joy[1]))
    gg.display.show()

def main(gg):
    #put your game loop here

    while(True):
        joyx = gg.getJoyStickX()//8
        joyy = gg.getJoyStickY()//9
        joy = (joyx, joyy)
        APressed, BPressed = gg.getButtons()
        if APressed or BPressed:
            break
        #rnd = gg.randint(0, 1000) #here is how to make a random number

        showBoard(gg, joy)
        #utime.sleep_ms(200)


if __name__ == '__main__':
    #setup the variables
    gg = gamerGorl()
    main(gg)