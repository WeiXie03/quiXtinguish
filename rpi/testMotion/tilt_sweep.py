import pigpio as pig
import testServo as servo
from time import sleep

def sweep(servo):
    print('turning')
    servo.turn(90.0)
    sleep(0.5)
    servo.turn(120.0)
    sleep(0.5)

if __name__ == "__main__":
    pi = pig.pi()
    PIN = int(input('Enter the RPi pin number the servo is connected to according to Broadcom\'s numbering.\t'))
    FREQUENCY = 72

    tilt = servo.Servo(pi, PIN, FREQUENCY, min_bound=650, max_bound=1140)
    tilt.close()

    try:
        sweep(tilt)
    finally:
        print('ending')
        tilt.close()
        pi.stop()
