import getopt
import os
import psycopg2
import sys

def main(argv):
	datasets = ["Amazon", "Gnutella", "RoadnetTX"]
	dataset = ''
	database_name = ''
	model = 0
	edge = 0

	try:
		opts, args = getopt.getopt(argv, "h:d:D:m:e:", ["dataset=", "database=", "model=", "edge="])
	except getopt.GetoptError:
		print("ProcessDataGraph.py -d <dataset> -D <database> -m <model:0(import)/1(clean)> -e <edge:0(undirected)/1(directed)>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("ProcessDataGraph.py -d <dataset> -D <database> -m <model:0(import)/1(clean)> -e <edge:0(undirected)/1(directed)>")
			sys.exit()
		elif opt in ("-d", "--dataset"):
			dataset = arg
		elif opt in ("-D", "--Database"):
			database_name = arg
		elif opt in ("-m","--model"):
			model = int(arg)
		elif opt in ("-e","--edge"):
			edge = int(arg)

	if model == 0:
		if dataset not in datasets:
			print("Invalid dataset.")
			sys.exit()

		if edge == 1:
			database_name += "_directed"
			edge_file_path = "/directededge.txt"
		else:
			edge_file_path = "/edge.txt"

		con = psycopg2.connect(database=database_name)
		cur = con.cursor()

		cur_path = os.getcwd() + '/'

		edge_file = open(cur_path + "../Data/Graph/" + dataset + edge_file_path, 'r')
		node_file = open(cur_path + "../Data/Graph/" + dataset + "/node.txt", 'r')

		code = "CREATE TABLE node (ID INTEGER NOT NULL);"
		cur.execute(code)
		code = "CREATE TABLE edge (FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);"
		cur.execute(code)
		code = "CREATE INDEX on node using hash (ID);"
		cur.execute(code)
		code = "CREATE INDEX on edge using hash (FROM_ID);"
		cur.execute(code)
		code = "CREATE INDEX on edge using hash (TO_ID);"
		cur.execute(code)

		con.commit()
		con.close()

		con = psycopg2.connect(database=database_name)
		cur = con.cursor()

		cur.copy_from(node_file, "node")
		cur.copy_from(edge_file, "edge", sep='|')

		con.commit()
		con.close()
	else:
		if edge == 1:
			database_name += "_directed"
			
		con = psycopg2.connect(database=database_name)
		cur = con.cursor()

		code = "drop table node;"
		cur.execute(code)
		code = "drop table edge;"
		cur.execute(code)

		con.commit()
		con.close()

if __name__ == "__main__":
	main(sys.argv[1:])