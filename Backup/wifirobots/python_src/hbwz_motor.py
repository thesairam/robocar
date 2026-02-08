# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :控制电机
@contact :
@Time    :2020/05/09
@File    :hbwz_motor.py
@Software: PyCharm
"""

import hbwz_i2c as I2c
import time


# 第五、六号电机状态
class Motor_surplus(object):
    @staticmethod
    def five_pro():
        value = 0x2821
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M5 Pro')

    @staticmethod
    def five_anti():
        value = 0x2822
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M5 Anti')

    @staticmethod
    def five_stop():
        value = 0x2820
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M5 Stop')

    @staticmethod
    def six_pro():
        value = 0x2921
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M6 Pro')

    @staticmethod
    def six_anti():
        value = 0x2922
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M6 Anti')

    @staticmethod
    def six_stop():
        value = 0x2920
        # 传参到I2C写入指令方法
        I2c.writeinstruction(value)
        print(value)
        print('M6 Stop')


# 小车状态
class SetcarStatus(object):
    # 先以静态方法处理，后续根据实际改动
    @staticmethod
    def carstop():
        print('carstop run...')
        value = 0x210A
        I2c.writeinstruction(value)
        print('i2c write 0x210A')
        I2c.writeinstruction(value)

    @staticmethod
    def carforward():
        print('carforward run...')
        value = 0x220A
        I2c.writeinstruction(value)
        print('i2c write 0x220A')

    @staticmethod
    def carback():
        print('carback run...')
        value = 0x230A
        I2c.writeinstruction(value)
        print('i2c write 0x230A')

    @staticmethod
    def carleft():
        print('carleft run...')
        value = 0x240A
        I2c.writeinstruction(value)
        print('i2c write 0x240A')

    @staticmethod
    def carright():
        print('carright run...')
        value = 0x250A
        I2c.writeinstruction(value)
        print('i2c write 0x250A')


# 电机调速
class SetSpeed(object):

    @staticmethod
    def leftspeed(speed):
        # 此处调用I2C写入指令操作
        left_motor = 0x26
        left_speed = speed
        a = left_motor << 8
        left_value = a + left_speed
        print(hex(left_value))
        I2c.writeinstruction(left_value)
        time.sleep(0.001)

    @staticmethod
    def rightspeed(speed):
        # 此处调用I2C写入指令操作
        right_motor = 0x27
        right_speed = speed
        a = right_motor << 8
        right_value = a + right_speed
        print(hex(right_value))
        I2c.writeinstruction(right_value)
        time.sleep(0.001)