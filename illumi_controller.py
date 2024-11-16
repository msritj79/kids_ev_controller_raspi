

import time
from rpi_ws281x import PixelStrip, Color

led_count = 52
led_pin = 21
led_freq_hz=800000
led_dma=10
led_brightness=50
led_invert=False
led_channel=0
update_interval=0.01

strip = None

def initialize():
    """Initializes the LED strip."""
    global strip
    strip = PixelStrip(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
    strip.begin()

def turn_off():
    """Turns off all LEDs."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set all pixels to black
    strip.setBrightness(0)
    strip.show()
    # strip._cleanup()

def set_color(red, green, blue, alpha):
    """Sets the LEDs to a specific color with brightness."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(red, green, blue))  # Set color to the specified RGB

    # convert alpha from 0~255 to 0=100
    alpha = int((alpha / 256) * 100)
    # strip.setBrightness(alpha)
    strip.show()

if __name__ == "__main__":
    # Initialize the LED strip
    initialize()
    
    # Test by setting the color to red with full brightness
    print("Setting LEDs to red...")
    set_color(255, 0, 0, 255)  # Red color with full brightness
    time.sleep(1)
    
    # Test by turning off the LEDs again
    print("Turning off the LEDs 1")
    turn_off()

    # Initialize the LED strip
    initialize()

    # Test by setting the color to red with full brightness
    print("Setting LEDs to red...")
    set_color(0, 255, 0, 255)  # Red color with full brightness
    time.sleep(1)
    
    # Test by turning off the LEDs again
    print("Turning off the LEDs 2")
    turn_off()


