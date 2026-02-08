#!/usr/bin/env python3
"""
Minimal stop command: writes 0x210A (car stop) to I2C addr 0x18, reg 0xFF.
Matches the reference SetcarStatus.carstop() behavior.
"""

import time
import smbus

I2C_BUS = 1
I2C_ADDR = 0x18
CMD_REG = 0xFF
CMD_STOP = 0x210A


def writeinstruction(value):
    bus = smbus.SMBus(I2C_BUS)
    try:
        bus.write_word_data(I2C_ADDR, CMD_REG, value)
        time.sleep(0.01)
    finally:
        bus.close()


def carstop():
    print('carstop run...')
    writeinstruction(CMD_STOP)
    print('i2c write 0x210A')
    # second send to mirror reference behavior
    writeinstruction(CMD_STOP)


def main():
    carstop()


if __name__ == "__main__":
    main()
