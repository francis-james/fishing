import sys
import time
import serial
import math
# import cv2

# camera = cv2.VideoCapture(0)
# camera.set(cv2.cv.CV_CAP_PROP_FPS, 60)

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=921600
)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def command(x, dx, pan, dpan, tilt, dtilt, home):
    x = clamp(int(x*65535), 0, 65534);
    xh = x >> 8 & 0xff
    xl = x & 0xff

    dx = clamp(int(dx*255), 0, 254)

    pan = clamp(int(pan*32767), -32767, 32767);
    panh = pan >> 8 & 0xff
    panl = pan & 0xff
    if panh < 0:
        panh = 255 - panh

    tilt = clamp(int(tilt*32767), -32767, 32767);
    tilth = tilt >> 8 & 0xff
    tiltl = tilt & 0xff
    if tilth < 0:
        tilth = 255 - tilth

    dpan = clamp(int(dpan/10.0*127), -127, 127)
    if dpan < 0:
        dpan = 255 + dpan
    dtilt = clamp(int(dtilt/10.0*127), -127, 127)
    if dtilt < 0:
        dtilt = 255 + dtilt

    flags = 0x00
    if home:
        flags = flags | 0x01

    checksum = (xh + xl + dx + panh + panl + tilth + tiltl + dtilt + dpan + flags) & 0x7f
    ser.write(bytearray([0xff, 0xff, dx, xh, xl, tilth, tiltl, panh, panl, dtilt, dpan, flags, checksum]))

import csv
with open('x.csv', 'rb') as f:
    reader = csv.reader(f)
    x_list = list(reader)
print x_list[33][8]

f.close()

with open('th.csv', 'rb') as f:
    reader = csv.reader(f)
    th_list = list(reader)
print th_list[33][8]
x = 0;
pan = -0.3
tilt = 0.8
tiltn = 0.8
tiltl = 0.7
tilth = 0.9

dt = 1/60.0
panlast = 0
tiltlast = 0
xlast = 0
dx = 0

command(0, 0, pan, 0, tilt, 0, True)


panlast = pan
tiltlast = tilt
xlast = x
x=float(x_list[250][200])
pan=float(th_list[250][200])

factor = 1

dtilt = (tilt - tiltlast)/dt
dpan = (pan - panlast)/dt

xdiff = abs(x - xlast)
if xdiff > 0:
    dx = xdiff/dt * 0.45

command(x, 0.2, pan, dpan, 0.6, dtilt, False)

# ret, frame = camera.read()
# cv2.imshow('fish', frame)
# cv2.waitKey(1)
time.sleep(dt)

dtilt=0.001
while True:
    command(x, 0.2, pan, dpan, 0.6, dtilt, False)
    time.sleep(1)
    command(x, 0.2, pan, dpan, 1, dtilt, False)
    time.sleep(1)

