import socket
import testServo
import RPi.GPIO as GPIO

HOST = '192.168.0.16'
PORT = 3027

#numbering scheme is physical board
TILT_PIN = 32
PAN_PIN = 12
FREQ = 60

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    tilt = testServo.pwmServo(TILT_PIN, FREQ)
    pan = testServo.pwmServo(PAN_PIN, FREQ)
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
