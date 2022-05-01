import math
import os
import sys
import time

repeat_times = 3
queries = ["Q12", "Q18", "Q5", "Q7"]
relations = ["sc", "sc", "sc", "sc"]
folders = ["", "", "_Sj", "_Sj"]
upper_bounds = [1875000000, 18750000000, 12500000, 250000000]
error_levels = [10, 1000, 10, 1000]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]
epsilons = [1]

p = 10

def Sum():
	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0

				for k in range(repeat_times):
					start = time.time()

					cmd = "../python/python " + cur_path + "/../Code/ComputeR_Sum" + folders[i] + ".py -I ../Information/TPCH/" + scales[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(upper_bounds[i] * math.pow(2, j))) + " -d " + str(error_levels[i]) + " -O ../Exponential/TPCH/" + scales[j] + "/Sum" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt"
				
					if folders[i] == "_Sj":
						cmd += " -p " + str(p)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					end = time.time()

					sum_time += end - start

				output_file.write(scales[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + "\n")
				output_file.flush()

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ExponentialSumScale.txt", 'w')

	Sum()

if __name__ == "__main__":
	main(sys.argv[1:])