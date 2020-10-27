import os
import sys


def update_al(al_file, uids_file, dirname):
	f1 = open(uids_file, 'r')
	line1 = f1.readline().strip('\n')

	print("Making the dict mapping. Starts from 1")	
	id_map = {}
	next_id = 0 
	while (line1):
		id_map[line1] = next_id
		next_id += 1
		line1 = f1.readline().strip('\n')
		if next_id % 1000 == 0:
			print(next_id)
	f1.close()

	print("Now writing to new file")
	ipf = open(dirname + "/" + al_file, 'r')
	of = open( dirname + "/al_songs_ints_5000.txt", 'w+')
	line = ipf.readline().strip('\n')
	
	while(line):
		lp = line.split(' ')
		try:
            #of.write(str(id_map[lp[0]]) + " " + str(id_map[lp[1]]) + "\n")
			of.write(str(id_map[lp[0]]) + " " + str(id_map[lp[1]]) + " " + lp[2] + "\n")
		except:
		 	print(lp)
		 	print("breaking!!")
		 	break
		line = ipf.readline().strip('\n')
	
	ipf.close()
	of.close()

update_al(sys.argv[1], sys.argv[2], sys.argv[3])
#update_al(sys.argv[1], sys.argv[2], "/media/tanvi/New Volume/Spotify_Project/network")
