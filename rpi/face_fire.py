import motiveServer as motion
import sys, os, subprocess
import socket
from time import sleep
import pdb


if __name__ == "__main__":
    #HOST = input('IP of remote: ')
    HOST = "192.168.43.250"
    PORT = 3030

    robot = motion.Robot(name='FireBot')

    try:
        print('streaming')
        #set everything to neutral, pan netural actually 95
        robot.rotate((95.0, 90.0))
        curang = 95.0

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1.5)
            print('connected')
            while True:
                try:
                    #send current angle to remote
                    sock.sendto(str(curang).encode(), (HOST, PORT))
                    print('sent')

                    shft, (HOST, PORT) = sock.recvfrom(1024)
                    shft = float(shft.decode())
                    print(shft)
                except socket.timeout as e:
                    print(e)
                    continue
                except socket.error as e:
                    print(e)
                    sys.exit()
                except ValueError:
                    print(shft)
                    continue
                else:
                    curang = shft
                    robot.pan.turn(curang)
                    sleep(0.2)

    finally:
        robot.left.close()
        robot.right.close()
        robot.pi.write(robot.pan.pin, 0)
        robot.pi.write(robot.tilt.pin, 0)
        robot.pi.stop()
        print(robot.name, 'dead')
