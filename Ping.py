import os
import multiprocessing
import subprocess

devices = ['8.8.8.8', '4.4.4.4']

DNULL = open(os.devnull, 'w')

def ping(host,mp_queue):
    response = subprocess.call(["ping", "-c", "2", host], stdout=DNULL)
    if response == 0:
        print(host, 'is up!')
        result = True
    else:
        print(host, 'is down!')
        result = False
    dostupnost = {host:result}
    mp_queue.put(dostupnost)

def worker(devices):
    mp_queue = multiprocessing.Queue()
    processes = []
    for device in devices:
        p = multiprocessing.Process(target=ping, args=(device, mp_queue))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    results = []
    for p in processes:
        results.append(mp_queue.get())
    return results

worker(devices)