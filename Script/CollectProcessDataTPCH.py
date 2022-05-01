import sys
import os

relations = ["sc"]
scales = ["_0", "_1", "_2", "_3", "_4", "_5"]

def main(argv):
	cur_path = os.getcwd()

	for scale in scales:
		for relation in relations:
			cmd = "python " + cur_path + "/../Code/ProcessTPCHData.py -d " + scale + " -D \"TPCH" + scale + "_" + relation + "\" -m 0 -r " + "../Relation/" + relation + ".txt"
			shell = os.popen(cmd, 'r')
			shell.read()
			shell.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])