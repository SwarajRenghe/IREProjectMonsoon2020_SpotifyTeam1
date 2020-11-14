import os
import sys
import pandas as pd
from itertools import chain
import ast

def get_artists():
    df = pd.read_csv("/home/tanvi/Desktop/IRE/Project/IREProjectMonsoon2020_SpotifyTeam1/data/custom/combined_features_1.csv", usecols=[1,5]) 
    print(df.head())
    dict1 = df.set_index('id').T.to_dict()

    df = pd.read_csv("/home/tanvi/Desktop/IRE/Project/IREProjectMonsoon2020_SpotifyTeam1/data/custom/combined_features_2_upd.csv", usecols=[1,5]) 
    print(df.head())
    dict2 = ( df.set_index('id').T.to_dict() )
    
    dict_final = dict(chain.from_iterable(d.items() for d in (dict1, dict2)))
    print(len(dict_final))
    return dict_final

def parsefile(infile, dirname):
    artist_network = {}
    
    f1 = open(dirname+"/"+infile, 'r')
    line = f1.readline().strip('\n')
    
    num_so_far = 0
    while (line):
        num_so_far += 1
        if num_so_far % 500000 == 0:
            print(infile, num_so_far)

        comps = (line.split())
        line = f1.readline().strip('\n')
        try:
            art1 = ast.literal_eval(a_dict[comps[0]]['artists'])
            art2 = ast.literal_eval(a_dict[comps[1]]['artists'])
        except:
            continue

        wt = int(comps[2])
        
        for a1 in art1:
            for a2 in art2:
                if a1 == a2:
                    continue
    
                if a1 in artist_network:
                    pass
                else:
                    artist_network[a1] = {}
        
                if a2 in artist_network[a1]:
                    artist_network[a1][a2] += wt
                else:
                    artist_network[a1][a2] = wt
                            

    f1.close()

    of = open(dirname+"/temp.txt", 'w')
    for artist_id in sorted(artist_network):
        of.write(artist_id+"=")
        for adj_id in sorted(artist_network[artist_id]):
            of.write(adj_id+":"+str(artist_network[artist_id][adj_id])+",")
        of.write("\n")

    of.close()

    os.remove(dirname+"/"+infile)
    os.rename(dirname+"/temp.txt", dirname+"/"+infile)

def parse(dirname):
    
    for filename in os.listdir(dirname):
        try:
            parsefile(filename, dirname)
        except:
            pass

a_dict = get_artists()        
parse("/media/tanvi/New Volume/Spotify_Project/network/for_artists")
