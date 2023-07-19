# Smart Devices 1
# Lesson 4:  Start a beeping buzzer and turn it off when the button is pressed

import machine
import utime

led = machine.Pin(15, machine.Pin.OUT)  # an acutator, or output
buzzer = machine.Pin(6, machine.Pin.OUT)  # an actuator, or output
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)  # a sensor, or input

for i in range(4):   # make the led blink 4 times
    led.value(1)
    utime.sleep(0.25)
    led.value(0)
    utime.sleep(0.25)

for i in range(3):  # when the program starts, beep 3 times
    buzzer.value(1)
    utime.sleep(0.3)
    buzzer.value(0)
    utime.sleep(0.3)

while button.value() == 0:       # while the button is not yet pressed
    led.value(1)  # turn on the LED
    buzzer.value(1)         # make a sound
    utime.sleep(0.5)  # wait for 0.5 second
    led.value(0)   # turn off the LED
    buzzer.value(0)         # turn off the buzzer
    utime.sleep(0.5)  # wait for half a second

buzzer.value(1)  # turn on the buzzer
utime.sleep(4)   # a long sound
buzzer.value(0)