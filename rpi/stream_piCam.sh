echo enter IP address of client\(receiver\):
echo "wei's desktop: 192.168.0.10
bulky dell laptop on home wifi: 192.168.0.20
bulky dell laptop on ethernet: 192.168.43.250"
read HOST
#HOST=192.168.0.10
#HOST=192.168.43.250

echo port for picam=6300
#read PICAM_PORT
PICAM_PORT=6300

#Raspberry Pi NoIR Camera(not official one, variant from Smraza)
#raspivid -t 0 -n -rot 180 -h 640 -w 480 -o udp://$HOST:$PICAM_PORT
#raspivid -t 0 -n -cd MJPEG -rot 270 -h 640 -w 480 -o - | nc $HOST $PICAM_PORT
#raspivid -n -t 0 -b 2500000 -fps 20 -w 640 -h 480 -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay pt=96 config-interval=5 ! udpsink host=$HOST port=$PICAM_PORT
raspivid -n -t 0 -b 2500000 -fps 20 -cd MJPEG -w 640 -h 480 -o - | gst-launch-1.0 fdsrc ! "image/jpeg,framerate=20/1" ! jpegparse ! rtpjpegpay ! udpsink host=$HOST port=$PICAM_PORT
