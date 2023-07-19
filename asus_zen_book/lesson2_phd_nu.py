# Machine Learning on Embedded Systems
# Raspberry Pi Pico
# PhD Data Science
# 
# Pin connections:   
#    Buzzer – GP15 and GND 
#    Ultrasonic sensor – GP16 (trigger), GP17 (echo), GND and VBUS (5v) 
#    Temperature sensor – ADC 4  (internal analog-to-digital converter)

from machine import Pin
import utime

class Ultrasonic():
    #---------------------------------------------------------
    # Pico ultrasonic sensor code was adapted from
    #   https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor
    # Tested sensors:
    #    HC-SR04  https://www.thegioiic.com/products/hc-sr04-cam-bien-sieu-am
    def __init__(self,trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
    def ultrasonic_distance(self):
        trigger = Pin(self.trigger_pin, Pin.OUT)
        echo = Pin(self.echo_pin, Pin.IN)    
        trigger.low()
        utime.sleep_us(2)
        trigger.high()
        utime.sleep_us(5)
        trigger.low()
        while echo.value() == 0:
           signaloff = utime.ticks_us()
        while echo.value() == 1:
           signalon = utime.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        # print("The distance from object is ",distance,"cm")
        return distance
#----------------------------------------

led_tiny = machine.Pin(25,machine.Pin.OUT)
sensor_ultrasonic = Ultrasonic(16,17)
sensor_temperature = machine.ADC(4)
conversion_factor = 3.3 / (65535)  
buzzer = machine.Pin(15,machine.Pin.OUT)
print("This is a demo of the ultrasonic distance sensor and temperature sensor")

while True:
    led_tiny.value(1)
    utime.sleep(0.1)
    led_tiny.value(0)
    reading = sensor_temperature.read_u16() * conversion_factor  # 0 .. 3.3
    temperature = 27 - (reading - 0.706)/0.001721  # conversion to Celsius
    distance = sensor_ultrasonic.ultrasonic_distance()
    print("Distance = ", distance, "  temperature = ", temperature)
    if distance < 5:
        buzzer.value(1)
        utime.sleep(0.2)
        buzzer.value(0)
    utime.sleep(0.1)
    
