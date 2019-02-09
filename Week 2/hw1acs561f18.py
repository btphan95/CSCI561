#CSCI 561 HW1a
#Created by Binh Phan

f = open('input.txt', 'r')
lines = f.read().splitlines()
print lines
output = open('output.txt','w')

for i in range(len(lines)):
  location, status = lines[i].split(',')
  if status == 'Dirty':
    output.write('Suck')
  elif location == 'A':
    output.write('Right')
  elif location == 'B':
    output.write('Left')
  if i != (len(lines)) - 1:
    output.write('\n')
f.close()
output.close()