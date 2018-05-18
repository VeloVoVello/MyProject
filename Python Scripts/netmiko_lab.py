#!/usr/bin/python3

from netmiko import Netmiko
import time
import getpass

def get_credentials():
    username = input('Username: ')
    password = None
    while not password:
        password = getpass.getpass(prompt='Password: ')
        password_verify = getpass.getpass(prompt='Retype your password: ')
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
time.sleep(2)
print('The program executes commands via SSH connection')
print('Authentification priority order: '
      'LDAP(Radius), then Local(master password)')
time.sleep(2)

# Get user Credentials (LDAP)

print('Enter your LDAP credentials')
ldapuser, ldappasswd = get_credentials()

# Set the device pool, create deice list

start_ip = input('Enter the first device IP: ')
end_ip = input('Enter the last device IP: ')
devices = ipRange(start_ip, end_ip)

# Get the command to perform

cmd = input('Enter the command you want to perform: ')
print('\nConnecting...\n')

# The CORE of the program

for device in devices:
    try:
        print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
        net_connect = Netmiko(ip=device, device_type='hp_procurve',
                              username=ldapuser, password=ldappasswd)
        print("\nAuthenticated with LDAP credentials\n")
        print(net_connect.send_command(cmd))
        print("\n>>>>>>>>> End <<<<<<<<<\n")
        net_connect.disconnect()
    except:
        print('LDAP authentication failed')

        try:
            if localuser not in locals():
                localuser, localpasswd = get_credentials()
                net_connect = Netmiko(ip=device, device_type='hp_procurve',
                                      username='localuser', password='localpasswd')
                print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
                print("Authenticated with local credentials")
                print(net_connect.send_command(cmd))
                print(">>>>>>>>> End <<<<<<<<<\n")
                net_connect.disconnect()
            else:
                print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
                print("Authenticated with local credentials")
                print(net_connect.send_command(cmd))
                print(">>>>>>>>> End <<<<<<<<<\n")
                net_connect.disconnect()
        except:
            print('>>>>>>>>> Device {0} <<<<<<<<<'.format(device))
            print('Local authentication failed')
            print(">>>>>>>>> End <<<<<<<<<\n")
            continue

#command = ssh.send_config_from_file('config.txt')

