import socket
import cv2
import data_collection.writeframes as stream
import numpy

def send_turn_angle(event, x, y, flags, data):
    #data should be iterable with calibration matrix, image, socket
    calib_mtx = data[0]
    foclx = calib_mtx[0]
    img = data[1]
    socket = data[2]

    #shape of a mat object is height, width, channel
    req_disp = img.shape[1]/2 - x
    req_angle = math.degrees(math.atan(req_disp/foclx))

    socket.sendall(str(req_angle).encode())

if __name__ == "__main__":
    HOST = input('IP address of RPi: ')
    PORT = 6300
    cam = stream.Cam(PORT, 'view', stream.Codec.H264)

    print('enter path of calibrated settings in terminal command')
    CALIB_PATH = sys.argv[1]
    calib_mtx = numpy.load(CALIB_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print('connected to RPi at', HOST, 'on port', PORT)
        sock.send(b'connected')
        while True:
            _, frame = cam.cap.read()
            cv2.imshow(cam.label, frame)
            key_hit = cv2.waitKey(1)

            cv2.setMouseCallback(cam.label, send_turn_angle, (calib_mtx, frame, sock))

            if key_hit == ord('q'):
                break
