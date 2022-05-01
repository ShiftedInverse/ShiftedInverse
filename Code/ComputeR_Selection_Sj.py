import cplex
import getopt
import math
import multiprocessing
import numpy as np
import os
import sys
import time

manager = multiprocessing.Manager()

def ReadInput():
	global input_path
	global value_list
	global num_users
	global num_tuples
	global query_result

	id_dict = {}
	id_num = 0

	users = []
	tuples = []
	value_dict = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_ = []
		value = float(elements[0])

		for element in elements[1 : ]:
			user_id = int(element)

			if user_id in id_dict.keys():
				user_id = id_dict[user_id]
			else:
				users.append(id_num)
				id_dict[user_id] = id_num
				user_id = id_num
				id_num += 1

			tuple_.append(user_id)

		tuple_ = tuple(sorted(set(tuple_)))

		if tuple_ in value_dict.keys():
			value_dict[tuple_].append(value)
		else:
			tuples.append(tuple_)
			value_dict[tuple_] = [value]

	num_users = len(users)

	value_list = [(users, i) for (users, values) in value_dict.items() for i in values]
	value_list = sorted(value_list, reverse=True, key=lambda item: item[1])

	num_tuples = len(value_list)
	if index > len(value_list):
		query_result = 0
	else:
		query_result = value_list[index - 1][1]

def LpSolver(num_tuples_lp):
	global value_list
	global num_users

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)
	
	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None)

	obj = np.append(np.ones(num_users), np.zeros(num_tuples_lp))
	ub = np.ones(num_users + num_tuples_lp)

	cols = []
	rows = []
	vals = []
	senses = "L" * (num_tuples_lp + 1)

	for i in range(num_tuples_lp):
		rows.append(i)
		cols.append(num_users + i)
		vals.append(1)

		for j in value_list[i][0]:
			rows.append(i)
			cols.append(j)
			vals.append(-1)

	for i in range(num_tuples_lp):
		rows.append(num_tuples_lp)
		cols.append(num_users + i)
		vals.append(-1)

	rhs = np.append(np.zeros(num_tuples_lp), np.array([- num_tuples_lp + index - 1]))

	cpx.variables.add(obj=obj, ub=ub)
	cpx.linear_constraints.add(rhs=rhs, senses=senses)
	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))

	cpx.solve()

	return cpx.solution.get_objective_value()

def BinarySearch(num_users_used, left_index, right_index):
	global cover_numbers

	while left_index < right_index:
		mid_index = math.floor((left_index + right_index) / 2)

		if mid_index in cover_numbers.keys():
			lp_output = cover_numbers[mid_index]
		else:
			lp_output = LpSolver(mid_index)
			cover_numbers[mid_index] = lp_output

		if lp_output >= num_users_used:
			next_right_index = mid_index
			return BinarySearch(num_users_used, left_index, next_right_index)
		else:
			next_left_index = mid_index + 1
			return BinarySearch(num_users_used, next_left_index, right_index)

	return left_index

def ThresholdRunAlgorithm(js):
	global num_tuples
	global index
	global check_fs

	for num_users_used in js:
		num_tuples_covered = BinarySearch(num_users_used, index, num_tuples)
		check_fs[num_users_used] = value_list[num_tuples_covered - 1][1]

def RunAlgorithm():
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global processor_num
	global cover_numbers
	global check_fs
	global tau

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	cover_numbers = manager.dict()

	check_fs = manager.dict()
	check_fs[0] = query_result

	for i in range(1, 2 * tau + 1):
		check_fs[i] = 0

	if query_result != 0:
		arrangement_of_js = []
		for i in range(processor_num):
			arrangement_of_js.append([])

		j = 0
		for i in range(1, 2 * tau + 1):
			arrangement_of_js[j].append(i)

			j = (j + 1) % processor_num

		threads = []

		for i in range(processor_num):
			threads.append(multiprocessing.Process(target=ThresholdRunAlgorithm, args=(arrangement_of_js[i],)))	
			threads[i].start()

		for i in range(processor_num):
			threads[i].join()

	cur_path = os.getcwd() + '/'
	output_file = open(cur_path + output_path, 'w')

	output_file.write(str(upper_bound) + "\n")
	output_file.write(str(query_result) + "\n")
	for j in range(1, 2 * tau + 1):
		value = check_fs[j]
		output_file.write(str(value) + "\n")
	output_file.write("0\n")

def main(argv):
	global input_path
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global index
	global processor_num

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:d:O:k:p:", ["InputPath=", "epsilon=", "beta=", "UpperBound=", "ErrorLevel=", "OutputPath=", "index=", "processorNum="])
	except getopt.GetoptError:
		print("ComputeR_Selection_Sj.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -k <index> -p <processor num>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ComputeR_Selection_Sj.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -k <index> -p <processor num>")
			sys.exit()
		elif opt in ("-I", "--InputPath"):
			input_path = str(arg)
		elif opt in ("-e", "--epsilon"):
			epsilon = float(arg)
		elif opt in ("-b", "--beta"):
			beta = float(arg)
		elif opt in ("-D", "--UpperBound"):
			upper_bound = int(arg)
		elif opt in ("-d", "--ErrorLevel"):
			error_level = float(arg)
		elif opt in ("-O", "--OutputPath"):
			output_path = str(arg)
		elif opt in ("-k", "--index"):
			index = int(arg)
		elif opt in ("-p", "--ProcessorNum"):
			processor_num = max(1, int(arg))

	ReadInput()
	RunAlgorithm()

if __name__ == "__main__":
	main(sys.argv[1 : ])