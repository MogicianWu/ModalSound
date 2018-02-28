import os
import time
from os.path import isfile, join
import subprocess
import thread
import threading

#function within one thread;
#read and check if cleaned mesh is water tight; if so add to folder
def thread_func(start_i,end_i):
	command = "/home/mogicianwu/Downloads/libigl-example-project/build/example_bin "
	command += str(start_i) + " " + str(end_i)
	os.system(command)

#get list of pure triangle obj files
mesh_dir = "/home/mogicianwu/Downloads/Thingi10K/cleaned"

onlyfiles = [f for f in os.listdir(mesh_dir) if isfile(join(mesh_dir, f))]

for t in range(8):
	thread_num_files = int(len(onlyfiles)/8)
	start_i = t * thread_num_files
	end_i = (t+1) * thread_num_files
	end_i = min(end_i,len(onlyfiles))
	args = (start_i,end_i)
	new_thread = threading.Thread(target = thread_func, args = args)
	new_thread.start()
	print ('thread ' + str(t) + ' started')




