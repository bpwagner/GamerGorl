import utime
from machine import I2C, Pin
import machine
import sh1106

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
Buzzer = wemos_d1_pins['D3']
LED = wemos_d1_pins['D4']
SDA = wemos_d1_pins['D1']
SCL = wemos_d1_pins['D2']
X_Sel_Pin = wemos_d1_pins['D5']
Y_Sel_Pin = wemos_d1_pins['D6']
Joy_Sw = wemos_d1_pins['D0']
A_Sw = wemos_d1_pins['D7']
B_Sw = wemos_d1_pins['D8']

def testOled():
    display.fill(0)
    display.text('Hello', 0, 0)
    display.text('World', 0, 10)
    display.rotate(True)
    display.show()

def getButtons():
    firstA = A.value()
    firstB = B.value()
    utime.sleep_ms(10)
    secondA = A.value()
    secondB = B.value()
    APressed = firstA and secondA
    BPressed = firstB and secondB
    #print(APressed)
    #print(BPressed)
    return APressed, BPressed

def getJoyStickX():
    Y_Sel = Pin(Y_Sel_Pin, Pin.IN)
    Y_Sel.value(0)
    X_Sel = Pin(X_Sel_Pin, Pin.OUT)
    X_Sel.value(1)
    utime.sleep_ms(200)
    X = adc.read()
    return 1024-X

def getJoyStickY():
    X_Sel = Pin(X_Sel_Pin, Pin.IN)
    X_Sel.value(0)
    Y_Sel = Pin(Y_Sel_Pin, Pin.OUT)
    Y_Sel.value(1)
    utime.sleep_ms(200)
    Y = adc.read()
    return 1024-Y

def main():
    count = 0
    while True:
        display.fill(0)
        JoyX = getJoyStickX()
        APressed, BPressed = getButtons()
        JoyY = getJoyStickY()
        display.text(str(APressed), 0, 0)
        display.text(str(BPressed), 0, 10)
        display.text(str(JoyX), 0, 20)
        display.text(str(JoyY), 0, 30)
        print(str(JoyX) + "/t" + str(JoyY))
        display.pixel(JoyX//10,JoyY//20,1)
        display.rotate(True)
        display.show()
        count = count + 1
    return APressed, BPressed


if __name__ == '__main__':
    #setup the variables
    i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

    A = Pin(A_Sw, Pin.IN, Pin.PULL_UP)
    B = Pin(B_Sw, Pin.IN, Pin.PULL_UP)

    X_Sel = Pin(X_Sel_Pin, Pin.OUT)
    Y_Sel = Pin(Y_Sel_Pin, Pin.OUT)
    adc = machine.ADC(wemos_d1_pins['A0'])

    #testOled()
    main()