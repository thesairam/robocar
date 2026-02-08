# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :I2C与单片机通信
@contact :
@Time    :2020/05/09
@File    :hbwz_i2c.py
@Software: PyCharm
"""

import smbus
import time, os
import traceback
import hbwz_global as t_global

# 创建smbus实例
bus = smbus.SMBus(1)  # 0代表/dev/i2c0  1代表/dev/i2c1
# I2C通信地址
address = 0x18

# 向I2C地址写入指令
def writeinstruction(values):
    # print('writeinstruction run...')
    try:
        bus.write_word_data(address, 0xff, values)
        time.sleep(0.01)
    except IOError:
        print('Write Error')
        os.system('sudo i2cdetect -y 1')


# 从I2C读取数据
def readinstruction():
    s = traceback.extract_stack()
    print(s[-2][2])
    # 红外巡线
    while(t_global.i2c_flag):
        pass
    t_global.i2c_flag=1
    if s[-2][2] == 'ir_trackline':  # 判断是谁在调用readinstruction方法
        try:
            # 发送红外读取指令0x32
            value = bus.read_word_data(address, 0x32)  # 返回值：0x00 0x01  0x10 0x11 四个其中一个
            t_global.i2c_flag=0
            # 返回红外状态指令
            return value
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

    elif s[-2][2] == 'get_distence':  # 判断是谁在调用readinstruction方法
        try:
            value = bus.read_word_data(address, 0x31)
            t_global.i2c_flag = 0
            time.sleep(0.02)
            print('value:', value)
            if value == 0xFF:
                information = 'ultrasound error!'
            elif value == 254:
                information = 'Beyond the measuring distance!'
            else:
                return value
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

    elif s[-2][2] == 'get_ldrintensity':
        try:
            led_lists = []
            instruction = [0x33, 0x34, 0x35]
            for i in instruction:
                value = bus.read_word_data(0x18, i)
                led_lists.append(value)
                time.sleep(0.015)
            t_global.i2c_flag=0
            return led_lists
        except IOError:
            print('Write Error')
            os.system('sudo i2cdetect -y 1')

