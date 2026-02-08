# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :寻光模式功能
@contact :
@Time    :2020/05/09
@File    :hbwz_photoresistor.py
@Software: PyCharm
"""

import hbwz_i2c as I2c
from hbwz_motor import SetcarStatus
# from XiaoR_motor import SetSpeed


def get_ldrintensity():
    intensity_lists = I2c.readinstruction()
    return intensity_lists


def photoconductor():
    # 光敏电阻遇到亮度越强其返回值越小，最亮的值最小
    led_1 = get_ldrintensity()[0]
    led_2 = get_ldrintensity()[1]
    led_3 = get_ldrintensity()[2]
    # led 1 2 3 分别对应左中右
    # print(led_1, led_2, led_3)
    if (led_3 - led_2) > (led_1 - led_3) and (led_3 - led_2) > 15 and (led_1 - led_3) < -40:
        SetcarStatus.carleft()
    elif (led_1 - led_3) > -30 and (led_3 - led_2) > (led_1 - led_3) and (led_3 - led_2) < 20:
        SetcarStatus.carforward()
    elif (led_1 - led_3) > (led_3 - led_2) and (led_1 - led_3) > 20 and (led_3 - led_2) < -10:
        SetcarStatus.carright()
    else:
        SetcarStatus.carforward()

