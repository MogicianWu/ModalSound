from tinydb import TinyDB, Query
from collections import Counter
import csv
import sys
import os

from shutil import copyfile
from sets import Set

if __name__ == '__main__':
	opt = sys.argv[1]
	#merge different thread's results
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
	#display results
	elif opt == '1':
		'''
		db1 = TinyDB('result.json')
		User1 = Query()
		db2 = TinyDB('result_reori.json')
		User2 = Query()

		'''	
		
		db = TinyDB('result.json')
		User = Query()
		for i in range(6):
			seg =  db.search(User.error_type == str(i))
			print ('type ' + str(i) + ' error: ' + str(len(seg)))
			for e in seg:
				print (e['error'])
		
		'''
		#copy type 1 error meshes to directory;
		db = TinyDB('result.json')
		User = Query()
		type_1_entries = db.search(User.error_type == '3')
		for entry in type_1_entries:
			id = entry['id']
			src = '/home/mogicianwu/Downloads/Thingi10K/watertight/' + str(id) + '.obj'
			dst = '/home/mogicianwu/Downloads/Thingi10K/type3/meshes/' + str(id) + '.obj'
			print ('file ' + str(id) + ' was copied')
			copyfile(src,dst)
		'''
		
	#remove meshes that have more than 1 connected components
	elif opt == '2':
		with open('/home/mogicianwu/Downloads/Thingi10K/raw_meshes.csv', 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			invalid_comp_rows = [row for row in reader if int(row['num_connected_components']) > 1]

		#generate set of ids
		ids = []
		for row in invalid_comp_rows:
			ids.append(row['basename'][:-5])
		#print ('need to remove' + str(len(ids)) + 'meshes')

		#remove invalid cases from watertight folder
		for id in ids:
			command = "rm -f /home/mogicianwu/Downloads/Thingi10K/watertight/" + id + ".obj"
			os.system(command)
			print ('mesh ' + id + ' was removed ')

		print ('need to remove' + str(len(ids)) + 'meshes')

		'''

		#read in crash cases; remove invalid cases
		db = TinyDB('result.json')
		User = Query()
		for i in range(6):
			seg =  db.search(User.error_type == str(i))
			for e in seg:
				if e['id'] in id_set:
					db.remove(User.id == e['id'])
					print ('mesh ' + e['id'] + ' was removed for having more than one connected component')
		'''

		




