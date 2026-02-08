# Simple four-direction drive test using the existing I2C motor board.
# Requires I2C enabled (bus 1) and the board at address 0x18.

import time
import hbwz_motor as motor


def demo_sequence(delay=1.0):
    """Drive forward, back, left, right, then stop."""
    motor.SetcarStatus.carforward()
    time.sleep(delay)

    motor.SetcarStatus.carback()
    time.sleep(delay)

    motor.SetcarStatus.carleft()
    time.sleep(delay)

    motor.SetcarStatus.carright()
    time.sleep(delay)

    motor.SetcarStatus.carstop()


def main():
    try:
        demo_sequence()
    finally:
        # Always stop motors on exit.
        motor.SetcarStatus.carstop()


if __name__ == "__main__":
    main()
