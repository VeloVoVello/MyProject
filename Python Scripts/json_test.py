import netmiko
import json

with open('devices.json') as dev_file:
    devices = json.load(dev_file)

username = input('Username: ')
password = input('Password: ')
cmd = input('Enter the command you want to perform: ')

for device in devices:
    device = [username] = username
    device = [password] = password
    try:
        print('~'*79)
        print('Connecting to device ', device['ip'])
        net_connect = Netmiko(**device)
        print(net_connect.send_command(cmd))
        net_connect.disconnect()
    except:
        print('Failed to ', device['ip'])
