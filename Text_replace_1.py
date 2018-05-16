# Read in the file
with open('Aruba_Full.txt', 'r', encoding='utf-8') as file:
    filedata = file.read()

# Replace data in the file
for r in (('XX.YY', '48.70'), ('MAG000_00', 'MAG012_70'), ('000', '012')):
    filedata = filedata.replace(*r)

# Write the file out again
with open('updated.txt', 'w') as file:
    file.write(filedata)