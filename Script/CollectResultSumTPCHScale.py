import math
import os
import sys
import time

repeat_times = 100
queries = ["Q12", "Q18", "Q5", "Q7"]
relations = ["sc", "sc", "sc", "sc"]
folders = ["", "", "_Sj", "_Sj"]
upper_bounds = [1875000000, 18750000000, 12500000, 1250000000]
error_levels = [10, 1000, 10, 1000]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]
epsilons = [1]

def main(argv):
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultSumScale.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/TPCH/" + scales[j] + "/Sum" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(upper_bounds[i] * math.pow(2, j))) + " -d " + str(error_levels[i])

				for k in range(repeat_times):
					start = time.time()

					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					errors.append(float(res[0]))

					shell.close()

					end = time.time()

					sum_time += end - start

				errors.sort()

				output_file.write(scales[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])