import getopt
import math
import numpy as np
import os
import random
import sys
import time

def ReadInput():
	global input_path
	global upper_bound
	global error_level
	global check_fs
	global query_result

	check_fs = []

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	i = 0

	for line in input_file.readlines():
		if i == 1:
			query_result = float(line)

		check_fs.append(math.ceil(float(line) / error_level) * error_level)
		i += 1

def RunAlgorithm():
	global check_fs
	global query_result
	global epsilon
	global beta
	global upper_bound
	global error_level
	global error
	global output

	tau = math.ceil(2 / epsilon * math.log((upper_bound / error_level + 1) / beta))

	upper_check_fs = check_fs[ : tau + 2]
	mid_check_fs = check_fs[tau + 1]
	lower_check_fs = check_fs[tau + 1 : ]

	upper_differences = []
	lower_differences = []

	for i in range(len(upper_check_fs) - 1):
		upper_differences.append(upper_check_fs[i] - upper_check_fs[i + 1])
	for i in range(len(lower_check_fs) - 1):
		lower_differences.append(lower_check_fs[i] - lower_check_fs[i + 1])

	pdf = []
	cdf = []

	for i in range(len(upper_differences)):
		pdf.append(math.exp(epsilon / 2 * (-tau + i - 1)) * upper_differences[i])
	pdf.append(1)
	for i in range(len(lower_differences)):
		pdf.append(math.exp(epsilon / 2 * (-i - 1)) * lower_differences[i])

	for i in range(len(pdf)):
		cdf.append(sum(pdf[ : i + 1]))

	error = 1e10

	sample_1 = random.uniform(0, cdf[-1])
	matches = [x for x in cdf if x <= sample_1]
	index = len(matches)

	if index <= tau:
		sample_2 = math.floor(random.random() * upper_differences[index] / error_level) * error_level
		output = upper_check_fs[index] - sample_2
		error = abs(upper_check_fs[index] - sample_2 - query_result)
	elif index == tau + 1:
		output = mid_check_fs
		error = abs(mid_check_fs - query_result)
	elif index > tau + 1:
		sample_2 = math.floor(random.random() * lower_differences[index - tau - 2] / error_level) * error_level
		output = lower_check_fs[index - tau - 2] - sample_2 - error_level
		error = abs(lower_check_fs[index - tau - 2] - sample_2 - error_level - query_result)

def main(argv):
	global input_path
	global epsilon
	global beta
	global upper_bound
	global error_level
	global output
	global error

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:d:", ["InputPath=", "epsilon=", "beta=", "UpperBound=", "ErrorLevel="])
	except getopt.GetoptError:
		print("Exponential.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("Exponential.py -I <input path> -e <epsilon> -b <beta> -D <upper bound> -d <error level>")
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

	start = time.time()

	ReadInput()
	RunAlgorithm()

	end = time.time()

	print(str(error) + " " + str(output) + " " + str(query_result) + " " + str(end - start))

if __name__ == "__main__":
	main(sys.argv[1 : ])