import numpy as np
import random

from config import *

def prob_select(res_songs):

    ids = np.array([item[0] for item in res_songs])

    #create a probability distribution
    probs = np.array([item[1] for item in res_songs] )
    probs = probs/np.sum(probs)
    probs = np.sort(probs)

    draw = np.random.choice(ids, TOP_RES, p=probs)
    return draw