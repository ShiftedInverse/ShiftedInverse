import math
import os
import sys
import time

repeat_times = 10
queries = ["Q12", "Q18", "Q5", "Q7"]
relations = ["sc", "sc", "sc", "sc"]
folders = ["", "", "_Sj", "_Sj"]
upper_bounds = [10000, 1000000, 10000, 1000000]
scales = ["_3"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

queries_f2 = ["Q11"]
relations_f2 = ["sc"]
folders_f2 = ["_Sj"]
upper_bounds_f2 = [100000000]

p = 10

def ProcessF2(i, j):
	read_file = open(cur_path + "/../Information/TPCH/" + scales[j] + "/" + queries_f2[i] + ".txt", 'r')
	write_file_f2 = open(cur_path + "/../Temp/TPCH" + scales[j] + "_" + queries_f2[i] + "_f2.txt", 'w')

	values = {}
	users = []
	variances = {}

	for line in read_file.readlines():
		elements = line.split()

		tuple_value = elements[0]
		user_id = int(float(elements[1]))

		if user_id in values.keys():
			if tuple_value in values[user_id].keys():
				values[user_id][tuple_value] += 1
			else:
				values[user_id][tuple_value] = 1
		else:
			values[user_id] = {}
			values[user_id][tuple_value] = 1
			users.append(user_id)

	for i in range(len(users)):
		for j in range(i, len(users)):
			tuple_ = tuple([users[i], users[j]])
			if users[i] == users[j]:
				variances[tuple_] = 0
				for tuple_value in values[users[i]].keys():
					variances[tuple_] += values[users[i]][tuple_value] * values[users[i]][tuple_value]
			else:
				variances[tuple_] = 0
				for tuple_value in values[users[i]].keys():
					if tuple_value in values[users[j]].keys():
						variances[tuple_] += 2 * values[users[i]][tuple_value] * values[users[j]][tuple_value]
						
	for variance_key, variance_value in variances.items():
		write_file_f2.write(str(variance_value) + " " + str(variance_key[0]) + " " + str(variance_key[1]) + "\n")

def main(argv):
	global cur_path

	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ResultSumR2T.txt", 'w')

	for i in range(len(queries)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Baseline/R2T" + folders[i] + ".py -I ../Information/TPCH/" + scales[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -b 0.1 -G " + str(upper_bounds[i])

				if folders[i] == "_Sj":
					cmd += " -p " + str(p)

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

	for i in range(len(queries_f2)):
		for j in range(len(scales)):
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cmd = "../python/python " + cur_path + "/../Code/Baseline/R2T" + folders_f2[i] + ".py -I ../Temp/TPCH" + scales[j] + "_" + queries_f2[i] + "_f2.txt -e " + str(epsilon) + " -b 0.1 -G " + str(upper_bounds_f2[i])

				if folders_f2[i] == "_Sj":
					cmd += " -p " + str(p)

				for k in range(repeat_times):
					start = time.time()

					ProcessF2(i, j)

					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()
		
					errors.append(float(res[-3]))

					shell.close()

					end = time.time()

					sum_time += end - start

				os.remove(cur_path + "/../Temp/TPCH" + scales[j] + "_" + queries_f2[i] + "_f2.txt")

				output_file.write(scales[j] + " " + queries_f2[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
				output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])