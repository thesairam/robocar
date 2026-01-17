#!/usr/bin/env python3
"""
Minimal forward drive at max speed:
- Set left speed to 0xFF via reg 0x26??
- Set right speed to 0xFF via reg 0x27??
- Issue forward command 0x220A
"""

import time
import smbus

I2C_BUS = 1
I2C_ADDR = 0x18
CMD_REG = 0xff
CMD_FORWARD = 0x220A
CMD_LEFT_SPEED = 0x26FF
CMD_RIGHT_SPEED = 0x27FF


def writeinstruction(value):
    bus = smbus.SMBus(I2C_BUS)
    try:
        bus.write_word_data(I2C_ADDR, CMD_REG, value)
        time.sleep(0.01)
    finally:
        bus.close()


def main():
    print("carforward run...")
    # Max both sides then go forward
    writeinstruction(CMD_LEFT_SPEED)
    writeinstruction(CMD_RIGHT_SPEED)
    writeinstruction(CMD_FORWARD)
    print("i2c write 0x26FF / 0x27FF then 0x220A")


if __name__ == "__main__":
    main()
