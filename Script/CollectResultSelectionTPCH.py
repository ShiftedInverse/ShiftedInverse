import os
import sys
import time

repeat_times = 100
queries = ["Q9", "Q18", "Q7"]
relations = ["sc", "sc", "sc"]
folders = ["", "", "_Sj"]
upper_bounds = [200000, 100000, 100000]
error_levels = [0.01, 0.01, 0.01]
scales = ["_3"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]
selections = ["_max", "_min"]

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

def main(argv):
	global cur_path
	
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultSelection.txt", 'w')

	for selection in selections:
		for i in range(len(queries)):
			for scale in scales:
				for epsilon in epsilons:
					sum_time = 0
					errors = []
					percentiles = []
					absolute_errors = []

					cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/TPCH/" + scale + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + selection + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(upper_bounds[i]) + " -d " + str(error_levels[i])
					
					for j in range(repeat_times):
						start = time.time()

						shell = os.popen(cmd, 'r')
						res = shell.read()
						res = res.split()

						shell.close()

						end = time.time()

						query_result = float(res[2])

						if selection == "_max":
							alpha = 1
							output_value = float(res[1])
							if queries[i] == "Q9":
								output_value -= 100000
						else:
							alpha = 0
							output_value = 100000 - float(res[1])

						if abs(float(res[1]) - query_result) <= 1e-5:
							error = 0
							percentile = 0
						else:
							error, percentile = GetRankError(i, scale, output_value, 1 - alpha)

						errors.append(error)
						percentiles.append(percentile)
						absolute_errors.append(abs(float(res[1]) - query_result))

						sum_time += end - start

					errors.sort()
					percentiles.sort()
					absolute_errors.sort()

					output_file.write(scale + " " + queries[i] + selection + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(percentiles[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + " " + str(sum(absolute_errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
					output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])