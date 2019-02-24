import RPi.GPIO as gpio
from time import sleep
gpio.setmode(gpio.BCM)

class pwmServo():
    def __init__(self, pin, freq):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.freq = freq
        self.turn = gpio.PWM(self.pin, self.freq)
        self.turn.start(0)

    def specTurn(self, angle):
        duty = (12/180.0)*angle + 3
        print(duty)
        gpio.output(self.pin, True)
        self.turn.ChangeDutyCycle(duty)
        sleep(1)
        gpio.output(self.pin, False)
        self.turn.ChangeDutyCycle(0)


if __name__ == '__main__':
    pwmPin = int(input('What is the Broadcom pin number of your PWM signal pin? '))
    tilt = pwmServo(pwmPin, 60)
    for it in range(50):
        try:
            angle = float(input('Enter the angle you would like the servo horn to turn to in degrees. Range: 0 to ~175, 90 = neutral.\t'))
            if angle <= 170 and angle >= 0:
                tilt.specTurn(angle)
                print('at ', angle)
            else:
                print('angle not in range')
        except KeyboardInterrupt:
            tilt.turn.stop()
            print('PWM signal terminated')
            break

    gpio.cleanup()
