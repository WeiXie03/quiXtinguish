import socket
import cv2
import data_collection.writeframes as stream
import numpy
import sys
import math

def send_turn_angle(event, x, y, flags, data):
    #data should be iterable with calibration matrix, image, socket
    calib_mtx = data[0]
    foclx = calib_mtx[0][0]
    print(foclx)
    img = data[1]
    addr = data[2]
    socket = data[3]

    if event == cv2.EVENT_LBUTTONDOWN:
        #shape of a mat object is height, width, channel
        req_disp = img.shape[1]/2 - x
        req_angle = math.degrees(math.atan(req_disp/foclx)) + 90

        print(req_angle)
        socket.sendto(str(req_angle).encode(), addr)

if __name__ == "__main__":
    HOST = input('IP address of RPi: ')
    PORT = 3030
    cam = stream.Cam(6300, 'view', stream.Codec.H264)

    print('enter path of calibrated settings in terminal command')
    CALIB_PATH = sys.argv[1]
    calib_mtx = numpy.load(CALIB_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(b'connected', (HOST, PORT))
        while True:
            _, frame = cam.cap.read()
            cv2.imshow(cam.label, frame)
            key_hit = cv2.waitKey(1)

            cv2.setMouseCallback(cam.label, send_turn_angle, (calib_mtx, frame, (HOST, PORT), sock))

            if key_hit == ord('q'):
                break
