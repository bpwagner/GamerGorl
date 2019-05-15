# class for all gamerGorl board
# Brian Wagner 3/25/19

import utime, time
from machine import I2C, Pin, PWM
import machine
import sh1106
from neopixel import NeoPixel


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

        self.i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=400000)
        self.display = sh1106.SH1106_I2C(128, 64, self.i2c, Pin(16), 0x3c)

        # button pins
        self.A = Pin(self.A_Sw, Pin.IN, Pin.PULL_UP)
        self.B = Pin(self.B_Sw, Pin.IN, Pin.PULL_UP)

        # joystick pins
        self.X_Sel = Pin(self.X_Sel_Pin, Pin.OUT)
        self.Y_Sel = Pin(self.Y_Sel_Pin, Pin.OUT)
        self.X_Sel.value(0)
        self.Y_Sel.value(0)
        adc = machine.ADC(wemos_d1_pins['A0'])

    def testOled(self):
        self.display.fill(0)
        self.display.text('Hello', 0, 0)
        self.display.text('World', 0, 10)
        self.display.rotate(True)
        self.display.show()

    def testNeoPixels(self):
        n = 10
        np = NeoPixel(Pin(self.Neo), n)

        # cycle
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            np[i % n] = (255, 255, 255)
            np.write()
            # time.sleep_ms(25)

        # bounce
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 128)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 0)
            else:
                np[n - 1 - (i % n)] = (0, 0, 0)
            np.write()
            # time.sleep_ms(60)

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

    def playSong(self):
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
        beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=440, duty=512)
        melody = 'cdefgabC'
        rhythm = [8, 8, 8, 8, 8, 8, 8, 8]

        for tone, length in zip(melody, rhythm):
            beeper.freq(tones[tone])
            time.sleep(tempo / length)
        beeper.deinit()

    def beep(self):
        beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=1000, duty=512)
        utime.sleep_ms(20)
        beeper.deinit()

    def lowBeep(self):
        beeper = PWM(Pin(self.Buzzer, Pin.OUT), freq=440, duty=512)
        utime.sleep_ms(20)
        beeper.deinit()