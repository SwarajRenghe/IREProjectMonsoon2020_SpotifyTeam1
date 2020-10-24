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


TOPK = 10
directory = sys.argv[1]
query = sys.argv[2].split(':')
query_id = query[0]
query_features = np.array(query[1].split(",")).astype(np.float)

features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness","loudness","mode","popularity","speechiness","tempo","valence","year"]


def compute_topk(filename):
    print("in for file", filename)
    time.sleep(3)
    index = {}
    with open(directory+filename, 'r') as f:
        
        song = f.readline()

        while song:
            song = song.strip().split(':')
            song_id = song[0]
            song_features = np.array(song[1].split(",")).astype(np.float)

            score = distance.cosine(query_features, song_features)
            index[song_id] = score

            song = f.readline()

    sorted_songs = sorted(index.items(), key=lambda x: x[1], reverse=True)
    return sorted_songs[:TOPK]




pool = multiprocessing.Pool() 
pool = multiprocessing.Pool() 
files = [filename for filename in os.listdir(directory)]   



outputs = pool.map(compute_topk, files)
print("out", outputs)