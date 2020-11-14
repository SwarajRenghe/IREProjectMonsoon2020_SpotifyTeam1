import os
import sys

def split(file1, dirname):
	f1 = open(file1, 'r')
	of = open(dirname+"/file0.txt", 'w')
	line1 = f1.readline().strip('\n')
	
	num = 0
	filenum = 1
	while (line1):
		
		of.write(line1 + '\n')
		num += 1	
		if num%1000000 == 0:
			of.close()
			of = open(dirname+"/file%s.txt"%(filenum), 'w')
			print("Writing file %d"%(filenum))
			filenum += 1

		line1 = f1.readline().strip('\n')
 
   
	f1.close()
	of.close()

split("/media/tanvi/New Volume/Spotify_Project/network/al_song_ids.txt", "/media/tanvi/New Volume/Spotify_Project/network/for_artists")
