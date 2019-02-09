#CSCI 561 HW2
#Created by Binh Phan

import numpy as np
import time


def assign_beds(LAHSA_beds, app):
	"""This function assigns an applicant's request to the available beds. It also checks if there is availability.
	If there is no availability, the function will return nothing"""
	availability = [int(x) for x in list(app[13:])]
# 	# print 'beds', LAHSA_beds
# 	# print 'availability', availability
	LAHSA_beds = LAHSA_beds - availability
# 	# print 'update', LAHSA_beds

	#check if the update is valid
	if sum(LAHSA_beds >= 0) == len(LAHSA_beds):
		return LAHSA_beds
	else:
		return np.array([])

def assign_lots(SPLA_lots, app):
	"""This function assigns an applicant's request to the available lots. It also checks if there is availability.
	If there is no availability, the function will return nothing"""
	availability = [int(x) for x in list(app[13:])]
	SPLA_lots = SPLA_lots - availability
# 	# print 'update', LAHSA_beds

	#check if the update is valid
	if sum(SPLA_lots >= 0) == len(SPLA_lots):
		return SPLA_lots
	else:
		return np.array([])

def LAHSA_valid(app):
	"""This function determines if an applicant fits LAHSA's criteria"""
	if app[5] != 'F': #must be female
		return False
	age = int(app[6:9]) # must be older than 17 years old
	if age < 18:
		return False
	if app[9] == 'Y': #must not have any pets
		return False
	return True

def SPLA_valid(app):
	"""This function determines if an applicant fits SPLA's criteria"""
	if app[10] == 'Y': #must not have any medical conditions
		return False
	if app[11] == 'N': #must have a car
		return False
	if app[12] == 'N': #must have a drivers license
		return False
	return True

def select_from_SPLA_pool(pool):
	"""selects the application with the most number of days from the SPLA pool, to maximize
	SPLA's efficiency. If there is a tie, choose the applicant with the lowest number"""
	num_days = [np.sum([int(x) for x in list(app[13:])]) for app in pool]
	# print 'pool ', pool
	# print 'num_days ', num_days

	mask = list(num_days == np.max(num_days))
	# print 'mask ', mask
	for i in range(len(num_days)):
		# print 'i ', i
		if mask[i] == False:
			# print 'FALSE'
			pool[i] = 'Z'

	# print 'pool ', pool
	# print 'min pool is ', min(pool)
	return min(pool)

def select_from_LAHSA_pool(pool):
	"""selects the application with the most number of days from the LAHSA pool, to maximize
	LAHSA's efficiency. If there is a tie, choose the applicant with the lowest number"""
	num_days = [np.sum([int(x) for x in list(app[13:])]) for app in pool]
# 	# print('num days ', num_days)
# 	# print 'argmax is ', pool[np.argmax(num_days)]

	mask = list(num_days == np.max(num_days))
	for i in range(len(num_days)):
		if mask[i] == False:
			pool[i] = 'Z'

	return min(pool)

def Backtracking(turn, SPLA_pool, LAHSA_pool, shared_pool, LAHSA_beds, SPLA_lots, SPLA_assignments,
				 efficiency, max_efficiency, max_assignments):
	"""finds the assignment giving the max efficiency for SPLA using backtracking"""
	explored_pool = []
	# print "i'm in"
	# print 'LAHSA pool, ', LAHSA_pool, ' SPLA pool ', SPLA_pool, 'shared pool ', shared_pool
	# if (int(time.clock()) % 10) == 0:
	# 	print time.clock() - start
	if time.clock() - start > 150:
		print 'timing out: bye!'
		return max_efficiency, max_assignments
	if turn == 'SPLA':
		#choosing to do depth-limited depth-first search here to conserve runtime.
		#Setting the max depth of the search to about 3 will almost guarantee an optimum result
		#because in most cases, the first few assignments determine the
		#final result, the maximum efficiency, almost always
		if len(SPLA_assignments) < 1:
			LAHSA_assigned = 0
			# print 'SPLA turn'
			#if shared pool is not empty: then choose an item from there first
			if shared_pool:
				for i in range(len(shared_pool)):
					if time.clock() - start > 150:
						print 'timing out: bye!'
						break
					# print 'SPLA assignments: ', SPLA_assignments
					assignment = select_from_SPLA_pool(list(set(shared_pool) - set(explored_pool)))
					#adding assignment to explored pool
					explored_pool.append(assignment)
					# print 'in shared pool: choosing ', assignment
					# assign lots at SPLA
					lots_before = SPLA_lots
					SPLA_lots = assign_lots(SPLA_lots, assignment)
					# assign spaces at SPLA
					# if there is no space left at SPLA, then backtrack, because this is not a valid option
					if SPLA_lots.size:
						shared_pool.pop(shared_pool.index(assignment))
						# print 'shared_pool after ', shared_pool
						# print 'SPLA before ', SPLA_pool
						SPLA_pool.pop(SPLA_pool.index(assignment))
						# print 'SPLA after ', SPLA_pool
						LAHSA_pool.pop(LAHSA_pool.index(assignment))
						SPLA_assignments.append(assignment)
						efficiency = np.sum(initial_lots - SPLA_lots)
						# print 'current efficiency: ', efficiency
						# print 'SPLA lots ', SPLA_lots
						# if current efficiency > max efficiency, save assignment
						if efficiency > max_efficiency:
							max_efficiency = efficiency
							max_assignments = [i for i in SPLA_assignments]
							print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						elif efficiency == max_efficiency:
							if max_assignments and SPLA_assignments:
								if int(max_assignments[0][0:5]) > int(SPLA_assignments[0][0:5]):
									# print int(max_assignments[0][0:5]), ' is less than ', int(SPLA_assignments[0][0:5])
									max_assignments = [i for i in SPLA_assignments]
									print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						efficiency, assignments = Backtracking('LAHSA', SPLA_pool, LAHSA_pool, shared_pool,
															  LAHSA_beds,
															  SPLA_lots, SPLA_assignments,
															  efficiency, max_efficiency, max_assignments)
						# print ' assignments ', assignments
						# print 'back to SPLA from recursion'
						# print 'efficiency, assignments', efficiency, assignments
						# print 'max efficiency, max assignments', max_efficiency, max_assignments
						# if current efficiency > max efficiency, save assignment
						if efficiency > max_efficiency:
							max_efficiency = efficiency
							max_assignments = [i for i in assignments]
							# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						elif efficiency == max_efficiency:
							if max_assignments and assignments:
								if int(max_assignments[0][0:5]) > int(assignments[0][0:5]):
									# print int(max_assignments[0][0:5]), ' is less than ', int(assignments[0][0:5])
									max_assignments = [i for i in assignments]
									# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						#after backtracking, revert changes
						# print'before reverting changes: '
						# print 'shared pool is ', shared_pool
						# print 'SPLA pool is ', SPLA_pool
						shared_pool.append(assignment)
						# print 'shared_pool after ', shared_pool
						# print 'SPLA before ', SPLA_pool
						SPLA_pool.append(assignment)
						# print 'SPLA after ', SPLA_pool
						LAHSA_pool.append(assignment)
						SPLA_assignments.pop(SPLA_assignments.index(assignment))
					# elif not SPLA_lots.size:
					# 	print 'SPLA LOTS FULL'
					SPLA_lots = lots_before
					# print 'shared pool is ', shared_pool
					# print 'SPLA pool is ', SPLA_pool
					# print 'efficiency, assignments', efficiency, assignments
					# print 'max efficiency, max assignments', max_efficiency, max_assignments
			#if shared pool is empty, then choose an item from SPLA_pool
			elif not shared_pool:
				if SPLA_pool:
					for i in range(len(SPLA_pool)):
						if time.clock() - start > 150:
							print 'timing out: bye!'
							break
						# print 'SPLA assignments: ', SPLA_assignments
						assignment = select_from_SPLA_pool(list(set(SPLA_pool) - set(explored_pool)))
						# print 'in SPLA pool: choosing ', assignment
						explored_pool.append(assignment)
						# assign lots at SPLA
						lots_before = SPLA_lots
						SPLA_lots = assign_lots(SPLA_lots, assignment)
						# if there is no space left at SPLA, then backtrack, because this is not a valid option
						if SPLA_lots.size:
							# print 'SPLA before ', SPLA_pool
							SPLA_pool.pop(SPLA_pool.index(assignment))
							# print 'SPLA after ', SPLA_pool
							if assignment in LAHSA_pool:
								LAHSA_assigned = 1
								LAHSA_pool.pop(LAHSA_pool.index(assignment))
							SPLA_assignments.append(assignment)
							efficiency = np.sum(initial_lots - SPLA_lots)
							# if current efficiency > max efficiency, save assignment
							if efficiency > max_efficiency:
								max_efficiency = efficiency
								max_assignments = [i for i in SPLA_assignments]
								# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
							elif efficiency == max_efficiency:
								if max_assignments and SPLA_assignments:
									if int(max_assignments[0][0:5]) > int(SPLA_assignments[0][0:5]):
										#  print int(max_assignments[0][0:5]), ' is less than ', int(SPLA_assignments[0][0:5])
										max_assignments = [i for i in SPLA_assignments]
										# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
								# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
							efficiency, assignments = Backtracking('LAHSA', SPLA_pool, LAHSA_pool, shared_pool,
																			  LAHSA_beds,
																			  SPLA_lots, SPLA_assignments,
																			  efficiency, max_efficiency, max_assignments)
							# print 'back to splap from recursion'
							# if current efficiency > max efficiency, save assignment
							if efficiency > max_efficiency:
								max_efficiency = efficiency
								max_assignments = [i for i in assignments]
								# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
							elif efficiency == max_efficiency:
								if max_assignments and assignments:
									if int(max_assignments[0][0:5]) > int(assignments[0][0:5]):
										# print int(max_assignments[0][0:5]), ' is less than ', int(assignments[0][0:5])
										max_assignments = [i for i in assignments]
										# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
							# after backtracking, revert changes
							# print 'SPLA before ', SPLA_pool
							SPLA_pool.append(assignment)
							# print 'SPLA after ', SPLA_pool
							if LAHSA_assigned == 1:
								LAHSA_pool.append(assignment)
								LAHSA_assigned = 0
							SPLA_assignments.pop(SPLA_assignments.index(assignment))
						SPLA_lots = lots_before

	# 				# print 'did it work? ',shared_pool,SPLA_pool,LAHSA_pool
	elif turn == 'LAHSA':
		shared_assigned = 0
		SPLA_assigned = 0
		# # print 'LAHSA turn'
		# # print 'LAHSA_pool is ', LAHSA_pool
		# #Avoid choosing an item in shared_pool, to maximize SPLA's efficiency
		# current_pool = list(set(LAHSA_pool) - set(shared_pool))
		# if current_pool:
		# 	for i in range(len(current_pool)):
		# 		if time.clock() - start > 150:
		# 			print 'timing out: bye!'
		# 			break
		# 		assignment = select_from_LAHSA_pool(list(set(current_pool) - set(explored_pool)))
		# 		# print 'LAHSA choosing ', assignment
		# 		# print 'hi bitch'
		# 		explored_pool.append(assignment)
		# 		beds_before = LAHSA_beds
		# 		LAHSA_beds = assign_beds(LAHSA_beds,assignment)
		# 		# print 'assigned beds '
		# 		if LAHSA_beds.size:
		# 			current_pool.pop(current_pool.index(assignment))
		# 			LAHSA_pool.pop(LAHSA_pool.index(assignment))
		# 			# print 'popping ', assignment, 'from LAHSA'
		# 			if assignment in shared_pool:
		# 				shared_assigned = 1
		# 				shared_pool.pop(shared_pool.index(assignment))
		# 				SPLA_assigned = 1
		# 				# print 'SPLA before ', SPLA_pool
		# 				SPLA_pool.pop(SPLA_pool.index(assignment))
		# 				# print 'SPLA after ', SPLA_pool
		# 			elif assignment in SPLA_pool:
		# 				# print 'popping ', assignment, 'from SPLA'
		# 				SPLA_assigned = 1
		# 				# print 'SPLA before ', SPLA_pool
		# 				SPLA_pool.pop(SPLA_pool.index(assignment))
		# 				# print 'SPLA after ', SPLA_pool
		# 			efficiency, assignments = Backtracking('SPLA', SPLA_pool, LAHSA_pool, shared_pool, LAHSA_beds,
		# 														SPLA_lots, SPLA_assignments,
		# 												   		efficiency, max_efficiency, max_assignments)
		# 			# print 'back to LAHSA from recursion'
		# 			# if current efficiency > max efficiency, save assignment
		# 			if efficiency > max_efficiency:
		# 				max_efficiency = efficiency
		# 				max_assignments = [i for i in assignments]
		# 				# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
		# 			elif efficiency == max_efficiency:
		# 				if max_assignments and assignments:
		# 					if int(max_assignments[0][0:5]) > int(assignments[0][0:5]):
		# 						# print int(max_assignments[0][0:5]), ' is less than ', int(assignments[0][0:5])
		# 						max_assignments = [i for i in assignments]
		# 						# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
		# 			#after backtracking, revert changes
		# 			current_pool.append(assignment)
		# 			LAHSA_pool.append(assignment)
		# 			if shared_assigned == 1:
		# 				shared_pool.append(assignment)
		# 				# print 'shared_pool after ', shared_pool
		# 				shared_assigned = 0
		# 				# print 'SPLA before ', SPLA_pool
		# 				SPLA_pool.append(assignment)
		# 				# print 'SPLA after ', SPLA_pool
		# 				SPLA_assigned = 0
		# 			elif SPLA_assigned == 1:
		# 				# print 'SPLA before ', SPLA_pool
		# 				SPLA_pool.append(assignment)
		# 				# print 'SPLA after ', SPLA_pool
		# 				SPLA_assigned = 0
		# 		LAHSA_beds = beds_before
		# elif not current_pool:
		if LAHSA_pool:
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print('SSSSSSSSSSSSSSSSSSSSSSS')
			# print 'LAHSA pool ISSSSSSSSSSSSSSSSSSSSSSS ', LAHSA_pool
			for i in range(len(LAHSA_pool)):
				if time.clock() - start > 150:
					print 'timing out: bye!'
					break
				# print 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII ', i
				# print 'LAHSA pool: ', LAHSA_pool
				# print 'explored pool: ', explored_pool
				assignment = select_from_LAHSA_pool(list(set(LAHSA_pool) - set(explored_pool)))
				# print 'LAHSAp choosing ', assignment
				explored_pool.append(assignment)
				beds_before = LAHSA_beds
				LAHSA_beds = assign_beds(LAHSA_beds, assignment)
				if LAHSA_beds.size:
					LAHSA_pool.pop(LAHSA_pool.index(assignment))
					if assignment in shared_pool:
						# print 'assignment ', assignment, ' in shared pool?'
						shared_assigned = 1
						shared_pool.pop(shared_pool.index(assignment))
						SPLA_assigned = 1
						SPLA_pool.pop(SPLA_pool.index(assignment))
					elif assignment in SPLA_pool:
						# print 'popping ', assignment, 'from SPLA'
						SPLA_assigned = 1
						SPLA_pool.pop(SPLA_pool.index(assignment))
					efficiency, assignments = Backtracking('SPLA', SPLA_pool, LAHSA_pool, shared_pool,
																  LAHSA_beds,
																  SPLA_lots, SPLA_assignments,
																  efficiency,
																  max_efficiency,
																  max_assignments)
					# print 'back to LAHSAp from recursion'
					# print 'assignment is ', assignment
					# if current efficiency > max efficiency, save assignment
					if efficiency > max_efficiency:
						max_efficiency = efficiency
						max_assignments = [i for i in assignments]
						# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
					elif efficiency == max_efficiency:
						if max_assignments and assignments:
							if int(max_assignments[0][0:5]) > int(assignments[0][0:5]):
								# print int(max_assignments[0][0:5]), ' is less than ', int(assignments[0][0:5])
								max_assignments = [i for i in assignments]
								# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
					# if LAHSA pool is empty after assignment, then assign all remaining SPLA applicants
					if not LAHSA_pool:
						explored_SPLA_assignments = []
						# print 'LAHSA_pool is empty! ADDING ALL SPLA APPLICANTS'
						# print 'current lot assignment ', SPLA_lots
						# print 'current max_efficiency ', max_efficiency
						# print 'SPLA_pool: ', SPLA_pool
						lots_before = SPLA_lots
						for item in SPLA_pool:
							# assignment = SPLA_pool.pop()
							# explored_SPLA_pool.append(assignment)
							# assign lots at SPLA
							SPLA_lots = assign_lots(SPLA_lots, item)
							# print 'SPLA lots for ', item, ' is ', SPLA_lots
							if SPLA_lots.size:
								explored_SPLA_assignments.append(item)
								SPLA_assignments.append(item)
								efficiency = np.sum(initial_lots - SPLA_lots)
								# print 'adding ', efficiency
							elif not SPLA_lots.size:
								SPLA_lots = lots_before
								break
						SPLA_lots = lots_before
						if efficiency > max_efficiency:
							max_efficiency = efficiency
							max_assignments = [i for i in SPLA_assignments]
						elif efficiency == max_efficiency:
							if max_assignments and assignments:
								if int(max_assignments[0][0:5]) > int(SPLA_assignments[0][0:5]):
									# print int(max_assignments[0][0:5]), ' is less than ', int(SPLA_assignments[0][0:5])
									max_assignments = [i for i in SPLA_assignments]
									# print 'yes! max efficiency updated to ', max_efficiency, ': ', max_assignments
						# for assignment in explored_SPLA_pool:
						# 	SPLA_pool.append(assignment)
						for item in explored_SPLA_assignments:
							SPLA_assignments.pop(SPLA_assignments.index(item))
					#after backtracking, revert changes
					LAHSA_pool.append(assignment)
					if shared_assigned == 1:
						# print 'shared_assigned == 1'
						# print 'assignment is ', assignment
						# print 'SPLA before ', SPLA_pool

						shared_pool.append(assignment)
						# print 'SPLA after ', SPLA_pool
						shared_assigned = 0
						SPLA_pool.append(assignment)
						# print 'shared_pool after ', shared_pool
						SPLA_assigned = 0
					elif SPLA_assigned == 1:
						# print 'SPLA before ', SPLA_pool

						SPLA_pool.append(assignment)
						# print 'SPLA after ', SPLA_pool
						SPLA_assigned = 0
				LAHSA_beds = beds_before
		# if LAHSA pool is empty after assignment, then assign all remaining SPLA applicants
		elif not LAHSA_pool:
			explored_SPLA_assignments = []
			# print 'LAHSA_pool is empty! ADDING ALL SPLA APPLICANTS'
			# print 'current lot assignment ', SPLA_lots
			# print 'current max_efficiency ', max_efficiency
			# print 'SPLA_pool: ', len(SPLA_pool)
			# print 'SPLA assignments: ', len(SPLA_assignments)
			lots_before = SPLA_lots
			for item in SPLA_pool:
				# assignment = SPLA_pool.pop()
				# explored_SPLA_pool.append(assignment)
				# assign lots at SPLA
				SPLA_lots = assign_lots(SPLA_lots, item)
# 					# print 'SPLA lots for ', assignment, ' is ', SPLA_lots
				if SPLA_lots.size:
					explored_SPLA_assignments.append(item)
					SPLA_assignments.append(item)
					efficiency = np.sum(initial_lots - SPLA_lots)
					# print 'adding ', efficiency
				elif not SPLA_lots.size:
					SPLA_lots = lots_before
					break
			SPLA_lots = lots_before
			if efficiency > max_efficiency:
				max_efficiency = efficiency
				max_assignments = [i for i in SPLA_assignments]
			# for assignment in explored_SPLA_pool:
			# 	SPLA_pool.append(assignment)
			for item in explored_SPLA_assignments:
				SPLA_assignments.pop(SPLA_assignments.index(item))

	# print 'byebye, returning ', max_efficiency, max_assignments
	return max_efficiency, max_assignments


start = time.clock()
f = open('input.txt', 'r')
lines = f.read().splitlines()
# # print lines

#creating array for the number of available beds at LAHSA for each day of the week
LAHSA_beds = np.ones(7)*int(lines[0])
#creating arrays for the number of available lots at SPLA for each day of the week
SPLA_lots = np.ones(7)*	int(lines[1])
initial_lots = SPLA_lots
#filtering out LAHSA apps
lines = lines[2:]
LAHSA_num_apps = int(lines[0])
LAHSA_apps = []
# # print(LAHSA_num_apps)
for i in range(LAHSA_num_apps):
	LAHSA_apps.append(lines[i+1])
print 'LAHSA apps ', LAHSA_apps
lines = lines[LAHSA_num_apps+1:]
#filtering out SPLA apps
SPLA_num_apps = int(lines[0])
print 'SPLA num apps ', SPLA_num_apps
SPLA_apps = []
for i in range(SPLA_num_apps):
	SPLA_apps.append(lines[i+1])
print 'SPLA apps: ', SPLA_apps
# # print(lines)

#creating a list containing all applications
apps = lines[SPLA_num_apps+2:]
print(apps)

#assigning LAHSA beds
for app in LAHSA_apps:
	matching = [s for s in apps if app in s]
	# print 'matching ', matching
	LAHSA_beds = assign_beds(LAHSA_beds, matching[0])
# 	# print matching
	i = apps.index(matching[0])
	apps.pop(i)
	# print 'new apps: ', apps

#assigning SPLA lots
for app in SPLA_apps:
	matching = [s for s in apps if app in s]
	SPLA_lots = assign_lots(SPLA_lots,matching[0])
	i = apps.index(matching[0])
	apps.pop(i)
# 	# print 'new apps: ', apps

#BACKTRACKING ALGORITHM
""" We will now implement a backtracking algorithm that parses the available applicants through brute force, 
thereby determining the maximum efficiency that SPLA can achieve.
"""

#creating empty pools of valid applicants for SPLA and LAHSA
SPLA_pool = []
LAHSA_pool = []

#filling applicant pools
for app in apps:
	if LAHSA_valid(app):
		LAHSA_pool.append(app)
	if SPLA_valid(app):
		SPLA_pool.append(app)
print 'SPLA pool', SPLA_pool
print 'LAHSA pool', LAHSA_pool

# #In order to maximize SPLA's efficiency, we should let SPLA choose applicants that LAHSA also want to accept, thus
# #giving SPLA more applicants
#
shared_pool = list(set(SPLA_pool) & set(LAHSA_pool))
print 'shared pool', shared_pool

#pick unassigned variable, from shared pool first, then from SPLA pool:
turn = 'SPLA'
SPLA_assignments = []
max_assignments = []
max_efficiency = 0
efficiency = 0
max_efficiency, max_assignments = Backtracking(turn, SPLA_pool, LAHSA_pool, shared_pool, LAHSA_beds,
										SPLA_lots, SPLA_assignments,
										efficiency, max_efficiency, max_assignments)

print "ANSWER!", max_efficiency, max_assignments
print 'ANSWER!', max_assignments[0][0:5]
output = open('output.txt','w')
output.write(max_assignments[0][0:5])
f.close()
output.close()

print "Time Elapsed: ", str(time.clock() - start) + 's'