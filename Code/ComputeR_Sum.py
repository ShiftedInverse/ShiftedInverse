import getopt
import math
import os
import sys
import time

def ReadInput():
	global input_path
	global aggregation_value_dict
	global query_result

	id_dict = {}
	id_num = 0

	aggregation_value_dict = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		aggregation_value = float(elements[0])
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		tuple_ = (user_id)

		if tuple_ in aggregation_value_dict.keys():
			aggregation_value_dict[tuple_] += aggregation_value
		else:
			aggregation_value_dict[tuple_] = aggregation_value

	query_result = sum(aggregation_value_dict.values())

def RunAlgorithm():
	global aggregation_value_dict
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	aggregation_values = sorted(aggregation_value_dict.values())

	cur_path = os.getcwd() + '/'
	output_file = open(cur_path + output_path, 'w')

	output_file.write(str(upper_bound) + "\n")
	output_file.write(str(query_result) + "\n")
	for j in range(1, 2 * tau + 1):
		value = sum(aggregation_values[-j : ])
		output_file.write(str(query_result - value) + "\n")
	output_file.write("0\n")

def main(argv):
	global input_path
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output_path

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:d:O:", ["InputPath=", "epsilon=", "beta=", "UpperBound=", "ErrorLevel=", "OutputPath="])
	except getopt.GetoptError:
		print("ComputeR_Sum.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ComputeR_Sum.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level> -O <output path>")
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

	ReadInput()
	RunAlgorithm()

if __name__ == "__main__":
	main(sys.argv[1 : ])