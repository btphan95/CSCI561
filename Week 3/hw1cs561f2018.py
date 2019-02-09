#CSCI 561 HW1b
#Created by Binh Phan

import numpy as np
import copy
import random
import time

start = time.clock()
f = open('input.txt', 'r')
lines = f.read().splitlines()
print lines
n = int(lines[0]) #city area
p = int(lines[1]) #number of police officers
s = (lines[2]) # number of scooters
board = np.eye(n) * 0
print('number of police officers: ',p)
print('number of scooters: ',s)

for x in range(3,len(lines)): #populating the board with all of the scooter traversals
	i,j = (lines[x].split(','))
	i,j = int(i), int(j)
	board[i][j] += 1
print(board)
# board_sol = np.eye(n) * 0
# board_sol[0][1] = 1
# board_sol[3][2] = 1
# board_sol[4][0] = 1
# print 'solution ', board_sol
# print 'score: ', np.sum(np.multiply(board_sol, board))

#HILL-CLIMBING SEARCH ALGORITHM

max_activity = 0
for i in range(10000):
	# print(i)
	# Random Restart: set coordinates of officers randomly, one in a different column
	columns = []
	p_locations = []
	while len(p_locations) != p:
		column = np.random.randint(n)
		if column not in columns:
			p_locations.append([np.random.randint(n), column])
			columns.append(column)
	# print(p_locations)

	board_p = np.eye(n) * 0
	for x in range(p):  # populating the board with police officers
		y, z = p_locations[x][0], p_locations[x][1]
		board_p[y][z] += 1
	# print('board police: ')
	# print(board_p)


	# determine h, the number of queen-pair collisions
	def collide(p, q):
		collide = False
		if (p[0] == q[0]) | (p[1] == q[1]):  # if rows/columns are the same
			collide = True
		# print('Collision found')
		elif np.abs(p[0] - q[0]) == np.abs(p[1] - q[1]):
			collide = True
		# print('Collision found')
		return collide


	def compute_h(p):
		h = 0
		for i in range(len(p)):
			for j in range(i + 1, len(p)):
				# print'Computing collision for ',p_locations[i],p_locations[j], ': ', collide(p_locations[i], p_locations[j])
				if collide(p[i], p[j]):
					h += 1
		# print('number of collisions: ', h)
		return h


	# print 'number of collisions: ', compute_h(p_locations)

	# finding all successors of the current state

	minimum = 3000

	while(1):
		successors = []
		p_candidates = [x for x in p_locations]
		# print 'starting p locations ', p_locations
		# print 'p candidates ', p_candidates
		for k in range(p):
			tmp = p_candidates[k][0]
			for j in range(n):
				p_candidates[k][0] = j
				# print(p_candidates)
				# board_p = np.eye(n) * 0
				# for x in range(p):  # populating the board with police officers
				# 	y, z = p_candidates[x][0], p_candidates[x][1]
				# 	board_p[y][z] += 1
				# print(board_p)
				# print 'number of collisions: ', compute_h(p_candidates)
				successors.append([p_candidates[k][:], compute_h(p_candidates)]) #need the [:] here because we need to create a copy of the list!
			p_candidates[k][0] = tmp

		#find the set of min h candidates
		# print 'successors ', successors
		min_h = min(x[1] for x in successors)
		# print 'min ', min_h



		if min_h == minimum:  # if hill-climbing does not improve, find scores of all minimum h candidates and end search
			# print 'hill-climbing local minimum found'
			mins = [x for x in successors if x[1] == min_h]
			max_score = 0
			for x in range(len(mins)):
				p_tmp = copy.deepcopy(p_locations)
				for k in range(p):
					if p_tmp[k][1] == mins[x][0][1]:
						p_tmp[k] = mins[x][0][:]
						break
				board_p = np.eye(n) * 0
				for x in range(p):  # populating the board with police officers
					y, z = p_tmp[x][0], p_tmp[x][1]
					board_p[y][z] += 1
				# print'officer board ', x, ': '
				# print(board_p)
				# print 'p_locations: ', p_tmp
				# print 'number of collisions: ', compute_h(p_tmp)
				score = np.sum(np.multiply(board_p, board))
				# print 'score: ', score
				if score > max_score:
					max_score = score
				# if max_score > max_activity:
				# 	max_activity = max_score
				# 	print('verifying max score ', max_activity, ': ')
				# 	print(board_p)
				# 	print(board)
			# print 'local max_score: ', max_score
			break



		elif min_h != 0:
			# print 'continuing hill-climbing: '
			mins = [x for x in successors if x[1] == min_h]
			# print 'mins ', mins

			#randomly choose a minimum traversal
			move = random.choice(mins)[0]
			# print 'move ', move
			# print 'p_locations: ', p_locations
			for k in range(p):
				if p_locations[k][1] == move[1]:
					p_locations[k] = move
					break
			# print 'p_locations updated: ', p_locations
			minimum = min_h




		elif min_h == 0:
			# print 'hill-climbing global maximum reached: '
			filtered = [x for x in successors if x[1] == 0]
			# print filtered

			max_score = 0
			if filtered:
				for x in range(len(filtered)):
					p_tmp = copy.deepcopy(p_locations)
					for k in range(p):
						if p_tmp[k][1] == filtered[x][0][1]:
							p_tmp[k] = filtered[x][0][:]
							break
					board_p = np.eye(n) * 0
					for w in range(p): #populating the board with police officers
						y,z = p_tmp[w][0], p_tmp[w][1]
						board_p[y][z] += 1
					# print'officer board ', x, ': '
					# print(board_p)
					# print 'p_locations: ', p_tmp
					# print 'number of collisions: ', compute_h(p_tmp)
					score = np.sum(np.multiply(board_p, board))
					# print 'score: ', score
					if score > max_score:
						max_score = score
					if max_score > max_activity:
						max_activity = max_score
						print('verifying global max score ', max_activity, ': ')
						print(board_p)
						print(board)

			# print 'max_score: ', max_score
			break
	if time.clock() - start > 175:
		print 'timing out: bye!'
		break

print 'max: ', max_activity
max_activity = int(max_activity)
output = open('output.txt','w')
output.write(str(max_activity) + '\n')
f.close()
output.close()

print "Time Elapsed: ", str(time.clock() - start) + 's'