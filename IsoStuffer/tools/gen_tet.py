import os
import time
import sys
from os.path import isfile, join
from tinydb import TinyDB, Query
import subprocess
import thread
import threading

#function within one thread;
#read and execute isostuffer for files range from start_i to end_i(exclusive)
def thread_func(start_i, end_i, db, files, output_dir):
	for i in range(start_i,end_i):
		f = files[i]
		f_id = f[:-4]
		found = False
		#only generate tets that were confirmed as good 
		for t in tetfiles:
			if t[:-4] == f_id:
				found = True
		if not found:
			continue
		
		#check if the watertight tetrahedron has been generated before
		#if so skip this mesh
		output_path = output_dir + f_id + ".tet"
		if os.path.isfile(output_path):
			continue

		#resolution of octree grid; 
		resolution = 7
		command = "../gcc-build/src/isostuffer "
		command += "-R " + str(resolution) + " "
		command += join(mesh_dir, f) + " "
		command += output_path

		start_time = time.time()
		proc = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
		output, error = proc.communicate()

		if proc.returncode != 0:
			runtime = time.time() - start_time
			percentage = float(i - start_i)/float(end_i - start_i)
			print ('mesh ' + str(f_id) + ' caused isostuffer to throw an error')
			print ('percentage done for this thread: ' + str(percentage))
			print ('runtime: ' + str(runtime))
		
			strings = error.split(" ")
			if len(strings) < 1:
				error_type = 0
			else:
				if strings[1] == "SHOULD":
					error_type = 1
				elif strings[1] == "triangle":
					error_type = 2
				elif strings[0] == "Segmentation":
					error_type = 3
				elif strings[0] == "Aborted":
					error_type = 4
				else:
					error_type = 5

			db.insert({'id': str(f_id), 'error' : str(error), 'runtime': str(runtime), 'error_type': str(error_type)})

if __name__ == '__main__':
	output_dir = "/home/mogician/Downloads/Thingi10K/FV_final_tets/"
	mesh_dir = "/home/mogician/Downloads/Thingi10K/cleaned_meshes/"
	num_threads = 8 #number of paralleled threads to run isostuffer; default is 8

	if len(sys.argv) == 4:
		output_dir = sys.argv[1]
		mesh_dir = sys.argv[2]
		num_threads = sys.argv[3]

	tetfiles = [f for f in os.listdir(output_dir) if isfile(join(output_dir, f))]
	onlyfiles = [f for f in os.listdir(mesh_dir) if isfile(join(mesh_dir, f))]

	#used tinydb to record errors in each call
	list_of_dbs = []
	for i in range(num_threads):
		name = 'result' + str(i) +'.json'
		list_of_dbs.append(TinyDB(name))
	
	for t in range(num_threads):
		thread_num_files = int(len(onlyfiles)/num_threads)
		start_i = t * thread_num_files
		end_i = (t+1) * thread_num_files
		if t == num_threads - 1:
			end_i = len(onlyfiles)
		args = (start_i, end_i, list_of_dbs[t], onlyfiles, output_dir)
		new_thread = threading.Thread(target = thread_func, args = args)
		new_thread.start()
		print ('thread ' + str(t) + ' started')




