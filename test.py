import machine
import utime

led25 = machine.Pin(25, machine.Pin.OUT)
led15 = machine.Pin(15, machine.Pin.OUT)

while True:
    led25.value(1)
    led15.value(1)
    utime.sleep(0.5)
    led25.value(0)
    led15.value(0)
    utime.sleep(0.5)