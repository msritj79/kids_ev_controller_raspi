import light_controller
import RPi.GPIO as GPIO
import time
# Setup GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) 
GPIO.setup(27, GPIO.OUT)

# try:
#     while True:
#         light_controller.headlight_on()
#         time.sleep(2)
#         light_controller.headlight_off()
#         time.sleep(2)
# except KeyboardInterrupt:
#     light_controller.headlight_off()  # Ensure headlights are off on exit
# finally:
#     GPIO.cleanup()

try:
    while True:
        light_controller.light_on("rear")
        time.sleep(2)
        light_controller.light_off("rear")
        time.sleep(2)
        light_controller.light_on("front")
        time.sleep(2)
        light_controller.light_off("front")
        time.sleep(2)
except KeyboardInterrupt:
    light_controller.light_off("rear")
    light_controller.light_off("front") 
finally:
    GPIO.cleanup()