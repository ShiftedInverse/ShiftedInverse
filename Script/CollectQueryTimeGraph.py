import os
import psycopg2
import sys
import time

repeat_times = 10

queries = ["edge", "triangle", "degree"]
databases = ["Amazon", "Bitcoin", "Gnutella", "RoadnetTX"]

queries_directed = ["indegree", "outdegree"]
databases_directed = ["Bitcoin_directed", "Gnutella_directed"]

queries_selection = ["select max(weight) from edge;",
					"select percentile_disc(0.75) within group (order by weight asc) from edge;",
					"select percentile_disc(0.5) within group (order by weight asc) from edge;",
					"select min(weight) from edge;"]
databases_selection = ["Bitcoin_directed"]

def ExtractRelationship(database_name, query):
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()

    cur.execute(query)

    con.commit()
    con.close()

def main(argv):
	cur_path = os.getcwd()

	output_file = open(cur_path + "/../Result/Graph/QueryTime.txt", 'w')

	for database_name in databases:
		for i in range(len(queries)):
			sum_time = 0

			for j in range(repeat_times):
				if i == 0:
					query = "select count(*) from node as r1, node as r2, edge where r1.id=edge.from_id and r2.id=edge.to_id and r1.id<r2.id;"
				elif i == 1:
					query = "select count(*) from node as r1, node as r2, node as r3, edge as r4, edge as r5, edge as r6 where r4.from_id = r6.to_id and r5.from_id = r4.to_id and r6.from_id = r5.to_id and r1.id = r4.from_id and r2.id = r5.from_id and r3.id = r6.from_id and r1.id<r2.id and r2.id<r3.id;"
				elif i == 2:
					query = "select max(aaa) from (select count(*) as aaa, id from edge, node where from_id=id group by id) as aaaaa;"

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " " + queries[i] + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

	for database_name in databases_directed:
		for i in range(len(queries_directed)):
			sum_time = 0

			for j in range(repeat_times):
				if i == 0:
					query = "select max(aaa) from (select count(*) as aaa, id from edge, node where to_id=id group by id) as aaaaa;"
				elif i == 1:
					query = "select max(aaa) from (select count(*) as aaa, id from edge, node where from_id=id group by id) as aaaaa;"

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " " + queries_directed[i] + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

	for database_name in databases_selection:
		for i in range(len(queries_selection)):
			sum_time = 0

			if i == 0:
				query_name = "maximum"
			elif i == 1:
				query_name = "median_0.75"
			elif i == 2:
				query_name = "median_0.5"
			elif i == 3:
				query_name = "minimum"
			
			for j in range(repeat_times):
				query = queries_selection[i]
			
				start = time.time()
			
				ExtractRelationship(database_name, query)
			
				end = time.time()
			
				sum_time += end - start
			
			output_file.write(database_name + " " + query_name + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])