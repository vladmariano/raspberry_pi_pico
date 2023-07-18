# neopixel code

# Neopixel ws2812 demo, adapted from
# https://github.com/raspberrypi/pico-micropython-examples/tree/master/pio/neopixel_ring
# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LEDs.
# NUM_LEDS = 15
# PIN_NUM = 4
# brightness = 0.3

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class WS2812:
#    NUM_LEDS = 1
#    PIN_NUM = 0
#    brightness = 0.5
#    sm = 0
#    ar = 0

    def __init__(self, PIN_NUM, NUM_LEDS, brightness):
        self.NUM_LEDS = NUM_LEDS
        self.PIN_NUM = PIN_NUM
        self.brightness = brightness
        # Create the StateMachine with the ws2812 program, outputting on pin
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(self.PIN_NUM))

        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])

    ##########################################################################
    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        time.sleep_ms(10)

    def pixels_set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

    def color_chase(self, color, wait):
        for i in range(self.NUM_LEDS):
            self.pixels_set(i, color)
            time.sleep(wait)
            self.pixels_show()
        time.sleep(0.2)
 
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
 
    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.NUM_LEDS):
                rc_index = (i * 256 // self.NUM_LEDS) + j
                self.pixels_set(i, self.wheel(rc_index & 255))
            self.pixels_show()
            time.sleep(wait)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

# while True:
#    print("fills")
#    for color in COLORS:       
#        pixels_fill(color)
#        pixels_show()
#        time.sleep(0.2)

#    print("chases")
#    for color in COLORS:       
#        color_chase(color, 0.01)

#    print("rainbow")
#    rainbow_cycle(0)
