#4/1/19 initial menu
#4/28/19 rework menu

import gc
import sys
import os
import gc
import utime
from gamerGorl import gamerGorl



#import uos
#fs_stat = uos.statvfs('/')
#fs_size = fs_stat[0] * fs_stat[2]
#fs_free = fs_stat[0] * fs_stat[3]
#print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))

menuList = ["About", "Snake", "Flappy Bird", "Simon", "Pong", "Music Box", "2048", "LED Fun", "Test All", "Files", "OS", "Reboot", "Sound: On"]
aboutList = ["Gamer Gorl by...", " Mr Wagner", " Sam A", " Katie E", " Adam M", " Jack R", " Mitchel G", " Michael W"]

def runMenu(current):
    drawMenu(current)
    while True:
        APressed, BPressed = gg.getButtons()
        gg.randint(0,1000) #keep randomizing
        JoyX = gg.getJoyStickX()
        if APressed or BPressed or JoyX >800:
            doMenuItem(current)
        JoyY = gg.getJoyStickY()
        if JoyY > 800:
            current += 1
            if current >= len(menuList):
                current = len(menuList)-1
            drawMenu(current)
        if JoyY < 200:
            current -= 1
            if current < 0:
                current = 0
            drawMenu(current)

def drawMenu(current):
    gg.display.fill(0)
    start = 0
    if current > 4:
        start = current - 4
    for i in range(start, len(menuList)):
        if i == current:
            s = "> " + menuList[i]
        else:
            s = "  " + menuList[i]
        gg.display.text(s, 0, (i-start)*10 + 4)
    gg.display.show()
    utime.sleep_ms(100)


def drawList(current, myList):
    gg.display.fill(0)
    start = 0
    if current > 4:
        start = current - 4
    for i in range(start, len(myList)):
        gg.display.text(myList[i], 0, (i - start) * 10 + 4)
    gg.display.show()


def runList(current, myList):
    drawList(current, myList)
    utime.sleep_ms(200)
    while True:
        JoyY = gg.getJoyStickY()
        JoyX = gg.getJoyStickX()
        if JoyY > 800:
            current += 1
            if current >= len(myList):
                current = len(myList)-1
        if JoyY < 200:
            current -= 1
            if current < 0:
                current = 0
        APressed, BPressed = gg.getButtons()
        if JoyX <200:
            break
        if APressed or BPressed:
            break
        else:
            drawList(current, myList)

def doMenuItem(current):
    #menuList = ["About", "Snake", "Flappy Bird", "Simon", "Breakout", "Music Box", "2048", "LED Fun", "Test All", Files]
    if current == 0:
        about()
    elif current == 1:
        import snake
        snake.main(gg)
        del sys.modules['snake']
        gc.collect()
        drawMenu(current)
    elif current == 2:
        import flappy
        flappy.main(gg)
        del sys.modules['flappy']
        gc.collect()
        drawMenu(2)
    elif current == 3:
        import simon
        simon.main(gg)
        del sys.modules['simon']
        gc.collect()
        drawMenu(3)
    elif current == 4:
        import AnimeBreakout
        AnimeBreakout.main(gg)
        del sys.modules['AnimeBreakout']
        gc.collect()
        drawMenu(current)
    elif current == 5:
        import music
        music.main(gg)
        del sys.modules['music']
        gc.collect()
        drawMenu(current)
    elif current == 6:
        import g2048
        g2048.main(gg)
        del sys.modules['g2048']
        gc.collect()
        drawMenu(current)
    elif current == 7:
        testLEDs()
    elif current == 8:
        testAll()
    elif current == 9:
        showFiles()
    elif current == 10:
        showOS()
    elif current == 11:
        import machine
        machine.reset()
    elif current == 12:
        utime.sleep_ms(200)
        if gg.playSound:
            menuList[12] = "Sound: Off"
            gg.playSound = False
        else:
            menuList[12] = "Sound: On"
            gg.playSound = True
            gg.beep()
            utime.sleep_ms(25)
            gg.lowBeep()
            utime.sleep_ms(25)
            gg.beep()
        utime.sleep_ms(200)
        drawMenu(current)
    gc.collect()


def dummy():
    gg.display.fill(0)
    gg.display.text("Dummy", 0, 30)
    gg.display.show()
    drawMenu(0)

def showFiles():
    myList = os.listdir()
    runList(0,myList)
    drawMenu(9)

def showOS():
    import micropython
    micropython.mem_info(1)
    gg.display.fill(0)
    gg.display.text("Free:  " + str(gc.mem_free()), 0, 10)
    gg.display.text("Alloc: " + str(gc.mem_alloc()), 0, 20)
    gg.display.show()
    utime.sleep_ms(5000)
    micropython.mem_info(1)
    gc.collect()
    drawMenu(10)

def testLEDs():
    gg.display.fill(0)
    gg.display.text("LED test", 0, 30)
    gg.display.show()
    gg.fillLEDs((255,0,255),1,19)
    utime.sleep_ms(500)
    gg.bounceLEDs((0,255,255),20,4)
    gg.cycleLEDs((255,255,0),30,2)
    gg.rainbowLEDs(5,5,0.1)
    drawMenu(7)

def about():
    runList(0, aboutList)
    drawMenu(0)

def testAll():
    count = 0
    keepGoing = True
    while keepGoing:
        gg.display.fill(0)
        JoyX = gg.getJoyStickX()
        JoyY = gg.getJoyStickY()
        APressed, BPressed = gg.getButtons()
        gg.display.text(str(APressed), 0, 0)
        if APressed:
            gg.beep()
        if BPressed:
            gg.lowBeep()
        gg.display.text(str(BPressed), 0, 10)
        gg.display.text(str(JoyX), 0, 20)
        gg.display.text(str(JoyY), 0, 30)
        print(str(JoyX) + "\t" + str(JoyY))
        gg.display.pixel(JoyX//20+50,JoyY//20,1)
        gg.display.show()
        count = count + 1
        if APressed and BPressed:
            keepGoing = False
    runMenu(0)

if __name__ == '__main__':
    #setup the variables
    gg = gamerGorl()
    gg.display.rotate(True)
    gg.showPBM('done.pbm')
    gg.rainbowLEDs(25, 4, 0.1)
    gg.display.invert(0)
    gc.collect()
    runMenu(0)