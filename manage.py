from mqtt_service import MQTTClient
import motor_controller
import light_controller
import time
import threading
import RPi.GPIO as GPIO
import accel_sensor
import illumi_controller
import engine_sound_controller

# cannot operate manually after remote control, for the duration of TIMEOUT
TIMEOUT = 3  # second
stop_timer = None
MANUAL_ACCEL_VALUE_FORWARD = 80
MANUAL_ACCEL_VALUE_BACKWARD = 100
is_remote_controlled = False
is_running_forward = False
is_running_backward = False
engine_sound_type = "sports"
is_illumi_initialized = False

# Example of subscribing to commands
def notify(command):
    print(f"Handling command: {command}")
    call_command(command)

def call_command(command):
    global is_running_forward
    global is_running_backward
    global engine_sound_type
    global is_illumi_initialized
    
    if "headLight" in command:
        if command["headLight"] == "ON":
            light_controller.headlight_on()
        elif command["headLight"] == "OFF":
            light_controller.headlight_off()
        else:
            print("Invalid headLight command")
    
    if "engine_sound" in command:
        engine_sound_type = command["engine_sound"]

    if "accel" in command:
        accel_value = command["accel"]
        if accel_value > 0:
            accel_value = max(accel_value, 50)
            accel_value = min(accel_value, 80)
            motor_controller.set_accel_speed(speed=accel_value, direction="forward")
            # print(f"[set_accel]speed:{accel_value}, direction:forward")

            if is_running_backward:
                engine_sound_controller.stop()
                is_running_backward = False
            if not is_running_forward:
                engine_sound_controller.play(sound_type= engine_sound_type, volume=1.0)
                is_running_forward = True

        elif accel_value < 0:
            accel_value = -accel_value
            accel_value = max(accel_value, 50)
            accel_value = min(accel_value, 100)
            motor_controller.set_accel_speed(speed=accel_value, direction="backward")
            # print(f"[set_accel]speed:{accel_value}, direction:backward")

            if is_running_forward:
                engine_sound_controller.stop()
                is_running_forward = False
            if not is_running_backward:
                engine_sound_controller.play(sound_type= "back", volume=1.0)
                is_running_backward = True
        
        # stop motor and engine sound
        else:
            is_running_backward = False
            is_running_forward = False
            accel_value = 0
            motor_controller.set_accel_speed(speed=accel_value, direction="forward")
            engine_sound_controller.stop()
        
        set_remote_motion_control_mode()

    if "steer" in command:
        direction = command["steer"]
        if direction == "left":
            motor_controller.set_steer(direction="left")

        elif direction == "right":
            motor_controller.set_steer(direction="right")
        set_remote_motion_control_mode()
        
    if "illumi" in command:
        illumi_data = command["illumi"]
        
        # Illumination On/Off control
        if "status" in illumi_data:
            if illumi_data["status"] == "on":
                if not is_illumi_initialized:
                    illumi_controller.initialize()
                    is_illumi_initialized = True
            elif illumi_data["status"] == "off":
                illumi_controller.turn_off()
            else:
                print("Invalid on command in illumi data")
        
        # Color control
        if all(color_key in illumi_data for color_key in ["r", "g", "b", "a"]):
            red = illumi_data["r"]
            green = illumi_data["g"]
            blue = illumi_data["b"]
            alpha = illumi_data["a"]
            
            # Set the illumination color (example method)
            illumi_controller.set_color(red, green, blue, alpha)
        else:
            print("invalid color data in illumi")

    # if "park" in command:
    #     if command["park"] == "ON":
    #         car_controller.park()
    #     elif command["park"] == "OFF":
    #         car_controller.unpark()
    #     else:
    #         print("Invalid park command")

def set_remote_motion_control_mode():
    global is_remote_controlled
    is_remote_controlled = True
    reset_timer()

def unset_remote_motion_control_mode():
    global is_remote_controlled
    global stop_timer
    is_remote_controlled = False
    stop_timer =None
    motor_controller.stop_motors()
    # don't clean up gpio since accel sensor cannot be stopped
    # GPIO.cleanup()

def reset_timer():
    """タイマーをリセットして再スタート"""
    global stop_timer
    if stop_timer:
        stop_timer.cancel()
    stop_timer = threading.Timer(TIMEOUT, unset_remote_motion_control_mode)
    stop_timer.start()

def manual_accel():
    if not is_remote_controlled:
        gear_state = accel_sensor.check_gear_state()
        if gear_state == "forward":
            motor_controller.set_accel_speed(speed=MANUAL_ACCEL_VALUE_FORWARD, direction="forward")
            engine_sound_controller.play(sound_type=engine_sound_type, volume=1.0)
        elif gear_state == "reverse":
            motor_controller.set_accel_speed(speed=MANUAL_ACCEL_VALUE_BACKWARD, direction="backward")
            engine_sound_controller.play(sound_type="back", volume=1.0)
        elif gear_state == "stop":
            motor_controller.set_accel_speed(speed=0, direction="forward")
            engine_sound_controller.stop()
        else:
            motor_controller.set_accel_speed(speed=0, direction="forward")
            engine_sound_controller.stop()

def initialize_mqtt():
    # Initialize the MQTT client with broker address, port, and username token
    mqtt_client = MQTTClient(subscribe_topic="LC500/command")
    mqtt_client.subscribe(notify_callback=notify)

    # Start the MQTT client
    mqtt_client.start()


if __name__ == "__main__":
    initialize_mqtt()

    # Keep the script running
    try:
        while True:
            time.sleep(1)
            manual_accel()

    except KeyboardInterrupt:
        unset_remote_motion_control_mode()


