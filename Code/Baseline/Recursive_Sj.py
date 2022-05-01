import sys
import getopt
import cplex
import numpy as np
import math
import time
import random
import os

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)
	if c > 0.5:
		return b
	else:
		return -b

def ReadInput():
	global input_path
	global users
	global tuples
	global aggregation_values
	global num_users
	global num_tuples
	global query_result

	id_dict = {}
	id_num = 0

	users = []
	tuples = []
	aggregation_value_dict = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_ = []
		aggregation_value = float(elements[0])

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

		if tuple_ in aggregation_value_dict.keys():
			aggregation_value_dict[tuple_] += aggregation_value
		else:
			tuples.append(tuple_)
			aggregation_value_dict[tuple_] = aggregation_value

	query_result = sum(aggregation_value_dict.values())

	num_users = len(users)
	num_tuples = len(tuples)

	aggregation_values = []
	for tuple_ in tuples:
		aggregation_values.append(aggregation_value_dict[tuple_])

def RunHLP(num):
	global users
	global tuples
	global aggregation_values
	global num_users
	global num_tuples
	global query_result

	print("HLP", num)
	
	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)
	
	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None) 

	obj = np.append(np.zeros(num_users), np.array(aggregation_values))
	ub = np.append(np.ones(num_users), np.array([cplex.infinity] * num_tuples))
	cpx.variables.add(obj=obj, ub=ub)

	rhs = np.zeros(2 * num_tuples + 2)
	senses = "L" * (2 * num_tuples + 2)

	cols = []
	rows = []
	vals = []

	for i in range(num_tuples):
		temp_list = tuples[i]
		rhs[i] = len(temp_list) - 1
		rows.append(i)
		cols.append(num_users + i)
		vals.append(-1)

		for j in temp_list:
			rows.append(i)
			cols.append(j)
			vals.append(1)

	for i in range(num_tuples):
		rhs[i + num_tuples] = 0
		rows.append(i + num_tuples)
		cols.append(num_users + i)
		vals.append(-1)

	rhs[2 * num_tuples] = num
	for i in range(num_users):
		rows.append(2 * num_tuples)
		cols.append(i)
		vals.append(1)

	rhs[2 * num_tuples + 1] = -1 * num
	for i in range(num_users):
		rows.append(2 * num_tuples + 1)
		cols.append(i)
		vals.append(-1)
		
	cpx.linear_constraints.add(rhs=rhs, senses=senses)
	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
	cpx.solve()

	return cpx.solution.get_objective_value()
	
def RunGLP(num):
	global users
	global tuples
	global aggregation_values
	global num_users
	global num_tuples
	global query_result

	print("GLP", num)

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)
	
	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None) 

	obj = np.append(np.zeros(num_users + num_tuples), np.ones(1))
	ub = np.append(np.ones(num_users), np.array([cplex.infinity] * (num_tuples + 1)))
	cpx.variables.add(obj=obj, ub=ub)

	rhs = np.zeros(2 * num_tuples + 2 + num_users)
	senses = "L" * (2 * num_tuples + 2 + num_users)

	cols = []
	rows = []
	vals = []
	
	for i in range(num_tuples):
		temp_list = tuples[i]
		rhs[i] = len(temp_list) - 1
		rows.append(i)
		cols.append(num_users + i)
		vals.append(-1)

		for j in temp_list:
			rows.append(i)
			cols.append(j)
			vals.append(1)

	for i in range(num_tuples):
		rhs[i + num_tuples] = 0
		rows.append(i + num_tuples)
		cols.append(num_users + i)
		vals.append(-1)

	rhs[2 * num_tuples] = num
	for i in range(num_users):
		rows.append(2 * num_tuples)
		cols.append(i)
		vals.append(1)

	rhs[2 * num_tuples + 1] = -1 * num
	for i in range(num_users):
		rows.append(2 * num_tuples + 1)
		cols.append(i)
		vals.append(-1)

	for i in range(num_users):
		rows.append(2 * num_tuples + 2 + i)
		cols.append(num_users + num_tuples)
		vals.append(-1)

		rhs[2 * num_tuples + 2 + i] = 0

	for i in range(num_tuples):
		temp_list = tuples[i]

		for j in temp_list:
			rows.append(2 * num_tuples + 2 + j)
			cols.append(num_users + i)
			vals.append(aggregation_values[i])
	
	cpx.linear_constraints.add(rhs=rhs, senses=senses)
	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))
	cpx.solve()

	return cpx.solution.get_objective_value()

def RunRecursive():
	global users
	global tuples
	global aggregation_values
	global num_users
	global num_tuples
	global query_result
	global epsilon
	global delta

	left_i = 0
	right_i = num_users
	beta = epsilon / math.log2(1 / delta)

	while right_i - left_i > 1:
		mid_i = int((left_i + right_i) / 2)
		temp_x = RunGLP(num_users - mid_i)
		if temp_x <= 0:
			temp_x = -10000000
		else:
			temp_x = math.log(temp_x,math.e)
		temp_y = mid_i * beta
		if temp_x >= temp_y:
			left_i = mid_i
		else:
			right_i = mid_i

	delta = math.pow(math.e,right_i * beta)
	delta = delta * math.pow(math.e,1 + beta / epsilon * LapNoise())

	left_i = 0
	right_i = num_users

	while right_i - left_i > 1:
		mid_i = int((left_i + right_i) / 2)
		a_value = 0
		b_value = 0
		if mid_i - 1 >= 0:
			a_value = RunHLP(mid_i - 1) + (num_users - mid_i + 1) * delta
		else:
			a_value = RunHLP(0) + (num_users) * delta
		b_value = RunHLP(mid_i) + (num_users - mid_i) * delta
		
		if b_value <= a_value:
			left_i = mid_i
		else:
			right_i = mid_i   

	l_value = RunHLP(left_i) + (num_users - left_i) * delta
	r_value = RunHLP(right_i) + (num_users - right_i) * delta

	res = 0

	if l_value < r_value:
		res = l_value
	else:
		res = r_value
	res = res + LapNoise() * delta / epsilon
	
	# print("Query Result")
	# print(query_result)
	# print("Noised Result")
	# print(res)
	# print("Error")
	print(abs(res - query_result))

def main(argv):
	global input_path
	global epsilon
	global delta   
	
	try:
		opts, args = getopt.getopt(argv,"I:e:d:",["Input=","epsilon=","delta="])
	except getopt.GetoptError:
		print("Recursive_Sj.py -I <input file> -e <epsilon> -d <delta>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("Recursive_Sj.py -I <input file> -e <epsilon> -d <delta>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_path = arg
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)*0.5
		elif opt in ("-d","--delta"):
			delta = float(arg)
	
	start = time.time()

	ReadInput()
	RunRecursive()

	end= time.time()

	# print("Time")
	# print(end - start)

if __name__ == "__main__":
   main(sys.argv[1:])