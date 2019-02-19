import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)

#using the pin corresponding(same number on L293D datasheet) to the pin connected to positive terminal on motor as in 1
in1_pin = 18
in2_pin = 16
#enable_pin = 33

gpio.setup(in1_pin, gpio.OUT)
gpio.setup(in2_pin, gpio.OUT)
#gpio.setup(enable_pin, gpio.OUT)
print('pins set up')

def clockwise():
    gpio.output(in1_pin, gpio.HIGH)
    gpio.output(in2_pin, gpio.LOW)

def counterclockwise():
    #reverse direction = reverse pins
    gpio.output(in1_pin, gpio.LOW)
    gpio.output(in2_pin, gpio.HIGH)

gpio.output(in1_pin, True)
gpio.output(in2_pin, True)

while True:
    try:
        direction = input("Which way?[f/b]: ")
        '''
        speed = int(input("How fast(duty cycle)? "))
        speed = speed*11
        #set speed using PWM to enable of L293D
        gpio.output(enable_pin, True)
        enable_pin.ChangeDutyCycle(speed)
        print('speed ', speed)
        '''

        if direction == 'f':
            clockwise()
        else:
            counterclockwise()
    except Exception:
        raise
        print('no')
        gpio.output(in1_pin, False)
        gpio.output(in2_pin, False)
        break

gpio.cleanup()
