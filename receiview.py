import numpy
import cv2

cap0 = cv2.VideoCapture('udpsrc port=5200 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)
cap1 = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)

win0 = cv2.namedWindow('cam0', cv2.WINDOW_OPENGL)
win1 = cv2.namedWindow('cam1', cv2.WINDOW_OPENGL)

while(True):
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    # Display the resulting frame
    cv2.imshow('cam0',frame0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('cam1',frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()
