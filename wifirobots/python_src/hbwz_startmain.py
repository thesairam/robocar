# coding:utf-8
"""
@version: python3.7
@Author  : hbwz
@Explain :主程序，多线程启动
@contact :
@Time    :2020/05/09
@File    :hbwz_startmain.py
@Software: PyCharm
"""
import os
import time
import threading
import hbwz_global as t_global
import hbwz_motor as motor
import hbwz_infrared as infrared
import hbwz_photoresistor as ldr
from hbwz_socket import Socket
from subprocess import call
from hbwz_ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()
socket = Socket()


# 多功能模式切换
def cruising_mod():
    time.sleep(0.05)
    if t_global.pre_cruising_flag != t_global.cruising_flag:
        if t_global.pre_cruising_flag != 0:
            motor.SetcarStatus.carstop()
        t_global.pre_cruising_flag = t_global.cruising_flag
    if t_global.cruising_flag == 1:
        print('红外巡线启动成功')
        # 调用红外避障
        infrared.ir_trackline()
        # elif t_global.cruising_flag == 2:
        #     print('超声波避障模式启动成功')
        #     # 调用超声波避障模式
        #     ultrasonic.avoidbyragar()
        time.sleep(0.1)
    elif t_global.cruising_flag == 3:
        print('寻光模式启动成功')
        # 调用寻光模式
        ldr.photoconductor()
    else:
        time.sleep(0.01)


# 蓝牙终端设置
print("------wifirobots start-----")
#os.system("sudo hciconfig hci0 name XiaoRGEEK")
time.sleep(0.1)
#os.system("sudo hciconfig hci0 reset")
time.sleep(0.3)
#os.system("sudo hciconfig hci0 piscan")
time.sleep(0.2)
print('NOW BT discoverable')

time.sleep(0.2)
threads = []

t1 = threading.Thread(target=socket.bluetooth_server, args=())
threads.append(t1)
t2 = threading.Thread(target=socket.tcp_server, args=())
threads.append(t2)
t3 = threading.Thread(target=ultrasonic.avoidbyragar, args=())
threads.append(t3)

path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
call("%s" % path_sh, shell=True)
time.sleep(1)
for t in threads:
    t.setDaemon(True)
    t.start()
    time.sleep(0.05)
    print('theads start...')
print('all theads start...')

while True:
    try:
        cruising_mod()
    except Exception as e:
        time.sleep(0.01)
        print('Cruising_Mod error：', e)
