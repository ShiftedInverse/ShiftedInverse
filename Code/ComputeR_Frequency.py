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
	global query_result
	global obj
	global ub
	global cols
	global rows
	global vals
	global senses
	global rhs

	id_dict = {}
	id_num = 0

	users = []
	contribution_value_dict = {}
	user_contribution_value_dict = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		contribution_value = str(elements[0])
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			users.append(id_num)
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		if contribution_value in contribution_value_dict.keys():
			contribution_value_dict[contribution_value] += 1
		else:
			contribution_value_dict[contribution_value] = 1

		if user_id in user_contribution_value_dict.keys():
			if contribution_value in user_contribution_value_dict[user_id].keys():
				user_contribution_value_dict[user_id][contribution_value] += 1
			else:
				user_contribution_value_dict[user_id][contribution_value] = 1
		else:
			user_contribution_value_dict[user_id] = {}
			user_contribution_value_dict[user_id][contribution_value] = 1

	contribution_values = list(contribution_value_dict.keys())
	contribution_value_frequencies = list(contribution_value_dict.values())
	query_result = max(contribution_value_frequencies)

	num_users = len(users)
	num_values = len(contribution_values)
	
	obj = np.append(np.zeros(num_users), np.array([1]))
	ub = np.append(np.ones(num_users), np.array([cplex.infinity]))

	cols = []
	rows = []
	vals = []
	senses = "L" * (num_values + 1)

	for i in range(num_values):
		value = contribution_values[i]
		rows.append(i)
		cols.append(num_users)
		vals.append(-1)

		for j in range(num_users):
			if value in user_contribution_value_dict[j].keys():
				rows.append(i)
				cols.append(j)
				vals.append(-user_contribution_value_dict[j][value])

	for i in range(num_users):
		rows.append(num_values)
		cols.append(i)
		vals.append(1)

	rhs = np.array([float(-x) for x in contribution_value_frequencies])

def LpSolver(j):
	global obj
	global ub
	global cols
	global rows
	global vals
	global senses
	global rhs

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)
	
	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None)

	rhs_j = np.append(rhs, np.array([j]))

	cpx.variables.add(obj=obj, ub=ub)
	cpx.linear_constraints.add(rhs=rhs_j, senses=senses)
	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))

	cpx.solve()

	return cpx.solution.get_objective_value()

def ThresholdRunAlgorithm(js):
	global check_fs

	for i in js:
		check_fs[i] = LpSolver(i)

def RunAlgorithm():
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global processor_num
	global check_fs

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	check_fs = manager.dict()

	arrangement_of_js = []
	for i in range(processor_num):
		arrangement_of_js.append([])

	j = 0
	for i in range(1,  2 * tau + 1):
		arrangement_of_js[j].append(i)
		check_fs[i] = 0

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
	output_file.write(str(math.log(query_result, 10)) + "\n")
	for j in range(1, 2 * tau + 1):
		value = check_fs[j]
		output_file.write(str(math.log(value, 10)) + "\n")
	output_file.write("0\n")

def main(argv):
	global input_path
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global processor_num

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:d:O:p:", ["InputPath=", "epsilon=", "beta=", "UpperBound=", "ErrorLevel=", "OutputPath=", "ProcessNum="])
	except getopt.GetoptError:
		print("ComputeR_Frequency.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -p <process num>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ComputeR_Frequency.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -p <process num>")
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
		elif opt in ("-p", "--ProcessorNum"):
			processor_num = max(1, int(arg))

	ReadInput()
	RunAlgorithm()

if __name__ == "__main__":
	main(sys.argv[1 : ])