import math
import os
import random
import sys
import time

from collections import Counter

repeat_times = 100
queries = ["Q18", "Q9"]
relations = ["sc", "sc"]
Ps = [256, 2048]
Cs = [32, 256]
upper_bounds = [100000, 100000]
lower_bounds = [0, -100000]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]
epsilons = [1]
alphas = [1, 0, 0.5, 0.75]

factor = 16
height = 4
num_nodes = int((math.pow(factor, height + 1) - 1)/ (factor - 1))
num_leaves = int(math.pow(factor, height))
leftmost_leaf_index = num_nodes - num_leaves

new_Ps = [0, 0]
new_Cs = [0, 0]
new_upper_bounds = [0, 0]
new_lower_bounds = [0, 0]

median_answer = {}
median_answer[0.5] = {"Q18_0": 26, "Q18_1": 26, "Q18_2": 26, "Q18_3": 26, "Q18_4": 26, "Q18_5": 26, "Q9_0": 17.8239432, "Q9_1": 18.0766042, "Q9_2": 18.6889626, "Q9_3": 19.8681264, "Q9_4": 19.86452, "Q9_5": 19.860612}
median_answer[0.25] = {"Q18_0": 38, "Q18_1": 38, "Q18_2": 38, "Q18_3": 38, "Q18_4": 38, "Q18_5": 38, "Q9_0": 31.842036, "Q9_1": 32.28512, "Q9_2": 33.052224, "Q9_3": 34.7351472, "Q9_4": 34.702224, "Q9_5": 34.7040832}
median_answer[0] = {"Q18_0": 50, "Q18_1": 50, "Q18_2": 50, "Q18_3": 50, "Q18_4": 50, "Q18_5": 50, "Q9_0": 94.085, "Q9_1": 95.137, "Q9_2": 97.454015, "Q9_3": 104.069, "Q9_4": 103.1225, "Q9_5": 102.873}
median_answer[1] = {"Q18_0": 1, "Q18_1": 1, "Q18_2": 1, "Q18_3": 1, "Q18_4": 1, "Q18_5": 1, "Q9_0": -8.209999, "Q9_1": -7.49064, "Q9_2": -8.917, "Q9_3": -8.043545, "Q9_4": -8.85555, "Q9_5": -8.43456}

def GetRankError(i, scale, output_value, alpha):
	file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')

	num = 0
	num_2 = 0
	total_num = 0

	for line in file.readlines():
		line = line.split()
		value = float(line[0])

		if value > output_value:
			num += 1
		elif value >= output_value - 1e-5:
			num_2 += 1

		total_num += 1

	error_1 = abs(num - total_num * alpha)
	error_2 = abs((num + num_2) - total_num * alpha)

	error = min(error_1, error_2)

	return error, error / total_num * 100

def GetIndex(value, i):
	return leftmost_leaf_index + int(math.floor(value / (new_upper_bounds[i] - new_lower_bounds[i]) * num_leaves))

def GetLeftValue(index, i):
	while index < leftmost_leaf_index:
		index = GetLeftmostChild(index)

	return new_upper_bounds[i] * (index - leftmost_leaf_index) / num_leaves

def GetRightValue(index, i):
	while index < leftmost_leaf_index:
		index = GetRightmostChild(index)

	return new_upper_bounds[i] * (index - leftmost_leaf_index + 1) / num_leaves

def GetLeftmostChild(index):
	return index * factor + 1

def GetRightmostChild(index):
	return (index + 1) * factor

def GetParent(index):
	return math.floor((index - 1) / factor)

def ReadInput(scale, i):
	id_dict = {}
	id_num = 0

	value_list = []
	quantile_tree = {}

	input_file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')
	output_file_C = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_C.txt", 'w')
	output_file_P = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_P.txt", 'w')

	for line in input_file.readlines():
		elements = line.split()

		tuple_value = min(new_upper_bounds[i] - new_lower_bounds[i], max(0, float(elements[0])))
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		value_list.append((user_id, GetIndex(tuple_value, i), tuple_value))
	
	num_users = len(id_dict)

	value_list = sorted(value_list, key=lambda item: item[2])
	value_list = sorted(value_list, key=lambda item: item[0])

	user_id = 0
	partitions = []

	for tuple_ in value_list:
		if tuple_[0] != user_id:
			partition_counter = Counter(partitions)
			partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])

			output_file_P.write(str(len(partition_counter)) + " " + str(tuple_[0]) + "\n")
			output_file_C.write(str(partition_counter[0][1]) + " " + str(tuple_[0]) + "\n")

			user_id = tuple_[0]
			partitions = []
		
		partitions.append(tuple_[1])

	partition_counter = Counter(partitions)
	partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])

	output_file_P.write(str(len(partition_counter)) + " " + str(tuple_[0]) + "\n")
	output_file_C.write(str(partition_counter[0][1]) + " " + str(tuple_[0]) + "\n")

def ProcessMaxMin(scale, i):
	read_file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')
	write_file_max = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_max.txt", 'w')
	write_file_min = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_min.txt", 'w')

	upper_bound = upper_bounds[i]
	lower_bound = lower_bounds[i]

	for line in read_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])

		if tuple_value >= 0:
			write_file_max.write(str(tuple_value) + " ")

			for j in range(1, len(elements) - 1):
				write_file_max.write(elements[j] + " ")

			write_file_max.write(elements[len(elements) - 1] + "\n")
		else:
			write_file_min.write(str(-tuple_value) + " ")

			for j in range(1, len(elements) - 1):
				write_file_min.write(elements[j] + " ")

			write_file_min.write(elements[len(elements) - 1] + "\n")

def GetUpperBound(scale, i, epsilon_0):
	cmd = "../python/python " + cur_path + "/../Code/Baseline/ZetaSqlParameter.py -I ../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_max.txt -e " + str(epsilon_0) + " -b 0.999999 -D " + str(upper_bounds[i])
						
	shell = os.popen(cmd, 'r')
	res = shell.read()
	res = res.split()

	new_upper_bounds[i] = int(float(res[0]))

	shell.close()

def GetLowerBound(scale, i, epsilon_0):
	cmd = "../python/python " + cur_path + "/../Code/Baseline/ZetaSqlParameter.py -I ../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_min.txt -e " + str(epsilon_0) + " -b 0.999999 -D " + str(-lower_bounds[i])
						
	shell = os.popen(cmd, 'r')
	res = shell.read()
	res = res.split()

	new_lower_bounds[i] = -int(float(res[0]))

	shell.close()

def GetC(scale, i, epsilon_0):
	cmd = "../python/python " + cur_path + "/../Code/Baseline/ZetaSqlParameter.py -I ../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_C.txt -e " + str(epsilon_0) + " -b 0.999999 -D " + str(Cs[i])
						
	shell = os.popen(cmd, 'r')
	res = shell.read()
	res = res.split()

	new_Cs[i] = int(float(res[0]))

	shell.close()

def GetP(scale, i, epsilon_0):
	cmd = "../python/python " + cur_path + "/../Code/Baseline/ZetaSqlParameter.py -I ../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_P.txt -e " + str(epsilon_0) + " -b 0.999999 -D " + str(Ps[i])
						
	shell = os.popen(cmd, 'r')
	res = shell.read()
	res = res.split()

	new_Ps[i] = int(float(res[0]))

	shell.close()

def ConstructTree(scale, i, alpha):
	id_dict = {}
	id_num = 0

	value_list = []
	quantile_tree = {}

	input_file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_value = min(new_upper_bounds[i], max(0, float(elements[0])))
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		value_list.append((user_id, GetIndex(tuple_value, i), tuple_value))
	
	num_users = len(id_dict)

	value_list = sorted(value_list, key=lambda item: item[2])
	query_result = value_list[min(len(value_list) - 1, int(len(value_list) * alpha))][2]

	value_list = sorted(value_list, key=lambda item: item[0])

	user_id = 0
	partitions = []

	for tuple_ in value_list:
		if tuple_[0] != user_id:
			partition_counter = Counter(partitions)
			partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])[ : new_Ps[i]]

			for index, count in partition_counter:
				count = min(count, new_Cs[i])

				while index > 0:
					if index in quantile_tree.keys():
						quantile_tree[index] += count
					else:
						quantile_tree[index] = count

					index = GetParent(index)

					if index in quantile_tree.keys():
						quantile_tree[index] += count
					else:
						quantile_tree[index] = count

			user_id = tuple_[0]
			partitions = []
		
		partitions.append(tuple_[1])

	partition_counter = Counter(partitions)
	partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])[ : new_Ps[i]]

	for index, count in partition_counter:
		count = min(count, new_Cs[i])

		while index > 0:
			if index in quantile_tree.keys():
				quantile_tree[index] += count
			else:
				quantile_tree[index] = count

			index = GetParent(index)

			if index in quantile_tree.keys():
				quantile_tree[index] += count
			else:
				quantile_tree[index] = count

	return quantile_tree, query_result

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def GetNextIndexAndRank(rank, leftmost_child_index, rightmost_child_index, noised_quantile_tree):
	gamma = 1e-3
	tolerance = 1e-6

	total_count = 0
	for i in range(leftmost_child_index, rightmost_child_index + 1):
		total_count += max(0.0, noised_quantile_tree[i])

	corrected_total_count = 0
	for i in range(leftmost_child_index, rightmost_child_index + 1):
		if noised_quantile_tree[i] >= total_count * gamma:
			corrected_total_count += noised_quantile_tree[i]
	if corrected_total_count == 0:
		return -1, -1

	partial_count = 0
	for i in range(leftmost_child_index, rightmost_child_index + 1):
		count = noised_quantile_tree[i]
		if count >= total_count * gamma:
			partial_count += count
			if partial_count / corrected_total_count >= rank - tolerance:
				next_rank = (rank - (partial_count - count) / corrected_total_count) / (count / corrected_total_count)
				next_rank = min(1, max(0, next_rank))
				return i, next_rank

def RunAlgorithm(i, epsilon_0, alpha, quantile_tree, query_result):
	index = 0
	rank = min(0.95, max(0.05, alpha))

	while index < leftmost_leaf_index:
		leftmost_child_index = GetLeftmostChild(index)
		rightmost_child_index = GetRightmostChild(index)

		noised_quantile_tree = {}
		for j in range(leftmost_child_index, rightmost_child_index + 1):
			if j in quantile_tree.keys():
				noised_quantile_tree[j] = quantile_tree[j] + LapNoise() * height * new_Ps[i] * new_Cs[i] / epsilon_0
			else:
				noised_quantile_tree[j] = LapNoise() * height * new_Ps[i] * new_Cs[i] / epsilon_0

		next_index, next_rank = GetNextIndexAndRank(rank, leftmost_child_index, rightmost_child_index, noised_quantile_tree)

		if next_index == -1:
			break
		else:
			index = next_index
			rank = next_rank

	ans = (1 - rank) * GetLeftValue(index, i) + rank * GetRightValue(index, i)

	return ans

def Selection():
	for alpha in alphas:
		for i in range(len(queries)):
			for scale in scales:
				for epsilon in epsilons:
					if lower_bounds[i] == 0:
						epsilon_0 = epsilon / 4
					else:
						epsilon_0 = epsilon / 5

					sum_time = 0
					errors = []
					percentiles = []
					absolute_errors = []

					start = time.time()

					ProcessMaxMin(scale, i)
					GetUpperBound(scale, i, epsilon_0)

					if lower_bounds[i] < 0:
						GetLowerBound(scale, i, epsilon_0)

					ReadInput(scale, i)

					GetC(scale, i, epsilon_0)
					GetP(scale, i, epsilon_0)

					quantile_tree, query_result = ConstructTree(scale, i, alpha)

					end = time.time()

					sum_time += end - start

					sum_time_2 = 0

					for j in range(repeat_times):
						start = time.time()

						ans = RunAlgorithm(i, epsilon_0, alpha, quantile_tree, query_result)

						end = time.time()

						sum_time_2 += end - start

						query_answer = median_answer[1 - alpha][queries[i] + scale]

						if abs(query_answer - ans) <= 1e-5:
							error = 0
							percentile = 0
						else:
							error, percentile = GetRankError(i, scale, ans, 1 - alpha)
						
						errors.append(error)
						percentiles.append(percentile)
						absolute_errors.append(abs(query_answer - ans))

					os.remove(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_max.txt")
					os.remove(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_min.txt")
					os.remove(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_C.txt")
					os.remove(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_ZetaSql_P.txt")

					errors.sort()
					percentiles.sort()
					absolute_errors.sort()

					if alpha == 0:
						alpha_name = "_min"
					elif alpha == 1:
						alpha_name = "_max"
					else:
						alpha_name = "_median_" + str(alpha)

					output_file.write(scale + " " + queries[i] + alpha_name + " " + str(epsilon) + " " + str(sum_time + sum_time_2 / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(percentiles[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(absolute_errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " ")
					output_file.write(str(new_upper_bounds[i]) + " " + str(new_lower_bounds[i]) + " " + str(new_Cs[i]) + " " + str(new_Ps[i]) + "\n")
					output_file.flush()

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultSelectionZetaSqlScale.txt", 'w')

	Selection()

if __name__ == "__main__":
	main(sys.argv[1:])