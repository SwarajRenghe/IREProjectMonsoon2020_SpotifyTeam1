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

import pickle
from pickle import load


TOPK = 100
TOP_RES = 10
directory = "../../data/custom/embeddings/"
index_dir = "../../data/custom/"
search_space = []

#load the id2name dataframe and prepare it
id2name = pd.read_csv(index_dir+'id2song.csv',sep=':')
song_name = id2name.set_index('id')['name'].to_dict()
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness",
            "loudness","mode","popularity","speechiness","tempo","valence","year"]


musical_df1 = pd.read_csv(index_dir+'combined_features_1.csv')
musical_df2 = pd.read_csv(index_dir+'combined_features_2.csv', names = musical_df1.columns)

#append csv parts into one dataframe
musical_df = pd.DataFrame(columns = musical_df1.columns)
musical_df = musical_df.append(musical_df1, ignore_index = True) 
musical_df = musical_df.append(musical_df2, ignore_index = True)
print("All features")
print(musical_df1.columns)