import socket
import RPi.GPIO as GPIO
import testServo
import pigpio as pig
import testMotors

HOST = '192.168.0.16'
PORT = 3027

#numbering scheme is BCM
TILT_PIN = 12 #PWM0
PAN_PIN = 13 #PWM1
FREQ = 330 #330 is max for servos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    tilt = testServo.pwmServo(TILT_PIN, FREQ)
    pan = testServo.pwmServo(PAN_PIN, FREQ)

    pi = pigpio.pi()
    left = testMotors.Motor(pi, 23, 24, 25, FREQ, 'left')
    right = testMotors.Motor(pi, 27, 22, 17, FREQ, 'right')

    sock.connect((HOST, PORT))

    while True:
        try:
            data = sock.recv(1024).decode()
            if data:
                #assign which servo and the angle
                data = data.split(', ')
                servo = data[0]
                angle = int(data[1])

                print('turning ', servo, ' to ', angle)
                if servo == 'tilt' or servo == 't':
                    tilt.specTurn(angle)
                elif servo == 'pan' or 'p':
                    pan.specTurn(angle)
        except Exception:
            raise
            tilt.turn.stop()
            pan.turn.stop()
            GPIO.cleanup()
            print('terminating')
            break
