import atexit
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

IN1, IN2, ENA = 17, 27, 22
IN3, IN4, ENB = 23, 24, 25


def _setup():
        for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
                GPIO.setup(pin, GPIO.OUT)

        pwm_a = GPIO.PWM(ENA, 5000)
        pwm_b = GPIO.PWM(ENB, 5000)
        pwm_a.start(100)
        pwm_b.start(100)
        return pwm_a, pwm_b


_pwmA, _pwmB = _setup()


def set_speed(duty_cycle: float) -> None:
        duty = max(0, min(100, duty_cycle))
        _pwmA.ChangeDutyCycle(duty)
        _pwmB.ChangeDutyCycle(duty)


def forward() -> None:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)


def reverse() -> None:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)


def right() -> None:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)


def left() -> None:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)


def start() -> None:
        forward()


def stop() -> None:
        for pin in [IN1, IN2, IN3, IN4]:
                GPIO.output(pin, GPIO.LOW)


def cleanup() -> None:
        stop()
        _pwmA.stop()
        _pwmB.stop()
        GPIO.cleanup()


atexit.register(cleanup)


if __name__ == "__main__":
        try:
                forward()
                time.sleep(10)
                stop()
        finally:
                cleanup()