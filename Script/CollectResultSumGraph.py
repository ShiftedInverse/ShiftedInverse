import math
import os
import sys
import time

repeat_times = 100
queries = ["edge", "triangle"]
folders = ["_Sj", "_Sj"]
error_levels = [[10, 10, 10], [10, 10, 10]]
upper_bounds = [1024, 256, 32]
nodes = [262111, 62586, 1379917]
powers = [1, 2]
divides = [2, 6]
databases = ["Amazon", "Gnutella", "RoadnetTX"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

def main(argv):
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/Graph/ResultSum.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(databases)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Exponential.py -I ../Exponential/Graph/" + databases[j] + "/Sum" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(math.pow(upper_bounds[j], powers[i]) * nodes[j] / divides[i])) + " -d " + str(error_levels[i][j])

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

				output_file.write(databases[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])