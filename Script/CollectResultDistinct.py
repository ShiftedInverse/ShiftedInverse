import math
import os
import sys
import time

repeat_times = 100
queries = ["Q_aq", "Q_ep", "Q_od", "Q_rd", "Q7"]
relations = ["sc", "sc", "sc", "sc", "sc"]
folders = ["", "", "", "", "_Sj"]
upper_bounds = [7, 7, 4, 4, 7]
error_levels = [0.001, 0.001, 0.001, 0.001, 0.001]
scales = ["_3"]
epsilons = [1]

answers = [9566, 194159, 2406, 2539, 1615444]

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultDistinct.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/TPCH/" + scales[j] + "/Distinct" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(upper_bounds[i] * math.pow(2, j))) + " -d " + str(error_levels[i])

				for k in range(repeat_times):
					start = time.time()

					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					errors.append(abs(answers[i] - math.pow(10, float(res[1]))))

					shell.close()

					end = time.time()

					sum_time += end - start

				errors.sort()

				output_file.write(scales[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])