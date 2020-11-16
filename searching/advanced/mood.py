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


def get_mood_songs(mood_file):

    index = []
    with open(mood_file, 'r') as f:
        
        song = f.readline()

        while song:
            song = song.strip().split(':')
            song_id = song[0]
            
            song_features = np.array(song[1].split(" ")).astype(np.float)

            # score = 1-distance.cosine(query_features, song_features)
            # if song_id == query_id:
            #     song = f.readline()
            #     continue
            # index[song_id] = score

            index.append(song_id)
            song = f.readline()

    # sorted_songs = sorted(index.items(), key=lambda x: x[1], reverse=True)

    return index