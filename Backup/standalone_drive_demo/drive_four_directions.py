#!/usr/bin/env python3
"""
Standalone forward drive using the exact functions from wifirobots/python_src/hbwz_motor.py.

Adds a probe mode to try alternative speed-register pairs in case your board
revision maps the right-side channel differently.
"""

import os
import sys
import time

# Allow importing the reference motor helpers.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PY_SRC = os.path.join(ROOT, "wifirobots", "python_src")
if PY_SRC not in sys.path:
    sys.path.insert(0, PY_SRC)

import hbwz_motor as motor
import hbwz_i2c as i2c

FORWARD_WORD = 0x220A  # direct forward command (addr 0x18, reg 0xFF)


def demo_forward(duration=4.0, speed=0xFF):
    """Forward at given speed using reference helpers; reassert speeds mid-run."""
    try:
        motor.SetSpeed.leftspeed(speed)
        motor.SetSpeed.rightspeed(speed)
        i2c.writeinstruction(FORWARD_WORD)

        # Reassert speeds once mid-run in case one channel misses a write.
        time.sleep(duration / 2)
        motor.SetSpeed.leftspeed(speed)
        motor.SetSpeed.rightspeed(speed)
        i2c.writeinstruction(FORWARD_WORD)
        time.sleep(duration / 2)
    finally:
        motor.SetcarStatus.carstop()


def probe_registers(duration=1.0, speed=0xFF):
    """Cycle through candidate speed registers to see which combos drive all wheels."""
    candidates = [0x26, 0x27, 0x28, 0x29]  # 0x28/0x29 are used for motors 5/6 in reference
    try:
        for left_reg in candidates:
            for right_reg in candidates:
                # Write speeds directly via I2C to test this pair
                i2c.writeinstruction((left_reg << 8) | speed)
                i2c.writeinstruction((right_reg << 8) | speed)
                motor.SetcarStatus.carforward()
                time.sleep(duration)
                motor.SetcarStatus.carstop()
                time.sleep(0.2)
    finally:
        motor.SetcarStatus.carstop()


def right_only(duration=3.0, speed=0xFF):
    """Debug helper: drive only the right channel to confirm it responds."""
    try:
        motor.SetSpeed.leftspeed(0)
        motor.SetSpeed.rightspeed(speed)
        motor.SetcarStatus.carforward()
        time.sleep(duration)
    finally:
        motor.SetcarStatus.carstop()


def left_only(duration=3.0, speed=0xFF):
    """Debug helper: drive only the left channel to confirm it responds."""
    try:
        motor.SetSpeed.leftspeed(speed)
        motor.SetSpeed.rightspeed(0)
        motor.SetcarStatus.carforward()
        time.sleep(duration)
    finally:
        motor.SetcarStatus.carstop()


def main():
    # Try the known-good path first
    # demo_forward()
    # Or isolate channels:
    # right_only()
    # left_only()
    # Or brute-force register pairs:
    probe_registers()


if __name__ == "__main__":
    main()
