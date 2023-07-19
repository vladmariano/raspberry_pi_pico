
import machine
import utime

print("Hello World")

led_onboard = machine.Pin("LED", machine.Pin.OUT)

while True:
    led_onboard.value(1)
    utime.sleep(0.2)
    led_onboard.value(0)
    utime.sleep(0.2)
