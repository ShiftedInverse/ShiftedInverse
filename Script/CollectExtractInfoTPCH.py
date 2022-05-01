import os
import sys
import time

repeat_times = 10
queries = ["Q5", "Q7", "Q9", "Q11", "Q12", "Q18", "Q7_count", "Q9_count", "Q18_count"]
relations = ["sc", "sc", "sc", "sc", "sc", "sc", "sc", "sc", "sc", "sc"]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]

# queries = ["Q_aq", "Q_d", "Q_ep", "Q_od", "Q_op", "Q_q", "Q_rd", "Q_sd", "Q_t"]
# relations = ["sc", "sc", "sc", "sc", "sc", "sc", "sc", "sc", "sc"]
# scales = ["_3"]

def main(argv):
	cur_path = os.getcwd()
	output_file = open(cur_path + "/../Result/TPCH/ExtractInfo.txt", 'w')

	for scale in scales:
		for i in range(len(queries)):
			sum_time = 0

			for j in range(repeat_times):
				start = time.time()

				cmd = "python " + cur_path + "/../Code/ExtractInformation.py -D \"TPCH" + scale + "_" + relations[i] + "\" -Q ../Query/TPCH/" + queries[i] + ".txt -O ../Information/TPCH/" + scale + "/" + queries[i] + ".txt"
				
				shell = os.popen(cmd, 'r')
				shell.read()
				shell.close()

				end = time.time()

				sum_time += end - start

			output_file.write(scale + " " + queries[i] + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])