import socket
import numpy
import pigpio as pig
from testMotion.testServo import *
from testMotion.testMotors import *
import sys

class Robot():
    def __init__(self, l_motor_pins=(19,26,13), r_motor_pins=(6,5,0), tilt_pin=24, pan_pin=23, frequency=100, name='robot'):
        self.pi = pig.pi()
        self.name = name

        self.freq = frequency
        self.left = Motor(self.pi, l_motor_pins, frequency, 'left')
        self.right = Motor(self.pi, r_motor_pins, frequency, 'right')
        #self.tilt = hwServo(self.pi, tilt_pin, frequency, 1420, 1750)
        self.tilt = Servo(self.pi, tilt_pin, frequency, 650, 1140)
        self.pan = Servo(self.pi, pan_pin, frequency, 670, 1380)

    def __repr__(self):
        return '{} using {} pigpio raspberry pi object\nfrequency={}, left motor controlled by pins {}, right by {}, tilt servo controlled by {}, pan by {}'.format(self.name, self.pi, self.freq, (self.left.in1_pin, self.left.in2_pin, self.left.enable_pin), (self.right.in1_pin, self.right.in2_pin, self.right.enable_pin), self.tilt.pin, self.pan.pin)

    def forward(self, lspeed, rspeed):
        self.left.clockwise(lspeed)
        self.right.clockwise(rspeed)

    def backward(self, lspeed, rspeed):
        self.left.counterclockwise(lspeed)
        self.right.counterclockwise(rspeed)

    def turnR_in_pos(self, speed):
        self.left.clockwise(speed)
        self.right.counterclockwise(speed)

    def turnL_in_pos(self, speed):
        self.left.counterclockwise(speed)
        self.right.clockwise(speed)

    def rotate(self, servo_angles):
        self.tilt.turn(servo_angles[1])
        self.pan.turn(servo_angles[0])

def parse_cmds(cmds, robot):
    #cmds is in form ['f' or 'b', 'l' or 'r', drive speed, pan angle, tilt angle]

    #motors
    #both of class Robot's driving functions take (robot, left motor speed, right motor speed)
    cmds[2] = int(cmds[2])
    if cmds[0] != 'pause':
        lspeed, rspeed = 0, 0
        if cmds[1] == 'pause':
            lspeed, rspeed = cmds[2], cmds[2]
        elif cmds[1] == 'l':
            lspeed, rspeed = cmds[2], 0
        else:
            lspeed, rspeed = 0, cmds[2]
        #actually command the motors
        if cmds[0] == 'f':
            robot.forward(lspeed, rspeed)
        else:
            robot.backward(lspeed, rspeed)

    else:
        if cmds[1] == 'l':
            robot.turnL_in_pos(cmds[2])
        elif cmds[1] == 'r':
            robot.turnR_in_pos(cmds[2])
        #elif cmds[1] is also pause, do nothing

    if cmds[0] == 'pause' and cmds[1] == 'pause':
        robot.forward(0, 0)
    #servos
    robot.rotate((int(cmds[3]), int(cmds[4])))

if __name__ == "__main__":
    PORT = 3027

    try:
        robot = Robot(name='FireBot')
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', PORT))
            while True:
                try:
                    cmds, addr = sock.recvfrom(2048)
                except socket.timeout as e:
                    print(e)
                except socket.error as e:
                    print(e)
                    sys.exit()
                else:
                    cmds = [ele for ele in (cmds.decode()).split(',')]
                    cmds[2] = int(cmds[2])

                    parse_cmds(cmds, robot)

                    cur_servo_angles = ','.join(cmds[3:]).encode()
                    print(cur_servo_angles)
                    sock.sendto(cur_servo_angles, addr)

    finally:
        robot.left.close()
        robot.right.close()
        robot.pi.write(robot.tilt.pin, 0)
        robot.pi.write(robot.pan.pin, 0)
        robot.pi.stop()
        print(robot.name, 'dead')
