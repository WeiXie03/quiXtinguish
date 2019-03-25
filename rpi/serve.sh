sudo pigpiod

echo intiating NIR cam stream
python3 ./motiveServer.py
sh ./stream_piCam.sh
