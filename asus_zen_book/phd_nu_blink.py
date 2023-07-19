
import machine
import utime
import random

led_tiny = machine.Pin(25, machine.Pin.OUT)
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
   reading = sensor_temp.read_u16() * conversion_factor
   temperature = 27 - (reading - 0.706)/0.001721
   print(random.randrange(1,10))
   print("temperature = ", temperature)
   led_tiny.value(1)
   utime.sleep(0.5)
   led_tiny.value(0)
   utime.sleep(0.5)
