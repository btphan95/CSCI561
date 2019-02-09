#CSCI 561 HW3
#Created by Binh Phan

import numpy as np
import time
import os

start = time.clock()

num0 = '2'
num1 = '5'
input_name = 'simulationMoves' + num0 + '_' + num1 + '.txt'
f = open(input_name, 'r')
lines = f.read().splitlines()
# # print lines

for x in range(len(lines)):
	if lines[x] == '(-1, 0)':
		lines[x] = 'left'
	if lines[x] == '(0, 1)':
		lines[x] = 'down'
	if lines[x] == '(0, -1)':
		lines[x] = 'up'
	if lines[x] == '(1, 0)':
		lines[x] = 'right'

output_name = 'simulationMovesX' + num0 + '_' + num1 + '.txt'
print output_name
print os.linesep
output = open(output_name,'w')
for line in lines:
	print line
	output.write(line + '\n')
f.close()
output.close()

print "Time Elapsed: ", str(time.clock() - start) + 's'