import pigpio as pig

class pwmServo():
    def __init__(self, pi, pin, freq):
        self.pin = pin
        self.pi = pi
        self.freq = freq
        self.pi.set_mode(self.pin, pig.OUTPUT)

    def specTurn(self, angle):
        pulse_wid = (1000/90) * angle + 500 #using points (0 deg, 500 us), (180 deg, 2500 us), derived: pulse width = (1000us/90deg)*angle+500us, us=microseconds
        if pulse_wid <= 1420:
            pulse_wid = 1420
            print('outside range of allowed angles, pulse width set to lower bound 1420 microseconds')
        elif pulse_wid >= 1750:
            pulse_wid = 1750
            print('outside range of allowed angles, pulse width set to upper bound 1750 microseconds')

        duty = (pulse_wid/10**6) * self.freq #pulse width is in us, frequency is cyc/s
        print('\tpulse width', pulse_wid)

        #scale to pigpio's range of 0 to 1 million, pigpio only takes ints
        duty = int(duty * 10**6)
        print('rounded duty for pigpio =', duty)
        self.pi.hardware_PWM(self.pin, self.freq, duty)

if __name__ == '__main__':
    pi = pig.pi()
    pin = int(input('Enter the RPi pin number the servo is connected to according to Broadcom\'s numbering.\t'))
    frequency = 50
    tilt = pwmServo(pi, pin, frequency)
    for it in range(100):
        try:
            angle = float(input('Enter the  you would like the servo horn to turn to in degrees. Range: 0 to 180, 90 = neutral.\t'))
            tilt.specTurn(angle)
        except:
            pi.stop()
            raise
            print('PWM signal terminated')
            break

