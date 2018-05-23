#!/usr/bin/env python3

from subprocess import Popen, DEVNULL

p = {} # ip -> process
for n in range(201, 206): # start ping processes
    ip = "81.200.248.%d" % n
    p[ip] = Popen(['ping', '-n', '-w5', '-c3', ip], stdout=DEVNULL)
    #NOTE: you could set stderr=subprocess.STDOUT to ignore stderr also

while p:
    for ip, proc in p.items():
        if proc.poll() is not None: # ping finished
            del p[ip] # remove from the process list
            if proc.returncode == 0:
                print('%s active' % ip)
            elif proc.returncode == 1:
                print('%s no response' % ip)
            else:
                print('%s error' % ip)
            break