import serial
import sys
import time
import credentials

def ser():
    print('Initializing serial connection')
    console = serial.Serial(
        port='COM6',
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=1
    )
    if not console.isOpen():
        sys.exit()

    f = open('Log.txt', 'a')

    while True:
        f.write(console.read(console.inWaiting()).decode())
        f.close()
        f = open('dataFile.txt', 'a')

    console.write('\r\n\r\n'.encode())
    time.sleep(3)
    msg = console.read(console.inWaiting())
    console.write('\r\n\r\n'.encode())
    time.sleep(1)
    msg = console.read(console.inWaiting())

    console.write()

"""
    console.write('exit'.encode() + '\n'.encode())
    console.write('exit'.encode() + '\n'.encode())
    console.write('y'.encode() + '\n'.encode())
    console.write('y'.encode() + '\n'.encode())
    msg = console.read(console.inWaiting())

    console.write('vlan 121'.encode() + '\n'.encode())
    console.write('name MGMT'.encode() + '\n'.encode())
    console.write('ip address 10.81.88.74 0.0.0.0'.encode() + '\n'.encode())
    console.write('write memory'.encode() + '\n'.encode())
    print(msg)
   # print('finished')
#console.close()

if __name__ == "main":
    main()