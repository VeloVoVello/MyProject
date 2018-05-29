import time
import ipaddress
from netmiko import Netmiko
from subprocess import Popen, DEVNULL

# ----------------------------- Main menu func -----------------------------

def menu():

    action = int(input('''
Выберите действие:\n
0. Выход
1. Проверка доступности устройств (Ping)
2. Выполнение команды на устройствах (SSH)\n
'''))

    if action == 0:
        quit()
    elif action == 1:
        ping()
    elif action == 2:
        execute()
    else:
        menu()

# ----------------------------- MGMT 121 VLAN func -----------------------------

def vlan():

    mag = int(input('\nВведите номер магазина: '))

    if mag <= 63:
        x = '10.81.{}.64/27'.format(str(mag * 4))
    elif mag > 63 and mag <= 126:
        x = '10.82.{}.64/27'.format(str((mag - 63) * 4))
    elif mag > 126 and mag <= 189:
        x = '10.86.{}.64/27'.format(str((mag - 126) * 4))
    elif mag > 189 and mag <= 252:
        x = '10.86.{}.64/27'.format(str((mag - 189) * 4))

    net = ipaddress.ip_network(x)
    devices = [x.compressed for x in net.hosts()]

    return devices

# ----------------------------- Ping func -----------------------------

def ping():

  #  while True:

    p = {}
    alive = []
    devices = []
    devices = vlan()
    for i in devices:
        p[i] = Popen(['ping', '-n', '-w5', '-c3', i], stdout=DEVNULL)

    while p:
        for ip, proc in p.items():
            if proc.poll() is not None:
                del p[ip]
                if proc.returncode == 0:
                    alive.append(ip)
                break

    print('\n' + str(len(alive)) + ' active devices:\n')
    alive = sorted(alive)

    for i in alive:
        print(i)

    return alive
'''
    again = input("Вы хотите продолжить? Введите y/n: ")
    again = again.lower()

    if again == "yes" or again == "y":
        ping()
    else:
        menu()
'''
# ----------------------------- Execute func -----------------------------

def execute():

    action = int(input('''
    0. Обратно в Главное меню
    1. Указать подсеть 
    2. Указать номер магазина \n
    '''))

    if action == 0:
        menu()
    elif action == 1:
        print('Функция находится в разработке')
    elif action == 2:
        devices = ping()
    else:
        menu()

    ldapuser = input('\nВведите имя пользователя LDAP: ')
    ldappasswd = input('Введите пароль LDAP: ')
    localpasswd = None
    cmd = input('Введите команду: ')

    for device in devices:
        try:
            print('\n>>>>>>>>> Device {} <<<<<<<<<'.format(device))
            net_connect = Netmiko(ip=device,
                                  device_type='hp_procurve',
                                  username=ldapuser,
                                  password=ldappasswd)
            print(net_connect.send_command(cmd))
            net_connect.disconnect()
        except:
            try:
                if localpasswd is None:
                    localpasswd = input('\nАутентификация через Radius'
                                        ' не поддерживается на устройстве!\n'
                                        'Dведите пароль'
                                        ' локального администратора: ')
                    net_connect = Netmiko(ip=device,
                                          device_type='hp_procurve',
                                          username='supervisor@system',
                                          password=localpasswd)
                    print(net_connect.send_command(cmd))
                    net_connect.disconnect()
                else:
                    net_connect = Netmiko(ip=device,
                                          device_type='hp_procurve',
                                          username='supervisor@system',
                                          password=localpasswd)
                    print(net_connect.send_command(cmd))
                    net_connect.disconnect()
                    continue
            except:
                print('Доступ на устройство {} не возможен, '
                      'следующее устройство...'.format(device))

menu()