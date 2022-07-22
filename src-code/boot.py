# This is script that run when device boot up or wake from sleep.

from network import WLAN, STA_IF
from machine import RTC
from ntptime import settime
from utime import mktime,localtime

rtc = RTC()
utc_shift = 2

wlan_ssid = "my_secret_ssid"
wlan_pass = "very_secret_pass"

wlan = WLAN(STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(wlan_ssid, wlan_pass)
    while not wlan.isconnected():
        print ('... connecting ...')
        pass
print('network config:', wlan.ifconfig())

settime()
tm = localtime(mktime(localtime()) + utc_shift*3600)
tm = tm[0:3] + (0,) + tm[3:6] + (0,)
rtc.datetime(tm)

print (rtc.datetime())

import webrepl
webrepl.start()
