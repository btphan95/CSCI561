#CSCI 561 HW3
#Created by Binh Phan

import numpy as np
import time
import os
import re

start = time.clock()

num = '1'
input_name = 'policy' + num + '.txt'
input = open(input_name, 'r')
lines = input.read().splitlines()
# # print lines

c = 5
m = 10
print 'length ', len(lines)
print 'lines end', lines[499]

for x in range(len(lines)):
	list_line = list(lines[x])
	f = lines[x][1]
	print 'f ', f

	g = lines[x][4]
	print 'g ', g
	list_line[1] = g
	list_line[4] = f
	lines[x] = "".join(list_line)
	lines[x] = re.sub(r': \(0, -1\)', ': up', lines[x])
	lines[x] = re.sub(r': \(0, 1\)', ': down', lines[x])
	lines[x] = re.sub(r': \(-1, 0\)', ': left', lines[x])
	lines[x] = re.sub(r': \(1, 0\)', ': right', lines[x])

for x in range(c):
	lines_sorted = lines[x*m*m:((x+1)*m*m)]
	print 'lines_sorted[0]', lines_sorted[0]
	print len(lines_sorted)
	lines_sorted.sort()
	lines_sorted[0] = 'CAR ' + str(x) + ':\n' + lines_sorted[0]
	lines[x*m*m:((x+1)*m*m)-1] = lines_sorted


output_name = 'policiesX' + num + '.txt'
print output_name
print os.linesep
output = open(output_name,'w')
for line in lines:
	output.write(line + '\n')
input.close()
output.close()

print "Time Elapsed: ", str(time.clock() - start) + 's'