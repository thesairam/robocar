import RPi.GPIO as GPIO
import time
import atexit

# -------------------
# GPIO setup (BCM)
# -------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor A (left)
IN1, IN2, ENA = 17, 27, 22
# Motor B (right)
IN3, IN4, ENB = 23, 24, 25

pins = [IN1, IN2, ENA, IN3, IN4, ENB]
GPIO.setup(pins, GPIO.OUT)

# -------------------
# PWM @ 5 kHz
# -------------------
PWM_FREQ = 5000
pwmA = GPIO.PWM(ENA, PWM_FREQ)
pwmB = GPIO.PWM(ENB, PWM_FREQ)

# -------------------
# Vehicle state
# -------------------
engine_on = False
current_speed = 60  # 0–100

# -------------------
# Core controls
# -------------------
def start():
    """Ignition ON"""
    global engine_on
    if not engine_on:
        pwmA.start(0)
        pwmB.start(0)
        engine_on = True
        print("Engine ON")

def stop():
    """Ignition OFF"""
    global engine_on
    if engine_on:
        try:
            pwmA.ChangeDutyCycle(0)
            pwmB.ChangeDutyCycle(0)
        finally:
            try:
                pwmA.stop()
            except Exception:
                pass
            try:
                pwmB.stop()
            except Exception:
                pass
        engine_on = False
        print("Engine OFF")

def set_speed(speed):
    global current_speed
    current_speed = max(0, min(100, speed))
    if engine_on:
        pwmA.ChangeDutyCycle(current_speed)
        pwmB.ChangeDutyCycle(current_speed)

# -------------------
# Motion commands
# -------------------
def forward():
    if not engine_on:
        return
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(current_speed)

def reverse():
    if not engine_on:
        return
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(current_speed)

def right():
    if not engine_on:
        return
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    set_speed(current_speed)

def left():
    if not engine_on:
        return
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    set_speed(current_speed)

# -------------------
# Cleanup ONLY at exit
# -------------------
def cleanup():
    global pwmA, pwmB, engine_on
    if engine_on:
        stop()
    # Ensure PWM objects are not left for __del__ when GPIO already torn down
    try:
        pwmA.stop()
    except Exception:
        pass
    try:
        pwmB.stop()
    except Exception:
        pass
    pwmA = None
    pwmB = None
    GPIO.cleanup()

atexit.register(cleanup)

# -------------------
# Example usage
# -------------------
if __name__ == "__main__":
    start()            # ignition on
    set_speed(50)
    forward()
    time.sleep(2)

    left()
    time.sleep(1)

    stop()             # ignition off
    time.sleep(2)

    start()            # ignition on again
    reverse()
    time.sleep(2)

    stop()
