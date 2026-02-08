# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :socket通信、指令解析
@contact :
@Time    :2020/05/09
@File    :hbwz_global.py
@Software: PyCharm
"""

from socket import *
import time
import binascii
import hbwz_motor as motor
import hbwz_servo as servo
import hbwz_light as light
import hbwz_global as t_global
#import bluetooth
import hbwz_i2c as i2c


class Socket:
    def __init__(self):
        self.rec_flag = 0  # 0xff字节接收标志
        self.count = 0  # 数据接收计数器标志
        self.buffer = []

    def load_server(self, server, servername):
        while True:
            print(print('waitting for %s connection...' % servername, "\r"))

            if servername == 'BT':
                print('start bluetooth >>>>>>>>>>')
                t_global.BT_Client = False
                t_global.BT_Client, socket_addr = server.accept()  # 初始化socket，创建客户端和地址
                client = t_global.BT_Client
                print((str(socket_addr[0]) + ' %s Connected!' % servername), "\r")

            elif servername == 'TCP':
                print('start tcp >>>>>>>>>>')
                t_global.TCP_Client = False
                t_global.TCP_Client, socket_addr = server.accept()
                client = t_global.TCP_Client
                print((str(socket_addr[0]) + ' %s Connected!' % servername), "\r")

            while True:
                try:
                    if servername == 'BT':
                        data = t_global.BT_Client.recv(t_global.recv_len)
                    elif servername == 'TCP':
                        data = t_global.TCP_Client.recv(t_global.recv_len)
                    # data = binascii.b2a_hex(data).decode('utf-8')
                    # print(data) #ff000100ff
                    if len(data) < t_global.recv_len:
                        break
                    if data[0] == 0xff and data[len(data) - 1] == 0xff:
                        buf = []
                        for i in range(1, 4):
                            buf.append(data[i])
                        self.command_analysis(buf)

                except Exception as e:  # 接收出错
                    print('socket received error:', e)  # 打印出错信息
                    break

            client.close()
            motor.SetcarStatus.carstop()
        server.close()

    # 上位机指令解析函数
    def command_analysis(self, lists):
        # 判断小车方向电机指令      FF  XX   XX   XX   FF
        if lists[0] == 0x00:  # 包头 功能  状态  数据 包尾
            if lists[1] == 0x00:
                print('carstop,command send...')
                motor.SetcarStatus.carstop()
            elif lists[1] == 0x01:
                #t_global.back_flag = 1
                if t_global.dis_flag == 1:
                    print('carforward,command send...')
                    motor.SetcarStatus.carforward()
            elif lists[1] == 0x02:
                print('carback,command send...')
                if t_global.cruising_flag == 3:
                    t_global.cruising_flag = 0
                motor.SetcarStatus.carback()
            elif lists[1] == 0x03:
                print('carleft,command send...')
                if t_global.cruising_flag == 3:
                    t_global.cruising_flag = 0
                motor.SetcarStatus.carleft()
            elif lists[1] == 0x04:
                print('carright,command send...')
                if t_global.cruising_flag == 3:
                    t_global.cruising_flag = 0
                motor.SetcarStatus.carright()
            elif lists[1] == 0x09:
                if lists[2] == 0x01:
                    print('five-pro,command send...')
                    print(lists)
                    motor.Motor_surplus.five_pro()
                elif lists[2] == 0x02:
                    print('five-anti,command send...')
                    print(lists)
                    motor.Motor_surplus.five_anti()
                elif lists[2] == 0x00:
                    print('five-stop,command send...')
                    print(lists)
                    motor.Motor_surplus.five_stop()
            elif lists[1] == 0x0A:
                if lists[2] == 0x01:
                    print('six-pro,command send...')
                    print(lists)
                    motor.Motor_surplus.six_pro()
                elif lists[2] == 0x02:
                    print('six-anti,command send...')
                    print(lists)
                    motor.Motor_surplus.six_anti()
                elif lists[2] == 0x00:
                    print('six-stop,command send...')
                    print(lists)
                    motor.Motor_surplus.six_stop()

        # 判断是否为调速指令
        elif lists[0] == 0x02:
            # 不存在0档调速，如果是0档调速那么置位1
            if lists[2] == 0x00:
                lists[2] = 0x01
            if lists[1] == 0x01:
                speed = lists[2]
                # 此处调用左侧调速函数
                motor.SetSpeed.leftspeed(speed)
            elif lists[1] == 0x02:
                speed = lists[2]
                # 此处此处调用右侧调速函数
                motor.SetSpeed.rightspeed(speed)

        # 判断是否为舵机控制指令
        elif lists[0] == 0x01:
            servernum = lists[1]
            severangle = lists[2]
            # 加入防抖并过滤重复角度
            if abs(t_global.before_angle[servernum - 1] - severangle) > 2:
                print('severangle:%s' % severangle)
                servo.set_server_angle(servernum, severangle)
                t_global.before_angle[servernum - 1] = severangle

        # 存储舵机角度
        elif lists[0] == 0x32:
            servo.Storage_servoangle()

        # 舵机角度初始化
        elif lists[0] == 0x33:
            servo.servo_initialize()

        # 判断功能模式
        elif lists[0] == 0x13:
            # 判断是否为红外巡线模式
            if lists[1] == 0x02:
                t_global.cruising_flag = 1
                print('进入红外巡线模式:%d' % t_global.cruising_flag)
            # 判断是否为超声波模式
            elif lists[1] == 0x04:
                # 进入超声波测速前，调整速度
                speed_lists = [0x2606, 0x2706]
                for i in speed_lists:
                    i2c.writeinstruction(i)
                # 开启超声波测速标志
                t_global.ultrasonic_flag = 1
                # 控制台打印测试
                print('进入超声波避障模式:%d' % t_global.cruising_flag)
            # 判断是否为寻光模式
            elif lists[1] == 0x06:
                t_global.cruising_flag = 3
                print('进入寻光模式:%d' % t_global.cruising_flag)
            elif lists[1] == 0x00:
                t_global.revstatus = 0
                # 更改cruising_mod中的标志位
                t_global.cruising_flag = 0
                # 进入正常模式前关闭超声波避障
                t_global.ultrasonic_flag = 0
                # 再次确保避障方向位置位1，否则无法前进
                t_global.dis_flag = 1
                # 恢复最大速度值
                speed_lists = [0x260A, 0x270A]
                for i in speed_lists:
                    i2c.writeinstruction(i)
                # 控制台打印测试
                print('进入正常模式:%d' % t_global.cruising_flag)
        # 判断是否开关大灯模式
        elif lists[0] == 0x05:
            # 判断是否控制左侧大灯
            if lists[1] == 0x01:
                if lists[2] == 0x00:
                    print(lists)
                    print('left light turn off command send...')
                    light.Control_Light.lightl_off()
                    print('3600')
                elif lists[2] == 0x01:
                    print(lists)
                    print('left light turn on command send...')
                    light.Control_Light.lightl_on()
                    print('3601')
            # 判断是否控制右侧侧大灯
            elif lists[1] == 0x02:
                if lists[2] == 0x00:
                    print(lists)
                    print('right light turn off command send...')
                    light.Control_Light.lightr_off()
                    print('3700')
                elif lists[2] == 0x01:
                    print(lists)
                    print('right light turn on command send...')
                    light.Control_Light.lightr_on()
                    print('3701')

    def bluetooth_server(self):
        self.load_server(t_global.BT_Server, 'BT')

    def tcp_server(self):
        self.load_server(t_global.TCP_Server, 'TCP')
