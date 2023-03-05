'''
To process iterable data in a parallel way 
'''

from joblib import Parallel, delayed  
import os
import pickle

def process_element(element):
	'''
	element: the element in the iterable data
	return: the processed results 
	'''
	return element
	
def process_iterable_data(id_cpu, iterable_data, num_cpu, output_path):
	'''
	id_cpu: the index of CPUs
	iterable_data: data that can be iterated, including strings, tuples, lists, sets, dictionaries
	num_cpu: the total number of CPUs
	'''
	# initialize index of integrable data and results
	index = -1
	list_results = []
	for element in iterable_data:
		index += 1
		if (index % num_cpu == id_cpu):
			result_element = process_element(element)
			list_results.append(result_element)
	# write results
	with open(output_path + str(id_cpu) + '.pickle', 'wb') as f:
		pickle.dump(list_results, f)
		
# input file settings 		
input_path = './data_4_test/'
input_name = 'mixing_results_110.json'
input_file_name = input_path + input_name
	
iterable_data = []
with open(input_file_name) as f:
	for line in f:
		iterable_data.append(line)

# output file settings
output_path = './results/'
os.makedirs(output_path, exist_ok=True)

# number of CPUs
num_cpu = 2

Parallel(n_jobs = num_cpu)(delayed(process_iterable_data)(id_cpu, iterable_data, num_cpu, output_path) for id_cpu in range(num_cpu)) 