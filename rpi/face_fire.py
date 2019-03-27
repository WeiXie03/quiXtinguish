import motiveServer as motion
#from data_collection.writeframes import *
import sys
import os
import socket
import subprocess

def load_calib(calib_path):
    #calibrated settings saved as a matrix in a NumPy file
    return np.load(calib_path)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 3030

    robot = motion.Robot(name='FireBot')

    try:
        stream_proc = subprocess.Popen(['sh', os.path.join('stream_piCam.sh')])
        robot.rotate((90, 90))

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', PORT))
            while True:
                try:
                    req_angle = sock.recv(1024)
                    req_angle = float(req_angle.decode())
                    print(req_angle)
                except socket.timeout as e:
                    print(e)
                except socket.error as e:
                    print(e)
                    sys.exit()
                except ValueError:
                    pass
                    continue
                else:
                    pass
                    #req_angle is a ref angle, need to add 90 deg
                    robot.pan.turn(45 + req_angle)

    finally:
        robot.left.close()
        robot.right.close()
        robot.pi.write(robot.pan.pin, 0)
        robot.pi.write(robot.tilt.pin, 0)
        robot.pi.stop()
        print(robot.name, 'dead')
