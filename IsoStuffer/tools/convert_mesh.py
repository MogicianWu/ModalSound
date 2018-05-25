import os
import sys
from os.path import isfile, join

#convert meshes into pure triangle mesh and reorient faces
if __name__ == "__main__":
	raw_mesh_dir = "/home/mogician/Downloads/Thingi10K/raw_meshes" #example raw mesh and output directories
	output_dir = "/home/mogician/Downloads/Thingi10K/reoriented_meshes/"

	if len(sys.argv) == 3:
		raw_mesh_dir = sys.argv[1]
		output_dir = sys.argv[2] 

	print ('reading raw mesh from directory: ' + str(raw_mesh_dir))
	print ('outputing cleaned mesh to: ' + str(output_dir))
	#first read in list of file names from raw mesh directory
	onlyfiles = [f for f in os.listdir(raw_mesh_dir) if isfile(join(raw_mesh_dir, f))]
	counter = 0

	#for each file, read them into meshlab, convert them into pure triangle meshes and reorient the faces
	for f in onlyfiles:
		counter += 1
		f_id = f[:-4]
		print ()
		print ("converting file: " + str(counter) + ' out of ' + str(len(onlyfiles)) + ' files')
		print ("mesh id: " + str(f_id))
		print ()
		command = "meshlabserver -i "
		command += join(raw_mesh_dir, f)
		command += (" -o " + output_dir + " " + f_id + ".obj ")
		command += "-s mesh_script.mlx -om"
		print ('command: ' + str(command))
		os.system(command)




