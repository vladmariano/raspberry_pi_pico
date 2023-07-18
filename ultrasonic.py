

from machine import Pin
import utime

class Ultrasonic():
    #---------------------------------------------------------
    # Pico ultrasonic sensor code was adapted from
    #   https://www.tomshardware.com/how-to/raspberry-pi-pico-ultrasonic-sensor
    # Tested sensors are:
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
