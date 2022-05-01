import math
import os
import sys
import time

repeat_times = 10
queries = ["Q_aq", "Q_ep", "Q_od", "Q_rd", "Q7"]
relations = ["sc", "sc", "sc", "sc", "sc"]
folders = ["", "", "", "", ""]
upper_bounds = [10000, 10000, 3000, 3000, 10000]
scales = ["_3"]
epsilons = [1]

p = 10

def main(argv):
	global cur_path

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultDistinctR2T.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Baseline/R2T" + folders[i] + "_Distinct_new.py -I ../Information/TPCH/" + scales[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -G " + str(upper_bounds[i]) + " -p " + str(p)

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
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])