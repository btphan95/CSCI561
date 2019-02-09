#CSCI 561 HW3
#Created by Binh Phan

import numpy as np
np.set_printoptions(suppress=True, linewidth=200)
import time

def max_u(coordinate):
	""" This function calculates the utilities of each transition (up, left, down, right) and returns the
	max utility"""
	# print 'original coordinates: ', coordinate
	u = 0
	#going up
	up = [coordinate[0] - 1, coordinate[1]]
	if up[0] < 0:
		up[0] = 0
	# print('up ', up)
	# going down
	down = [coordinate[0] + 1, coordinate[1]]
	if down[0] > (s-1):
		down[0] = s-1
	# print('down ', down)
	# going left
	left = [coordinate[0], coordinate[1] - 1]
	if left[1] < 0:
		left[1] = 0
	# print('left ', left)
	# going right
	right = [coordinate[0], coordinate[1] + 1]
	if right[1] > (s-1):
		right[1] = s-1
	# print 'right, ', right
	u_up = 0.7 * utility_car[up[0]][up[1]] + 0.1 * utility_car[down[0]][down[1]] + 0.1 * utility_car[left[0]][left[1]] \
		   + 0.1 * utility_car[right[0]][right[1]]
	# print 'u_up = ', gas, ' + ', y, ' * (0.7 * ', utility_car[up[0]][up[1]], ' + 0.1 * ', utility_car[down[0]][down[1]], ' + 0.1 *  utility_car[down[0]][down[1]]', utility_car[left[0]][
	# 	left[1]], ' + 0.1 * ', utility_car[right[0]][right[1]]
	u_down = 0.1 * utility_car[up[0]][up[1]] + 0.7 * utility_car[down[0]][down[1]] + 0.1 * utility_car[left[0]][left[1]] \
		   + 0.1 * utility_car[right[0]][right[1]]
	# print 'u_down = ', gas, ' + ', y, ' * (0.1 * ', utility_car[up[0]][up[1]], ' + 0.7 * ', utility_car[down[0]][
	# 	down[1]], ' + 0.1 *  utility_car[down[0]][down[1]]', utility_car[left[0]][
	# 	left[1]], ' + 0.1 * ', utility_car[right[0]][right[1]]
	u_left = 0.1 * utility_car[up[0]][up[1]] + 0.1 * utility_car[down[0]][down[1]] + 0.7 * utility_car[left[0]][left[1]] \
		   + 0.1 * utility_car[right[0]][right[1]]
	# print 'u_left = ', gas, ' + ', y, ' * (0.1 * ', utility_car[up[0]][up[1]], ' + 0.1 * ', utility_car[down[0]][
	# 	down[1]], ' + 0.1 *  utility_car[down[0]][down[1]]', utility_car[left[0]][
	# 	left[1]], ' + 0.7 * ', utility_car[right[0]][right[1]]
	u_right = 0.1 * utility_car[up[0]][up[1]] + 0.1 * utility_car[down[0]][down[1]] + 0.1 * utility_car[left[0]][left[1]] \
		   + 0.7 * utility_car[right[0]][right[1]]
	# print 'u_right = ', gas, ' + ', y, ' * (0.1 * ', utility_car[up[0]][up[1]], ' + 0.1 * ', utility_car[down[0]][
	# 	down[1]], ' + 0.1 *  utility_car[down[0]][down[1]]', utility_car[left[0]][
	# 	left[1]], ' + 0.7 * ', utility_car[right[0]][right[1]]
	# print ' wow ', coordinate, ': ', [u_up, u_down, u_left, u_right]
	u_max = max(u_down,u_left,u_right,u_up)
	# print 'current value: ', utility_car[coordinate]
	u_update = city_car[coordinate] + y * u_max
	# print 'updated value: ', u_update
	# print 'up ', u_up, ' down ', u_down, ' left ', u_left, ' right ', u_right
	# print(u_down)
	# print(max(u_down,u_left,u_right,u_up))
	return u_update

def set_policy(utility_car):
	""" This function returns a car's policy map given its utility map
	policy key:
	0 - up
	1 - down
	2 - right
	3 - left
	4 - end
	"""
	policy = utility_car * 0
	for x in range(utility_car.size):
		coordinate = np.unravel_index(x, (s, s), order='C')
		if (coordinate != car_end[car]):
			u = []
			#retrieving adjacent utility values
			if not (coordinate[0] - 1) < 0:
				u.append(utility_car[coordinate[0] - 1][coordinate[1]]) #up
			else:
				u.append(-10000)
			if not (coordinate[0] + 1 > (s - 1)):
				u.append(utility_car[coordinate[0] + 1][coordinate[1]]) #down
			else:
				u.append(-10000)
			if not (coordinate[1] + 1) > (s - 1):
				u.append(utility_car[coordinate[0]][coordinate[1] + 1]) #right
			else:
				u.append(-10000)
			if not (coordinate[1] - 1) < 0:
				u.append(utility_car[coordinate[0]][coordinate[1] - 1]) #left
			else:
				u.append(-10000)
			policy[coordinate] = np.argmax(u)
		else:
			policy[coordinate] = 4
	return policy

def turn_left(move):
	""" This function turns a given policy move left"""
	if move == 0: #up
		move = 3 #left
	elif move == 1: #down
		move = 2 #right
	elif move == 3: #left
		move = 1 #down
	elif move == 2: #right
		move = 0 #up
	return move

def make_move(coordinate, move):
	"""
	:param move: which direction to move coordinate
	:return: the coordinates after moving
	"""
	if move == 0: #up
		coordinate = [coordinate[0] - 1, coordinate[1]]
		if coordinate[0] < 0:
			coordinate[0] = 0
	elif move == 1: #down
		coordinate = [coordinate[0] + 1, coordinate[1]]
		if coordinate[0] > (s - 1):
			coordinate[0] = s - 1
	elif move == 3: #left
		coordinate = [coordinate[0], coordinate[1] - 1]
		if coordinate[1] < 0:
			coordinate[1] = 0
	elif move == 2: #right
		coordinate = [coordinate[0], coordinate[1] + 1]
		if coordinate[1] > (s - 1):
			coordinate[1] = s - 1
	return (coordinate[0],coordinate[1])









start = time.clock()
f = open('input.txt', 'r')
# policy_name = 'policyXX' + num + '.txt'
# policy_out = open(policy_name,'w')

lines = f.read().splitlines()
# # print lines

s = int(lines[0]) #size of city grid
lines.pop(0)
#create the city's grid
city = (np.eye(s) * 0) - 1

n = int(lines[0]) # number of cars
lines.pop(0)
o = int(lines[0]) # number of obstacles
lines.pop(0)

#add obstacles to the city grid, adding -100 to those coordinates
obs = []
for x in range(o):
	i,j = (lines[0].split(','))
	i,j = int(i), int(j)
	city[i][j] -= 100
	obs.append((j,i))
	lines.pop(0)

#add car start coordinates to list
car_start = []
for x in range(n):
	i, j = (lines[0].split(','))
	i, j = int(i), int(j)
	car_start.append((j,i))
	lines.pop(0)

#add car destination coordinates to list
car_end = []
for i in range(n):
	i, j = (lines[0].split(','))
	i, j = int(i), int(j)
	car_end.append((j, i))
	# city[i][j] += 100
	lines.pop(0)
# print 'car_start ', car_start
# print 'car_end ', car_end

# since the coordinates given are translated, we will translate the coordinates to use the numpy coordinates
city = city.T
# print(city)

#discount factor
y = 0.9
#within epsilon of optimal value
epsilon = 0.1
#delta must be less than this to converge
delta_max = epsilon*((1 - y)/y)
# print('delta max', delta_max)
#cost of gas for moving one timestep
gas = -1

#we want to record the costs. We will keep them in a list
costs = []

for car in range(len(car_start)):

# USING MARKOV DECISION PROCESS
# for each car, we will use MDP value iteration to find the best policies for each coordinate in the city grid
	city_car = city.copy()
	#adding the reward of 100 to car's destination in city grid
	city_car[car_end[car]] += 100
	utility_car = city_car.copy()
	# print 'utility_car[', car,']: '
	# print utility_car
	k = 0
	while(1):
		k += 1
		# print k
		delta = 0
		u_temp = utility_car.copy()
		for i in range(utility_car.size):
			coordinate = np.unravel_index(i, (s, s), order='C')
			if coordinate != car_end[car]:
				u_before = u_temp[coordinate]
				# print(coordinate)
				u_temp[coordinate] = max_u(coordinate)
				# if (abs(u_temp[coordinate] - u_before)) > delta:
				# 	delta = abs(u_temp[coordinate] - u_before)
			delta = max(delta, abs(utility_car[coordinate] - u_temp[coordinate]))
		# print 'delta ', delta
		utility_car = u_temp.copy()

		# print 'delta ', delta
		# print 'delta max ', delta_max
		# print(delta)
		if delta < delta_max:
			break
		# print 'utility_car[', car, ']: '
		# print utility_car
	# print 'utility car is '
	# print np.around(utility_car,decimals=2)
	policy = set_policy(utility_car)
	# print 'policy '
	# print policy
	# policy_lines = []
	# policy_out.write('CAR ' + str(car) + ':' + '\n')
	for i in range(policy.size):
		X = np.unravel_index(i, (s, s), order='C')
		if policy[X] == 0:
			move_txt = 'up'
		if policy[X] == 1:
			move_txt = 'down'
		if policy[X] == 2:
			move_txt = 'right'
		if policy[X] == 3:
			move_txt = 'left'
		if policy[X] == 4:
			move_txt = 'None'
		# policy_lines.append(str(X) + ': ' + move_txt + '\n')
	# policy_lines.sort()
	# for line in policy_lines:
	# 	policy_out.write(line)
# TESTING OUR POLICIES ON SPECIFIED RANDOM SEEDS
# in order to reproduce our results, we will now test our policies using random seeds
	cost_x = []
	# directions_name = 'SIMULATIONMOVES' + num + '_' + str(car) + 'X.txt'
	# directions = open(directions_name,'w')

	for x in range(10):
		# directions.write(str(x) + '~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		cost = 0
		# print 'now at iteration ', x
		coordinate = car_start[car]
		# print 'start coordinate: ', coordinate
		np.random.seed(x)
		swerve = np.random.random_sample(1000000)
		k = 0
		while coordinate != car_end[car]:
			# print 'coordinate is ', coordinate
			move = policy[coordinate]
			# print 'swerve prob is ', swerve[k]
			# print 'correct move is ', move
			# if swerve[k] > 0.9: #turn 180
			# 	move = turn_left(turn_left(move))
			# elif swerve[k] > 0.8: #turn left
			# 	move = turn_left(move)
			# elif swerve[k] > 0.7: #turn right
			# 	move = turn_left(turn_left(turn_left(move)))
			if swerve[k] > 0.7:
				if swerve[k] > 0.8:
					if swerve[k] > 0.9:

						move = turn_left(turn_left(move))
					else:

						move = turn_left(turn_left(turn_left(move)))

				else:
					move = turn_left(move)

			coordinate = make_move(coordinate,move)
			if move == 0:
				move_txt = 'up'
			if move == 1:
				move_txt = 'down'
			if move == 2:
				move_txt = 'right'
			if move == 3:
				move_txt = 'left'
			if move == 4:
				move_txt = 'None'
			# print 'moving ', move_txt
			# directions.write(move_txt + '\n')
			# print 'now at ', coordinate
			# print 'city coordinate ', city_car[coordinate]
			cost += city_car[coordinate]
			# print 'cost ', cost
			k += 1
		cost_x.append(cost)
	# print 'cost_x ', cost_x
	costs.append((np.average(cost_x)))
	# directions.close()
print(costs)
output = open('output.txt','w')
for cost in costs:
	output.write(str(cost) + '\n')
f.close()
output.close()
# policy_out.close()

print "Time Elapsed: ", str(time.clock() - start) + 's'