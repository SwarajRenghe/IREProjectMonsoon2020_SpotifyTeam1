import os
import sys

def parse_line(line):
	s1 = line.split("=")
	return s1[0]

def extract_ids(file1, dirname):
	f1 = open(dirname+"/"+file1, 'r')
	of = open("unique_ids_postmerge.txt", 'w')
	line1 = f1.readline().strip('\n')
	
	while (line1):
		of.write(parse_line(line1) + '\n')
		line1 = f1.readline().strip('\n')
   
	f1.close()
	of.close()
	

extract_ids("file0.txt", "/media/tanvi/New Volume/Spotify_Project/network")