# A large proof-of-concept project where many actuators, sensors
# and communications are connected and tested

from machine import UART,Pin,I2C
import utime
import time

import mpr121

# A tutorial and Github repo for controlling the LCD through the i2c PCF8574 module
# https://www.instructables.com/RPI-Pico-I2C-LCD-Control/
# https://github.com/T-622/RPI-PICO-I2C-LCD
from machine import Pin,I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

i2c_1 = I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=400000)
lcd = I2cLcd(i2c_1, 0x3F, 2, 16) # I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS  NOTE: I2C_ADDR may be 0x27
lcd.clear()
lcd.move_to(0,0)   # x=0..15, y=0..//1
lcd.putstr("Hello Pico!")

mpr = mpr121.MPR121(i2c_1, 0x5A)   # 0x5A is address on i2c bus 1

# print("Scanning i2c bus 0... )
# print(i2c_0.scan())  # print addresses on i2c bus 0
print("Scanning i2c bus 1... ")
print(i2c_1.scan())  # print addresses on i2c bus 1

import _thread
import WS2812

neopixel = WS2812.WS2812(4, 15, 0.3)  # pin, num_of_pixels, brightness=0..1

def neopixel_demo():    # neopixel demo
        lcd.clear()
        print("neopixel fills")
        lcd.putstr("neopixel fills\n")
        for color in WS2812.COLORS:       
            neopixel.pixels_fill(color)
            neopixel.pixels_show()
            time.sleep(0.2)
        print("neopixel chases")
        lcd.putstr("neopixel chases\n")
        for color in WS2812.COLORS:       
            neopixel.color_chase(color, 0.01)
        print("neopixel rainbow")
        lcd.putstr("neopixel rainbow\n")
        neopixel.rainbow_cycle(0)
        neopixel.pixels_fill(WS2812.BLACK)
        neopixel.pixels_show()
        lcd.clear()

#        _thread.exit()

#----------------------------------------------------------
#  Raspi Pico and Microbit communication over serial UART. Check page 13 of
#  https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf 
#----------------------------------------------------------

import ultrasonic

# actuators
led = machine.Pin(13, machine.Pin.OUT)  
led_onboard = machine.Pin(25, machine.Pin.OUT)  # 25 is the internal onboard led
buzzer = machine.Pin(11, machine.Pin.OUT)
xmas_lights = machine.PWM(machine.Pin(21))

# sensors
button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
potentiometer = machine.ADC(28)
ultrasonic_1 = ultrasonic.Ultrasonic(16,17)    # trigger pin, echo pin
sensor_temperature = machine.ADC(4)
conversion_factor = 3.3 / (65535)  # used for temperature sensor

# serial communication with the Microbit pin1 (tx) and pin2 (rx)
# Refer to page 13 of Raspberry Pi Pico Python SDK  (Chapter 3.2 UART)
# https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf
uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
#txData = b'Pico says hello\n\r'

# serial input from the Thonny console
print("Hello Pico from Thonny editor 002")
num_blink = 3
# num_blink = int(input("How many times do you want to blink ?"))
print("I will blink " + str(num_blink) + " times...")

for i in range(num_blink):
    led.value(1)
    utime.sleep(0.5)
    led.value(0)
    utime.sleep(0.5)

print("Entering loop...")

while True:
    #lcd.clear()
    dist_1 = ultrasonic_1.ultrasonic_distance()
    print("Ultrasonic dist (trig=16,echo=17) = ", dist_1, end='  ')
#    txData = b'distance 234\n\r' # + str(distance) + '\n\r'
    txData = 'distance ' + str(dist_1) + '\n' # \r'
    print("txData = " + txData)
    lcd.move_to(0,0)
    lcd.putstr("ds=" + '{:.1f}'.format(dist_1) + "  ")
    reading = sensor_temperature.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    lcd.move_to(9,0)
    lcd.putstr("tm=" + '{:.1f}'.format(temperature) + "  ")
    uart0.write(bytes(txData,'utf-8'))
    if button.value() == 1:
        print("Button pressed True")
        led.value(1)
        for i in range(66):
            xmas_lights.duty_u16(i * 1000)
            utime.sleep(0.05)
        neopixel_demo()
        for i in range(66):
            xmas_lights.duty_u16((65-i)*1000)
            utime.sleep(0.05)
#        _thread.exit()
#        _thread.start_new_thread(neopixel_demo,())

    # the potentiometer value is 0..65535  (unsigned 16-bit)
    print("Potentiometer = ", potentiometer.read_u16() * 100 / 65535, end='  ')
    lcd.move_to(0,1)
    lcd.putstr("pot=" + '{:.1f}'.format(potentiometer.read_u16() * 100 / 65535) + "  ")

    rxData = bytes()
    while uart0.any() > 0:
        rxData += uart0.read(1)
    rx_string = rxData.decode('utf-8') 
    print("rxData = " + rx_string)
    if rx_string.find("Microbit") != -1:
        buzzer.value(1)
    if rx_string.find('pin ') == 0:
        words = rx_string.split()
        pin = int(words[1])
        value = int(words[2])
        if pin == 12:
            buzzer.value(value )
        elif pin == 14:
            led.value(value)
        elif pin == 25:
            led_onboard.value(value)
    lcd.move_to(9,1)
    lcd.putstr("tc=" + str(mpr.touched()) + "   ")
    utime.sleep(0.2)
    buzzer.value(0)
    led.value(0)
