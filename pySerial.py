import serial
import sys
import time
import credentials

console = serial.Serial(
        port='COM6',
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=1
    )

f = open('Command_set_1.txt', 'r')
input = f.read()

if console.isOpen():

    print(console.name + ' is open')
    time.sleep(1)
    print('Configuration begins...')

    console.write('\r\n\r\n'.encode())
    time.sleep(3)
    msg = console.read(console.inWaiting()).decode()
    if "Username" in msg:
        console.write(credentials.username.encode() + '\n'.encode())
        msg = console.read(console.inWaiting()).decode()
        time.sleep(1)

    if "Password" in msg:
        console.write(credentials.password.encode() + '\n'.encode())
        time.sleep(1)

        # Запись конфигурации из файла

    console.write(input.encode())

    """
    console.write('configure terminal'.encode() + '\n'.encode())
    console.write('vlan 151'.encode() + '\n'.encode())
    console.write('write memory'.encode() + '\n'.encode())
    input_data = console.read(console.inWaiting()).decode()
    """

else:

    print('Serial port is closed')

console.close()
f.close()

print('Finished')


