from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO
#constants
gpio_status = GPIO.LOW
pins = {
        'front':17,
        'rear':27
}

def toggle_light(pin, value):
    global gpio_status
    if value == "on":
        if gpio_status != GPIO.HIGH:
            GPIO.output(pin, GPIO.HIGH)
            gpio_status = GPIO.HIGH
            print(f"Light on (Pin: {pin})")
    elif value == "off":
        if gpio_status != GPIO.LOW:
            GPIO.output(pin, GPIO.LOW)
            gpio_status = GPIO.LOW
            print(f"Light off (Pin: {pin})")

def light_on(light_type:str):
    global gpio_status
    pin = pins.get(light_type)
    toggle_light(pin, "on")
    print(f"{light_type} light on")


def light_off(light_type:str):
    global gpio_status
    pin = pins.get(light_type)
    toggle_light(pin, "off")
    print(f"{light_type} light off")

#早いのはこっちだと思いますが、上でRear,Frontを一つにまとめました。
#たぶん、そんなにこの機能を使わないかと思ったので。
# def headlight_on():
#     global gpio_status
#     print("headlight on")
#     toggle_light(17, "on")

# def headlight_off():
#     global gpio_status
#     print("headlight off")
#     toggle_light(17, "off")

# def rearlight_on():
#     global gpio_status
#     print("headlight on")
#     toggle_light(17, "on")

# def rearlight_off():
#     global gpio_status
#     print("headlight off")
#     toggle_light(17, "off")