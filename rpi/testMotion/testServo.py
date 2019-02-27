import pigpio as pig

<<<<<<< HEAD
class pwmServo():
    def __init__(self, pi, pin, freq, lBound=1420, uBound=1750):
=======
class Servo():
    def __init__(self, pi, pin, freq, min_bound=1000, max_bound=2000):
>>>>>>> b9c4d2962bc93cb15cde6defcf3bf017f82d1c47
        self.pin = pin
        self.pi = pi
        self.freq = freq
        #set range of pulse widths
        self.lBound = lBound
        self.uBound = uBound

        self.cur_angle = 90
        self.pi.set_mode(self.pin, pig.OUTPUT)
        self.pi.set_PWM_frequency(self.pin, freq)
        self.pwm_range = 40000
        self.pi.set_PWM_range(self.pin, self.pwm_range) #set default range to 10000

    def calc_duty(self, angle):
        pulse_wid = (1000/90) * angle + 500 #using points (0 deg, 500 us), (180 deg, 2500 us), derived: pulse width = (1000us/90deg)*angle+500us, us=microseconds
<<<<<<< HEAD
        if pulse_wid <= self.lBound:
            pulse_wid = self.lBound
            #print('outside range of allowed angles, pulse width set to lower bound {} microseconds'.format(lBound))
        elif pulse_wid >= self.uBound:
            pulse_wid = self.uBound
            #print('outside range of allowed angles, pulse width set to upper bound {} microseconds'.format(uBound))

        duty = (pulse_wid/10**6) * self.freq #pulse width is in us, frequency is cyc/s
        #print('\tpulse width', pulse_wid)

        #scale to pigpio's range of 0 to 1 million, pigpio only takes ints
        duty = int(duty * 10**6)
        #print('rounded duty for pigpio =', duty)
        self.pi.hardware_PWM(self.pin, self.freq, duty)
        self.cur_angle = angle
=======
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
    def __init__(self, pi, pin, freq, min_bound=1000, max_bound=2000)
        super().__init__(self, pi, pin, freq, min_bound=1000, max_bound=2000)
    def specTurn(self, duty):
        #scale to pigpio pwm range set, pigpio only takes ints
        duty = int(duty * self.pwm_range)
        #print('rounded duty for pigpio =', duty)
        self.pi.hardware_PWM(self.pin, self.freq, duty) #set default range to 10000
>>>>>>> b9c4d2962bc93cb15cde6defcf3bf017f82d1c47

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

