#!/bin/sh
python /home/pi/work/wifirobots/python_src/hbwz_startmain.py &

sleep 12

node /home/pi/work/wifirobots/XiaoRGeekBle/code/XiaoRGeek/main.js &
exit 0
#./wifirobots &



