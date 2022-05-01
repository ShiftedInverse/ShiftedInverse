import getopt
import math
import os
import random
import sys
import time

from collections import Counter

def GetIndex(value):
	global num_nodes
	global num_leaves
	global leftmost_leaf_index
	global upper_bound

	return leftmost_leaf_index + int(math.floor(value / upper_bound * num_leaves))

def GetLeftValue(index):
	global num_nodes
	global num_leaves
	global leftmost_leaf_index
	global upper_bound

	while index < leftmost_leaf_index:
		index = GetLeftmostChild(index)

	return upper_bound * (index - leftmost_leaf_index) / num_leaves

def GetRightValue(index):
	global num_nodes
	global num_leaves
	global leftmost_leaf_index
	global upper_bound

	while index < leftmost_leaf_index:
		index = GetRightmostChild(index)

	return upper_bound * (index - leftmost_leaf_index + 1) / num_leaves

def GetLeftmostChild(index):
	global factor

	return index * factor + 1

def GetRightmostChild(index):
	global factor

	return (index + 1) * factor

def GetParent(index):
	global factor

	return math.floor((index - 1) / factor)

def ReadInput():
	global quantile_tree
	global input_path
	global max_partition
	global max_contribution
	global alpha
	global query_result

	id_dict = {}
	id_num = 0

	value_list = []
	quantile_tree = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		tuple_value = min(upper_bound, max(0, float(elements[0])))
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		value_list.append((user_id, GetIndex(tuple_value), tuple_value))
	
	num_users = len(id_dict)

	value_list = sorted(value_list, key=lambda item: item[2])
	query_result = value_list[min(len(value_list) - 1, int(len(value_list) * alpha))][2]

	value_list = sorted(value_list, key=lambda item: item[0])

	user_id = 0
	partitions = []

	for tuple_ in value_list:
		if tuple_[0] != user_id:
			partition_counter = Counter(partitions)
			partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])[ : max_partition]

			for index, count in partition_counter:
				count = min(count, max_contribution)

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
	partition_counter = sorted(list(partition_counter.items()), reverse=True, key=lambda item: item[1])[ : max_partition]

	for index, count in partition_counter:
		count = min(count, max_contribution)

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

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def GetNextIndexAndRank(rank, leftmost_child_index, rightmost_child_index, noised_quantile_tree):
	global num_leaves

	gamma = 0.0075
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

def RunAlgorithm():
	global epsilon
	global height
	global max_partition
	global max_contribution
	global alpha
	global quantile_tree
	global num_nodes
	global num_leaves
	global leftmost_leaf_index
	global query_result
	global error

	index = 0
	rank = min(0.995, max(0.005, alpha))

	while index < leftmost_leaf_index:
		leftmost_child_index = GetLeftmostChild(index)
		rightmost_child_index = GetRightmostChild(index)

		noised_quantile_tree = {}
		for i in range(leftmost_child_index, rightmost_child_index + 1):
			if i in quantile_tree.keys():
				noised_quantile_tree[i] = quantile_tree[i] + LapNoise() * height * max_partition * max_contribution / epsilon
			else:
				noised_quantile_tree[i] = LapNoise() * height * max_partition * max_contribution / epsilon

		next_index, next_rank = GetNextIndexAndRank(rank, leftmost_child_index, rightmost_child_index, noised_quantile_tree)

		if next_index == -1:
			break
		else:
			index = next_index
			rank = next_rank

	ans = (1 - rank) * GetLeftValue(index) + rank * GetRightValue(index)
	error = abs(ans - query_result)

def main(argv):
	global input_path
	global epsilon
	global height
	global factor
	global max_partition
	global max_contribution
	global upper_bound
	global alpha
	global num_nodes
	global num_leaves
	global leftmost_leaf_index
	global error

	try:
		opts, args = getopt.getopt(argv,"h:I:e:d:f:P:C:D:a:", ["InputPath=", "epsilon=", "height=", "factor=", "MaxPartition=", "MaxContribution=", "UpperBound=", "alpha="])
	except getopt.GetoptError:
		print("ZetaSql.py -I <input path> -e <epsilon> -d <height> -f <branching factor> -P <max partition> -C <max contribution> -D <upper bound> -a <alpha>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ZetaSql.py -I <input path> -e <epsilon> -d <height> -f <branching factor> -P <max partition> -C <max contribution> -D <upper bound> -a <alpha>")
			sys.exit()
		elif opt in ("-I", "--InputPath"):
			input_path = str(arg)
		elif opt in ("-e", "--epsilon"):
			epsilon = float(arg)
		elif opt in ("-d", "--height"):
			height = int(arg)
		elif opt in ("-f", "--factor"):
			factor = int(arg)
		elif opt in ("-P", "--MaxPartition"):
			max_partition = int(arg)
		elif opt in ("-C", "--MaxContribution"):
			max_contribution = int(arg)
		elif opt in ("-D", "--UpperBound"):
			upper_bound = int(arg)
		elif opt in ("-a", "--alpha"):
			alpha = float(arg)

	num_nodes = int((math.pow(factor, height + 1) - 1)/ (factor - 1))
	num_leaves = int(math.pow(factor, height))
	leftmost_leaf_index = num_nodes - num_leaves

	ReadInput()
	RunAlgorithm()

	print(error)

if __name__ == "__main__":
	main(sys.argv[1 : ])