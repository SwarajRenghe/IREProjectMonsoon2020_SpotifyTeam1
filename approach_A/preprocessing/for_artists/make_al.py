import os
import sys

#parses the posting list
def parse_pl(pl):
	temp_dict = {}
	logs = pl.split(",")
	for song_id in logs:
		tmp = song_id.split(":")
		if len(tmp) == 2:
			temp_dict[tmp[0]] = (tmp[1])
	return temp_dict
	return pl

def parse_line(line):
	s1 = line.split("=")
	return s1[0], parse_pl(s1[1])

def dict_to_al(file1, outfile, dirname):
	f1 = open(dirname+"/"+file1, 'r')
	of = open(dirname+"/al_all.txt", 'w')
	line1 = f1.readline().strip('\n')
	
	while (line1):

		word1, pl1 = parse_line(line1)
        
		for song_id in pl1:
			if song_id == word1:
				continue
			of.write(word1 + ' ' + song_id + ' ' + pl1[song_id] + '\n')
		line1 = f1.readline().strip('\n')
  		

	f1.close()
	of.close()

dict_to_al("file0.txt", "artis_al.txt", "/media/tanvi/New Volume/Spotify_Project/network/for_artists")
