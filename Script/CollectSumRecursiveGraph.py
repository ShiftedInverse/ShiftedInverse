import math
import os
import sys
import time

repeat_times = 10
queries = ["triangle"]
folders = ["_Sj"]
databases = ["Gnutella", "RoadnetTX"]
epsilons = [0.125, 0.25, 0.5, 1, 2, 4, 8]

def main(argv):
    cur_path = os.getcwd()
    output_file = open(cur_path + "/../Result/Graph/ResultSumRecursive.txt", 'w')

    for i in range(len(queries)):
        for j in range(len(databases)):
            for epsilon in epsilons:
                sum_time = 0
                errors = []

                cmd = "../python/python " + cur_path + "/../Code/Baseline/Recursive" + folders[i] + ".py -I ../Information/Graph/" + databases[j] + "/" + queries[i] + ".txt -e " + str(epsilon) + " -d 0.1"

                for k in range(repeat_times):
                    start = time.time()

                    shell = os.popen(cmd, 'r')
                    res = shell.read()
                    res = res.split()
        
                    errors.append(float(res[-3]))

                    shell.close()

                    end = time.time()

                    sum_time += end - start

                errors.sort()

                output_file.write(databases[j] + " " + queries[i] + " " + str(epsilon) + " " + str(sum_time / repeat_times) + " " + str(sum(errors[int(repeat_times * 0.2) : int(repeat_times * 0.8)]) / int(repeat_times * 0.6)) + "\n")
                output_file.flush()

if __name__ == "__main__":
    main(sys.argv[1:])