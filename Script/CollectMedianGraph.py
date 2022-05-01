import math
import os
import sys
import time

repeat_times = 10
queries = ["weightededge"]
folders = ["_Sj"]
upper_bounds = [10]
upper_bounds_count = [6022144]
lower_bounds = [-10]
error_levels_count = [10]
error_levels = [0.01]
databases = ["Bitcoin"]
epsilons = [1]

p = 10
p2 = 10

median_answers = {}
median_answers[0.5] = 11
median_answers[0.25] = 12

def GetRankError(i, database, output_value, alpha):
	file = open(cur_path + "/../Information/Graph/" + database + "/" + queries[i] + ".txt", 'r')

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

def ProcessMedian(database, i):
	read_file = open(cur_path + "/../Information/Graph/" + database + "/" + queries[i] + ".txt", 'r')
	write_file_median = open(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_median.txt", 'w')

	upper_bound = upper_bounds[i]
	lower_bound = lower_bounds[i]

	for line in read_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])

		write_file_median.write(str(tuple_value - lower_bound) + " ")

		for j in range(1, len(elements) - 1):
			write_file_median.write(elements[j] + " ")

		write_file_median.write(elements[len(elements) - 1] + "\n")

def SelectionMedian(percent):
	for i in range(len(queries)):
		for database in databases:
			for epsilon in epsilons:
				sum_time = 0
				errors = []
				percentiles = []
				absolute_errors = []

				for k in range(repeat_times):
					start = time.time()

					cmd = "../python/python " + cur_path + "/../Code/ComputeR_Sum" + folders[i] + ".py -I ../Information/Graph/" + database + "/directededge.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds_count[i]) + " -d " + str(int(error_levels_count[i])) + " -O ../Exponential/Graph/" + database + "/Sum" + folders[i] + "/" + queries[i] + "_count_" + str(epsilon / 2) + ".txt"

					if folders[i] == "_Sj":
						cmd += " -p " + str(p)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/Graph/" + database + "/Sum" + folders[i] + "/" + queries[i] + "_count_" + str(epsilon / 2) + ".txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds_count[i]) + " -d " + str(int(error_levels_count[i]))

					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					index = int(float(res[1]) * percent)

					shell.close()

					ProcessMedian(database, i)

					cmd = "../python/python " + cur_path + "/../Code/ComputeR_Selection" + folders[i] + ".py -I ../Temp/Graph" + database + "_" + queries[i] + "_median.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_median.txt -k " + str(index)

					if folders[i] == "_Sj":
						cmd += " -p " + str(p2)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_median.txt -e " + str(epsilon / 2) + " -b 0.1 -D " + str(upper_bounds[i]) + " -d " + str(error_levels[i])
					
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					shell.close()

					end = time.time()

					alpha = percent
					output_value = float(res[1]) - 10

					answer = median_answers[percent]

					if abs(answer - float(res[1])) <= 1e-5:
						error = 0
						percentile = 0
					else:
						error, percentile = GetRankError(i, database, output_value, percent)
		
					errors.append(error)
					percentiles.append(percentile)
					absolute_errors.append(abs(answer - float(res[1])))

					sum_time += end - start

				os.remove(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_median.txt")

				errors.sort()
				percentiles.sort()
				absolute_errors.sort()

				output_file.write(database + " " + queries[i] + "_median_" + str(1 - percent) + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(percentiles[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(absolute_errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
				output_file.flush()

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/Graph/ResultMedian.txt", 'w')

	SelectionMedian(0.5)
	SelectionMedian(0.25)

if __name__ == "__main__":
	main(sys.argv[1:])