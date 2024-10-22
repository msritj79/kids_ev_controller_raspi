from mqtt_service import MQTTClient
import motor_controller
import light_controller
import time

# Example of subscribing to commands
def notify(command):
    print(f"Handling command: {command}")
    call_command(command)

def call_command(command):
    if "headLight" in command:
        if command["headLight"] == "ON":
            light_controller.headlight_on()
        elif command["headLight"] == "OFF":
            light_controller.headlight_off()
        else:
            print("Invalid headLight command")

    if "accel" in command:
        accel_data = command["accel"]
        if "status" in accel_data and "value" in accel_data:
            if accel_data["status"] == "ON":
                motor_controller.set_accel(accel_data["value"])
            elif accel_data["status"] == "OFF":
                motor_controller.stop_accel()
            else:
                print("Invalid accel status")
        else:
            print("Invalid accel data format")

    # if "park" in command:
    #     if command["park"] == "ON":
    #         car_controller.park()
    #     elif command["park"] == "OFF":
    #         car_controller.unpark()
    #     else:
    #         print("Invalid park command")


# Initialize the MQTT client with broker address, port, and username token
mqtt_client = MQTTClient(subscribe_topic="LC500/command")
mqtt_client.subscribe(notify_callback=notify)

# Start the MQTT client
mqtt_client.start()

# Keep the script running
while True:
    time.sleep(1)

