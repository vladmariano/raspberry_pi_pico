
# Using the Raspberry Pi Pico W publish and subscribe
# adapted from a tutorial from Tom's Hardware
# https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt

import random
import machine
sensor_temperature = machine.ADC(4)
conversion_factor = 3.3 / (65535)  # used for temperature sensor
LED = machine.Pin("LED", machine.Pin.OUT) # Pico W onboard LED

import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#wlan.connect("Wi-Fi AP","PASSWORD")
#wlan.connect("SKYWORTH-1D65","322042285")
wlan.connect("Ball","11223344")

time.sleep(5)
print("Is the WIFI connected? ",wlan.isconnected())

sensor = Pin(16, Pin.IN)

mqtt_server = 'broker.hivemq.com'
client_id = 'bigles'
topic_pub = b'TomsHardware'
topic_sub = b'TomsHardware' # code for subscribing
topic_msg = b'Sg A Random Event'
#topic_msg = b'Movement Detected'

# This function is part of code for subscribe
def sub_cb(topic, msg):
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        LED.on()
    elif msg == "off":
        LED.off()

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.set_callback(sub_cb)  # code for subscribing
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    
while True:
    client.subscribe(topic_sub)   # code for subscribing
    time.sleep(1)   # code for subscribing
    
    temp_reading = sensor_temperature.read_u16() * conversion_factor
    temperature = 27 - (temp_reading - 0.706)/0.001721
    print("temperature = " + '{:.1f}'.format(temperature))
    
#    if sensor.value() == 0:
    r = random.randint(0,100)
    if r >= 0:
        print("Publish... ",r)
#        client.publish(topic_pub, topic_msg)
        client.publish(topic_pub, "Saigon A Random Event "+str(r)) #topic_msg)
        if r > 50:
            client.publish(topic_pub, "on") #topic_msg)
        else:
            client.publish(topic_pub, "off") #topic_msg)            
        time.sleep(2)
    else:
        pass