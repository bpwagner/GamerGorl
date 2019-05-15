import utime
from machine import Pin

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

#Game pins
Buzzer = D3
LED = D4
SDA = D1
SCL = D2
Joy_Sw = D0
A_Sw = D7
B_Sw = D8

def main():
    led = Pin(2, Pin.OUT)
    enabled = False
    while True:
        if enabled:
            led.off()
        else:
            led.on()
        utime.sleep_ms(1000)
        enabled = not enabled

def testOled():
    from machine import I2C, Pin
    import sh1106

    i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)

    display.fill(0)
    display.text('Hello', 0, 0)
    display.text('World', 0, 10)
    display.rotate(True)
    display.show()


if __name__ == '__main__':
    testOled()
    #main()