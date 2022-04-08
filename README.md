A project aimed at augmenting firefighting and fire safety with robotics to achieve early fire detection and autonomous extinguishing.
FireBot is a "home" robot that (1) visually detects fire, (2) communicates with first responders (currently just streaming live video), and (3) autonomously or by remote control shoots water to extinguish. This is the software, which can roughly be divided into a few main parts:
1. Visual Fire Detection using a CNN with near infrared cameras, training under [ml/](ml/)
  - trained on self-created and collected candle data (see the [poster & deck](https://sites.google.com/view/tom-x/projects/firebot-augmenting-firefighting-with-ai) for more information) [stored using Python Pickle](data_collection/)
  - OpenCV, NumPy, PyTorch
2. Each pair of Python scripts in [rpi/](rpi/) and [./](./) are standalone. To start "using" FireBot, [rpi/serve.sh](rpi/serve.sh) and [client.sh](client.sh) are launched on the onboard RPi and first responders' device, respectively.
  - all implement streaming live video from onboard Raspberry Pi to server/first responders' computer (over LAN)
    - Camera stream class wrapping gStreamer and OpenCV components in [data_collection/recvid_multipi.py](data_collection/recvid_multipi.py), [data_collection/writeframes.py](data_collection/writeframes.py)
3. Aiming
  - The angles to turn to are calculated on the client (first responder device) side.
  - The FireBot uses a stereo camera setup, enabling depth estimation. Based on projectile motion, [the angle to tilt to is calculated](projectile_motion/projectile.py).
  - These angles are sent to separate ports on the RPi, which controls its [2 servos through PWM on GPIO](rpi/motiveServer.py)

Read more about the project at https://sites.google.com/view/tom-x/projects/firebot-augmenting-firefighting-with-ai
