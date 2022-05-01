import os
import sys
import getopt
import math
import time
import random

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
	global aggregation_value_list
	global num_tuples
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

	num_tuples = len(aggregation_value_dict.values())
	query_result = sum(aggregation_value_dict.values())

	aggregation_value_list = sorted(aggregation_value_dict.values())

def RunHLP(num):
	global aggregation_value_list

	return sum(aggregation_value_list[ : num])
	
def RunGLP(num):
	global aggregation_value_list

	return aggregation_value_list[num]

def RunRecursive():
	global epsilon
	global delta
	global output

	left_i = 0
	right_i = num_tuples
	beta = epsilon / math.log2(1 / delta)

	while right_i - left_i > 1:
		mid_i = int((left_i + right_i) / 2)
		temp_x = RunGLP(num_tuples - mid_i)

		if temp_x <= 0:
			temp_x = -10000000
		else:
			temp_x = math.log(temp_x, math.e)

		temp_y = mid_i * beta
		if temp_x >= temp_y:
			left_i = mid_i
		else:
			right_i = mid_i

	delta = math.pow(math.e, right_i * beta)
	delta *= math.pow(math.e, 1 + beta / epsilon * LapNoise())

	left_i = 0
	right_i = num_tuples

	while right_i - left_i > 1:
		mid_i = int((left_i + right_i) / 2)
		a_value = 0
		b_value = 0

		if mid_i >= 1:
			a_value = RunHLP(mid_i - 1) + (num_tuples - mid_i + 1) * delta
		else:
			a_value = RunHLP(0) + (num_tuples) * delta
		b_value = RunHLP(mid_i) + (num_tuples - mid_i) * delta
		
		if b_value <= a_value:
			left_i = mid_i
		else:
			right_i = mid_i

	l_value = RunHLP(left_i) + (num_tuples - left_i) * delta
	r_value = RunHLP(right_i) + (num_tuples - right_i) * delta

	if l_value < r_value:
		output = l_value
	else:
		output = r_value

	output += LapNoise() * delta / epsilon

def main(argv):
	global input_path
	global epsilon
	global delta
	global query_result
	global output
	
	try:
		opts, args = getopt.getopt(argv,"I:e:d:",["Input=","epsilon=","delta="])
	except getopt.GetoptError:
		print("Recursive.py -I <input file> -e <epsilon> -d <delta>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("Recursive.py -I <input file> -e <epsilon> -d <delta>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_path = arg
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg) * 0.5
		elif opt in ("-d","--delta"):
			delta = float(arg)
	
	start = time.time()

	ReadInput()
	RunRecursive()

	end= time.time()

	# print("Query Result")
	# print(query_result)
	# print("Noised Result")
	# print(output)
	# print("Error")
	print(abs(output - query_result))
	# print("Time")
	# print(end - start)

if __name__ == "__main__":
   main(sys.argv[1:])