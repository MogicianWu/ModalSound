import os
import time
from os.path import isfile, join
from tinydb import TinyDB, Query
import subprocess
import thread
import threading

#function within one thread;
#read and execute isostuffer for files range from start_i to end_i(exclusive)
def thread_func(start_i,end_i,db,files,meta_dir):
	for i in range(start_i,end_i):
		f = files[i]
		f_id = f[:-4]

		#read in meta info; decide what grid resolution to use
		meta_f = open(meta_dir + str(f_id) + ".txt", "r")
		max_x,max_y,max_z = meta_f.readline().split(",")
		min_x,min_y,min_z = meta_f.readline().split(",")
		min_d = meta_f.readline()

		#check if the watertight tetrahedron has been generated before
		#if so skip this mesh
		output_path = "/home/mogicianwu/Downloads/Thingi10K/corner_cases/tets/" + f_id + ".tet"
		if os.path.isfile(output_path):
			continue

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
			print ('progress: ' + str(percentage))
			print ('finished processing, runtime: ' + str(runtime))
			print ("id: " + str(f_id))
		
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


list_of_dbs = []
for i in range(8):
	name = 'result' + str(i) +'.json'
	list_of_dbs.append(TinyDB(name))

mesh_dir = "/home/mogicianwu/Downloads/Thingi10K/corner_cases/cleaned_reori_meshes/"
meta_dir = "/home/mogicianwu/Downloads/Thingi10K/meta/"

onlyfiles = [f for f in os.listdir(mesh_dir) if isfile(join(mesh_dir, f))]

for t in range(8):
	thread_num_files = int(len(onlyfiles)/8)
	start_i = t * thread_num_files
	end_i = (t+1) * thread_num_files
	end_i = min(end_i,len(onlyfiles))
	args = (start_i,end_i,list_of_dbs[t],onlyfiles,meta_dir)
	new_thread = threading.Thread(target = thread_func, args = args)
	new_thread.start()
	print ('thread ' + str(t) + ' started')




