import os
import sys
import time

repeat_times = 3
queries = ["weightededge"]
folders = ["_Sj"]
upper_bounds = [10]
lower_bounds = [-10]
error_levels = [0.01]
databases = ["Bitcoin"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

p = 10
p2 = 10

def ProcessMax(database, i):
	read_file = open(cur_path + "/../Information/Graph/" + database + "/" + queries[i] + ".txt", 'r')
	write_file_max = open(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_max.txt", 'w')

	upper_bound = upper_bounds[i]
	lower_bound = lower_bounds[i]

	for line in read_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])

		write_file_max.write(str(tuple_value - lower_bound) + " ")

		for j in range(1, len(elements) - 1):
			write_file_max.write(elements[j] + " ")

		write_file_max.write(elements[len(elements) - 1] + "\n")

def ProcessMin(database, i):
	read_file = open(cur_path + "/../Information/Graph/" + database + "/" + queries[i] + ".txt", 'r')
	write_file_min = open(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_min.txt", 'w')

	upper_bound = upper_bounds[i]
	lower_bound = lower_bounds[i]

	for line in read_file.readlines():
		elements = line.split()

		tuple_value = float(elements[0])

		write_file_min.write(str(upper_bound - tuple_value) + " ")

		for j in range(1, len(elements) - 1):
			write_file_min.write(elements[j] + " ")

		write_file_min.write(elements[len(elements) - 1] + "\n")

def SelectionMax():
	for database in databases:
		for i in range(len(queries)):
			for epsilon in epsilons:
				sum_time = 0

				for j in range(repeat_times):
					start = time.time()

					ProcessMax(database, i)

					if folders[i] == "_Sj":
						cmd = "../python/python " + cur_path + "/../Code/ComputeR_Max" + folders[i] + ".py -I /../Temp/Graph" + database + "_" + queries[i] + "_max.txt -e" + str(epsilon) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_max.txt -k 1"
					else:
						cmd = "../python/python " + cur_path + "/../Code/ComputeR_Selection" + folders[i] + ".py -I /../Temp/Graph" + database + "_" + queries[i] + "_max.txt -e" + str(epsilon) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_max.txt -k 1"

					if folders[i] == "_Sj":
						cmd += " -p " + str(p)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					end = time.time()

					sum_time += end - start

				os.remove(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_max.txt")

				output_file.write(database + " " + queries[i] + "_max " + str(epsilon) + " " + str(sum_time / repeat_times) + "\n")

def SelectionMin():
	for database in databases:
		for i in range(len(queries)):
			for epsilon in epsilons:
				sum_time = 0

				for j in range(repeat_times):
					start = time.time()

					ProcessMin(database, i)

					if folders[i] == "_Sj":
						cmd = "../python/python " + cur_path + "/../Code/ComputeR_Max" + folders[i] + ".py -I /../Temp/Graph" + database + "_" + queries[i] + "_min.txt -e" + str(epsilon) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_min.txt -k 1"
					else:
						cmd = "../python/python " + cur_path + "/../Code/ComputeR_Selection" + folders[i] + ".py -I /../Temp/Graph" + database + "_" + queries[i] + "_min.txt -e" + str(epsilon) + " -b 0.1 -D " + str(upper_bounds[i] - lower_bounds[i]) + " -d " + str(error_levels[i]) + " -O ../Exponential/Graph/" + database + "/Selection" + folders[i] + "/" + queries[i] + "_" + str(epsilon) + "_min.txt -k 1"

					if folders[i] == "_Sj":
						cmd += " -p " + str(p)

					shell = os.popen(cmd, 'r')
					shell.read()
					shell.close()

					end = time.time()

					sum_time += end - start

				os.remove(cur_path + "/../Temp/Graph" + database + "_" + queries[i] + "_min.txt")

				output_file.write(database + " " + queries[i] + "_min " + str(epsilon) + " " + str(sum_time / repeat_times) + "\n")

def main(argv):
	global cur_path
	global output_file

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/Graph/ExponentialSelection.txt", 'w')

	SelectionMax()
	SelectionMin()

if __name__ == "__main__":
	main(sys.argv[1:])