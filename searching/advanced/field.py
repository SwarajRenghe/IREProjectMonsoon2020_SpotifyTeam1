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

direc = index_dir

def get_field_query_val(df, query_id, field_type_name):

    df_copy = df
    sub_df = df_copy.loc[df_copy['id'] == query_id][field_type_name]  

    if len(sub_df.index) == 0:
        return ""

    sub_df = sub_df.to_dict() 
    id_key = next(iter(sub_df))
    val = float(sub_df[id_key])
    return val


def get_field_k(df,field_query_val, field_type_name, mood_songs):
    
    df[field_type_name] -= field_query_val
    df = df.sort_values(by=field_type_name, ascending=True)

    df = df[['id', field_type_name]] 
    df = df[df[field_type_name] <= 0.2]
    df[field_type_name]=df[field_type_name].abs()
    df[field_type_name]*=-1
    df[field_type_name]+=2

    result = df.set_index('id').to_dict()[field_type_name]

    sorted_songs = sorted(result.items(), key=lambda x: abs(x[1]), reverse=True)
    return sorted_songs



def get_field_songs(field_query_val,field_type_name, field_type, mood_songs):

    if field_type == "num":
        field_query_val = float(field_query_val)

    else:
        pool0 = multiprocessing.Pool() 
        pool0 = multiprocessing.Pool() 
        dataframes = [musical_df1, musical_df2]  
        get_field_query_v = partial(get_field_query_val, query_id = field_query_val, field_type_name = field_type_name)
        outputs = pool0.map(get_field_query_v, dataframes)
        
        field_query_val = [item for item in outputs if item!=''][0]
     

    #Perform multithreaded search for the songs
    pool = multiprocessing.Pool() 
    pool = multiprocessing.Pool() 
    dataframes = [musical_df1, musical_df2]  
    get_field = partial(get_field_k, field_query_val = field_query_val, field_type_name=field_type_name, 
                        mood_songs = mood_songs)
    outputs = pool.map(get_field, dataframes)

    #format the outputs to flatten list
    #sort the sub results
    outputs = [item for sublist in outputs for item in sublist]
    my_dict = dict(outputs)
    sorted_output = sorted(my_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    return sorted_output
