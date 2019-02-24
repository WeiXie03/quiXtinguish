import pigpio as pig
import math

class pwmServo():
    def __init__(self, pi, pin, freq):
        self.pin = pin
        self.freq = freq
        self.pi = pi
        self.pi.set_mode(self.pin, pig.OUTPUT)

    def specTurn(self, time):
        if time <= 1420:
            time = 1420
        elif time >= 1700:
            time = 1700
        duty = time/(10.0**6.0) * self.freq * self.pi.get_PWM_range(self.pin) #(12/180.0)*angle + 3
        print('duty', duty)
        duty = math.floor(duty)
        print('duty rounded to', int(duty))
        self.pi.hardware_PWM(self.pin, self.freq, int(duty))
        print('pulse width=', time)

if __name__ == '__main__':
    frequency = 50
    pi = pig.pi()
    pwmPin = int(input('What is the Broadcom pin number of your PWM signal pin? '))
    tilt = pwmServo(pi, pwmPin, frequency)
    for it in range(100):
        try:
            time = float(input('Enter pulse width of signal in microseconds. Range: 3(dead signal) or 500 to 2500, 1000=neutral.\t'))
            #if angle <= 175 and angle >= 0:
            tilt.specTurn(time)
            '''
            else:
                print('angle not in range')
            '''
        except KeyboardInterrupt:
            print('PWM signal terminated')
            break

    pi.write(tilt.pin, 0)
