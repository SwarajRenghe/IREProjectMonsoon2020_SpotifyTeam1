'''
Script to output the result of the regression model 
for a new song that is queried, using its musical features
from the spotify API results.
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

from config import *


#load and prepare the regression model 
scaler = load(open('../../approach_A/training/scaler.pkl', 'rb'))
filename='../../approach_A/training/MLPRegressor_model.sav'
mlpreg_model =pickle.load(open(filename, 'rb'))


def get_from_api(query_id):

    final = {}

    #API endpoint 
    URL1 = "https://api.spotify.com/v1/audio-features/"
    URL2 = "https://api.spotify.com/v1/tracks/"
    try:
        TOKEN = sys.argv[1]
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