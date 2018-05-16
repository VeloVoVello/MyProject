#!/usr/bin/env python

from netmiko import Netmiko
import time
from getpass import getpass

# Manual IP list creation
"""
devices = '''
10.81.8.65
'''.strip().splitlines()
"""

# IP list generator
def get_credentials():
    username = input('Enter LDAP login: ')
    password = None
    while not password:
        password = getpass('Enter LDAP password: ')
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match')


def ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    devices = []

    devices.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        devices.append(".".join(map(str, temp)))

    return devices

print('Запущен скрипт для выполнения команд на сетевом оборудовании')
time.sleep(1)

start_ip = input('Enter first device IP: ')
end_ip = input('Enter last device IP: ')
ldap = input(': ')
ldap = getpass.getpass()
ldappasswd = input('Введите LDAP пароль: ')

devices = ipRange(start_ip, end_ip)

#username = raw_input("Username? ")
#password = getpass.getpass()

for device in devices:

    try:
        net_connect = Netmiko(ip=device, device_type='hp_procurve',
                              username=ldap, password=ldappasswd)
        print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
        print(net_connect.send_command('display version | inc Processor'))
        print("Authenticated with LDAP\n")
        #print(">>>>>>>>> End <<<<<<<<<\n")
        net_connect.disconnect()
    except:
        #print('Authentication with LDAP failed.')
        try:
            net_connect = Netmiko(ip=device, device_type='hp_procurve',
                                  username='supervisor', password='password')
            print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
            print(net_connect.send_command('display version | inc Processor'))
            print("Authenticated with supervisor\n")
            #print(">>>>>>>>> End <<<<<<<<<\n")
            net_connect.disconnect()
        except:
            #print('Authentication with supervisor failed.')
            try:
                net_connect = Netmiko(ip=device, device_type='hp_procurve',
                                      username='supervisor@system', password='password')
                print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
                print(net_connect.send_command('display version | inc Processor'))
                print("Authenticated with supervisor@system\n")
                #print(">>>>>>>>> End <<<<<<<<<\n")
                net_connect.disconnect()
            except:
                #print("Unable to connect with supervisor@system!")
                print("Unable to connect device {}\n".format(device))
                continue

#command = ssh.send_config_from_file('config.txt')

