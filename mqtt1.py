# MQTT test, adapted from:
# https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt

import utime

import network
import time
import machine
from machine import Pin
from umqtt.simple import MQTTClient

print("Hello Pico W")
led_onboard = Pin("LED", Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Ball","11223344")
time.sleep(5)
print("Is connected to WIFI = ",wlan.isconnected())

mqtt_server = "broker.hivemq.com"
client_id = 'bigles'
topic_pub = b'TomsHardware'  #publish to this topic
topic_sub = b'TomsHardware'  #subscribe to this topic
topic_msg = b'the message'

def sub_cb(topic, msg):
    msg = msg.decode('utf-8')
    print(msg)

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive = 3600)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT broker. Reconnecting...')
    time.sleep(3)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

# Reading onboard temperature, adapted from
# https://how2electronics.com/read-temperature-sensor-value-from-raspberry-pi-pico/
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
count = 0

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    print("count= ",count, " Temperature = ", temperature)
#    client.publish(topic_pub, topic_msg)
    client.publish(topic_pub, bytes(str(count)+' temp= '+str(temperature), 'utf-8'))
    led_onboard.value(1)
    utime.sleep(0.15)
    led_onboard.value(0)
    utime.sleep(0.15)
    
    client.subscribe(topic_sub)
    count += 1
