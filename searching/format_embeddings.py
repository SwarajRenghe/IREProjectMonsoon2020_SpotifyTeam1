'''
Script to remove format the network embeddings results
by removing all the null songs from the embeddings file

Also prefix the song ID for each embedding along with it
'''

import json
import pandas as pd
import numpy as np
from scipy.spatial import distance
import multiprocessing 
import time 
import os
import sys

data_dir = sys.argv[1]
emb_file = sys.argv[2]

with open(data_dir+"null_songs.txt", 'r') as f:
    null_songs = f.readlines()
null_songs = [x.strip() for x in null_songs]

with open(data_dir+"unique_ids_postmerge.txt",'r') as f1, open(emb_file,'r') as f2, open(data_dir+"emb.txt",'a+') as wf:

    song_id = f1.readline().strip()
    emb = f2.readline().strip()
    s=0
    e=0
    nu = 0

    while(song_id and emb):

        s+=1
        e+=1

        if song_id in null_songs:
            nu+=1
            song_id = f1.readline().strip() 
            emb = f2.readline().strip()
            continue

        mystring = song_id+":"+emb+"\n"
        wf.write(mystring)

        song_id = f1.readline().strip()
        emb = f2.readline().strip()


print("All done")
print("S = ", s)
print("E = ", e)
print("Null = ", nu)

print("\nEmbeddings = ", e-nu)











