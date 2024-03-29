import pigpio as gpio

class Motor():
    def __init__(self, rpi, pins, frequency=100, name='default'):
        #pigpio raspberry pi object motor will be controlled by
        self.pi = rpi
        #both sides of L293D have pair of connections to motor and an enable controlled by RPi
        self.in1_pin = pins[0]
        self.in2_pin = pins[1]

        self.enable_pin = pins[2]
        self.freq = frequency
        self.pi.set_PWM_range(self.enable_pin, 255)
        self.pwmRange = self.pi.get_PWM_range(self.enable_pin)

        self.setupPins()
        self.name = name

    def setupPins(self):
        self.pi.set_mode(self.in1_pin, gpio.OUTPUT)
        self.pi.set_mode(self.in2_pin, gpio.OUTPUT)

        #pwm connected to enable for speed control
        self.pi.set_mode(self.enable_pin, gpio.OUTPUT)
        self.pi.set_PWM_frequency(self.enable_pin, self.freq)

        print('pins set up')

    def __repr__(self):
        return self.name

    def setSpeed(self, dutCyc):
        print('percentage of max speed ', dutCyc, '%')
        dutCyc = int(self.pwmRange*dutCyc/100)
        #set speed using PWM to enable of L293D
        #duty cycle should be in percent
        self.pi.set_PWM_dutycycle(self.enable_pin, dutCyc)

    def clockwise(self, dutCyc):
        self.pi.write(self.in1_pin, 1)
        self.pi.write(self.in2_pin, 0)
        self.setSpeed(dutCyc)

    def counterclockwise(self, dutCyc):
        #reverse direction = reverse pins
        self.pi.write(self.in1_pin, 0)
        self.pi.write(self.in2_pin, 1)
        self.setSpeed(dutCyc)

    def close(self):
        self.pi.write(self.in1_pin, 0)
        self.pi.write(self.in2_pin, 0)
        self.pi.set_PWM_dutycycle(self.enable_pin, 0)
        print('terminated signals from pins ', self.in1_pin, self.in2_pin, self.enable_pin)

    '''
    def __del__(self):
        self.pi.write(self.in1_pin, 0)
        self.pi.write(self.in2_pin, 0)
        self.pi.set_PWM_dutycycle(self.enable_pin, 0)
        print('terminated signals from pins ', self.in1_pin, self.in2_pin, self.enable_pin)
    '''

if __name__ == "__main__":
    try:
        pi = gpio.pi()
        FREQUENCY = 1000#Hz
        #in1, in2, enable, frequency
        left = Motor(pi, 23, 24, 25, FREQUENCY, 'left')
        right = Motor(pi, 27, 22, 17, FREQUENCY, 'right')

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
                    pi.stop()
                    break
    finally:
        left.close()
        right.close()
