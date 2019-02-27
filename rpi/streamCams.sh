#sending v4l2 video over UDP in RTP packets as JPEG frames to desktop, refer to https://stackoverflow.com/questions/46219454/how-to-open-a-gstreamer-pipeline-from-opencv-with-videowriter/46636126#46636126

#gst-launch-1.0 -v v4l2src device=/dev/video1 ! video/x-raw,format=BGR,width=800,height=600 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.0.16 port=5000
#gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=960,height=540 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.0.16 port=5000 &
#gst-launch-1.0 -v v4l2src device=/dev/video1 ! video/x-raw,format=YUY2,width=960,height=540 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.0.16 port=5200

gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=960,height=720 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.43.250 port=5000 &
gst-launch-1.0 -v v4l2src device=/dev/video1 ! video/x-raw,format=YUY2,width=960,height=720 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.43.250 port=5200

#sending v4l2 video over UDP in RTP packets with H.264 compression to desktop, refer to https://devtalk.nvidia.com/default/topic/1037884/jetson-tx1/convert-gstreamer-pipeline-to-opencv-in-python/

#gst-launch-1.0 -v v4l2src device=/dev/video0 ! video/x-raw,width=800,height=600,format=BGR ! videoconvert ! x264enc tune=zerolatency speed-preset=superfast ! rtph264pay ! udpsink host=192.168.0.16 port=5000 &

#gst-launch-1.0 -v v4l2src device=/dev/video1 ! video/x-raw,width=800,height=600,format=BGR ! videoconvert ! x264enc tune=zerolatency speed-preset=superfast ! rtph264pay ! udpsink host=192.168.0.16 port=5200
