'''Works ONLY in *nix'''

from subprocess import Popen, DEVNULL

dict = {}
list = []

for n in range(65, 94):
    ip = "10.81.4.%d" % n
    dict[ip] = Popen(['ping', '-n', '-w5', '-c3', ip], stdout=DEVNULL)

while dict:
    for ip, proc in dict.items():
        if proc.poll() is not None:
            del dict[ip]
            if proc.returncode == 0:
                list.append(ip)
            break


print('\n' + str(len(list)) + ' active devices:\n')
list = sorted(list)

for i in list:
    print(i)
print('\n')
