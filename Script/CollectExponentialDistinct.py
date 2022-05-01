import math
import os
import sys
import time

repeat_times = 3
queries = ["Q_aq", "Q_ep", "Q_od", "Q_rd" "Q7"]
relations = ["sc", "sc", "sc", "sc", "sc"]
folders = ["", "", "", "", "_Sj"]
upper_bounds = [7, 7, 4, 4, 7]
error_levels = [0.001, 0.001, 0.001, 0.001, 0.001]
scales = ["_3"]
epsilons = [1]

p = 10

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ExponentialDistinct.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0

				for k in range(repeat_times):
					start = time.time()

					cmd = "../python/python " + cur_path + "/../Code/ComputeR_Distinct" + folders[i] + ".py -I ../Information/TPCH/" + scales[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(upper_bounds[i] * math.pow(2, j))) + " -d " + str(error_levels[i]) + " -O ../Exponential/TPCH/" + scales[j] + "/Distinct" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt -p " + str(p)
					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					end = time.time()

					sum_time += end - start

				output_file.write(scales[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + "\n")
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])