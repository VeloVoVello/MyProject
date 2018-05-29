'''Works ONLY in Windows'''

import ipaddress
from subprocess import Popen, PIPE

count = 1

while count <= 10:

    mag = int(input('Введите номер магазина: '))

    if mag <= 63:
        x = '10.81.{}.64/27'.format(str(mag * 4))
    elif mag > 63 and mag <= 126:
        x = '10.82.{}.64/27'.format(str((mag - 63) * 4))
    elif mag > 126 and mag <= 189:
        x = '10.86.{}.64/27'.format(str((mag - 126) * 4))
    elif mag > 189 and mag <= 252:
        x = '10.86.{}.64/27'.format(str((mag - 189) * 4))

    p = {}

    net = ipaddress.ip_network(x)
    hosts = [x.compressed for x in net.hosts()]
    alive = []

    for i in hosts:
        p[i] = Popen('ping ' + i + ' -n 1', stdout=PIPE)

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
    print('\n')

    count += 1