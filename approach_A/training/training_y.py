'''
Script to prepare the ground truth values for the
training data that is used in the regression model
'''

import json
import pandas as pd
import time 
import os
import sys

data_dir = sys.argv[1]

with open(data_dir+"emb.txt",'r') as f1, open(data_dir+"emb_train_y.csv",'a+') as wf:

    emb = f1.readline().strip()
    while(emb):

        emb = emb.replace(':'," ")
        wf.write(emb+"\n")
        emb = f1.readline().strip()