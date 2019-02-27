import pigpio as pig

class Servo():
    def __init__(self, pi, pin, freq, min_bound=1000, max_bound=2000):
        self.pin = pin
        self.pi = pi
        self.freq = freq
        #set range of pulse widths
        self.min_bound = min_bound
        self.max_bound = max_bound

        self.cur_angle = 90
        self.pi.set_mode(self.pin, pig.OUTPUT)
        self.pi.set_PWM_frequency(self.pin, freq)
        self.pwm_range = 40000
        self.pi.set_PWM_range(self.pin, self.pwm_range) #set default range to 10000

    def calc_duty(self, angle):
        pulse_wid = (1000/90) * angle + 500 #using points (0 deg, 500 us), (180 deg, 2500 us), derived: pulse width = (1000us/90deg)*angle+500us, us=microseconds
        if pulse_wid <= min_bound:
            pulse_wid = min_bound
            print('outside range of allowed angles, pulse width set to lower bound {} microseconds').format(min_bound)
        elif pulse_wid >= max_bound:
            pulse_wid = max_bound
            print('outside range of allowed angles, pulse width set to upper bound {} microseconds').format(max_bound)

        print('\tpulse width', pulse_wid)
        duty = (pulse_wid/10**6) * self.freq #pulse width is in us, frequency is cyc/s
        return duty

    def specTurn(self, duty):
        #scale to pigpio pwm range set, pigpio only takes ints
        duty = int(duty * self.pwm_range)
        #print('rounded duty for pigpio =', duty)
        self.pi.set_PWM_dutycycle(self.pin, self.duty) #set default range to 10000

class hwServo(Servo):
    def __init__(self, pi, pin, freq, min_bound=1000, max_bound=2000):
        super().__init__(pi, pin, freq, min_bound, max_bound)
    def specTurn(self, duty):
        #scale to pigpio pwm range set, pigpio only takes ints
        duty = int(duty * self.pwm_range)
        #print('rounded duty for pigpio =', duty)
        self.pi.hardware_PWM(self.pin, self.freq, duty) #set default range to 10000

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

