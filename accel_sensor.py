import RPi.GPIO as GPIO
from time import sleep


# ギア取得用の入力ピン設定
FORWARD_PIN = 14
REVERSE_PIN = 15

is_initialized = False

def initialize_gpio():
    global is_initialized
    if is_initialized:
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # 入力ピンの設定とプルダウン抵抗の有効化
    GPIO.setup(FORWARD_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(REVERSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    is_initialized = True
    print("GPIO is initialized")

def check_gear_state():
    if GPIO.input(FORWARD_PIN) == GPIO.LOW:
        return "forward"
    elif GPIO.input(REVERSE_PIN) == GPIO.LOW:
        return "reverse"
    else:
        return "stop"

if __name__ == "__main__":
    try:
        initialize_gpio()
        while True:
            gear_state = check_gear_state()

            print(f"gear_state:{gear_state}")
            
            sleep(1)  # 1秒ごとに状態をチェック

    except KeyboardInterrupt:
        GPIO.cleanup()
