import getopt
import math
import os
import sys
import time

def ReadInput():
	global input_path
	global index
	global num_users
	global value_list
	global query_result

	id_dict = {}
	id_num = 0

	value_list = []

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		value_list.append((user_id, tuple_value))

	num_users = len(id_dict)
	value_list = sorted(value_list, reverse=True, key=lambda item: item[1])
	if index > len(value_list):
		query_result = 0
	else:
		query_result = value_list[index - 1][1]

def ComputeValues(tau):
	global check_fs
	global num_users
	global value_list
	global index

	j = 0
	counters = {}
	check_fs = [0] * (2 * tau + 2)

	if index > len(value_list):
		return

	for i in range(num_users):
		counters[i] = 0

	num = 0
	for tuple_ in value_list:
		if num <= index - 1:
			counters[tuple_[0]] += 1
			num += 1

			continue
		else:
			counters_list = sorted(counters.values(), reverse=True)

			if sum(counters_list[j : ]) <= index - 1:
				check_fs[j] = tuple_[1]
			else:
				j += 1

				if j > 2 * tau + 1:
					return

				check_fs[j] = tuple_[1]

			counters[tuple_[0]] += 1

def RunAlgorithm():
	global check_fs
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path
	global index

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	ComputeValues(tau)

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

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:d:O:k:", ["InputPath=", "epsilon=", "beta=", "UpperBound=", "ErrorLevel=", "OutputPath=", "index="])
	except getopt.GetoptError:
		print("ComputeR_Selection.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path> -k <index>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ComputeR_Selection.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path>  -k <index>")
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

	ReadInput()
	RunAlgorithm()

if __name__ == "__main__":
	main(sys.argv[1 : ])