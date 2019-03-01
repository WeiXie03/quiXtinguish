#using UDP and RTP to stream video from V4L2 as JPEG frames, this script is the receiver, RPi is the sender, refer to https://stackoverflow.com/questions/46219454/how-to-open-a-gstreamer-pipeline-from-opencv-with-videowriter/46636126#46636126

gst-launch-1.0 -v udpsrc port=5000 ! application/x-rtp, media=video, encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0 #& receive both in camera streams in parrallel, use clockspeed= to manually set hard framerate(not frames/sec)

#gst-launch-1.0 -v udpsrc port=5200 ! application/x-rtp, media=video, encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! xvimagesink sync=0


#using UDP and RTP to stream video from V4L2 with H.264 compression, this script is the receiver, RPi is the sender, refer to https://devtalk.nvidia.com/default/topic/1037884/jetson-tx1/convert-gstreamer-pipeline-to-opencv-in-python/

#gst-launch-1.0 -v udpsrc port=5000 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink &

#gst-launch-1.0 -v udpsrc port=5200 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! decodebin ! videoconvert ! autovideosink
