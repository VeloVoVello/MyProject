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


# sample usage
devices = ipRange("192.168.1.0", "192.171.3.25")
for ip in devices:
    print(ip)