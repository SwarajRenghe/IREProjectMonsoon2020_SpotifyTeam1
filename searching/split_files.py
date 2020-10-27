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

emb_file = sys.argv[1]
output_dir = sys.argv[2]
os.mkdir(output_dir) 

with open(emb_file,'r') as f:

    song = f.readline().strip()
    mystring = ""
    i = 0

    while(song):
        
        mystring += song+"\n"
        i+=1

        if i%40000 == 0:
            with open(output_dir+str(i)+".txt",'w+') as wf:
                wf.write(mystring)
            mystring=""

        song = f.readline().strip()


    #residual ids in the last file
    if mystring:
        with open(output_dir+str(i)+".txt",'w+') as wf:
            wf.write(mystring)
        mystring=""


