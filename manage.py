from mqtt_service import MQTTClient
import motor_controller
import light_controller
import time
import threading
import RPi.GPIO as GPIO
import accel_sensor

# タイムアウト設定
TIMEOUT = 10  # 秒
stop_timer = None

# Example of subscribing to commands
def notify(command):
    print(f"Handling command: {command}")
    call_command(command)
    reset_timer()  # 操作があったためタイマーをリセット

def call_command(command):
    if "headLight" in command:
        if command["headLight"] == "ON":
            light_controller.headlight_on()
        elif command["headLight"] == "OFF":
            light_controller.headlight_off()
        else:
            print("Invalid headLight command")

    if "accel" in command:
        accel_value = command["accel"]
        motor_controller.set_accel(accel_value)

    # if "park" in command:
    #     if command["park"] == "ON":
    #         car_controller.park()
    #     elif command["park"] == "OFF":
    #         car_controller.unpark()
    #     else:
    #         print("Invalid park command")

def reset_timer():
    """タイマーをリセットして再スタート"""
    global stop_timer
    if stop_timer:
        stop_timer.cancel()
    stop_timer = threading.Timer(TIMEOUT, stop_gpio)
    stop_timer.start()

def stop_gpio():
    motor_controller.stop_motors()
    GPIO.cleanup()

def manual_accel():
    gear_state = accel_sensor.check_gear_state()

    if gear_state == "forward":
        motor_controller.set_accel(50)
    elif gear_state == "reverse":
        pass
    else:
        pass


# Initialize the MQTT client with broker address, port, and username token
mqtt_client = MQTTClient(subscribe_topic="LC500/command")
mqtt_client.subscribe(notify_callback=notify)

# Start the MQTT client
mqtt_client.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
        manual_accel()

except KeyboardInterrupt:
    stop_gpio()


