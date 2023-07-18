# Lesson 3 with Terrence
# Adding the potentiometer and temperature sensor

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
potentiometer = machine.ADC(26)   # page 96-98 of Get Started book
sensor_temp = machine.ADC(4)

conversion_factor = 3.3 / (65535)

while button.value() == 0:  # while the red button is not pressed
    buzzer.value(1)   # turn on the buzzer and the LED
    led.value(1)      
    utime.sleep(0.1)  # keep them on for 0.2 seconds
    buzzer.value(0)   # turn off the buzzer and LED
    led.value(0)
    # the potentiometer is like a "faucet" for electrons
    voltage = potentiometer.read_u16() * conversion_factor  # 0..3.3 v
    percent = 100.0 * voltage / 3.3   # convert to 0..100
    # print("voltage = ", voltage)
    reading = sensor_temp.read_u16() * conversion_factor  # 0..3.3
    temperature = 27 - (reading - 0.706)/0.001721  # converts to degrees Celsius
    print("percent (0..100) = ", percent, "  temperature = ", temperature)
    utime.sleep(1)    # keep them off for 1 second

buzzer.value(1)
utime.sleep(2)    # flatline sound for 5 seconds
buzzer.value(0)




