# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :控制大灯
@contact :
@Time    :2020/05/09
@File    :hbwz_light.py
@Software: PyCharm
"""

import hbwz_i2c as I2c


class Control_Light(object):

    @staticmethod
    def lightl_on():
        value = 0x3601
        I2c.writeinstruction(value)

    @staticmethod
    def lightl_off():
        value = 0x3600
        I2c.writeinstruction(value)

    @staticmethod
    def lightr_on():
        value = 0x3701
        I2c.writeinstruction(value)

    @staticmethod
    def lightr_off():
        value = 0x3700
        I2c.writeinstruction(value)
