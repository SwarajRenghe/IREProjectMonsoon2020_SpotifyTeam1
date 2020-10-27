'''
Script to search for the top K songs that 
are similar to a given query song

Uses threading and cosine similarity for each song
'''

import json
import pandas as pd
import numpy as np
from scipy.spatial import distance
import multiprocessing 
import time 
import os
import sys
import time 


TOPK = 10
directory = sys.argv[1]
# query = sys.argv[2].split(':')
index_dir = sys.argv[3]

query_id = sys.argv[2]
# query_features = np.array(query[1].split(" ")).astype(np.float)

#load the id2name dataframe and prepare it
id2name = pd.read_csv(index_dir+'id2song.csv',sep=':')
song_name = id2name.set_index('id')['name'].to_dict()

def compute_emb(filename):
    # print("emb", filename)
    with open(directory+filename, 'r') as f:
        
        song = f.readline()
        while song:
            song = song.strip().split(':')
            song_id = song[0]
            
            song_features = np.array(song[1].split(" ")).astype(np.float)


            if song_id == query_id:
                return song_features

            song = f.readline()

    return ""


def compute_topk(filename):
    # print("in for file", filename)
    index = {}
    with open(directory+filename, 'r') as f:
        
        song = f.readline()

        while song:
            song = song.strip().split(':')
            song_id = song[0]
            
            song_features = np.array(song[1].split(" ")).astype(np.float)

            score = 1-distance.cosine(query_features, song_features)
            if song_id == query_id:
                song = f.readline()
                continue

            index[song_id] = score

            song = f.readline()

    sorted_songs = sorted(index.items(), key=lambda x: x[1], reverse=True)
    return sorted_songs[:TOPK]


print("\nGenerating Playlist ... \n")

# Find appropriate network embedding for query
pool0 = multiprocessing.Pool() 
pool0 = multiprocessing.Pool() 
files = [filename for filename in os.listdir(directory)]   
outputs0 = pool0.map(compute_emb, files)
query_features = [item for sublist in outputs0 for item in sublist]

#Perform multithreaded search for the songs
pool = multiprocessing.Pool() 
pool = multiprocessing.Pool() 
files = [filename for filename in os.listdir(directory)]   
outputs = pool.map(compute_topk, files)

#format the outputs to flatten list
#sort the sub results
outputs = [item for sublist in outputs for item in sublist]
my_dict = dict(outputs)
sorted_output = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)


print("\nInput song = ", song_name[query_id])

print("\n===================================")
print("Your Playlist is:")
print("===================================")

for o in sorted_output[:TOPK]:
    print(song_name[o[0]])
