import socket
import numpy
import pigpio as pig
from testMotion.testServo import *
from testMotion.testMotors import *
import sys

class Robot():
    def __init__(self, l_motor_pins=(26,19,13), r_motor_pins=(5,6,0), tilt_pin=23, pan_pin=24, frequency=50, name='robot'):
        self.pi = pig.pi()
        self.name = name

        self.freq = frequency
        self.left = Motor(pi, l_motor_pins, frequency, 'left')
        self.right = Motor(pi, r_motor_pins, frequency, 'right')
        self.tilt = hwServo(pi, tilt_pin, frequency, 1420, 1750)
        self.pan = Servo(pi, pan_pin, frequency)

    def __repr__(self):
        return '{} using {} pigpio raspberry pi object\nfrequency={}, left motor controlled by pins {}, right by {}, tilt servo controlled by {}, pan by {}'.format(self.name, self.pi, self.freq, (self.left.in1_pin, self.left.in2_pin, self.left.enable_pin), (self.right.in1_pin, self.right.in2_pin, self.right.enable_pin), self.tilt.pin, self.pan.pin)

    def forward(self, lspeed, rspeed):
        self.left.clockwise(self, lspeed)
        self.right.clockwise(self, rspeed)

    def backward(self, lspeed, rspeed):
        self.left.counterclockwise(self, lspeed)
        self.right.counterclockwise(self, rspeed)

    def rotate(self, servo_angles):
        self.tilt.specTurn(self.tilt.calc_duty(servo_angles[0]))
        self.pan.specTurn(self.pan.calc_duty(servo_angles[1]))

def parse_cmds(cmds, robot):
    #cmds is in form ['f' or 'b', 'l' or 'r', drive speed, tilt angle, pan angle]

    #motors
    #both of class Robot's driving functions take (robot, left motor speed, right motor speed)
    lspeed, rspeed = 0, 0
    if cmds[0] != 'pause':
        if cmds[1] == 'pause':
            lspeed, rspeed = cmds[2], cmds[2]
        elif cmds[1] == 'l':
            lspeed, rspeed = cmds[2], cmds[2]/2
        else:
            lspeed, rspeed = cmds[2]/2, cmds[2]
        #actually command the motors
        if cmds[0] == 'f':
            robot.forward(lspeed, rspeed)
        else:
            robot.backward(lspeed, rspeed)
    else:
        if cmds[1] == 'l':
            lspeed, rspeed = 0, cmds[2]
        elif cmds[1] == 'r':
            lspeed, rspeed = cmds[2], 0
        #elif cmds[1] is also pause, do nothing

        #turn one track forward while the other does not; pivot forward
        robot.forward(lspeed, rspeed)

    #servos
    self.rotate((cmds[3], cmds[4]))

if __name__ == "__main__":
    HOST = input('Enter IP address of RPi. ')
    PORT = 3027

    try:
        robot = Robot(name='FireBot')
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, PORT))
            while True:
                try:
                    cmds, addr = sock.recvfrom(2048)
                except socket.timeout as e:
                    print(e)
                    print('waiting(?)')
                except socket.error as e:
                    print(e)
                    sys.exit()
                else:
                    cmds = [ele for ele in (cmds.decode()).split(',')]
                    for cmd in cmds[2:]:
                        cmd = int(cmd)

                    parse_cmds(cmds, robot)

                    cur_servo_angles = ','.join(cmds[3:]).encode()
                    sock.sendto(cur_servo_angles, addr)

        finally:
            robot.left.close()
            robot.right.close()
            robot.pi.write(robot.tilt.pin, 0)
            robot.pi.write(robot.pan.pin, 0)
            robot.pi.stop()
            print(robot.name, 'dead')
            break
