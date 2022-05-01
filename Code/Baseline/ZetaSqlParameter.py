import getopt
import math
import os
import random
import sys
import time

def ReadInput():
	global input_path
	global max_value_dict

	id_dict = {}
	id_num = 0

	max_value_dict = {}

	cur_path = os.getcwd() + '/'
	input_file = open(cur_path + input_path, 'r')

	for line in input_file.readlines():
		elements = line.split()

		max_value = float(elements[0])
		user_id = int(elements[1])

		if user_id in id_dict.keys():
			user_id = id_dict[user_id]
		else:
			id_dict[user_id] = id_num
			user_id = id_num
			id_num += 1

		tuple_ = (user_id)

		if tuple_ in max_value_dict.keys():
			if max_value > max_value_dict[tuple_]:
				max_value_dict[tuple_] = max_value
		else:
			max_value_dict[tuple_] = max_value

def GetLeftIndex(max_value_dict, size, x):
	l = 0
	h = size - 1

	while (l < h):
		mid = math.ceil((l + h) / 2)
		if (max_value_dict[mid][1] > x):
			h = mid - 1
		else:
			l = mid

	return l

def GetRightIndex(max_value_dict, size, x):
	l = 0
	h = size - 1

	while (l < h):
		mid = math.ceil((l + h) / 2)
		if (max_value_dict[mid][1] <= x):
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

def RunAlgorithm():
	global max_value_dict
	global epsilon
	global beta
	global upper_bound

	max_value_dict = sorted(list(max_value_dict.items()), key=lambda item: item[1])

	num_bins = math.ceil(math.log(upper_bound, 2))
	counts = [0] * (num_bins + 1)

	for i in range(num_bins + 1):
		if i == 0:
			left_index = GetLeftIndex(max_value_dict, len(max_value_dict), 0)
		else:
			left_index = GetLeftIndex(max_value_dict, len(max_value_dict), math.pow(2, i - 1))
		right_index = GetRightIndex(max_value_dict, len(max_value_dict), math.pow(2, i))

		counts[i] = right_index - left_index

	threshold = -1 / epsilon * math.log(1 - math.pow(beta, 1 / (num_bins - 1)))

	for i in range(num_bins, -1, -1):
		aaa = counts[i] + 2 * LapNoise() / epsilon

		if aaa > threshold:
			return math.pow(2, i)

	return 1

def main(argv):
	global input_path
	global epsilon
	global beta
	global upper_bound

	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:D:", ["InputPath=", "epsilon=", "beta=", "UpperBound="])
	except getopt.GetoptError:
		print("ZetaSqlParameter.py -I <input path> -e <epsilon> -b <beta> -D <upper bound>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ZetaSqlParameter.py -I <input path> -e <epsilon> -b <beta> -D <upper bound>")
			sys.exit()
		elif opt in ("-I", "--InputPath"):
			input_path = str(arg)
		elif opt in ("-e", "--epsilon"):
			epsilon = float(arg)
		elif opt in ("-b", "--beta"):
			beta = float(arg)
		elif opt in ("-D", "--UpperBound"):
			upper_bound = int(arg)

	ReadInput()
	ans = RunAlgorithm()

	print(ans)

if __name__ == "__main__":
	main(sys.argv[1 : ])