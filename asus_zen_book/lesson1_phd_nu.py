# Code on page 98-99 of Get Started
# https://hackspace.raspberrypi.org/books/micropython-pico

import machine
import utime

print("Hello Pico !")
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
  reading = sensor_temp.read_u16() * conversion_factor
  temperature = 27 - (reading - 0.706)/0.001721
  print("temperature = ",temperature)
  utime.sleep(0.5)