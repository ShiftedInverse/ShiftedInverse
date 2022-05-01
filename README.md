# (Approx)ShiftedInverse
(Approx)ShiftedInverse is a general framework which estimates monotonic functions under user-DP. The work is submitted to CCS 2022. The project is structured as follows.

```
project
│   README.md
└───Code
│   └───Baseline
└───Data
│   └───Graph
│   └───TPCH
└───Exponential
└───Information
│   └───Graph
│   └───TPCH
└───Query
└───Result
└───Script
└───Temp
```

`./Code` includes the codes for (Approx)ShiftedInverse, and `./Code/Baseline` includes the codes for the baselines, including ZetaSQL, R2T and RM.

`./Data/Graph` and `./Data/TPCH` store the relations for the graph and TPCH datasets. Due to the size of the files, the relations are not uploaded here, and can be found at [*To be uploaded*].

`./Exponential` stores the computation results of \check{f}(V,j)'s.

`./Information/Graph` and `./Information/TPCH` store the extracted information of the queries for the graph and TPCH datasets. The information is also not uploaded, and can be downloaded at [*To be uploaded*].

`./Query` stores the queries used in the experiments.

`./Result` stores the results of the experiments.

`./Script` stores the scripts used in the experiments.

`./Temp` is used to store tempoaray files generated in the experiments.

## Prerequisites
The framework is built on the following tools:
* [PostgreSQL](https://www.postgresql.org/)
* [Cplex](https://www.ibm.com/analytics/cplex-optimizer)

The framework is built on [Python3.7](https://www.python.org/downloads/release/python-3713/), and relies on the following dependencies.
* `getopt`
* `math`
* `matplotlib`
* `multiprocessing`
* `numpy`
* `os`
* `psycopg2`
* `random`
* `sys`
* `time`

## Demo Example
A simple example is included here on how the framework works.

### Step 1: Create database and import data.
The first step is to create a database for the graph dataset and import the relations. To create the database, run
```
createdb Gnutella;
```
To import the relations to the database, go to `./Code/` and run `ProcessDataGraph.py` with
```
python ProcessDataGraph.py -d Gnutella -D Gnutella -m 0 -e 0
```
 - `-d`: the name of the folder containing all the relations;
 - `-D`: the name of the database;
 - `-m`: 0 for import and 1 for clean;
 - `-e`: 0 for undirected and 1 for directed;

### Step 2: Extract the information.
The second step is to extract the information, i.e., the relationship between the users and the tuples, for the given function and dataset. For the particular example here, run
```
python ExtractInformation.py -D Gnutella -Q ../Query/Graph/edge.txt -O ../Information/Graph/Gnutella/edge.txt
```
 - `-D`: the name of the database;
 - `-Q`: the path for the query;
 - `-O`: the path for the output information;

### Step 3: Compute \check{f}(V,j)'s.
The third step is to compute the \check{f}(V,j)'s as stated in our algorithm by running
```
python ComputeR_Sum_Sj.py -I ../Information/Graph/Gnutella/edge.txt -e 1 -b 0.1 -D 8011008 -d 10 -O ../Exponential/Graph/Gnutella/Sum_Sj/edge_1.txt -p 10
```
 - `-I`: the path for the information;
 - `-e`: the privacy budget \varepsilon;
 - `-b`: the failure probability \beta;
 - `-D`: the upper bound D;
 - `-d`: the error level of the output;
 - `-O`: the path for the output \check{f}(V,j)'s;
 - `-p`: the number of processors;

### Step 4: Sample an output.
Finally, we can sample an output using the \check{f}(V,j)'s. More specifically, run
```
python Exponential.py -I ../Exponential/Graph/Gnutella/Sum_Sj/edge_1.txt -e 1 -b 0.1 -D 8011008 -d 10
```
 - `-I`: the path for the information;
 - `-e`: the privacy budget \varepsilon;
 - `-b`: the failure probability \beta;
 - `-D`: the upper bound D;
 - `-d`: the error level of the output;

Note that the value for `-e`, `-b`, `-D`, `-d` should be the same for step 3 and 4 to ensure the mechanism satisfies DP.
