'''Works ONLY in *nix'''

import ipaddress
from subprocess import Popen, DEVNULL

p = {}
net = ipaddress.ip_network('10.81.172.64/27')
hosts = [x.compressed for x in net.hosts()]
alive = []

for i in hosts:
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
print('\n')
