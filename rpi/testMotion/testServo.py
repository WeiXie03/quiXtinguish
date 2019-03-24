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
        print(self.pi.get_PWM_range(self.pin))
        self.pi.set_PWM_range(self.pin, 40000)
        self.pwm_range = self.pi.get_PWM_range(self.pin)
        self.close()

    def calc_pulsewidth(self, angle):
        pulse_wid = (1000/90) * angle #using points (0 deg, 500 us), (180 deg, 2500 us), derived: pulse width = (1000us/90deg)*angle+500us, us=microseconds
        #for tilt, no 500us offset
        if pulse_wid <= self.min_bound:
            pulse_wid = self.min_bound
            print('outside range of allowed angles, pulse width set to lower bound {} microseconds'.format(self.min_bound))
        elif pulse_wid >= self.max_bound:
            pulse_wid = self.max_bound
            print('outside range of allowed angles, pulse width set to upper bound {} microseconds'.format(self.max_bound))

        print('\tpulse width', pulse_wid)
        return pulse_wid

    def calc_duty(self, angle):
        pulse_wid = (1000/90)*angle #using points (0 deg, 500 us), (180 deg, 2500 us), derived: pulse width = (1000us/90deg)*angle+500us, us=microseconds
        if pulse_wid <= self.min_bound:
            pulse_wid = self.min_bound
            print('outside range of allowed angles, pulse width set to lower bound {} microseconds'.format(self.min_bound))
        elif pulse_wid >= self.max_bound:
            pulse_wid = self.max_bound
            print('outside range of allowed angles, pulse width set to upper bound {} microseconds'.format(self.max_bound))

        print('\tpulse width', pulse_wid)
        duty = (pulse_wid/10**6) * self.freq #pulse width is in us, frequency is cyc/s
        return duty

    def specTurn(self, duty):
        #scale to pigpio pwm range set, pigpio only takes ints
        print(duty)
        duty = int(duty * self.pwm_range)
        print('rounded duty for pigpio =', duty, 'range is ', self.pwm_range)
        self.pi.set_PWM_dutycycle(self.pin, duty) #set default range to 10000

    def turnPulseWidth(self, pulse_width):
        pulse_width = min(int(pulse_width), 2500)
        if not pulse_width == 0:
            pulse_width = max(int(pulse_width), 500)
        print(pulse_width)
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)

    def turn(self, angle):
        self.turnPulseWidth(self.calc_pulsewidth(angle))

    def close(self):
        print("pulse width set to OFF")
        self.pi.set_servo_pulsewidth(self.pin, 0)

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
    print(pi)
    pin = int(input('Enter the RPi pin number the servo is connected to according to Broadcom\'s numbering.\t'))
    frequency = 50
    tilt = Servo(pi, pin, frequency, min_bound=500, max_bound=2500)
    tilt.close()
    try:
        for it in range(100):
            try:
                angle = float(input('Enter the  you would like the servo horn to turn to in degrees. Range: 0 to 180, 90 = neutral.\t'))
                tilt.turn(angle)
            except:
                raise
                print('PWM signal terminated')
                break
    finally:
        print('ending')
        tilt.close()
        pi.stop()
