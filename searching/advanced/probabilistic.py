import numpy as np
import random

from config import *

def prob_select(res_songs):

    res_songs = res_songs[:50]
    ids = np.array([item[0] for item in res_songs])

    #create a probability distribution
    probs = np.array([item[1] for item in res_songs] )
    probs = probs/np.sum(probs)
    probs = np.sort(probs)

    draw = np.random.choice(ids, TOP_RES, p=probs, replace=False)
    return draw


def gen_random_prob(song_list):

    probs = np.random.random_sample((len(song_list),))
    probs = probs/np.sum(probs)
    
    prob_list = []
    for i,song in enumerate(song_list):
        prob_list.append((song, probs[i]))


    return prob_list
