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
import requests 

import pickle
from pickle import load


TOPK = 10

try:
    directory = sys.argv[1]
    index_dir = sys.argv[3]
    query_id = sys.argv[2]
except:
    print("Script Usage:")
    print("python3 top_k.py <path to embeddings directory> <query song ID> <ID2Songs directory> <Auth token (optional)>")
    exit(0)

#load the id2name dataframe and prepare it
id2name = pd.read_csv(index_dir+'id2song.csv',sep=':')
song_name = id2name.set_index('id')['name'].to_dict()
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness",
            "loudness","mode","popularity","speechiness","tempo","valence","year"]

#load and prepare the regression model 
scaler = load(open('../approach_A/training/scaler.pkl', 'rb'))
filename='../approach_A/training/MLPRegressor_model.sav'
mlpreg_model =pickle.load(open(filename, 'rb'))


def get_from_api():

    final = {}

    #API endpoint 
    URL1 = "https://api.spotify.com/v1/audio-features/"
    URL2 = "https://api.spotify.com/v1/tracks/"
    try:
        TOKEN = sys.argv[4]
    except:
        print("Please pass an authorization token")
        exit(0)
    
    r = requests.get(url = URL1+query_id,  headers={'Authorization': 'Bearer '+TOKEN})
    data1 = r.json()
    r = requests.get(url = URL2+query_id,  headers={'Authorization': 'Bearer '+TOKEN})
    data2 = r.json()

    if (('error' in data1) and (data1['error']['status']==401)) or (('error' in data2) and (data2['error']['status']==401)) :
        print("Token expired :( ")
        exit(0)
    elif ('error' in data1) or ('error' in data2):
        print("\nSorry, spotify doesn't seem to have this song you are looking for :/")
        exit(0)

    print("Data retrieved\n")

    final['year'] = data2['album']['release_date']
    final['popularity'] = data2['popularity']
    song_name[query_id] = data2['name']


    for key in data1:
        if key in features:
            final[key] = data1[key]

    final = sorted(final.items(), key=lambda x: x[0])
    final = np.array([float(i[1]) for i in final]).reshape(1, -1)

    model_result=scaler.inverse_transform(mlpreg_model.predict(final))

    return model_result

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

if ("".join(map(str, query_features)) == ""):
    print("Getting spotify features ...")
    query_features = get_from_api()


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
