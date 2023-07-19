# Smart Devices 1
# Lesson 1

import machine 
import utime

led_onboard = machine.Pin(15, machine.Pin.OUT)

while True:
  led_onboard.value(1)
  utime.sleep(0.1)
  led_onboard.value(0)
  utime.sleep(0.1)
