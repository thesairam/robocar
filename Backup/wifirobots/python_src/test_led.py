# 正 IIC（写）+ 地址（0X18） + 0xFF + 0x21+ 0x1X# I2C与Arduino通信
import smbus
import time, os

# 创建smbus实例
bus = smbus.SMBus(1)  # 0代表/dev/i2c0  1代表/dev/i2c1
# I2C通信地址
address = 0x18
print('writeinstruction run...')
try:
    while True:
        led_lists = []
        instruction = [0x33, 0x34, 0x35]
        for i in instruction:
            value = bus.read_word_data(address, i)
            led_lists.append(value)
        with open('./led.txt', 'a') as tmp:
            print(led_lists[0], led_lists[1], led_lists[2], end = '\n', sep = ',', file = tmp)
        time.sleep(0.05)
        print(led_lists)
except IOError:
    print('Write Error')
    os.system('sudo i2cdetect -y 1')