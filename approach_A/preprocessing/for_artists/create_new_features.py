import os
import pandas as pd
from itertools import chain
import ast

def load_artists(ids, emb):
    f1 = open(ids, 'r')
    line1 = f1.readline().strip('\n')

    f2= open(emb, 'r')
    line2 = f2.readline().strip('\n')
    
    dict_ret = {}

    while(line1):
        
        dict_ret[line1] = line2.split()

        line1 = f1.readline().strip('\n')
        line2 = f2.readline().strip('\n')


    f1.close()
    f2.close()

    return dict_ret

def get_artists():

    df = pd.read_csv("../../../data/custom/combined_features_1.csv", usecols=[1,5]) 
    print(df.head())
    dict1 = df.set_index('id').T.to_dict()

    df_cols = df.columns

    df = pd.read_csv("../../../data/custom/combined_features_2.csv", names=df_cols, usecols=[1,5]) 
    print(df.head())
    dict2 = ( df.set_index('id').T.to_dict() )
    
    dict_final = dict(chain.from_iterable(d.items() for d in (dict1, dict2)))
    print(len(dict_final))
    return dict_final


def append_to_file(infile, outfile, skip=False):
    f1 = open(infile, 'r')
    line1 = f1.readline().strip('\n')
    of = open(outfile, 'w')
    num_features = len(art_dict['3EvzCyNmY3kbUkMawjsndF'])

    if skip:
        of.write(line1)
        for i in range(num_features):
                of.write(",a"+str(i))
        of.write("\n")
        line1 = f1.readline().strip('\n')

    while(line1):
        song_id=line1.split(",")[1]
        artists = ast.literal_eval(a_dict[song_id]['artists'])
        
        vals = [0, 0, 0, 0]
        for av in artists:
            for i in range(num_features):
                vals[i] += float(art_dict[av][i])
        
        of.write(line1)

        for i in range(num_features):
            of.write(","+str(vals[i]/len(artists)))

        of.write("\n")
        line1 = f1.readline().strip('\n')

art_dict = load_artists("unique_artists.txt","outfile_ARTISTS524288.txt")
a_dict = get_artists()
append_to_file("../../../data/custom/combined_features_1.csv","file1_updated.csv", True)
append_to_file("../../../data/custom/combined_features_2.csv","file2_updated.csv")
