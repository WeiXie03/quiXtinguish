import sys
import socket
import numpy as np
import cv2
import keyboard
from data_collection.writeframes_stereo import *
from time import sleep

class Stream(cv2.VideoCapture):
    def __init__(self, port, side):
        super().__init__('udpsrc port={} ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink'.format(port), cv2.CAP_GSTREAMER)
        self.side = side
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)
        self.port = port

    def __str__(self):
        return 'video stream of {} camera on port {}'.format(self.side, self.port)

    def __del__(self):
        cv2.destroyAllWindows()

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
    speed = 0.5
    if keyboard.is_pressed('j'):
        targetAngles[0] -= speed
    elif keyboard.is_pressed('l'):
        targetAngles[0] += speed
    elif keyboard.is_pressed('i'):
        targetAngles[1] += speed
    elif keyboard.is_pressed('k'):
        targetAngles[1] -= speed
    return targetAngles

if __name__ == "__main__":
    HOST = input('Enter IP address of RPi: ')
    PORT = 3027
    TIMEOUT_SECONDS = 1e-3

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT_SECONDS)
        #sock.connect((HOST, PORT))
        print('connected to RPi at', HOST, 'on port', PORT)

        '''
        lcam = Stream(5000, 'left')
        rcam = Stream(5200, 'right')
        '''
        curServoAngles = [90.0, 90.0]
        while True:
            try:
                data = sock.recv(1024).decode()
                #print('cur', curServoAngles)
            except socket.timeout as e:
                pass
            except socket.error as e:
                print(e)
                sys.exit(1)
            else:
                print(data)
                #curServoAngles = [int(x) for x in curServoAngles.split(',')]


            cmds = [None, None, None, None, None]

            #setting speed to 40% of max for now
            cmds[0], cmds[1] = drive()
            cmds[2] = 40

            #targetAngles = curServoAngles.copy()
            curServoAngles = rotate_servos(curServoAngles)
            #cmds[3], cmds[4] = curServoAngles
            curServoAngles[0] = numpy.clip(curServoAngles[0], 80.0, 110.0)
            curServoAngles[1] = numpy.clip(curServoAngles[1], 80.0, 110.0)
            cmds[3], cmds[4] = tuple([int(x) for x in curServoAngles])

            print(curServoAngles)

            cmdsBytes = ','.join([str(x) for x in cmds]).encode()
            #print(cmdsBytes.decode())

            #print(','.join([str(x) for x in cmds]), (HOST, PORT))
            sock.sendto(cmdsBytes, (HOST, PORT))

            '''
            for stream in (lcam, rcam):
                _, frame = stream.read()
                cv2.imshow(stream.side, frame)
            '''

            sleep(0.1)
