#!/bin/sh -e

# Add your code here

sed -i '$d' /etc/hostapd/hostapd.conf
MAC=$(ifconfig | awk  '/ether/{print $2 ;exit}' |sed 's/\://g')
ID="ssid=LABISTS_"
SSID=${ID}${MAC}
echo $SSID >> /etc/hostapd/hostapd.conf

ifconfig wlan0 down
sleep 5
ifconfig wlan0 192.168.1.1 netmask 255.255.255.0 up
service dnsmasq restart
sleep 5 
hostapd -B /etc/hostapd/hostapd.conf & > /dev/null 2>&1
#hostapd -B /etc/hostapd/hostapd.conf
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
#************************************#
exit 0
