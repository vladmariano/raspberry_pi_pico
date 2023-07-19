# Lesson 2 with Terrence

import machine
import utime
import random

led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(6, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
print("Hello Pico!!!")

# beep 3 times
for i in range(3):   # i is from 0..2
    buzzer.value(1)  # turn on buzzer
    utime.sleep(0.2) # 0.2 seconds
    buzzer.value(0)  # turn off buzzer
    utime.sleep(0.2)  # wait 

# blink the leds 5 times
for i in range(5):   # i = 0,1,2,3,4
    led.value(1)   # turn on 
    utime.sleep(0.2)
    led.value(0)
    utime.sleep(0.2)

import machine
import utime
import random

led = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.Pin(6, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
potentiometer = machine.ADC(26)
conversion_factor = 3.3 / (65535)

while button.value() == 0:  # while the red button is not pressed
    buzzer.value(1)   # turn on the buzzer and the LED
    led.value(1)      
    utime.sleep(0.1)  # keep them on for 0.2 seconds
    buzzer.value(0)   # turn off the buzzer and LED
    led.value(0)
    voltage = potentiometer.read_u16() * conversion_factor
    print("voltage = ", voltage)
    utime.sleep(1)    # keep them off for 1 second

buzzer.value(1)
utime.sleep(2)    # flatline sound for 5 seconds
buzzer.value(0)




