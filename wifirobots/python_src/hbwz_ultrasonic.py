# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :超声波模式功能
@contact :
@Time    :2020/05/09
@File    :hbwz_ultrasonic.py
@Software: PyCharm
"""
import RPi.GPIO as GPIO
import hbwz_i2c as I2c
from hbwz_motor import SetcarStatus
import hbwz_global as t_global
import time

class Ultrasonic:
    def __init__(self):
        pass
    def get_distence(self):
        # 获取超声波距离函数
        time_count = 0
        time_out = 0
        time.sleep(0.01)
        GPIO.output(t_global.Trig, True)
        time.sleep(0.000015)  # 发送10um以上高电平方波
        GPIO.output(t_global.Trig, False)  # 拉低
        while not GPIO.input(t_global.Echo):  # 等待Echo引脚由低电平变成高电平
            if time_out < 1201:
                time_out += 1
                time.sleep(0.00001)
            else:
                break
        t1 = time.time()  # 记录Echo引脚高电平开始时间点
        while GPIO.input(t_global.Echo):  # 等待Echo引脚由低电平变成低电平
            if time_count < 4096:  # 超时检测，防止死循环
                time_count = time_count + 1
                time.sleep(0.000001)
            else:
                print("NO ECHO receive! Please check connection")
                break
        # 记录Echo引脚高电平结束时间点
        t2 = time.time()
        distance = (t2 - t1) * 340 / 2 * 100
        # t2-t1时间单位s,声波速度340m/s,x100将距离值单位m转换成cm
        print("distance is %d" % distance)  # 打印距离值
        if 0 <= distance <= 600:  # 正常检测距离值
            # print("distance is %d"%distance)
            t_global.distance = round(distance, 2)
            return t_global.distance
        elif distance == -1:
            return -1
        else:
            # 如果距离值大于5m,超出检测范围
            t_global.distance = 0
            return 0

    def avoidbyragar(self):
        while True:
            try:
                if t_global.ultrasonic_flag:
                    # 超声波避障函数
                    dis = self.get_distence()
                    # 距离大于25cm小于300cm超声波的测距范围,等于0的时候是远距离超过超声波测距范围
                    if dis > 25 or dis == 0:
                        t_global.dis_flag = 1
                        print(t_global.dis_flag)
                    # 异常数据不做任何处理
                    elif dis == -1:
                        print('Exceptional Data: -1')
                    else:
                        if t_global.dis_flag == 1:
                            SetcarStatus.carstop()
                            t_global.dis_flag = 0
                        print(t_global.dis_flag)
                    time.sleep(0.08)
                else:
                    #print('Ultrasonic avoidbyragar stop!')
                    # 退出超声波前方向标志置位1
                    t_global.dis_flag = 1
                    time.sleep(0.08)
                #print('++++++++++++++++++++++++++++++++++++++++++++++')
            except Exception:
                print('restart')
