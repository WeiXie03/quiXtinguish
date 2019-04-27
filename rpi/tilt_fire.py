import motiveServer as motion
import sys, os, subprocess
import socket
from time import sleep
import pdb

if __name__ == "__main__":
    #HOST = input('IP of remote: ')
    HOST = "192.168.43.250"
    #HOST = "192.168.0.20"
    PORT = 3027

    robot = motion.Robot(name='FireBot', frequency=60)

    try:
        print('streaming')
        #set everything to neutral, pan netural actually 95
        robot.tilt.turn(90.0)
        curang = 90.0

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', PORT))
            sock.settimeout(4.0)
            print('connected')
            while True:
                try:
                    des, (HOST, PORT) = sock.recvfrom(1024)
                    print(HOST, PORT)
                    des = float(des.decode())
                    print(des)
                except socket.timeout as e:
                    print(e)
                    continue
                except socket.error as e:
                    print(e)
                    sys.exit()
                except ValueError:
                    continue
                else:
                    print('got it')
                    break

        #sock.sendto(str('done').encode(), (HOST, PORT))
        if curang > des:
            for shft in range(int(abs(des-curang))),int(des)-1, -4):
                robot.tilt.turn(shft+curang)
                sleep(0.1)
        else:
            for shft in range(int(abs(des-curang)), int(des)+1, 4):
                robot.tilt.turn(shft+curang)
                sleep(0.1)


    finally:
        robot.left.close()
        robot.right.close()
        robot.pi.write(robot.pan.pin, 0)
        robot.pi.write(robot.tilt.pin, 0)
        robot.pi.stop()
        print(robot.name, 'dead')
