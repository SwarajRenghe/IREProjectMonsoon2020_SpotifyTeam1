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

mood_dir = index_dir+"mood_emb/"
mood_files = [filename for filename in os.listdir(mood_dir)]

print(mood_files)

for file in mood_files:
    print("accessing file", file)
    with open(mood_dir+file, 'r') as f, open(index_dir+"mood_songs/"+file,'w+') as to:

        songid = f.readline().strip().split(':')[0]


        while(songid):
            to.write(song_name[songid]+"\n")
            songid = f.readline().strip().split(':')[0]

    


