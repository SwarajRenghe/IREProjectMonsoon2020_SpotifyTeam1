'''
Script to generate playlist of songs using the 
advanced search option wherein the user provides
a set of paramters based on which the search results
are produced
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
from functools import partial

import pickle
from pickle import load

from config import *
from mood import * 
from positive import *
from negative import *
from field import *
from api_songs import *
from probabilistic import *


def compute_emb(filename, query_id):

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


# Find appropriate network embedding for query
def get_embeddings(query_id):
    pool0 = multiprocessing.Pool() 
    pool0 = multiprocessing.Pool() 
    files = [filename for filename in os.listdir(directory)]   
    compute = partial(compute_emb, query_id = query_id)
    outputs0 = pool0.map(compute, files)
    query_features = [item for sublist in outputs0 for item in sublist]

    if ("".join(map(str, query_features)) == ""):
        print("Getting spotify features ...")
        query_features = get_from_api(query_id)

    return query_features


def set_subtraction(pos, neg, field, mood_ids,search_space):
    
    # print("len pos ", len(pos))
    # print("len neg ", len(neg))
    # print("len field ", len(field))
    # print("len ss ", len(search_space))

    pos_ids = [i[0] for i in pos]
    neg_ids = [i[0] for i in neg]
    field_ids = [i[0] for i in field]
    ss_ids = [i[0] for i in search_space]

    if pos:
        # print("in pos")
        final = [i for i in pos if i[0] not in neg_ids]
        if field:
            final  = [i for i in final if i[0] in field_ids]

    elif neg:
        # print("in neg")
        final = neg
        if field:
            final  = [i for i in final if i[0] in field_ids]
    elif field:
        # print("in field")
        final = field


    final_ids = [i[0] for i in final]
    if search_space:
        # print("in search")
        final = [value for value in search_space if value[0] in final_ids]

    if mood_ids :
        # print("mood ids")
        final = [value for value in final if value[0] in mood_ids] 
    
    return final


while (1):

    res_songs      = []
    positive_songs = []
    negative_songs = []
    field_songs    = []
    mood_songs     = []
    mood_file = ""

    print(Fore.GREEN+Style.BRIGHT+"\n\n************************************************"+Fore.RESET+Style.RESET_ALL)
    print(Fore.GREEN+Style.BRIGHT+"\tSONGIFY : PLAYLIST GENERATOR"+Fore.RESET+Style.RESET_ALL)
    print(Fore.GREEN+Style.BRIGHT+"************************************************\n\n"+Fore.RESET+Style.RESET_ALL)
    # print(len(search_space))
    print("> 'r' to reset")
    print("> 'q' to quit")
    print("> any key to continue\n")
    
    inp = input("Choice :")
    if inp == "q":
        break
    if inp == 'r':
        search_space.clear()

    mood_type = input("Enter a Mood: ") 
    pos_query_id = input("Enter a similarity song: ") 
    neg_query_id = input("Enter dissimilar song: ") 
    field = input("Enter a field details <field_type_name {'num','id'} song_id/numval> : ")
    if field:
        try:
            field_type_name, field_type, field_query_val = field.split()
        except:
            print("Please enter all the necessary entries ...")
            continue

    
    print("\nGenerating Playlist ... \n")


    #mood based search space
    if mood_type != "":
        #reset search space
        search_space.clear()
        mood_file = mood_dict[mood_type]
        mood_songs = get_mood_songs(mood_file)

    #positively related songs
    if pos_query_id != "":
        pos_query_features = get_embeddings(pos_query_id)
        positive_songs = get_positive_songs(pos_query_id, pos_query_features, mood_file)

    #negatively related songs
    if neg_query_id != "":
        neg_query_features = get_embeddings(neg_query_id)
        negative_songs = get_negative_songs(neg_query_id, neg_query_features, mood_file)


    #field based search
    if field!= "":
        field_songs = get_field_songs(field_query_val,field_type_name, field_type, mood_songs)

    #generating results as topk from mood if no other query is passed
    if pos_query_id == "" and neg_query_id == "" and field == "":
        res_songs = gen_random_prob(mood_songs)
        # for o in res_songs[:TOP_RES]:
        #     print(song_name[o])
            
        # search_space = res_songs
        # continue

    
    #using set subtraction with the queries passed 
    else:
        res_songs = set_subtraction(positive_songs, negative_songs, field_songs, mood_songs, search_space)


    search_space = res_songs

    print(Fore.CYAN+Style.BRIGHT+"\n====================================="+Fore.RESET+Style.RESET_ALL)
    print(Fore.CYAN+Style.BRIGHT+"\tYour Playlist is:"+Fore.RESET+Style.RESET_ALL)
    print(Fore.CYAN+Style.BRIGHT+"====================================="+Fore.RESET+Style.RESET_ALL)

    if not res_songs:
        print("Sorry, there were no songs for your request, please start fresh")
        search_space = []

    else:
        res_songs = prob_select(res_songs[:TOP_RES+50])

    for o in res_songs[:TOP_RES]:
        print(song_name[o])




