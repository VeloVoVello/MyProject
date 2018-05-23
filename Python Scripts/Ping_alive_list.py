from subprocess import Popen, PIPE, DEVNULL
import ipaddress

alive = []
p = {} # ip -> process
subnet = ipaddress.ip_network('10.81.172.64/27', strict=False)
for i in subnet.hosts():
    i = str(i)
    hostup = Popen(["ping", "-c1", i], stdout=DEVNULL)
    output = hostup.communicate()[0]
    retval = hostup.returncode
    if retval == 0:
        alive.append(i)
        print(i, "is pinging")
    else:
        print(i, "is not responding")