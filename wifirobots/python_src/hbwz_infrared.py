# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :红外传感器相关功能
@contact :
@Time    :2020/05/09
@File    :hbwz_infrared.py
@Software: PyCharm
"""

from hbwz_motor import SetcarStatus
import hbwz_i2c as I2c
import time


# 红外巡线
def ir_trackline():
    print('ir_trackline run...')
    # 获取红外状态
    status = I2c.readinstruction()
    print(hex(status))      
    if status == 1:
        SetcarStatus.carstop()
        SetcarStatus.carright()
    elif status == 16:
        SetcarStatus.carstop()
        SetcarStatus.carleft()
    # 两边都没有检测到黑线
    elif status == 17:
        SetcarStatus.carstop()
    else:
        SetcarStatus.carforward()
        
