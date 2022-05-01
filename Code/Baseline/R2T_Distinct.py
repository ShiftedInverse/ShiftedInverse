import getopt
import math
import sys
import random
import cplex
import numpy as np
import time
import gc
import multiprocessing
from multiprocessing.sharedctypes import Value
from ctypes import c_double
manager = multiprocessing.Manager()
gc.enable()



class Optimizer(cplex.callbacks.SimplexCallback):
	def __call__(self):
		global primals
		global duals
		global stop_primals
		global stop_duals
		global early_stops
		global global_max
		value = self.get_objective_value()
		if self.LP_type==0:
			primals[self.tau_index] = value
			#Update the threshold for early stop
			if global_max.value<=self.factor+value:
				global_max.value=self.factor+value
			#If arrive the stop condition for the approximate algorithm
			#If the dual/primal has already stopped
			#If arrive the early stop
			if stop_duals[self.tau_index]==1 or abs(duals[self.tau_index]-value)<=self.tau or early_stops[self.tau_index]==1:
				self.abort()
		else:
			duals[self.tau_index] = value
			if value+self.factor<global_max.value:
				early_stops[self.tau_index]=1
				self.abort()
			if stop_primals[self.tau_index]==1 or abs(primals[self.tau_index]-value)<=self.tau:
				self.abort()
				
				

def ReadInput():
	global input_file_path
	global ids
	global values
	global joins
	global value_join_dic
	global id_join_dic
	global indirect_sensitivity
	global real_query_result

	id_dic = {}
	id_num = 0

	join_dic = {}
	join_num = 0

	value_dic = {}
	value_num = 0

	value_join_dic = {}
	id_join_dic = {}

	entities = {}
	entities_sensitivity_dic = {}

	indirect_sensitivity = 0

	input_file = open(input_file_path,'r')

	aaa = 0

	for line in input_file.readlines():
		elements = line.split()

		# join_id = int(elements[1])
		join_id = aaa
		aaa += 1

		if join_id in join_dic.keys():
			join_id = join_dic[join_id]
		else:
			join_dic[join_id] = join_num
			join_id = join_num
			join_num += 1

		distinct_value = elements[0]
		if distinct_value in value_dic.keys():
			distinct_value = value_dic[distinct_value]

			value_join_dic[distinct_value].append(join_id)
		else:
			value_dic[distinct_value] = value_num
			distinct_value = value_num
			value_num += 1

			value_join_dic[distinct_value] = []
			value_join_dic[distinct_value].append(join_id)

		# for element in elements[2:]:
		for element in elements[1:]:
			element = int(element)

			if element in id_dic.keys():
				element = id_dic[element]
			else:
				id_dic[element] = id_num
				element = id_num
				id_num += 1

			if element in id_join_dic.keys():
				id_join_dic[element].append(join_id)
			else:
				id_join_dic[element] = []
				id_join_dic[element].append(join_id)

			id_sensitivity = len(id_join_dic[element])
			if indirect_sensitivity <= id_sensitivity:
				indirect_sensitivity = id_sensitivity

	real_query_result = value_num

	values = list(value_dic.values())
	joins = list(join_dic.values())
	ids = list(id_dic.values())

def LapNoise():
	a = random.uniform(0,1)
	b = math.log(1/(1-a))
	c = random.uniform(0,1)
	if c>0.5:
		return b
	else:
		return -b
	
	

def RunAlgorithm():
	global global_sensitivity
	global connections
	global indirect_sensitivity
	global epsilon
	global beta
	global real_query_result
	global approximate_factor
	#Used to store the primals and duals of LPs
	global primals
	global duals
	#Used for the optimizations
	#Stop the LP if its dual/primal stops
	global stop_primals
	global stop_duals
	#Used for the earily stop
	global early_stops
	global global_max
	#Base of Log function
	#Besides, one notice is that we also optimize the base used in Theorem 5.1. 
	#In the paper, we use 2 while it can be proven the optimal one is e (by optimizing the error bound in Theorem 5.1). 
	#Here, we use 2e for its better practical performance. 
	#Please note any theoretical result in the paper will not be affected as long as the base is still a constant number.
	base = 5.5
	#The number of all tau's
	max_i = int(math.log(global_sensitivity,base))
	if max_i<=1:
		max_i+=1
	#Used to store the results
	#The Q(I,tau)
	Q_tau = {}
	#The Q(I,tau)-factor+Noise
	tilde_Q_tau = {}
	#The Q(I,tau)+Noise
	hat_Q_tau = {}
	#Initialize the variables for optimizations
	primals = manager.dict()
	duals = manager.dict()
	stop_primals = manager.dict()
	stop_duals = manager.dict()
	early_stops = manager.dict()
	global_max = Value(c_double, -global_sensitivity/epsilon,lock=True)
	#Assign the tau's
	arrangement_of_tau_ids = []
	for i in range(processor_num):
		arrangement_of_tau_ids.append([])
	#Indicate which processor assigned to one given tau/i
	j = 0
	#Enumerate i inversely
	for ii in range(max_i+1):
		i = max_i-ii
		tau = math.pow(base,i)
		arrangement_of_tau_ids[j].append(i)
		j = (j+1)%processor_num
		Q_tau[i] = 0
		#Add the noise
		hat_Q_tau[i] = LapNoise()*tau/epsilon*max_i*(approximate_factor+1)
		#Add the noise and the factor
		tilde_Q_tau[i] = hat_Q_tau[i]-tau/epsilon*max_i*math.log(max_i/beta)*(approximate_factor+1)
		primals[i] = 0
		duals[i] = 10*real_query_result
		stop_duals[i] = 0
		stop_primals[i] = 0
		early_stops[i] = 0
	#Create the processors
	threads = []
	for i in range(processor_num):
		#Try to make  parameters locally
		threads.append(multiprocessing.Process(target=ThresholdRunAlgorithm, args=(base, indirect_sensitivity, arrangement_of_tau_ids[i], 1, tilde_Q_tau)))	
		threads[i].start()
	for i in range(processor_num):
		threads[i].join()
	#Obtain the tau with maximum tilde_Q_tau
	max_ind = 1
	max_val = 0
	for i in range(1,max_i+1):
		tau = math.pow(base,i)
		if tau>=indirect_sensitivity:
			Q_tau[i] = real_query_result
		else:
			if stop_duals[i]==1:
				Q_tau[i] = duals[i]
			else:
				Q_tau[i] = primals[i]
		hat_Q_tau[i] += Q_tau[i]
		tilde_Q_tau[i] += Q_tau[i]
		#The the the LP is early stoped, the result should not be counted
		if early_stops[i]==1:
			continue
		if tilde_Q_tau[i]>max_val:
			max_val = tilde_Q_tau[i]
			max_ind = i
	final_res = tilde_Q_tau[max_ind]
	return final_res



def ThresholdRunAlgorithm(base, indirect_sensitivity, assigned_of_tau_ids, LP_type, tilde_Q_tau):
	for i in assigned_of_tau_ids:
		tau = math.pow(base,i)
		if tau<indirect_sensitivity:
			LPSolver(tau, LP_type, i, tilde_Q_tau[i])



def LPSolver(tau, LP_type, tau_index, factor):
	global ids
	global values
	global joins
	global value_join_dic
	global id_join_dic
	global approximate_factor
	global stop_primals
	global stop_duals
	global global_max
	global primals
	global duals

	num_ids = len(ids)
	num_values = len(values)
	num_joins = len(joins)

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.maximize)

	obj = np.append(np.ones(num_values), np.zeros(num_joins))
	ub = np.ones(num_values + num_joins)
	cpx.variables.add(obj=obj, ub=ub)

	rhs = np.append(np.zeros(num_values), np.ones(num_ids) * tau)
	senses = "L" * (num_values + num_ids)
	cpx.linear_constraints.add(rhs=rhs, senses=senses)

	#Set the coefficients
	cols = []
	rows = []
	vals = []

	for i in range(num_values):
		cols.append(i)
		rows.append(i)
		vals.append(1)

		for j in value_join_dic[i]:
			cols.append(num_values + j)
			rows.append(i)
			vals.append(-1)

	for i in range(num_ids):
		for j in id_join_dic[i]:
			cols.append(num_values + j)
			rows.append(num_values + i)
			vals.append(1)

	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))

	cpx.set_log_stream(None)
	cpx.set_error_stream(None)
	cpx.set_warning_stream(None)
	cpx.set_results_stream(None)

	#Set the optimizer
	if LP_type == 0:
		cpx.parameters.lpmethod.set(1)
	else:
		cpx.parameters.lpmethod.set(2)

	optimizer = cpx.register_callback(Optimizer)
	optimizer.threshold = tau * approximate_factor
	optimizer.tau = tau
	optimizer.LP_type = LP_type
	optimizer.tau_index = tau_index
	optimizer.factor = factor
	cpx.solve()

	# If the get the feasible solution, update the information
	if LP_type == 0 and cpx.solution.get_status() == cpx.solution.status.optimal:
		primals[tau_index] = cpx.solution.get_objective_value()
		if global_max.value <= factor + primals[tau_index]:
			global_max.value = factor + primals[tau_index]
		stop_primals[tau_index] = 1
		if global_max.value <= factor + primals[tau_index]:
			global_max.value = factor + primals[tau_index]
	elif LP_type == 1 and cpx.solution.get_status() == cpx.solution.status.optimal:
		duals[tau_index] = cpx.solution.get_objective_value()
		if global_max.value <= factor + duals[tau_index]:
			global_max.value = factor + duals[tau_index]
		stop_duals[tau_index]=1
		if global_max.value <= factor + duals[tau_index]:
			global_max.value = factor + duals[tau_index]

def main(argv):
	#The input file including the relationships between aggregations and base tuples
	global input_file_path
	#Privacy budget
	global epsilon
	#Error probablity: with probablity at least 1-beta, the error can be bounded
	global beta
	#The global sensitivity
	global global_sensitivity
	#The number of processor
	global processor_num
	#The approximate factor
	global approximate_factor
	approximate_factor = 0
	#The real query result
	global real_query_result
	try:
		opts, args = getopt.getopt(argv,"h:I:e:b:G:p:",["Input=","epsilon=","beta=","GlobalSensitivity=","ProcessorNum="])
	except getopt.GetoptError:
		print("R2T.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("R2T.py -I <input file> -e <epsilon(default 0.1)> -b <beta(default 0.1)> -G <global sensitivity(default 1000,000)> -p <processor number(default 10)>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)
		elif opt in ("-b","--beta"):
			beta = float(arg)
		elif opt in ("-G","--GlobalSensitivity"):
			global_sensitivity = float(arg)
		elif opt in ("-p","--ProcessorNum"):
			processor_num = int(arg)
	#Two processors for one task: primal and dual
			
	processor_num = int(processor_num)
	if processor_num <1:
		processor_num = 1
	start = time.time()
	ReadInput()
	res = RunAlgorithm()

	if res < 0:
		res = 0
		
	end = time.time()
	# print("Query Result")
	# print(real_query_result)
	# print("Noised Result")
	# print(res)
	# print("Error")
	print(abs(res - real_query_result))
	# print("Time")
	# print(end-start)

if __name__ == "__main__":
	main(sys.argv[1:])