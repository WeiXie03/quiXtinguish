import socket

HOST = input('IP address of RPi: ')
PORT = 3027

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    # will keep accepting connections until 5 bad attempts
    sock.listen(5)
    conn, addr = sock.accept()
    with conn:
        print('Connected at ', addr)
        while True:
            #get angles for servos to turn to
            print('tilt servo')
            tilt = input('tilt angle(deg): ')
            print('\npan servo')
            pan = input('pan angle(deg): ')

            #get direction and speed for both motors
            print('\nleft motor')
            leftDir = input('(f)orward or (b)ackwards: ')
            leftSpeed = input('percentage of maximum speed of motors: ')
            print('\nright motor')
            rightDir = input('(f)orward or (b)ackwards: ')
            rightSpeed = input('percentage of maximum speed of motors: ')

            sendString = '{0}, {1}, {2}, {3}, {4}, {5}'.format(tilt, pan, leftDir, leftSpeed, rightDir, rightSpeed)
            conn.sendall(sendString.encode())
            print('sent ' + sendString)
