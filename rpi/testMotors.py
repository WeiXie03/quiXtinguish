import RPi.GPIO as gpio

class Motor():
    def __init__(self, in1, in2, enable, frequency=100, name='default'):
        #both sides of L293D have pair of connections to motor and an enable controlled by RPi
        self.in1_pin = in1
        self.in2_pin = in2
        self.enable_pin = enable
        self.freq = frequency
        self.pwm = self.setupPins()
        self.name = name

    def __repr__(self):
        return self.name

    def setupPins(self):
        gpio.setup(self.in1_pin, gpio.OUT)
        gpio.output(self.in1_pin, True)
        gpio.setup(self.in2_pin, gpio.OUT)
        gpio.output(self.in2_pin, True)

        #pwm connected to enable for speed control
        gpio.setup(self.enable_pin, gpio.OUT)
        pwm = gpio.PWM(self.enable_pin, self.freq)
        gpio.output(self.enable_pin, True)
        #start the signal at 0 intensity(doesn't actually make anything happen)
        pwm.start(0)
        return pwm

        print('pins set up')

    def setSpeed(self, dutCyc):
        #set speed using PWM to enable of L293D
        #duty cycle should be in percent
        self.pwm.ChangeDutyCycle(dutCyc)
        print('percentage of max speed ', dutCyc, '%')

    def clockwise(self, dutCyc):
        gpio.output(self.in1_pin, gpio.HIGH)
        gpio.output(self.in2_pin, gpio.LOW)
        self.setSpeed(dutCyc)

    def counterclockwise(self, dutCyc):
        #reverse direction = reverse pins
        gpio.output(self.in1_pin, gpio.LOW)
        gpio.output(self.in2_pin, gpio.HIGH)
        self.setSpeed(dutCyc)

if __name__ == "__main__":
    gpio.setmode(gpio.BOARD)
    FREQUENCY = 120#Hz
    #in1, in2, enable, frequency
    left = Motor(16, 18, 33, FREQUENCY, 'left')
    right = Motor(13, 15, 7, FREQUENCY, 'right')

    while True:
        for motor in (left, right):
            print(motor)
            try:
                direction = input("Which way?[f/b]: ")
                speed = float(input('How fast(portion of maximum speed in percentage)? '))
                if direction == 'f':
                    motor.clockwise(speed)
                else:
                    print('back')
                    motor.counterclockwise(speed)
            except:
                print('no')
                raise
                gpio.output(left.in1_pin, False)
                gpio.output(left.in2_pin, False)
                #stop the pwm signal
                left.pwm.stop()
                gpio.output(left.enable_pin, False)
                break

    gpio.cleanup()
