# Lesson 1 with Terrence

import machine
import utime
import random

led15 = machine.Pin(15, machine.Pin.OUT)
buzzer6 = machine.Pin(6, machine.Pin.OUT)
button14 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
print("Hello Pico!!!")

while True:
    print(random.randint(1,10))
    led15.value(1)
    utime.sleep(0.2)
    led15.value(0)
    if button14.value() == 1:
        buzzer6.value(1)
        utime.sleep(0.2)
    buzzer6.value(0)
    utime.sleep(0.2)
    
