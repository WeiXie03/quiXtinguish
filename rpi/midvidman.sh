echo enter IP address of client\(receiver\):
echo "wei's desktop: 192.168.0.10
dell laptop on home wifi: 192.168.0.20"
read HOST

echo enter IP address of other RPi
echo other Pi set to 169.254.253.198
RPi=169.254.253.198

echo left cam port=5400
LPORT=5400
echo right cam port=5800
RPORT=5800

#Forwarding a gstream and sending one from an 3rd party RPi NoIR Camera Module
#raspivid -n -t 0 -b 3250000 -fps 16 -w 640 -h 480 -cd MJPEG -ex antishake -ifx none -awb sun -co 5 -sh 5 -br 50 -o - | gst-launch-1.0 fdsrc ! jpegparse ! rtpjpegpay pt=96 ! udpsink host=$HOST port=$RPORT &
raspivid -n -t 0 -b 3250000 -fps 16 -w 640 -h 480 -cd MJPEG -o - | gst-launch-1.0 fdsrc ! jpegparse ! rtpjpegpay pt=96 ! udpsink host=$HOST port=$RPORT &

gst-launch-1.0 udpsrc port=$LPORT ! udpsink host=$HOST port=$LPORT
