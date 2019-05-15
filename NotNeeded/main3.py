import utime, time
from machine import I2C, Pin, PWM
import machine
import sh1106
from neopixel import NeoPixel

#Pin defs for Wemos D1 Mini
D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D5 = 14
D6 = 12
D7 = 13
D8 = 15
A0 = 0

wemos_d1_pins = {
    'D0': 16,  # GPIO
    'D1': 5,   # GPIO, I2C SCL
    'D2': 4,   # GPIO, I2C SDA
    'D3': 0,   # GPIO
    'D4': 2,   # GPIO
    'D5': 14,  # GPIO, SPI SCK (Serial Clock)
    'D6': 12,  # GPIO, SPI MISO (Master in, Slave out)
    'D7': 13,  # GPIO, SPI MOSI (Master out, Slave in)
    'D8': 15,  # GPIO, SPI SS (Slave select)
    'A0': 0,   # Analog in, via ADC
    'RX': 3,   # Receive
    'TX': 1    # Transmit
}

#Game pins
Buzzer = wemos_d1_pins['D8']
Neo = wemos_d1_pins['D4']
SDA = wemos_d1_pins['D2']
SCL = wemos_d1_pins['D1']
X_Sel_Pin = wemos_d1_pins['D6']
Y_Sel_Pin = wemos_d1_pins['D5']
Joy_Sw = wemos_d1_pins['D3']
A_Sw = wemos_d1_pins['D7']
B_Sw = wemos_d1_pins['D3']

def testOled():
    display.fill(0)
    display.text('Hello', 0, 0)
    display.text('World', 0, 10)
    display.rotate(True)
    display.show()

def testNeoPixels():
    n=10
    np = NeoPixel(Pin(Neo), n)

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        #time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        #time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def getButtons():
    firstA = A.value()
    firstB = B.value()
    utime.sleep_ms(10)
    secondA = A.value()
    secondB = B.value()
    APressed = not (firstA and secondA)
    BPressed = not (firstB and secondB)
    #print(APressed)
    #print(BPressed)
    return APressed, BPressed

def getJoyStickX():
    Y_Sel.value(0)
    X_Sel.value(1)
    #utime.sleep_ms(200)
    X = adc.read()
    X_Sel.value(0)
    return X

def getJoyStickY():
    X_Sel.value(0)
    Y_Sel.value(1)
    #utime.sleep_ms(200)
    Y = adc.read()
    Y_Sel.value(0)
    return 1024-Y


def playSong():
    tempo = 5
    tones = {
        'c': 262,
        'd': 294,
        'e': 330,
        'f': 349,
        'g': 392,
        'a': 440,
        'b': 494,
        'C': 523,
        ' ': 0,
    }
    beeper = PWM(Pin(Buzzer, Pin.OUT), freq=440, duty=512)
    melody = 'cdefgabC'
    rhythm = [8, 8, 8, 8, 8, 8, 8, 8]

    for tone, length in zip(melody, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo / length)
    beeper.deinit()


def beep():
    beeper = PWM(Pin(Buzzer, Pin.OUT), freq=1000, duty=512)
    utime.sleep_ms(20)
    beeper.deinit()

def lowBeep():
    beeper = PWM(Pin(Buzzer, Pin.OUT), freq=440, duty=512)
    utime.sleep_ms(20)
    beeper.deinit()

def main():
    count = 0
    while True:
        display.fill(0)
        JoyX = getJoyStickX()
        JoyY = getJoyStickY()
        APressed, BPressed = getButtons()
        display.text(str(APressed), 0, 0)
        if APressed:
            beep()
        if BPressed:
            lowBeep()
        display.text(str(BPressed), 0, 10)
        display.text(str(JoyX), 0, 20)
        display.text(str(JoyY), 0, 30)
        print(str(JoyX) + "\t" + str(JoyY))
        display.pixel(JoyX//20+50,JoyY//20,1)
        display.rotate(True)
        display.show()
        count = count + 1

if __name__ == '__main__':
    #setup the variables

    i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

    #button pins
    A = Pin(A_Sw, Pin.IN, Pin.PULL_UP)
    B = Pin(B_Sw, Pin.IN, Pin.PULL_UP)

    #joystick pins
    X_Sel = Pin(X_Sel_Pin, Pin.OUT)
    Y_Sel = Pin(Y_Sel_Pin, Pin.OUT)
    X_Sel.value(0)
    Y_Sel.value(0)
    adc = machine.ADC(wemos_d1_pins['A0'])

    #testOled()
    #testNeoPixels()
    #playSong()
    main()