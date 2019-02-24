import socket
#going to use pigpio for servos as well
#import RPi.GPIO as GPIO
#import testServo
import pigpio as pig
import testMotors

class Robot():
    lMotorPins = (19, 26, 13)
    rMotorPins = (6, 5, 0)
    frequency = 100
    tiltPin = 12
    panPin = 18
    #numbering scheme is Broadcom

    def __init__(rpi):
        self.pi = rpi
        self.leftMotor = motorSetup(Robot.lMotorPins, 'left')
        self.rightMotor = motorSetup(Robot.rMotorPins, 'right')

    def motorSetup(self, motorPins, name='default motor'):
        #motorPins should be a tuple of pins on the RPi in the form in1, in2, enable
        motor = testMotors.Motor(self.pi, motorPins[0], motorPins[1], motorPins[2], self.freq, name)
        return motor

    def servoSetup(self, pwmPin):
        self.pi.set_PWM_range(pwmPin, )

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

if __name__ == "__main__":
    HOST = '192.168.0.16'
    PORT = 3027

    #numbering scheme is BCM
    TILT_PIN = 12 #PWM0
    PAN_PIN = 13 #PWM1
    FREQ = 330 #330 is max for servos
