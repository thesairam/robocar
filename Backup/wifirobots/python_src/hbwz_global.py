# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :全局静态文件
@contact :
@Time    :2020/05/09
@File    :hbwz_global.py
@Software: PyCharm
"""
import RPi.GPIO as GPIO
import time
from socket import *

revstatus = 0
cruising_flag = 0
pre_cruising_flag = 0
min_distence = 15

# 定义TCP服务器相关变量

BT_Server = socket(AF_INET, SOCK_STREAM)
BT_Server.bind(('', 2002))
BT_Server.listen(1)
BT_buffer = []

TCP_Server = socket(AF_INET, SOCK_STREAM)
TCP_Server.bind(('', 2001))
TCP_Server.listen(1)
TCP_buffer = []

recv_len = 5  # 接收的字符长度

BT_Client = False
TCP_Client = False
socket_flag = 0
before_angle = [0, 0, 0, 0, 0, 0, 0, 0]

# 超声波标志位
dis_flag = 1
back_flag = 1
distance = 0
# i2c写入标志位
i2c_flag = 0
# 超声波接口定义
Echo = 5  # 超声波接收脚位
Trig = 6  # 超声波发射脚位
ultrasonic_flag = 0  # 超声波避障模式开关标志位

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# trig引脚设置为输出，并初始化为低电平
GPIO.setup(Trig, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(0.5)
GPIO.output(Trig,GPIO.LOW)
# echo引脚设置为输入
GPIO.setup(Echo, GPIO.IN, pull_up_down=GPIO.PUD_UP)
