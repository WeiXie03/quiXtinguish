import socket

HOST = input('Enter IP address of RPi. ')
PORT = 3027

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(HOST, PORT)
    sock.listen(5)
    conn, addr = sock.accept()
    with conn:
        print('Connected at ', addr)
        while True:
            print('tilt servo')
            tilt = input('Enter angle you\'d like to turn to in degrees. ')
            print('pan servo')
            tilt = input('Enter angle you\'d like to turn to in degrees. ')

            print('left motor')
            left = input('Enter percentage of maximum speed you want motors to spin at. ')
            print('right motor')
            left = input('Enter percentage of maximum speed you want motors to spin at. ')
