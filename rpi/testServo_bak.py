# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
# [GCC 6.3.0 20170516]
# Embedded file name: /home/pi/Public/rpi/testServo.py
# Compiled at: 2019-02-16 16:09:25
import RPi.GPIO as gpio
from time import sleep
import math
gpio.setmode(gpio.BOARD)

class pwmServo(object):

    def __init__(self, pin, freq):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.freq = freq
        self.turn = gpio.PWM(self.pin, self.freq)

    def specTurn(self, angle):
        duty = 12 / 180.0 * angle + 3
        print duty
        gpio.output(self.pin, True)
        self.turn.ChangeDutyCycle(duty)
        sleep(1)
        gpio.output(self.pin, False)
        self.turn.ChangeDutyCycle(0)


if __name__ == '__main__':
    tilt = pwmServo()
    tilt.turn.start(0)
    for it in range(50):
        try:
            angle = float(input('Enter the angle you would like the servo horn to turn to in degrees. Range: 0 to ~175, 90 = neutral.\t'))
            if angle <= 170 and angle >= 0:
                tilt.specTurn(angle)
                print ('at ', angle)
            else:
                print 'angle not in range'
        except KeyboardInterrupt:
            tilt.turn.stop()
            print 'PWM signal terminated'
            break

    gpio.cleanup()