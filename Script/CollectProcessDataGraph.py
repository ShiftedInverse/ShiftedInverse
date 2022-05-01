import os
import sys

databases = ["Amazon", "Gnutella", "RoadnetTX"]
weighted_databases = ["Bitcoin"]

def main(argv):
	cur_path = os.getcwd()

	for database in databases:
		for e in [0, 1]:
			cmd = "python " + cur_path + "/../Code/ProcessDataGraph.py -d " + database + " -D " + database + " -m 0 -e " + str(e)
				
			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

	for database in weighted_databases:
		for e in [0, 1]:
			cmd = "python " + cur_path + "/../Code/ProcessDataWeightedGraph.py -d " + database + " -D " + database + " -m 0 -e " + str(e)

			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()

if __name__ == "__main__":
	main(sys.argv[1:])