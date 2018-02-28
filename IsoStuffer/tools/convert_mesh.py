import os
from os.path import isfile, join

#first read in list of file names from Thingi10k database
mesh_dir = "/home/mogicianwu/Downloads/Thingi10K/corner_cases/meshes"
onlyfiles = [f for f in os.listdir(mesh_dir) if isfile(join(mesh_dir, f))]
counter = 0

#for each file, read them into meshlab and re-orient them
for f in onlyfiles:
	counter += 1
	f_id = f[:-4]
	print ("converting file: " + str(counter))
	print ("id: " + str(f_id))
	command = "meshlabserver -i "
	command += join(mesh_dir, f)
	command += (" -o /home/mogicianwu/Downloads/Thingi10K/corner_cases/reori_meshes/" + f_id + ".obj ")
	command += "-s reorient-face.mlx -om"
	print ('command: ' + str(command))
	os.system(command)




