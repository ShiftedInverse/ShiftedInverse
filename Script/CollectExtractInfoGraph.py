import os
import sys
import time

repeat_times = 10
queries = ["edge", "triangle", "degree", "indegree", "outdegree", "directededge"]
database_names = ["", "", "", "_directed", "_directed", "_directed"]
databases = ["Amazon", "Gnutella", "RoadnetTX"]

weighted_queries = ["weightededge", "triangle", "degree", "indegree", "outdegree", "directededge"]
weighted_database_names = ["_directed", "", "", "_directed", "_directed", "_directed"]
weighted_databases = ["Bitcoin"]

def main(argv):
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/Graph/ExtractInfo.txt", 'w')

	for database in databases:
		for i in range(len(queries)):
			print(database, queries[i])
			sum_time = 0

			for j in range(repeat_times):
				start = time.time()

				cmd = "python " + cur_path + "/../Code/ExtractInformation.py -D " + database + database_names[i] + " -Q ../Query/Graph/" + queries[i] + ".txt -O ../Information/Graph/" + database + "/" + queries[i] + ".txt"
				
				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

				end = time.time()

				sum_time += end - start

			output_file.write(database + " " + queries[i] + " " + str(sum_time / repeat_times) + "\n")

	for database in weighted_databases:
		for i in range(len(weighted_queries)):
			sum_time = 0

			for j in range(repeat_times):
				start = time.time()

				cmd = "python " + cur_path + "/../Code/ExtractInformation.py -D " + database + weighted_database_names[i] + " -Q ../Query/Graph/" + weighted_queries[i] + ".txt -O ../Information/Graph/" + database + "/" + weighted_queries[i] + ".txt"
				
				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

				end = time.time()

				sum_time += end - start

			output_file.write(database + " " + weighted_queries[i] + " " + str(sum_time / repeat_times) + "\n")

if __name__ == "__main__":
	main(sys.argv[1:])