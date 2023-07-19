# Programmer:  Vladimir Mariano
# Last update:  27, October, 2022
#
# Modules needed for this program:
# lcd_api.py and
# pico_i2c_lcd.py
#    Code for Pico accessing LCD via i2c copied from:
#    https://github.com/T-622/RPI-PICO-I2C-LCD
#    https://github.com/T-622/RPI-PICO-I2C-LCD/blob/main/lcd_api.py   
#    https://github.com/T-622/RPI-PICO-I2C-LCD/blob/main/pico_i2c_lcd.py
# WS2812.py
#    Code of WS2812 "Neopixels" adapted from:
#    https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio/neopixel_ring
# ultrasonic.py
#    Pico ultrasonic sensor code was adapted from
#       https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor
#    Tested sensors are:
#       HC-SR04  https://www.thegioiic.com/products/hc-sr04-cam-bien-sieu-am

# For the new Pico W, the firmware upgrade can be downloaded here:
#    https://micropython.org/download/rp2-pico-w/
# The use of Pico's 2nd core, on function second_thread(), was adapted from:
#    https://www.electrosoftcloud.com/en/multithreaded-script-on-raspberry-pi-pico-and-micropython/

import machine
import utime
import ultrasonic
import WS2812
import _thread
import random

from machine import Pin,I2C,PWM
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

i2c_1 = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)
lcd = I2cLcd(i2c_1, 0x27, 2, 16) # I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS  NOTE: I2C_ADDR may be 0x3F or 0x27

neopixel = WS2812.WS2812( 15, 15, 0.5) # pin, num_leds, brightness

# led_onboard = machine.Pin(25, machine.Pin.OUT) # for the old Pico
led_onboard = machine.Pin("LED", machine.Pin.OUT) # for the new Pico W
pot1 = machine.ADC(26)
pot2 = machine.ADC(27)
#global pot1_100,pot2_100
pot1_100,pot2_100 = 0.0,0.0
conversion_factor = 3.3 / 65535
#buzzer = machine.Pin(28, machine.Pin.OUT)
buzzer = PWM(machine.Pin(28))
buzzer.freq(500)
buzzer.duty_u16(1000)
utime.sleep(1)
buzzer.duty_u16(0)

button1 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
b1,b2,b3 = 0,0,0   # button status:  1/0  for  on/off
b1_prev,b2_prev_,b3_prev = 0,0,0  # previous value
is_slow_rainbow = 1
ultra1 = ultrasonic.Ultrasonic(16,17)
line0_lcd,line1_lcd = "",""

# Music-playing on the buzzer using PWM is adapted from
# https://www.tomshardware.com/how-to/buzzer-music-raspberry-pi-pico
tones = {
"B0": 31,
"C1": 33,"CS1": 35,"D1": 37,"DS1": 39,"E1": 41,"F1": 44,"FS1": 46,
"G1": 49,"GS1": 52,"A1": 55,"AS1": 58,"B1": 62,
"C2": 65,"CS2": 69,"D2": 73,"DS2": 78,"E2": 82,"F2": 87,"FS2": 93,
"G2": 98,"GS2": 104,"A2": 110,"AS2": 117,"B2": 123,
"C3": 131,"CS3": 139,"D3": 147,"DS3": 156,"E3": 165,"F3": 175,"FS3": 185,
"G3": 196,"GS3": 208,"A3": 220,"AS3": 233,"B3": 247,
"C4": 262,"CS4": 277,"D4": 294,"DS4": 311,"E4": 330,"F4": 349,"FS4": 370,
"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,
"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,"E5": 659,"F5": 698,"FS5": 740,
"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,
"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1319,"F6": 1397,"FS6": 1480,
"G6": 1568,"GS6": 1661,"A6": 1760,"AS6": 1865,"B6": 1976,
"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,"F7": 2794,"FS7": 2960,
"G7": 3136,"GS7": 3322,"A7": 3520,"AS7": 3729,"B7": 3951,
"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978
}

song = ["E5","G5","A5","P","E5","G5","B5","A5","P","E5","G5","A5","P","G5","E5"]

def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        utime.sleep(0.3)
    bequiet()


def neopixel_demo():    # neopixel demo
#        lcd.clear()
#        print("neopixel fills")
#        lcd.putstr("neopixel fills\n")
        for color in WS2812.COLORS:       
            neopixel.pixels_fill(color)
            neopixel.pixels_show()
            utime.sleep(0.5)
#        print("neopixel chases")
#        lcd.putstr("neopixel chases\n")
#        for color in WS2812.COLORS:       
#            neopixel.color_chase(color, 0.05)
#        print("neopixel rainbow")
#        lcd.putstr("neopixel rainbow\n")
#        neopixel.rainbow_cycle(0)
        neopixel.pixels_fill((50,50,50)) # WS2812.BLACK)
        neopixel.pixels_show()
#        lcd.clear()

# Demo of using the Pico's 2nd core
# https://www.electrosoftcloud.com/en/multithreaded-script-on-raspberry-pi-pico-and-micropython/
def second_thread(): 
    while True:
#            if counter % 5 == 0:
        lcd.move_to(0,0)
        lcd.putstr("b="+str(b1)+","+str(b2)+","+str(b3)+" d="+'{:5.1f}'.format(ultra1.ultrasonic_distance()))
        lcd.move_to(0,1)
        lcd.putstr("p1="+'{:4.1f}'.format(pot1_100)+" p2="+'{:4.1f}'.format(pot2_100))    
        print(random.randint(10,20)," Hello, this is 2nd thread")
        if b1 == 1:
            is_slow_rainbow = 0
            playsong(song)
            neopixel_demo()

def main():
    global b1,b2,b3  # these variables are set to "global" so the function can modify them
    global b1_prev,b2_prev,b3_prev
    global pot1_100,pot2_100
    global is_slow_rainbow
    global is_water_on
    print( i2c_1.scan() )
    lcd.clear()
    lcd.move_to(0,0)   # x=0..15, y=0..1
    lcd.putstr("Hello Pico!")

# initialize execution in the second core
# The second argument is a list or dictionary with the arguments
# that will be passed to the function.
    _thread.start_new_thread(second_thread, ())  

    neopixel.pixels_fill((255,255,255)) # WS2812.BLACK)
    neopixel.pixels_show()
    counter = 0

    while True:
        pot1_100 = pot1.read_u16() * 100.0 / 65535
        pot2_100 = pot2.read_u16() * 100.0 / 65535
        b1_prev,b2_prev,b3_prev = b1,b2,b3
        b1,b2,b3 = 1-button1.value(),1-button2.value(),1-button3.value()
    
#    print("b1=",b1,", b2=",b2,", b3=",b3,
#          ", pot1="+'{:.1f}'.format(pot1_100), ", pot2="+'{:.1f}'.format(pot2_100),
#          ", dist="+'{:.1f}'.format(ultra1.ultrasonic_distance()))
        led_onboard.toggle()
        if b1 == 1:
            #buzzer.value(1)
            pass
        else:
            #buzzer.value(0)
            pass
        if b2 == 1:
            # Interestingly, these loops don't work in second_thread().
            # Putting them here in the main() thread would work, but will block the fast
            # polling of the button and pot sensors.
            for color in WS2812.COLORS:       
                neopixel.color_chase(color, 0.05)
            neopixel.rainbow_cycle(0)
            neopixel.pixels_fill((50,50,50)) # WS2812.BLACK)
            neopixel.pixels_show()

        if b3_prev == 0 and b3 == 1:  # button 3 is pressed!  Toggle the slow rainbow
            is_slow_rainbow = 1 - is_slow_rainbow
        if is_slow_rainbow:
            neopixel.pixels_fill(neopixel.wheel(counter % 256)) # WS2812.BLACK)
            neopixel.pixels_show()
        else:
            neopixel.pixels_fill( WS2812.BLACK )
            neopixel.pixels_show()

        utime.sleep(0.04)
        counter += 1
    
if __name__ == "__main__":
    main()