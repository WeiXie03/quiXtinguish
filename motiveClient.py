import sys
import socket
import numpy as np
import cv2
import keyboard
from data_collection.receivewrite2 import *
from time import sleep

#NOTE: OpenCV in Python just cannot handle video streaming and keyboard control at the same time, will just manually run receiverwrite2.py concurrently

def drive():
    cmd = ['','']
    if keyboard.is_pressed('w'):
        cmd[0] = 'f'
    elif keyboard.is_pressed('s'):
        cmd[0] = 'b'
    else:
        cmd[0] = 'pause'

    if keyboard.is_pressed('a'):
        cmd[1] = 'l'
    elif keyboard.is_pressed('d'):
        cmd[1] = 'r'
    else:
        cmd[1] = 'pause'

    return cmd

def rotate_servos(targetAngles):
    #targetAngles is [horizontal(panning), vertical(tilting)]
    if keyboard.is_pressed('j'):
        targetAngles[0] -= 1
    elif keyboard.is_pressed('l'):
        targetAngles[0] += 1
    elif keyboard.is_pressed('i'):
        targetAngles[1] += 1
    elif keyboard.is_pressed('k'):
        targetAngles[1] -= 1
    return targetAngles

HOST = input('Enter IP address of RPi: ')
PORT = 3027
TIMEOUT_SECONDS = 1e-3

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(TIMEOUT_SECONDS)
    #sock.connect((HOST, PORT))
    print('connected to RPi at', HOST, 'on port', PORT)

    curServoAngles = [90, 90]
    while True:
        try:
            curServoAngles = sock.recv(1024).decode()
        except socket.timeout as e:
            pass
        except socket.error as e:
            print(e)
            sys.exit(1)
        else:
            curServoAngles = [int(x) for x in curServoAngles.split(',')]

        cmds = [None, None, None, None, None]

        #setting speed to 40% of max for now
        cmds[0], cmds[1] = drive()
        cmds[2] = 40

        targetAngles = curServoAngles.copy()
        targetAngles = rotate_servos(targetAngles)
        cmds[3], cmds[4] = targetAngles
        cmds[3] = numpy.clip(cmds[3], 0, 180)
        cmds[4] = numpy.clip(cmds[4], 0, 180)

        cmdsBytes = ','.join([str(x) for x in cmds]).encode('ascii')
        print(cmdsBytes.decode('ascii'))

        print(','.join([str(x) for x in cmds]), (HOST, PORT))
        sock.sendto(cmdsBytes, (HOST, PORT))
        sleep(0.02)
