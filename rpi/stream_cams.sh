#sending v4l2 video over UDP in RTP packets as JPEG frames to desktop, refer to https://stackoverflow.com/questions/46219454/how-to-open-a-gstreamer-pipeline-from-opencv-with-videowriter/46636126#46636126

echo enter IP address of client\(receiver\):
echo "wei's desktop: 192.168.0.10
bulky dell laptop on home wifi: 192.168.0.20
bulky dell laptop on ethernet: 192.168.43.250"
read HOST
#HOST=192.168.0.10

echo left camera port=5000
#read LEFT_PORT
LEFT_PORT=5000
echo right cam port=5200
#read RIGHT_PORT
RIGHT_PORT=5200
echo port for picam=6300
#read PICAM_PORT
PICAM_PORT=6300

gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480 ! jpegenc ! rtpjpegpay ! udpsink host=$HOST port=$LEFT_PORT &
gst-launch-1.0 -v v4l2src device=/dev/video2 ! video/x-raw, format=YUY2, width=640, height=480 ! jpegenc ! rtpjpegpay ! udpsink host=$HOST port=$RIGHT_PORT

#Raspberry Pi NoIR Camera(not official one, variant from Smraza)
#raspivid -t 0 -n -rot 180 -h 640 -w 480 -o udp://$HOST:$PICAM_PORT
#raspivid -t 0 -n -cd MJPEG -rot 270 -h 640 -w 480 -o - | nc $HOST $PICAM_PORT
#raspivid -n -t 0 -b 2500000 -fps 20 -w 640 -h 480 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=$HOST port=$PICAM_PORT
#raspivid -n -t 0 -b 2500000 -w 640 -h 480 -cd MJPEG  -o - | gst-launch-1.0 -v fdsrc ! jpegparse ! rtpjpegpay ! udpsink host=$HOST port=$PICAM_PORT
#gst-launch-1.0 -v v4l2src device=/dev/video4 ! video/x-raw, format=YUY2, width=800, height=600 ! jpegenc ! rtpjpegpay ! udpsink host=$HOST port=$PICAM_PORT

#h264:
#sending v4l2 video over UDP in RTP packets with H.264 compression to desktop, refer to https://devtalk.nvidia.com/default/topic/1037884/jetson-tx1/convert-gstreamer-pipeline-to-opencv-in-python/
#gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,width=800,height=600,format=BGR ! videoconvert ! x264enc tune=zerolatency speed-preset=superfast ! rtph264pay ! udpsink host=192.168.0.16 port=5000 &
#gst-launch-1.0 -v v4l2src device=/dev/video1 ! video/x-raw,width=800,height=600,format=BGR ! videoconvert ! x264enc tune=zerolatency speed-preset=superfast ! rtph264pay ! udpsink host=192.168.0.16 port=5200
