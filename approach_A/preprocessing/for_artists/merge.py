import os
import sys

#parses the posting list
def parse_pl(pl):
	temp_dict = {}
	logs = pl.split(",")
	for song_id in logs:
		tmp = song_id.split(":")
		if len(tmp) == 2:
			temp_dict[tmp[0]] = int(tmp[1])
	return temp_dict
def merge_pl(pl1, pl2):
	dict1 = parse_pl(pl1)
	dict2 = parse_pl(pl2)

	for song_id in dict2:
		if song_id in dict1:
			dict1[song_id] += dict2[song_id]
		else:
			dict1[song_id] = dict2[song_id]
	
	pl = ""		
	for adj_sid in sorted(dict1):
		pl += adj_sid+":"+str(dict1[adj_sid])+","

	return pl

def parse_line(line):
	s1 = line.split("=")
	return s1[0], s1[1]

def merge_two_files(file1, file2, outfile, dirname):
	f1 = open(dirname+"/"+file1, 'r')
	f2 = open(dirname+"/"+file2, 'r')
	of = open(dirname+"/temp.txt", 'w')
	line1 = f1.readline().strip('\n')
	line2 = f2.readline().strip('\n')
	
	while (line1 or line2):

		if not(line2):
			of.write(line1 + '\n')
			line1 = f1.readline().strip('\n')
  		
		elif not(line1):
			of.write(line2 + '\n')
			line2 = f2.readline().strip('\n')
 
		else:
			word1, pl1 = parse_line(line1)
			word2, pl2 = parse_line(line2)
			#print(word1, word2)
			
			if word1 == word2:
				#print("same")
				of.write(word1 + '=' + merge_pl(pl1,pl2) + '\n')
				line1 = f1.readline().strip('\n')
				line2 = f2.readline().strip('\n')
 		
			elif word1 < word2:
				of.write(line1 + '\n')
				line1 = f1.readline().strip('\n')

			else:
				of.write(line2 + '\n')
				line2 = f2.readline().strip('\n')
   
	f1.close()
	f2.close()
	of.close()
	
	print("removing %s and %s, renaming temp.txt to %s"%(file1, file2, outfile))
	os.remove(dirname+"/"+file1)
	os.remove(dirname+"/"+file2)
	os.rename(dirname+"/temp.txt", dirname+"/"+outfile)

def merge_all_files(out_dir):
	print(out_dir)
	all_files = [name for name in os.listdir(out_dir) ]
	total_files = len(all_files)#ignoring the title file
	
	print(total_files)
	while total_files > 1:
		print("total files at loop beginning:", total_files)
		i = 0
		while i*2 + 1 < total_files:
			file1 = "file"+ str(2*i) + ".txt"
			file2 = "file"+ str(2*i + 1) + ".txt"
			outfile = "file"+ str(i) + ".txt" 
			merge_two_files(file1, file2, outfile, out_dir)
			print("merged %s and %s into %s"%(file1, file2, outfile))
			i += 1
		if total_files % 2 == 1:
			os.rename(out_dir+"/file"+str(2*i)+".txt", out_dir+"/file"+str(i)+".txt")
		total_files = (total_files + 1) // 2
		print("\rtotalfiles is %d"%(total_files))

merge_all_files("/media/tanvi/New Volume/Spotify_Project/network/for_artists")
