# class for all gamerGorl board
# Brian Wagner 3/25/19

import utime
from machine import I2C, Pin, PWM
import machine
import sh1106
from neopixel import NeoPixel
import urandom
import framebuf

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


# from https://stackoverflow.com/questions/24852345/hsv-to-rgb-color-conversion
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)

class gamerGorl:

    def __init__(self):

        wemos_d1_pins = {
            'D0': 16,  # GPIO
            'D1': 5,  # GPIO, I2C SCL
            'D2': 4,  # GPIO, I2C SDA
            'D3': 0,  # GPIO
            'D4': 2,  # GPIO
            'D5': 14,  # GPIO, SPI SCK (Serial Clock)
            'D6': 12,  # GPIO, SPI MISO (Master in, Slave out)
            'D7': 13,  # GPIO, SPI MOSI (Master out, Slave in)
            'D8': 15,  # GPIO, SPI SS (Slave select)
            'A0': 0,  # Analog in, via ADC
            'RX': 3,  # Receive
            'TX': 1  # Transmit
        }


        # Game pins
        self.Buzzer = wemos_d1_pins['D8']
        self.Neo = wemos_d1_pins['D4']
        self.SDA = wemos_d1_pins['D2']
        self.SCL = wemos_d1_pins['D1']
        self.X_Sel_Pin = wemos_d1_pins['D6']
        self.Y_Sel_Pin = wemos_d1_pins['D5']
        self.Joy_Sw = wemos_d1_pins['D3']
        self.A_Sw = wemos_d1_pins['D7']
        self.B_Sw = wemos_d1_pins['D3']

        self.i2c = I2C(scl=Pin(self.SCL), sda=Pin(self.SDA), freq=400000)
        self.display = sh1106.SH1106_I2C(128, 64, self.i2c, Pin(16), 0x3c)

        # button pins
        self.A = Pin(self.A_Sw, Pin.IN, Pin.PULL_UP)
        self.B = Pin(self.B_Sw, Pin.IN, Pin.PULL_UP)

        # joystick pins
        self.X_Sel = Pin(self.X_Sel_Pin, Pin.OUT)
        self.Y_Sel = Pin(self.Y_Sel_Pin, Pin.OUT)
        self.X_Sel.value(0)
        self.Y_Sel.value(0)
        self.adc = machine.ADC(wemos_d1_pins['A0'])

        #led
        self.numLEDs = 19
        self.np = NeoPixel(Pin(self.Neo), self.numLEDs)

        #sound on
        self.playSound = True

    def soundOn(self):
        self.playSound = True

    def soundOff(self):
        self.playSound = False

    def getNumLEDs(self):
        return self.numLEDs

    def setNumLEDs(self, n):
        self.numLEDs = n

    def randint(self, a, b):
        x = urandom.getrandbits(16)
        x = x % (b+1-a) + a
        return x

    def clearLEDs(self):
        # clear
        for i in range(self.numLEDs):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def fillLEDs(self, color, fromLED, toLED):
        for i in range(fromLED, toLED):
            self.np[i] = color
        self.np.write()

    def cycleLEDs(self, color, mstime, times):
        for i in range(times * self.numLEDs):
            for j in range(self.numLEDs):
                self.np[j] = (0, 0, 0)
            self.np[i % self.numLEDs] = color
            self.np.write()
            utime.sleep_ms(mstime)

    def bounceLEDs(self, color, mstime, times):
        for i in range(times * self.numLEDs):
            for j in range(self.numLEDs):
                self.np[j] = color
            if (i // self.numLEDs) % 2 == 0:
                self.np[i % self.numLEDs] = (0, 0, 0)
            else:
                self.np[self.numLEDs - 1 - (i % self.numLEDs)] = (0, 0, 0)
            self.np.write()
            utime.sleep_ms(mstime)

    def rainbowLEDs(self, mstime, times, increment):
        hue = increment
        for i in range(times * self.numLEDs):
            color = hsv_to_rgb(hue, 1.0, 1.0)
            color = (int(color[0]),int(color[1]), int(color[2]))
            #print(color)
            self.np[i % self.numLEDs] = color
            self.np.write()
            hue += increment
            utime.sleep_ms(mstime)

    def getButtons(self):
        firstA = self.A.value()
        firstB = self.B.value()
        utime.sleep_ms(10)
        secondA = self.A.value()
        secondB = self.B.value()
        APressed = not (firstA and secondA)
        BPressed = not (firstB and secondB)
        # print(APressed)
        # print(BPressed)
        return APressed, BPressed

    def getJoyStickX(self):
        self.Y_Sel.value(0)
        self.X_Sel.value(1)
        # utime.sleep_ms(200)
        X = self.adc.read()
        self.X_Sel.value(0)
        return X

    def getJoyStickY(self):
        self.X_Sel.value(0)
        self.Y_Sel.value(1)
        # utime.sleep_ms(200)
        Y = self.adc.read()
        self.Y_Sel.value(0)
        return 1024 - Y

    def beep(self):
        if self.playSound:
            beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=1000, duty=512)
            utime.sleep_ms(20)
            beeper.deinit()

    def lowBeep(self):
        if self.playSound:
            beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=440, duty=512)
            utime.sleep_ms(20)
            beeper.deinit()

    def playTone(self, tone, tone_duration, total_duration):
        if self.playSound:
            print(str(tone_duration) + " " + str(total_duration))
            beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=tones[tone], duty=512)
            utime.sleep_ms(tone_duration)
            beeper.deinit()
            utime.sleep_ms(int(total_duration * 1000)-tone_duration)

    #https://forum.micropython.org/viewtopic.php?t=4901
    #
    def showPBM(self, filename):
        f = open(filename, 'rb')
        f.readline()  # Magic number
        f.readline()  # Creator comment
        f.readline()  # Dimensions
        #data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(bytearray(f.read()), 128, 64, framebuf.MONO_HLSB)

        self.display.invert(1)
        self.display.blit(fbuf, 0, 0)
        self.display.show()
        f.close()


    def flashRed(self, fromLED, toLED):
        for i in range(0, 2 * 256, 1):
            for j in range(fromLED, toLED):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.np[j] = (val, 0, 0)
            self.np.write()

        # clear
        for i in range(self.numLEDs):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def flashGreen(self, fromLED, toLED):
        for i in range(0, 2 * 256, 1):
            for j in range(fromLED, toLED):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.np[j] = (0, val, 0)
            self.np.write()

        # clear
        for i in range(self.numLEDs):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def flashBlue(self, fromLED, toLED, fromLED2, toLED2):
        for i in range(0, 2 * 256, 1):
            for j in range(fromLED, toLED):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.np[j] = (0, 0, val)
            for j in range(fromLED2, toLED2):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.np[j] = (0, 0, val)
            self.np.write()

        # clear
        for i in range(self.numLEDs):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def flashYellow(self, fromLED, toLED):
        for i in range(0, 2 * 256, 1):
            for j in range(fromLED, toLED):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                self.np[j] = (val, val, 0)
            self.np.write()

        # clear
        for i in range(self.numLEDs):
            self.np[i] = (0, 0, 0)
        self.np.write()