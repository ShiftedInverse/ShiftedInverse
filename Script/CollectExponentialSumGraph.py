import math
import os
import sys
import time

repeat_times = 3
queries = ["edge", "triangle"]
folders = ["_Sj", "_Sj"]
error_levels = [[10, 10, 10], [10, 10, 10]]
upper_bounds = [1024, 256, 32]
nodes = [262111, 62586, 1379917]
powers = [1, 2]
divides = [2, 6]
databases = ["Amazon", "Gnutella", "RoadnetTX"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

p = 10

def Sum():
	for i in range(len(queries)):
		for j in range(len(databases)):
			for epsilon in epsilons:
				sum_time = 0

				for k in range(repeat_times):
					start = time.time()

					cmd = "../python/python " + cur_path + "/../Code/ComputeR_Sum" + folders[i] + ".py -I ../Information/Graph/" + databases[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -D " + str(int(math.pow(upper_bounds[j], powers[i]) * nodes[j] / divides[i])) + " -d " + str(error_levels[i][j]) + " -O ../Exponential/Graph/" + databases[j] + "/Sum" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + ".txt"
				
					if folders[i] == "_Sj":
						cmd += " -p " + str(p)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					end = time.time()

					sum_time += end - start

				output_file.write(databases[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + "\n")
				output_file.flush()

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/Graph/ExponentialSum.txt", 'w')

	Sum()

if __name__ == "__main__":
	main(sys.argv[1:])