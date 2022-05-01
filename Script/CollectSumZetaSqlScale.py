import math
import os
import random
import sys
import time

from collections import Counter

repeat_times = 10
queries = ["Q12", "Q18"]
relations = ["sc", "sc"]
upper_bounds = [10000, 1000000]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]
epsilons = [1]

def ReadInput(j, i):
	global value_list
	global query_result

	value_dict = {}
	query_result = 0

	input_file = open(cur_path + "/../Information/TPCH/" + scales[j] + "/" + queries[i] + ".txt", 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])
		user_id = int(elements[1])

		if user_id in value_dict.keys():
			value_dict[user_id] += tuple_value
		else:
			value_dict[user_id] = tuple_value

	value_list = sorted(value_dict.values())
	query_result = sum(value_list)

def GetLeftIndex(value_list, size, x):
	l = 0
	h = size - 1

	while (l < h):
		mid = math.ceil((l + h) / 2)
		if (value_list[mid] > x):
			h = mid - 1
		else:
			l = mid

	return l

def GetRightIndex(value_list, size, x):
	l = 0
	h = size - 1

	while (l < h):
		mid = math.ceil((l + h) / 2)
		if (value_list[mid] <= x):
			l = mid
		else:
			h = mid - 1

	return h

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def GetC(i, epsilon_0):
	global value_list

	beta = 0.999999
	upper_bound = upper_bounds[i]

	num_bins = math.ceil(math.log(upper_bound, 2))
	counts = [0] * (num_bins + 1)

	for j in range(num_bins + 1):
		if j == 0:
			left_index = GetLeftIndex(value_list, len(value_list), 0)
		else:
			left_index = GetLeftIndex(value_list, len(value_list), math.pow(2, j - 1))
		right_index = GetRightIndex(value_list, len(value_list), math.pow(2, j))

		counts[j] = right_index - left_index

	threshold = -1 / epsilon_0 * math.log(1 - math.pow(beta, 1 / (num_bins - 1)))

	for j in range(num_bins, -1, -1):
		aaa = counts[j] + LapNoise() / epsilon_0

		if aaa > threshold:
			return math.pow(2, j)

	return 1

def Sum():
	global value_list
	global query_result

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				start = time.time()

				ReadInput(j, i)

				bound = GetC(i, epsilon / 2)

				end = time.time()

				sum_time += end - start

				sum_time_2 = 0

				for k in range(repeat_times):
					start = time.time()

					ans = 0

					for value_ in value_list:
						ans += min(bound, value_)

					ans += LapNoise() * bound / epsilon * 2

					error = abs(ans - query_result)
					errors.append(error)

					end = time.time()

					sum_time_2 += end - start

				errors.sort()

				output_file.write(scales[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time + sum_time_2 / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " ")
				output_file.write(str(bound) + "\n")
				output_file.flush()

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultSumZetaSqlScale.txt", 'w')

	Sum()

if __name__ == "__main__":
	main(sys.argv[1:])