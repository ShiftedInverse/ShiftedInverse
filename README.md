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
[*Todo*].

### Step 2: Extract the information.
[*Todo*].

### Step 3: Compute \check{f}(V,j)'s.
[*Todo*].

### Step 4: Sample an output.
[*Todo*].
