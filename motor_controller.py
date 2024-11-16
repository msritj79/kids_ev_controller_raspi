# https://github.com/CytronTechnologies/Cytron_MDD10_Hat/blob/master/Example%20Code/Raspberry%20PI%203/HatMDD10SM.py

import RPi.GPIO as GPIO			# using Rpi.GPIO module
from time import sleep			# import function sleep for delay

AN2 = 13				# set pwm2 pin on MD10-Hat
AN1 = 12				# set pwm1 pin on MD10-hat
DIG2 = 24				# set dir2 pin on MD10-Hat
DIG1 = 26				# set dir1 pin on MD10-Hat
# speed and time to rotate steer motor for smooth control 
STEER_CONTROL_SPEED = 70
STEER_CONTROL_TIME = 0.2

pwm_accel = None
pwm_steer = None
is_initialized = False

def initialize_gpio():
    global is_initialized, pwm_accel, pwm_steer
    if is_initialized:
        return
    try:
        GPIO.setmode(GPIO.BCM)			# GPIO numbering
        GPIO.setwarnings(False)			# enable warning from GPIO
        GPIO.setup(AN2, GPIO.OUT)		# set pin as output
        GPIO.setup(AN1, GPIO.OUT)		# set pin as output
        GPIO.setup(DIG2, GPIO.OUT)		# set pin as output
        GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
        sleep(1)				# delay for 1 seconds
        pwm_accel = GPIO.PWM(AN1, 100)
        pwm_steer = GPIO.PWM(AN2, 100)
        pwm_accel.start(0)
        pwm_steer.start(0)

        is_initialized = True
        print("GPIO for motion control is initialized")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def set_accel_speed(speed, direction):
    """
    Accelモータの速度と方向を設定する
    :param speed: 速度（0〜100）
    :param direction: 方向（"forward" または "backward"）
    """
    if not is_initialized:
        initialize_gpio()

    # print(f"[set_accel]speed:{speed}, direction:{direction}")
    if direction == "forward":
        GPIO.output(DIG1, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(DIG1, GPIO.HIGH)
    else:
        raise ValueError("Invalid direction for Accel. Use 'forward' or 'backward'.")
    
    pwm_accel.ChangeDutyCycle(speed)

def set_steer(direction):
    """
    Steerモータの速度と方向を設定する
    :param speed: 速度（0〜100）
    :param direction: 方向（"left" または "right"）
    """
    if not is_initialized:
        initialize_gpio()

    # print(f"[steer]angle:{angle}, direction:{direction}")
    if direction == "left":
        GPIO.output(DIG2, GPIO.HIGH)
    elif direction == "right":
        GPIO.output(DIG2, GPIO.LOW)
    else:
        raise ValueError("Invalid direction for Steer. Use 'left' or 'right'.")
    # control steer for 1s
    pwm_steer.ChangeDutyCycle(STEER_CONTROL_SPEED)
    sleep(STEER_CONTROL_TIME)
    pwm_steer.ChangeDutyCycle(0)

def stop_motors():
    """モータを停止し、GPIOをクリーンアップする"""
    # global is_initialized
    set_accel_speed(0, "forward")
    # set_steer("left")
    # pwm_accel.stop()
    # pwm_steer.stop()
    # GPIO.cleanup([AN1, AN2, DIG1, DIG2])

    # print("Motors stopped")
    # initializeを再度するときになぜかエラーになるのでやらない
    # is_initialized = False

if __name__ == "__main__":
    try:
        while True:
            # 加速と操舵を個別に設定して走行制御
            set_accel_speed(80, "forward")
            set_steer("left")
            sleep(2)

            set_accel_speed(80, "backward")
            set_steer("right")
            sleep(2)

            # 停止
            set_accel_speed(0, "forward")
            set_steer("left")
            sleep(2)

    except KeyboardInterrupt:
        # 終了時にモータを停止
        stop_motors()
        GPIO.cleanup()