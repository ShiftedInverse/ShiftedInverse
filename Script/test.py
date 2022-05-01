import math
import multiprocessing
import os
import sys
import time

repeat_times = 10
queries = ["Q9", "Q18"]
relations = ["sc", "sc"]
folders = ["", ""]
upper_bounds = [100000, 100000]
upper_bounds_count = [800000000, 800000000]
lower_bounds = [-100000, 0]
error_levels = [0.01, 0.01]
error_levels_count = [10, 10]

repeat_times_Sj = 5
queries_Sj = ["Q7"]
relations_Sj = ["sc"]
folders_Sj = ["_Sj"]
upper_bounds_Sj = [100000]
upper_bounds_count_Sj = [800000000]
lower_bounds_Sj = [0]
error_levels_Sj = [0.1]
error_levels_count_Sj = [10]

scales = ["_3"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

median_answer = {}
median_answer[0.5] = {"Q18_0": 26, "Q18_1": 26, "Q18_2": 26, "Q18_3": 26, "Q18_4": 26, "Q18_5": 26, "Q9_0": 100017.8239432, "Q9_1": 100018.0766042, "Q9_2": 100018.6889626, "Q9_3": 100019.8681264, "Q9_4": 100019.86452, "Q9_5": 100019.860612, "Q7_0": 32.752863, "Q7_1": 33.1092, "Q7_2": 33.657876, "Q7_3": 34.856586, "Q7_4": 34.863892, "Q7_5": 34.855592}
median_answer[0.25] = {"Q18_0": 38, "Q18_1": 38, "Q18_2": 38, "Q18_3": 38, "Q18_4": 38, "Q18_5": 38, "Q9_0": 100031.842036, "Q9_1": 100032.28512, "Q9_2": 100033.052224, "Q9_3": 100034.7351472, "Q9_4": 100034.702224, "Q9_5": 100034.7040832, "Q7_0": 49.1995944, "Q7_1": 49.6359936, "Q7_2": 50.5904469, "Q7_3": 52.4329988, "Q7_4": 52.3946592, "Q7_5": 52.388832}
median_answer[0.1] = {"Q18_0": 46, "Q18_1": 46, "Q18_2": 45, "Q18_3": 45, "Q18_4": 45, "Q18_5": 45, "Q9_0": 100045.8825938, "Q9_1": 100046.4024596, "Q9_2": 100047.32917, "Q9_3": 100049.3353, "Q9_4": 100049.3273272, "Q9_5": 100049.3270875, "Q7_0": 63.9321228, "Q7_1": 64.3972308, "Q7_2": 65.4092436, "Q7_3": 67.5144162, "Q7_4": 67.500864, "Q7_5": 67.5103554}

manager = multiprocessing.Manager()

p = 10
p2 = 10

# def GetRankError(i, scale, output_value, alpha):
# 	file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')

# 	num = 0
# 	num_2 = 0
# 	total_num = 0

# 	for line in file.readlines():
# 		line = line.split()
# 		value = float(line[0])

# 		if value > output_value:
# 			num += 1
# 		elif value >= output_value - 1e-5:
# 			num_2 += 1

# 		total_num += 1

# 	error_1 = abs(num - total_num * alpha)
# 	error_2 = abs((num + num_2) - total_num * alpha)

# 	error = min(error_1, error_2)

# 	return error, error / total_num * 100

def GetRankError_Sj(i, scale, output_value, alpha):
	file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries_Sj[i] + ".txt", 'r')

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

# def ProcessMedian(scale, i, k):
# 	read_file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries[i] + ".txt", 'r')
# 	write_file_median = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries[i] + "_median_" + str(k) + ".txt", 'w')

# 	upper_bound = upper_bounds[i]
# 	lower_bound = lower_bounds[i]

# 	for line in read_file.readlines():
# 		elements = line.split()

# 		tuple_value = float(elements[0])

# 		write_file_median.write(str(tuple_value - lower_bound) + " ")

# 		for j in range(1, len(elements) - 1):
# 			write_file_median.write(elements[j] + " ")

# 		write_file_median.write(elements[len(elements) - 1] + "\n")

# def ProcessMedian_Sj(scale, i):
# 	read_file = open(cur_path + "/../Information/TPCH/" + scale + "/" + queries_Sj[i] + ".txt", 'r')
# 	write_file_median = open(cur_path + "/../Temp/TPCH" + scale + "_" + queries_Sj[i] + "_median.txt", 'w')

# 	upper_bound = upper_bounds_Sj[i]
# 	lower_bound = lower_bounds_Sj[i]

# 	for line in read_file.readlines():
# 		elements = line.split()

# 		tuple_value = float(elements[0])

# 		write_file_median.write(str(tuple_value - lower_bound) + " ")

# 		for j in range(1, len(elements) - 1):
# 			write_file_median.write(elements[j] + " ")

# 		write_file_median.write(elements[len(elements) - 1] + "\n")

# def ThresholdRunAlgorithm(js, j, i, epsilon, percent):
# 	global times
# 	global errors
# 	global percentiles
# 	global absolute_errors

# 	for k in js:
# 		start = time.time()

# 		cmd = "../python/python " + cur_path + "/../Code/ComputeR_Sum" + folders[i] + ".py -I ../Information/TPCH/" + scales[j] + "/" + queries[i] + "_count.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(int(upper_bounds_count[i] * math.pow(2, j))) + " -d " + str(int(error_levels_count[i])) + " -O ../Temp/TPCH" + scales[j] + "_Sum" + folders[i] + "_" + queries[i] + "_count_" + str(epsilon / 2) + "_" + str(k) + ".txt"

# 		shell = os.popen(cmd, 'r')
# 		shell.read()
# 		shell.close()

# 		cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Temp/TPCH" + scales[j] + "_Sum" + folders[i] + "_" + queries[i] + "_count_" + str(epsilon / 2) + "_" + str(k) + ".txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(int(upper_bounds_count[i] * math.pow(2, j))) + " -d " + str(int(error_levels_count[i]))

# 		shell = os.popen(cmd, 'r')
# 		res = shell.read()
# 		res = res.split()

# 		index = int(float(res[1]) * percent)

# 		shell.close()

# 		ProcessMedian(scales[j], i, k)

# 		cmd = "../python/python " + cur_path + "/../Code/ComputeR_Selection" + folders[i] + ".py -I ../Temp/TPCH" + scales[j] + "_" + queries[i] + "_median_" + str(k) + ".txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Temp/TPCH" + scales[j] + "_Selection" + folders[i] + "_" + queries[i] + "_" + str(epsilon) + "_median_" + str(k) + ".txt -k " + str(index)

# 		shell = os.popen(cmd, 'r')
# 		shell.read()
# 		shell.close()

# 		cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Temp/TPCH" + scales[j] + "_Selection" + folders[i] + "_" + queries[i] + "_" + str(epsilon) + "_median_" + str(k) + ".txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds[i]) + " -d " + str(error_levels[i])
					
# 		shell = os.popen(cmd, 'r')
# 		res = shell.read()
# 		res = res.split()

# 		shell.close()

# 		end = time.time()

# 		output_value = float(res[1])
# 		if queries[i] == "Q9":
# 			output_value -= 100000

# 		answer = median_answer[percent][queries[i] + scales[j]]
		
# 		if abs(float(res[1]) - answer) <= 1e-5:
# 			error = 0
# 			percentile = 0
# 		else:
# 			error, percentile = GetRankError(i, scales[j], output_value, percent)
		
# 		errors[k] = error
# 		percentiles[k] = percentile
# 		absolute_errors[k] = abs(float(res[1]) - answer)

# 		times[k] = end - start

# 		os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_" + queries[i] + "_median_" + str(k) + ".txt")
# 		os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_Sum" + folders[i] + "_" + queries[i] + "_count_" + str(epsilon / 2) + "_" + str(k) + ".txt")
# 		os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_Selection" + folders[i] + "_" + queries[i] + "_" + str(epsilon) + "_median_" + str(k) + ".txt")

# def SelectionMedian(percent):
# 	global times
# 	global errors
# 	global percentiles
# 	global absolute_errors

# 	for i in range(len(queries)):
# 		for j in range(len(scales)):
# 			for epsilon in epsilons:
# 				times = manager.dict()
# 				errors = manager.dict()
# 				percentiles = manager.dict()
# 				absolute_errors = manager.dict()

# 				arrangement_of_js = []
# 				for k in range(p):
# 					arrangement_of_js.append([])

# 				l = 0
# 				for k in range(repeat_times):
# 					arrangement_of_js[l].append(k)

# 					l = (l + 1) % p

# 				threads = []

# 				for k in range(p):
# 					threads.append(multiprocessing.Process(target=ThresholdRunAlgorithm, args=(arrangement_of_js[k], j, i, epsilon, percent, )))	
# 					threads[k].start()

# 				for k in range(p):
# 					threads[k].join()

# 				sum_time = sum(times.values())
# 				errors = errors.values()
# 				percentiles = percentiles.values()
# 				absolute_errors = absolute_errors.values()

# 				errors.sort()
# 				percentiles.sort()
# 				absolute_errors.sort()

# 				output_file.write(scales[j] + " " + queries[i] + "_median_" + str(1 - percent) + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(percentiles[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(absolute_errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
# 				output_file.flush()

# def SelectionMedian_Sj(percent):
# 	for i in range(len(queries_Sj)):
# 		for j in range(len(scales)):
# 			epsilon = 1
# 			sum_time_Sj = 0
# 			errors_Sj = []

# 			for k in range(repeat_times_Sj):
# 				start = time.time()

# 				cmd = "../jr_python/python " + cur_path + "/../Code/ComputeR_Sum" + folders_Sj[i] + ".py -I ../Information/TPCH/" + scales[j] + "/" + queries_Sj[i] + "_count.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(int(upper_bounds_count_Sj[i] * math.pow(2, j))) + " -d " + str(int(error_levels_count_Sj[i])) + " -O ../Temp/TPCH" + scales[j] + "_Sum" + folders_Sj[i] + "_" + queries_Sj[i] + "_count_" + str(epsilon / 2) + ".txt -p " + str(p2)

# 				shell = os.popen(cmd, 'r')
# 				shell.read()
# 				shell.close()

# 				cmd = "../jr_python/python " + cur_path + "/../Code/Exponential.py -I ../Temp/TPCH" + scales[j] + "_Sum" + folders_Sj[i] + "_" + queries_Sj[i] + "_count_" + str(epsilon / 2) + ".txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(int(upper_bounds_count_Sj[i] * math.pow(2, j))) + " -d " + str(int(error_levels_count_Sj[i]))

# 				shell = os.popen(cmd, 'r')
# 				res = shell.read()
# 				res = res.split()

# 				index = int(float(res[1]) * percent)

# 				shell.close()

# 				ProcessMedian_Sj(scales[j], i)

# 				cmd = "../jr_python/python " + cur_path + "/../Code/ComputeR_Selection" + folders_Sj[i] + ".py -I ../Temp/TPCH" + scales[j] + "_" + queries_Sj[i] + "_median.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds_Sj[i] - lower_bounds_Sj[i]) + " -d " + str(error_levels_Sj[i]) + " -O ../Exponential/TPCH" + scales[j] + "_Selection" + folders_Sj[i] + "_" + queries_Sj[i] + "_" + str(epsilon) + "_median.txt -k " + str(index) + " -p " + str(p2)

# 				shell = os.popen(cmd, 'r')
# 				shell.read()
# 				shell.close()

# 				cmd = "../jr_python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/TPCH" + scales[j] + "_Selection" + folders_Sj[i] + "_" + queries_Sj[i] + "_" + str(epsilon) + "_median.txt -e " + str(epsilon) + " -b 0.1 -D " + str(upper_bounds_Sj[i]) + " -d " + str(error_levels_Sj[i])
					
# 				shell = os.popen(cmd, 'r')
# 				res = shell.read()
# 				res = res.split()

# 				output = float(res[1])
# 				answer = median_answer[percent][queries_Sj[i] + scales[j]]
# 				error = abs(output - answer)

# 				output_file.write(str(output) + "\n")
		
# 				errors_Sj.append(error)

# 				shell.close()

# 				end = time.time()

# 				sum_time_Sj += end - start

# 				# os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_" + queries_Sj[i] + "_median.txt")
# 				# os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_Sum" + folders_Sj[i] + "_" + queries_Sj[i] + "_count_" + str(epsilon / 2) + ".txt")
# 				# os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_Selection" + folders_Sj[i] + "_" + queries_Sj[i] + "_" + str(epsilon) + "_median.txt")

# 			output_file.write(str(sum_time_Sj / repeat_times_Sj))

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/test.txt", 'w')

	# SelectionMedian(0.5)
	# SelectionMedian(0.25)

	# SelectionMedian_Sj(0.5)
	# SelectionMedian_Sj(0.25)

	print(GetRankError_Sj(0, "_3", 35.1, 0.5))
	print(GetRankError_Sj(0, "_3", 52.6, 0.25))

if __name__ == "__main__":
	main(sys.argv[1:])