import gamerGorl
import utime, time
from machine import I2C, Pin, PWM
import machine
import sh1106
from neopixel import NeoPixel
import urandom

#BackToMain = False

songList = ['Mario Theme', 'God Only Knows', 'Shire Theme', 'Main Menu']
tones = {
        'c4': 262,
        'd4': 294,
        'e4': 330,
        'f4': 349,
        'f#4': 370,
        'g4': 392,
        'g#4': 415,
        'a4': 440,
        "a#4": 466,
        'b4': 494,
        'c5': 523,
        'c#5': 554,
        'd5': 587,
        'd#5': 622,
        'e5': 659,
        'f5': 698,
        'f#5': 740,
        'g5': 784,
        'g#5': 831,
        'a5': 880,
        'b5': 988,
        'c6': 1047,
        'c#6': 1109,
        'd6': 1175,
        ' ': 0
    }

def runMusicMenu(gg, current, backToMain):
    drawMusicMenu(gg, current)
    while not backToMain:
        APressed, BPressed = gg.getButtons()
        JoyX = gg.getJoyStickX()
        if APressed or BPressed or JoyX >800:
            if current == 3:
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
    #songList = ['Mario Theme', 'God Only Knows', 'Shire Theme', 'Main Menu']
    if current == 0:
        marioTheme(gg)
        drawMusicMenu(gg, current)
    elif current == 1:
        godOnlyKnows(gg)
        drawMusicMenu(gg, current)
    elif current == 2:
        shireTheme(gg)
        drawMusicMenu(gg, current)

def dummy():
    gg.display.fill(0)
    gg.display.text("Dummy", 0, 30)
    gg.display.show()
    drawMusicMenu(gg, 0)

def marioTheme(gg):
    tempo = 5
    beeper = PWM(Pin(gg.Buzzer, Pin.OUT), freq=440, duty=512)
    melody = ['e5', 'e5', 'e5', 'c5', 'e5', 'g5', 'g4',  # bar 1
              'c5', 'g4', 'e4', 'a4', 'b4', 'a#4', 'a4',  # bar 2
              'g4', 'e5', 'g5', 'a5', 'f5', 'g5', 'e5', 'c5', 'd5', 'b4',  # bar 3
              'c5', 'g4', 'e4', 'a4', 'b4', 'a#4', 'a4',  # bar 4
              'g4', 'e5', 'g5', 'a5', 'f5', 'g5', 'e5', 'c5', 'd5', 'b4',  # bar 5
              'g5', 'f#5', 'f5', 'd#5', 'e5', 'g#4', 'a4', 'c5', 'a4', 'c5', 'd5',  # bar 6
              'g5', 'f#5', 'f5', 'd#5', 'e5', 'c6', 'c6', 'c6',  # bar 7
              'g5', 'f#5', 'f5', 'd#5', 'e5', 'g#4', 'a4', 'c5', 'a4', 'c5', 'd5',  # bar 8
              'd#5', 'd5', 'c5']  # bar 9
    rhythm = [8, 16, 8, 16, 16, 4, 4,  # bar 1
              8, 8, 8, 16, 16, 16, 16,  # bar 2
              8, 16, 16, 8, 8, 8, 8, 16, 16, 8,  # bar 3
              8, 8, 8, 16, 16, 16, 16,  # bar 4
              8, 16, 16, 8, 8, 8, 8, 16, 16, 8,  # bar 5
              16, 16, 16, 16, 8, 16, 16, 8, 16, 16, 8,  # bar 6
              16, 16, 16, 16, 8, 8, 16, 8,  # bar 7
              16, 16, 16, 16, 8, 16, 16, 8, 16, 16, 8,  # bar 8
              8, 8, 8]  # bar 9

    for tone, length in zip(melody, rhythm):
        print(tone)
        print(length)
        APressed, BPressed = gg.getButtons()
        if BPressed:
            break
        beeper.freq(tones[tone])
        time.sleep(tempo / length)
    beeper.deinit()

def godOnlyKnows(gg):
    tempo = 5
    beeper = PWM(Pin(gg.Buzzer, Pin.OUT), freq=440, duty=512)
    melody = ['d5', 'c#5', 'd5', 'c#5', 'b4', 'f#4', 'b4', ' ', # bar 1-2
              'a4', 'a4', 'g#4', 'a4', 'c#5', 'f#5', 'a4', 'b4', 'c#5', ' ', # bar 3-4
              'e5', 'd#5', 'e5', 'f#5', 'b4', 'c#5', 'd5', ' ', #bar 5-6
              'e5', 'e5', 'd#5', 'e5', 'g#5', 'c#5', 'd#5', 'e5', ' ', #bar 7-8
              'c#5', 'b4', 'c#5', 'b4', 'e5', 'b4', 'a4', 'g#4', 'e4', 'f#4'] # bar 9-11
    rhythm = [16, 16, 16, 8, 16, 8, 8, 8, # bar 1-2
              8, 8, 16, 16, 8, 8, 16, 16, 8, 8, # bar 3-4
              4, 16, 16, 8, 16, 8, 8, 8, # bar 5-6
              8, 8, 16, 16, 8, 8, 16, 8, 8, # bar 7-8
              4, 16, 16, 8, 8, 16, 8, 16, 8, 4] # bar 9-11

    for tone, length in zip(melody, rhythm):
        print(tone)
        print(length)
        APressed, BPressed = gg.getButtons()
        if BPressed:
            break
        beeper.freq(tones[tone])
        time.sleep(tempo / length)
    beeper.deinit()

def shireTheme(gg):
    tempo = 5
    beeper = PWM(Pin(gg.Buzzer, Pin.OUT), freq=440, duty=512)
    melody = ['d4', 'e4', 'f#4', 'a4', 'f#4', 'e4', 'f#4', 'e4', 'd4', 'f#4', 'a4', #bar 3-4
              'b4', 'd5', 'c#5', 'a4', 'f#4', 'g4', 'f#4', 'e4', 'd4'] #bar 5-6
    rhythm = [8, 8, 8, 8, 16, 16, 8, 8, 8, 8,
              8, 8, 8, 8, 8, 8, 8, 8]

    for tone, length in zip(melody, rhythm):
        print(tone)
        print(length)
        APressed, BPressed = gg.getButtons()
        if BPressed:
            break
        beeper.freq(tones[tone])
        time.sleep(tempo / length)
    beeper.deinit()

def main(gg):
    runMusicMenu(gg, 0, False)