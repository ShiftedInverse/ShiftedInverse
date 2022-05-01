import os
import psycopg2
import sys
import time

repeat_times = 10

queries_sum = ["select count(*) from orders, lineitem where o_orderkey = l_orderkey;",
				"select count(*) from ids as id1, ids as id2, region, nation, customer, supplier, orders, lineitem where id1.i_id = c_id and id2.i_id = s_id and r_regionkey=n_regionkey and n_nationkey=c_nationkey and n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey;",
				"select sum(l_quantity) from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey;", 
				"select sum(l_extendedprice * (1 - l_discount)/1000) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31';",
				"with aaaaa(aaa, bbb, ccc) as (select p_brand, s_suppkey, count(*) from nation, supplier, part, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and s_nationkey = n_nationkey and n_nationkey = 24 group by p_brand, s_suppkey) select sum(aaaaa_1.ccc * aaaaa_2.ccc) from aaaaa as aaaaa_1, aaaaa as aaaaa_2 where aaaaa_1.aaa = aaaaa_2.aaa and aaaaa_1.bbb != aaaaa_2.bbb;",
				"with aaaaa(aaa, bbb, ccc) as (select p_brand, s_suppkey, count(*) from nation, supplier, part, partsupp where ps_suppkey = s_suppkey and ps_partkey = p_partkey and s_nationkey = n_nationkey and n_nationkey = 24 group by p_brand, s_suppkey) select sum(aaaaa_1.ccc * aaaaa_1.ccc) from aaaaa as aaaaa_1;"]
queries_selection = ["select max((l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000) from supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey;", 
					"select percentile_disc(0.75) within group (order by profit asc) from (select (l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000 as profit, s_suppkey from supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey) as aaaaa;", 
					"select percentile_disc(0.5) within group (order by profit asc) from (select (l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000 as profit, s_suppkey from supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey) as aaaaa;", 
					"select min((l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity)/1000) from supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey;", 
					"select max(l_quantity) from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey;", 
					"select percentile_disc(0.75) within group (order by l_quantity asc) from (select l_quantity, c_custkey from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey) as aaaaa;", 
					"select percentile_disc(0.5) within group (order by l_quantity asc) from (select l_quantity, c_custkey from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey) as aaaaa;", 
					"select min(l_quantity) from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey;", 
					"select max(l_extendedprice * (1 - l_discount)/1000) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31';",
					"select percentile_disc(0.75) within group (order by revenue asc) from (select (l_extendedprice * (1 - l_discount)/1000) as revenue, id1.i_id, id2.i_id from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31') as aaaaa;",
					"select percentile_disc(0.5) within group (order by revenue asc) from (select (l_extendedprice * (1 - l_discount)/1000) as revenue, id1.i_id, id2.i_id from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31') as aaaaa;",
					"select min(l_extendedprice * (1 - l_discount)/1000) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31';"]
queries_distinct = ["select count(distinct(s_suppkey)) from supplier, partsupp where s_suppkey=ps_suppkey and (ps_partkey<=100 or ps_partkey>=199900);",
					"select count(distinct(ps_availqty)) from supplier, partsupp where s_suppkey=ps_suppkey and s_nationkey>=24;",
					"select count(distinct(l_extendedprice)) from supplier, lineitem where s_suppkey=l_suppkey and s_nationkey>=24;",
					"select count(distinct(o_orderdate)) from customer, orders where c_custkey=o_custkey and c_nationkey >= 24;",
					"select count(distinct(l_receiptdate)) from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey and c_nationkey >= 24;",
					"select count(distinct(l_extendedprice * (1 - l_discount)/1000)) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31';"]
queries_frequency = ["with aaaaa(aaa, bbb) as (select l_quantity, count(c_custkey) from customer, orders, lineitem where c_custkey = o_custkey and o_orderkey = l_orderkey group by l_quantity) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select o_orderpriority, count(c_custkey) from customer, orders where c_custkey=o_custkey group by o_orderpriority) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select s_nationkey, count(s_suppkey) from supplier group by s_nationkey) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select l_tax, count(s_suppkey) from supplier, partsupp, lineitem where s_suppkey = l_suppkey and ps_suppkey = l_suppkey and ps_partkey = l_partkey group by l_tax) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select ps_availqty, count(s_suppkey) from supplier, partsupp where ps_suppkey = s_suppkey group by ps_availqty) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select l_quantity, count(*) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' group by l_quantity) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select l_discount, count(*) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' group by l_discount) select max(bbb) from aaaaa;",
					"with aaaaa(aaa, bbb) as (select l_shipdate, count(*) from ids as id1, ids as id2, nation as n1, nation as n2, customer, supplier, orders, lineitem where id1.i_id=c_id and id2.i_id=s_id and n1.n_nationkey=c_nationkey and n2.n_nationkey=s_nationkey and c_custkey=o_custkey and s_suppkey=l_suppkey and o_orderkey=l_orderkey and l_shipdate>=date'1995-01-01' and l_shipdate<=date'1996-12-31' group by l_shipdate) select max(bbb) from aaaaa;"]

databases = ["TPCH_3_sc"]

def ExtractRelationship(database_name, query):
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()

    cur.execute(query)

    con.commit()
    con.close()

def main(argv):
	cur_path = os.getcwd()

	output_file = open(cur_path + "/../Result/TPCH/QueryTime.txt", 'w')

	for database_name in databases:
		for i in range(len(queries_sum)):
			sum_time = 0

			for j in range(repeat_times):
				query = queries_sum[i]

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " sum_" + str(i) + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

	for database_name in databases:
		for i in range(len(queries_selection)):
			sum_time = 0

			for j in range(repeat_times):
				query = queries_selection[i]

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " selection_" + str(i) + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

	for database_name in databases:
		for i in range(len(queries_distinct)):
			sum_time = 0

			for j in range(repeat_times):
				query = queries_distinct[i]

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " distinct_" + str(i) + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

	for database_name in databases:
		for i in range(len(queries_frequency)):
			sum_time = 0

			for j in range(repeat_times):
				query = queries_frequency[i]

				start = time.time()

				ExtractRelationship(database_name, query)

				end = time.time()

				sum_time += end - start

			output_file.write(database_name + " frequency_" + str(i) + " " + str(sum_time / repeat_times) + "\n")
			output_file.flush()

if __name__ == "__main__":
	main(sys.argv[1:])