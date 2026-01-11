#!/usr/bin/env python3
"""
Standalone four-direction drive demo for the XiaoRGEEK-style motor board at I2C addr 0x18.
No repo imports; only depends on smbus (I2C enabled on Pi).

Commands (write_word_data to addr 0x18, command register 0xFF):
- 0x220A: forward
- 0x230A: back
- 0x240A: left
- 0x250A: right
- 0x210A: stop

Wiring: I2C1 on Raspberry Pi (SDA=BCM2 pin3, SCL=BCM3 pin5, 3.3V, GND).
"""

import time
import smbus

I2C_ADDR = 0x18
CMD_REG = 0xFF

CMD_STOP = 0x210A
CMD_FWD = 0x220A
CMD_BACK = 0x230A
CMD_LEFT = 0x240A
CMD_RIGHT = 0x250A


class MotorBoard:
    def __init__(self, bus_id=1, addr=I2C_ADDR):
        self.bus = smbus.SMBus(bus_id)
        self.addr = addr

    def send(self, value):
        self.bus.write_word_data(self.addr, CMD_REG, value)
        time.sleep(0.01)  # small gap for the MCU

    def stop(self):
        self.send(CMD_STOP)

    def forward(self):
        self.send(CMD_FWD)

    def back(self):
        self.send(CMD_BACK)

    def left(self):
        self.send(CMD_LEFT)

    def right(self):
        self.send(CMD_RIGHT)


def demo(delay=1.0):
    board = MotorBoard()
    try:
        board.forward()
        time.sleep(delay)

        board.back()
        time.sleep(delay)

        board.left()
        time.sleep(delay)

        board.right()
        time.sleep(delay)

    finally:
        board.stop()


def main():
    demo()


if __name__ == "__main__":
    main()
