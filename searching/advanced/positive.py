import json
import pandas as pd
import numpy as np
from scipy.spatial import distance
import multiprocessing 
import time 
import os
import sys
import time 
import requests 
from functools import partial

import pickle
from pickle import load

from config import *


direc = directory

def get_positive_k(filename,query_id, query_features):
    
    index = {}
    with open(direc+filename, 'r') as f:
        
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

def get_positive_songs(query_id, query_features, mood_file):


    #Perform multithreaded search for the songs
    pool = multiprocessing.Pool() 
    pool = multiprocessing.Pool() 
    files = [filename for filename in os.listdir(direc)]  
    get_pos = partial(get_positive_k, query_id = query_id, query_features = query_features)
    outputs = pool.map(get_pos, files)

    #format the outputs to flatten list
    #sort the sub results
    outputs = [item for sublist in outputs for item in sublist]
    my_dict = dict(outputs)
    sorted_output = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_output