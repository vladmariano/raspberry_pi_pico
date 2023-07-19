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
import random

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

k_means = 8    # set the value of K, the number of clusters.  Clusters are numbered 0,1,2,...K-1
num_converge = 20   # We assume that the clustering has converged after these number of iterations
length = 5000

labels = []             # which is the cluster where it belongs
for i in range(labels):
    labels.append(0)

mean_cluster = [] # the center of each of the K clusters
# initialize means
for m in range(k_means):
    mean_cluster.append(random.randint(1,2000))  # the means are far apart. Convergence will happen faster.

print("Here are the means")
print (mean_cluster)
print("Press any key...")

def kmeans_clustering():
    for n in range(num_converge):
        # print("Iteration ", n, " of ", num_converge)
        num_cluster = []
        sum_cluster = []
        # for each data point p, find the center (mean) that is closest, and assign p to that cluster
        for i in range(length):  # for each pixel
            dist = 100000000000
            for m in range(k_means):   # for each mean of the K clusters
                m_dist = abs(img[y,x] - mean_cluster[m])   # compute the distance from the data point to the mean
                if m_dist < dist:
                    labels[i] = m   # the pixel is "labelled" by the cluster number
                    label_belong = m
                    dist = m_dist
                # At this point, we have found the cluster whose center is closest to our data point in [x,y]
                # The cluster number is recorded in labels[x,y]
            sum_cluster[label_belong] += img[y,x]
            num_cluster[label_belong] += 1
    # At this point, each data point has been assigned its label
    for m in range(k_means):
        mean_cluster[m] = sum_cluster[m] / num_cluster[m]  # update each mean (center)

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
    
