# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :控制舵机
@contact :
@Time    :2020/05/09
@File    :hbwz_servo.py
@Software: PyCharm
"""

import hbwz_i2c as I2c
import time


# 从上位机buffer中得到角度
def get_angel(angelnum_from_buffer):
    angel = hex(eval('0x' + angelnum_from_buffer))
    angel = int(angel, 16)  # 16为进制
    # 设置角度保护
    if angel > 160:
        angel = 160
    elif angel < 15:
        angel = 15
    return angel


# 设置角度
def set_server_angle(servonum, servoangle):
    # 调用I2C发送舵机号和角度给单片机
    # 0xFF 0x744 0x0160
    data = (servonum << 8) + servoangle
    # print(data)
    I2c.writeinstruction(data)


# 存储舵机角度
def Storage_servoangle():
    data = 0x1101
    I2c.writeinstruction(data)
    print('Storage_servoangle run...')
    time.sleep(0.1)


# 角度初始化
def servo_initialize():
    data = 0x1100
    I2c.writeinstruction(data)
    print('servo_initialize run..')
    time.sleep(0.1)
