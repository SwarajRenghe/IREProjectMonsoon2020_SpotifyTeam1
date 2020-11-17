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
import random

import pickle
from pickle import load

from colorama import Fore, Back, Style
from colorama import init
init()



TOPK = 100
TOP_RES = 10
directory = "../../data/custom/embeddings/"
index_dir = "../../data/custom/"
for_artist_dir = "../../approach_A/preprocessing/for_artists/"

search_space = []

#load the id2name dataframe and prepare it
id2name = pd.read_csv(index_dir+'id2song.csv',sep=':')

# nancount = id2name['name'].isna().sum()
# print("id2song nan", nancount)

song_name = id2name.set_index('id')['name'].to_dict()
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness",
            "loudness","mode","popularity","speechiness","tempo","valence","year"]


musical_df1 = pd.read_csv(index_dir+'combined_features_1.csv')
musical_df2 = pd.read_csv(index_dir+'combined_features_2.csv', names = musical_df1.columns)

#append csv parts into one dataframe
musical_df = pd.DataFrame(columns = musical_df1.columns)
musical_df = musical_df.append(musical_df1, ignore_index = True) 
musical_df = musical_df.append(musical_df2, ignore_index = True)


def load_artists(ids, emb):
    f1 = open(ids, 'r')
    line1 = f1.readline().strip('\n')

    f2= open(emb, 'r')
    line2 = f2.readline().strip('\n')
    
    dict_ret = {}

    while(line1):
        
        dict_ret[line1] = line2.split()

        line1 = f1.readline().strip('\n')
        line2 = f2.readline().strip('\n')


    f1.close()
    f2.close()

    return dict_ret

artists_dict = load_artists(for_artist_dir+"unique_artists.txt",for_artist_dir+"outfile_ARTISTS524288.txt")


mood_dir = index_dir + "mood_emb/"
mood_dict = {
    "mood0" : mood_dir + "mood_0.txt",
    "mood1" : mood_dir + "mood_1.txt",
    "mood2" : mood_dir + "mood_2.txt",
    "mood3" : mood_dir + "mood_3.txt",
    "mood4" : mood_dir + "mood_4.txt",
    "mood5" : mood_dir + "mood_5.txt",
    "mood6" : mood_dir + "mood_6.txt",
    "mood7" : mood_dir + "mood_7.txt",
    "mood8" : mood_dir + "mood_8.txt",
    "mood9" : mood_dir + "mood_9.txt"
}
