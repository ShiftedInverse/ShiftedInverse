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
	query_result = value_list[index - 1][1]

def LpSolver(num_tuples):
	global value_list
	global num_users

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)
	
	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None)

	obj = np.append(np.ones(num_users), np.zeros(num_tuples))
	ub = np.ones(num_users + num_tuples)

	cols = []
	rows = []
	vals = []
	senses = "L" * (num_tuples + 1)

	for i in range(num_tuples):
		rows.append(i)
		cols.append(num_users + i)
		vals.append(1)

		for j in value_list[i][0]:
			rows.append(i)
			cols.append(j)
			vals.append(-1)

	for i in range(num_tuples):
		rows.append(num_tuples)
		cols.append(num_users + i)
		vals.append(-1)

	rhs = np.append(np.zeros(num_tuples), np.array([- num_tuples + index - 1]))

	cpx.variables.add(obj=obj, ub=ub)
	cpx.linear_constraints.add(rhs=rhs, senses=senses)
	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))

	cpx.solve()

	return cpx.solution.get_objective_value()

def ThresholdRunAlgorithm(processor_index, js):
	global index
	global cover_numbers
	global tau
	global stop_variable

	for i in js:
		if stop_variable[0]:
			if i < index:
				cover_numbers[i] = 0
			else:
				cover_numbers[i] = LpSolver(i)
				if cover_numbers[i] > 2 * tau + 1:
					print(processor_index, cover_numbers[i])
					stop_variable[processor_index] = False
		else:
			break

def RunAlgorithm():
	global value_list
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global index
	global processor_num
	global cover_numbers
	global tau
	global stop_variable

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	cover_numbers = manager.dict()

	stop_variable = manager.dict()
	for i in range(processor_num):
		stop_variable[i] = True

	arrangement_of_js = []
	for i in range(processor_num):
		arrangement_of_js.append([])

	j = 0
	for i in range(1, len(value_list)):
		arrangement_of_js[j].append(i)

		j = (j + 1) % processor_num

	threads = []

	for i in range(processor_num):
		threads.append(multiprocessing.Process(target=ThresholdRunAlgorithm, args=(i, arrangement_of_js[i],)))	
		threads[i].start()

	for i in range(processor_num):
		threads[i].join()

	check_fs = [0] * (2 * tau + 1)
	check_fs[0] = query_result

	cover_numbers = list(cover_numbers.items())
	cover_numbers = sorted(cover_numbers, key=lambda item: item[0])

	for (num_tuples_covered, num_users_used) in cover_numbers:
		if num_users_used > 0 and num_users_used <= 2 * tau:
			num_users_used = math.floor(num_users_used)
			check_fs[num_users_used] = value_list[num_tuples_covered + index - 1][1]

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
		print("ComputeR_Max_Sj.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -k <index> -p <processor num>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ComputeR_Max_Sj.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -k <index> -p <processor num>")
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