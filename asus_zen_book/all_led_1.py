# LED animation - using pins to turn on LEDs

import machine
import utime

led_pwm = []
num_pins = 29
for i in range(num_pins):
    led_pwm_temp = machine.PWM(machine.Pin(i))
    led_pwm_temp.freq(1000)
    led_pwm.append(led_pwm_temp)

button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
#led_pwm_1 = machine.PWM(machine.Pin(1))
#led_pwm_1.freq(1000)

#led_1 = machine.Pin(1, machine.Pin.OUT)

print("Hello LEDs")

num = 2000
p = 0
direction = 1
while True:
    button_pressed = (button.value() == 0)
    # print(button_pressed)
    num = num + direction * 1024
    if num < 1025 or num > 64000:
        direction *= -1
    for i in range(num_pins):
        led_pwm[i].duty_u16(0 if button_pressed else num)
    utime.sleep(0.05)
                 

#led0.value(1)
#    utime.sleep(1)
#    led0.value(0)
#    utime.sleep(1)
