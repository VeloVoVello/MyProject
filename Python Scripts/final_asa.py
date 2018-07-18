import getpass
from netmiko import Netmiko
from subprocess import Popen, DEVNULL, PIPE

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
        sub_menu_3()
    elif action == 2:
        command()
        sub_menu_2()
    else:
        menu()

# ----------------------------- Sub menu 1 Ping func -----------------------------

def sub_menu_1():

    action = int(input('''
    0. Обратно в Главное меню
    1. Выполнить ICMP запрос\n
    '''))

    if action == 0:
        menu()
    elif action == 1:
        devices = ping()
    else:
        menu()

# ----------------------------- Sub menu 2 SSH func -----------------------------

def sub_menu_2():

    action = int(input('''
    0. Обратно в Главное меню
    1. Выполнить команду\n
    '''))

    if action == 0:
        menu()
    elif action == 1:
        devices = command()
    else:
        menu()

# ----------------------------- Sub menu 3 continue func -----------------------------

def sub_menu_3():

    action = input("\nВы хотите продолжить? Введите y/n: ")
    action = action.lower()

    if action == "yes" or action == "y":
        ping()
    else:
        menu()

# ----------------------------- Getpass func -----------------------------

def get_credentials():

    username = input('Введите имя пользователя LDAP: ')
    password = None
    while not password:
        password = getpass.getpass(prompt='Введите пароль LDAP: ')
        password_verify = getpass.getpass(prompt='Введите пароль еще раз: ')
        if password != password_verify:
            print('Пароли не совпадают, попробуйте еще раз: ')
            password = None

    return username, password

# ----------------------------- MGMT 121 VLAN func -----------------------------

def vlan():

    asa = []

    x = [i for i in range(1, 255) if i % 4 == 0]

    for i in x:
        asa.append('10.81.' + str(i) + '.86')
    for i in x:
        asa.append('10.82.' + str(i) + '.86')

    return asa

  # ----------------------------- Ping func -----------------------------

def ping():

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

    for i in alive:
        print(i)

    return alive

# ----------------------------- Command func -----------------------------

def command():

#    ldapuser = input('\nВведите имя пользователя LDAP: ')
#    ldappasswd = input('Введите пароль LDAP: ')

    ldapuser, ldappasswd = get_credentials()
    cmd = input('|Введите команду: ')
'''
    commands = ['configure terminal',
                'snmp-server host management 10.80.32.11 community 73oFVQR6H5Qt2JuV version 2c',
                'show run | inc 10.80.32.11'
                'exit'
                'write mem']
'''
    devices = ping()



    for device in devices:

        try:
            print('\n>>>>>>>>> Device {} <<<<<<<<<'.format(device))
            net_connect = Netmiko(ip=device,
                                  device_type='cisco_ios',
                                  username=ldapuser,
                                  password=ldappasswd)
            net_connect.enable()
#            print(net_connect.send_config_set(commands))
            print(net_connect.send_command(cmd))
            net_connect.disconnect()
        except:
            print('Доступ на устройство {} не возможен, '
                  'следующее устройство...'.format(device))



menu()