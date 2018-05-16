from netmiko import ConnectHandler

# Read in the file
with open('Aruba.txt', 'r', encoding = 'utf-8') as file:
    filedata = file.read()

# Replace data in the file
for r in (('20.68', '100.67'), ('MAG005_68', 'MAG025_67')):
    filedata = filedata.replace(*r)

# Write the file out again
with open('updated.txt', 'w') as file:
    file.write(filedata)

aruba = {
'device_type': 'hp_procurve',
'ip': '10.81.4.67',
'username': '60052959',
'password': 'hGf!64235*'
}

ssh = ConnectHandler(**aruba)