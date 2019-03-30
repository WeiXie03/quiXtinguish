import testServo as serv
import pigpio
from time import sleep

pi = pigpio.pi()
pin = 23
print(pi, 'created, using pin', pin, 'for panning')
frequency = 100
print('frequency =', frequency, 'Hz')

pan = serv.Servo(pi, pin, frequency, 670, 1380)
cur = 135

for deg in range(65*2):
    cur -= 0.5
    pan.turn(cur)
    sleep(0.3)
