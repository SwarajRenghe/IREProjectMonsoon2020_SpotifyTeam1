import os
import sys

def parse_line(line):
    s1 = line.split("=")
    return s1[0]

def extract_ids(file1, file2, dirname):
    f1 = open(dirname + "/" + file1, 'r')
    line1 = f1.readline().strip('\n')
    maps = {}
    num = 0

    while (line1):
        maps[line1] = num
        num += 1
        if line1 == "0001ZVMPt41Vwzt1zsmuzp":
            print(maps)
        line1 = f1.readline().strip('\n')
    f1.close()
    
    f1 = open(dirname+"/"+file2, 'r')
    of = open(dirname + "/artists_al_ints.txt", 'w')
    line1 = f1.readline().strip('\n')

    while (line1):
        comps = line1.split()
        of.write(str(maps[comps[0]])+" "+ str(maps[comps[1]])+" "+comps[2]+"\n") 
        line1 = f1.readline().strip('\n')
        
    of.close()
    f1.close()

extract_ids("unique_artists.txt", "al_all.txt", "/media/tanvi/New Volume/Spotify_Project/network/for_artists/")
