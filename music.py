import utime

songList = ['Mario Theme', 'God Only Knows', 'Shire Theme', 'Wonderwall', 'Main Menu']

def runMusicMenu(gg, current, backToMain):
    drawMusicMenu(gg, current)
    while not backToMain:
        APressed, BPressed = gg.getButtons()
        JoyX = gg.getJoyStickX()
        if APressed or BPressed or JoyX >800:
            if current == 4:
                backToMain = True
            else:
                doMusicMenuItem(gg, current)

        JoyY = gg.getJoyStickY()
        if JoyY > 800:
            current += 1
            if current >= len(songList):
                current = len(songList)-1
            drawMusicMenu(gg, current)
        if JoyY < 200:
            current -= 1
            if current < 0:
                current = 0
            drawMusicMenu(gg, current)

def drawMusicMenu(gg, current):
    gg.display.fill(0)
    start = 0
    if current > 4:
        start = current - 4
    for i in range(start, len(songList)):
        if i == current:
            s = "> " + songList[i]
        else:
            s = "  " + songList[i]
        gg.display.text(s, 0, (i-start)*10 + 4)
    gg.display.show()
    utime.sleep_ms(100)


def drawSongList(gg, current, myList):
    gg.display.fill(0)
    start = 0
    if current > 4:
        start = current - 4
    for i in range(start, len(myList)):
        gg.display.text(myList[i], 0, (i - start) * 10 + 4)
    gg.display.show()


def runSongList(gg, current, myList):
    drawSongList(gg, current, myList)
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
            drawSongList(gg, current, myList)

def doMusicMenuItem(gg, current):
    #songList = ['Mario Theme', 'God Only Knows', 'Shire Theme', 'Wonderwall', 'Main Menu']
    if current == 0:
        playSong(gg, "marioTheme", 75, 3.0)
        drawMusicMenu(gg, current)
    elif current == 1:
        #godOnlyKnows(gg)
        drawMusicMenu(gg, current)
    elif current == 2:
        #shireTheme(gg)
        drawMusicMenu(gg, current)
    elif current == 3:
        #wonderwall(gg)
        drawMusicMenu(gg, current)


def playSong(gg, filename, tone_duration, tempo):
    mario = open("marioTheme", "r")
    while True:
        linesplit = mario.readline().split(",")
        tone = linesplit[0]
        length = int(linesplit[1])
        if tone == "end":
            break
        print("note: " + tone + " " + str(length))
        APressed, BPressed = gg.getButtons()
        if BPressed:
            break
        duration = tempo/length
        print(duration)
        gg.playTone(tone, tone_duration, duration)
    mario.close()

def main(gg):
    runMusicMenu(gg, 0, False)