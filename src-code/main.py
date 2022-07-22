from machine import Pin
from neopixel import NeoPixel
from utime import sleep, mktime,localtime
from machine import RTC
from ntptime import settime
from network import WLAN, STA_IF

wlan = WLAN(STA_IF)

#clock digit mappings
digits = {
    0: {
        0: [ 38, 37, 36, 35,34 ],
        1: [ 33, 32 ],
        2: [ 31, 30, 29, 28, 27 ],
        3: [ 25, 26 ],
        4: [ 13, 14, 15, 16, 17 ],
        5: [ 19, 18 ],
        6: [ 24, 23, 22, 21, 20 ]
        },
    1: {
        0: [ 52, 51, 50, 49, 48 ],
        1: [ 47, 46 ],
        2: [ 45, 44, 43, 42, 41 ],
        3: [ 39, 40 ],
        4: [ 1, 2 ,3 ,4, 5 ],
        5: [ 7, 6 ],
        6: [ 12, 11, 10, 9, 8]
        },
    2: {
        0: [ 58, 57, 56, 55, 54 ],
        1: [ 105, 104 ],
        2: [ 103, 102, 101, 100, 99 ],
        3: [ 59, 60 ],
        4: [ 72, 71, 70, 69, 68 ],
        5: [ 67, 66 ],
        6: [ 65, 64, 63, 62, 61 ]
        },
    3: {
        0: [ 98, 97, 96, 95, 94 ],
        1: [ 92, 93 ],
        2: [ 91, 90, 89, 88, 87 ],
        3: [ 85, 86 ],
        4: [ 84, 83, 82, 81, 80 ],
        5: [ 79, 78 ],
        6: [ 77, 76, 75, 74, 73 ]
        }
    }

# the separator
dots = [ 53, 0 ]

#numbers as digit combos
numbers = {
    0: [ 0, 1, 2, 4, 5, 6],
    1: [ 2, 4 ],
    2: [ 1, 2, 3, 5, 6 ],
    3: [ 1, 2, 3, 4, 5 ],
    4: [ 0, 2, 3, 4 ],
    5: [ 1, 0, 3, 4, 5 ],
    6: [ 0, 1, 3, 4, 5, 6 ],
    7: [ 1, 2, 4 ],
    8: [ 0, 1, 2, 3, 4, 5, 6 ],
    9: [ 0, 1, 2, 3, 4, 5 ]
    }


rtc = RTC()

pin = Pin(16, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 106)   # create NeoPixel driver on GPIO0 for 8 pixels
np.ORDER=(1,0,2,3)
print("Starting ...")
dot_state = 0
count = 0

def update_time():
    if wlan.isconnected():
        print("updating time")
        settime()
        tm = localtime(mktime(localtime()) + utc_shift*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)

def write_digit(digit, value, color):
    segs = digits[digit]
    number = numbers[value]
    for seg in number:
        #print("Segment: "+str(seg))
        for line in segs[seg]:
            np[line] = (color)

def toggle_dots():
    global dot_state
    if (dot_state == 0):
        np[0] = (255, 0, 0)
        np[53] = (255, 0 , 0)
        dot_state = 1
    else:
        np[0] = (0, 0, 0)
        np[53] = (0, 0, 0)
        dot_state = 0
    
def run_clock():
    hour = rtc.datetime()[4]
    min = rtc.datetime()[5]
    if len(str(hour)) < 2:
        write_digit(0, int(("0"+str(hour))[0]), (0,255,0))
        write_digit(1, int(("0"+str(hour))[1]), (0,255,0))
    else:
        write_digit(0, int(str(hour)[0]), (0,255,0))
        write_digit(1, int(str(hour)[1]), (0,255,0))
    if len(str(min)) < 2:
        write_digit(2, int(("0"+str(min))[0]), (0,255,0))
        write_digit(3, int(("0"+str(min))[1]), (0,255,0))
    else:
        write_digit(2, int(str(min)[0]), (0,255,0))
        write_digit(3, int(str(min)[1]), (0,255,0))

def main():
    global count
    while 1:
        if count == 300:
            update_time()
            count = 0
        np.fill((0,0,0))
        toggle_dots()
        run_clock()
        np.write()
        sleep(1)
        count += 1

main()