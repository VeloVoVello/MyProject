#!/usr/bin/env python

from netmiko import Netmiko
import time
from getpass import getpass

def get_credentials():
    username = input('Enter LDAP login: ')
    password = None
    while not password:
        password = getpass('Enter LDAP password: ')
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match. Try again.')
            password = None
    return username, password

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

# Welcome to the program

print('Welcome to the Network Device Configurator')
time.sleep(1)
print('The program pick up your LDAP credentials,\n'
      'SSH devices from the pool and execute command set')
time.sleep(1)
print('Authentification is performed in such priority: '
      'LDAP(Radius) then Local(master password)')

# Get user Credentials (LDAP)
ldapuser, ldappasswd = get_credentials()

# Set the device pool, create deice list
start_ip = input('Enter the first device IP: ')
end_ip = input('Enter the last device IP: ')
devices = ipRange(start_ip, end_ip)

# The CORE of the program
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

