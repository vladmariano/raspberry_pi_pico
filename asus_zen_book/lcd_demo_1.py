# LCD control
# Page #120 of Get Started with MicroPython on Raspberry Pi Pico
# https://hackspace.raspberrypi.org/books/micropython-pico

#import machine
#import utime
#import random

#sda = machine.Pin(0)
#scl = machine.Pin(1)
#i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
# print(i2c.scan())  # print i2c addresses

#adc = machine.ADC(4)
#conversion_factor = 3.3 / (65535)
#while True:
#    i2c.writeto(62, '\x7C')
#    i2c.writeto(62, '\x7D')
#    i2c.writeto(62, "hello LCD")
#    print(random.randint(0,10))
#    utime.sleep(1)

from LCD_I2C import *
import utime

lcd = LCD(sda = 0, scl = 1)
lcd.set_cursor(1,1)
lcd.on(cursor=True,blink=True)
while True:
#    lcd.on()
    utime.sleep(0.5)
#    lcd.off()
#    lcd.clear()
    lcd.write("Hello World\n")
#    lcd.write("second line")
    utime.sleep(0.5)