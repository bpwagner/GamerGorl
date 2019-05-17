from gamerGorl import gamerGorl

import utime
#BarPosition = ()
def showBoard(gg, bar,opponentbar, ball):
    # put drawing commands here
    # here are the commands https://docs.micropython.org/en/latest/library/framebuf.html


    gg.display.fill(0)
    gg.display.rect(0, 0, 128, 64, 1)
    gg.display.rect(bar[0],bar[1],20,5,1)
    gg.display.rect(opponentbar[0], opponentbar[1], 20, 5, 1)
    gg.display.rect(ball[0] ,ball[1] ,5,5,1)
    #gg.display.text("Pornhub.com", 40, 22)
  #  gg.display.text(str(69), 82, 32)


    gg.display.show()



def main(gg):
#put your game loop here

    playing = 1
    # BALL CONTROL
    z = 64
    up = False
    down = True
    left = False
    right = True

    ball = (32, 32)
    bspeed = 5
    x = 64
#createblocks

#blockx= (0, 10, 20, 30, 40, 50)
#blocky= (0,  0,  0,  0,  0,  0)
#blockbool = (True,True,True,True,True,True)

#for i in range(6):
  #  gg.display.rect(blockx[i], blocky[i], 10, 5, 1)






    while (playing == 1):
        JoyX = gg.getJoyStickX()
        if JoyX < 200:
                x -= 10
        elif JoyX > 800:
                x += 10

        if (ball[0] >= 124):

                    right = False
                    left = True

        if (ball[0] <= 1):

                    right = True
                    left = False

        if ball[1] > 55 and ball[0] > x-5 and ball[0] < x+20:
           if ball[0] <= x + 20 and ball[0] > x+13:
                right = True
                left = False
                up = True
                down = False
           elif ball[0] >= x-5 and ball[0] <= x+7:
                left = True
                right = False
                up = True
                down = False
           elif ball[0] > x + 7 and ball[0] < x + 12:
               left = False
               right = False
               up = True
               down = False
        elif ball[1] > 64:
           # gg.display.text("Pornhub.com", 40, 22)
            playing = 2
            break

        if ball[1] < 5 and ball[0] > z and ball[0] < z + 20:
            down = True
            up = False
        elif ball[1] <= 0:

           #gg.display.text("Pornhub.com", 40, 22)
            playing = 2
            break

        ballx = ball[0]
        bally = ball[1]
        rnd = gg.randint(1, 2)  # here is how to make a random number
        if (up):
            bally = ball[1] - bspeed
        if (down):
            bally = ball[1]+bspeed
        if (left):
            ballx = ball[0] -bspeed #*rnd
        if (right):
            ballx = ball[0] +bspeed #*rnd
            # AI
        if ball[0] < z+10:
                z -= 5
        if ball[0] > z+10:
                z += 5
        #JoyY = gg.getJoyStickY()
        bar = (x,60)
        opponentbar = (z,0)
        ball = (ballx, bally)
        APressed, BPressed = gg.getButtons()


        showBoard(gg, bar,opponentbar, ball)
        #utime.sleep_ms(200)
    gg.display.fill(0)
    gg.display.rect(0, 0, 128, 64, 1)
    gg.display.text("GG", 1, 22)
    gg.display.show()





if __name__ == '__main__':
    #setup the variables
    gg = gamerGorl()
    main(gg)