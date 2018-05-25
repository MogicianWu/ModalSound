from tinydb import TinyDB, Query
from collections import Counter
import csv
import sys
import os

from shutil import copyfile
from sets import Set

#retrieve error type messages from results of gen_tet.py
if __name__ == '__main__':
	opt = sys.argv[1]
	#merge different thread's results into one tinydb file
	if opt == '0':
		db = TinyDB('result.json')
		User = Query()
		#read in results from different threads
		for i in range(8):
			print ('copying from thread: ' + str(i))
			db_name = 'result' + str(i) + '.json'
			thread_db = TinyDB(db_name)
			for e in range(6):
				entries = thread_db.search(User.error_type == str(e))
				for entry in entries:
					id = entry['id']
					error = entry['error']
					error_type = entry['error_type']
					runtime = entry['runtime']
					db.insert({'id':id, 'error': error, 'error_type': error_type, 'runtime':runtime})
	#display error results of each type
	elif opt == '1':
		db = TinyDB('result.json')
		User = Query()
		for i in range(6):
			seg =  db.search(User.error_type == str(i))
			print ('type ' + str(i) + ' error: ' + str(len(seg)))
			for e in seg:
				print (e['error'])
	#remove meshes that have more than 1 connected components
	elif opt == '2':
		with open('/home/mogicianwu/Downloads/Thingi10K/raw_meshes.csv', 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			invalid_comp_rows = [row for row in reader if int(row['num_connected_components']) > 1]

		#generate set of ids
		invalid_ids = []
		for row in invalid_comp_rows:
			invalid_ids.append(row['basename'][:-5])

		#remove invalid cases from cleaned_meshes folder
		for id in invalid_ids:
			command = "rm -f /home/mogicianwu/Downloads/Thingi10K/cleaned_meshes/" + id + ".obj"
			os.system(command)
			print ('mesh ' + id + ' was removed ')




