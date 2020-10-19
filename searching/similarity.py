'''
[Brute Force Implementation]
Script to find top k closest songs for each
vectorized song. Uses the cosine similarity between
the vectors, to compute the distance between two songs.
'''

import json
import pandas as pd
import numpy as np
from scipy.spatial import distance

df1 = pd.read_csv('./combined-features.csv')
# df2 = pd.read_csv('./combined_features_2.csv')

#append csv parts into one dataframe
df = pd.DataFrame(columns = df1.columns)
df = df.append(df1, ignore_index = True) 
# df = df.append(df2, ignore_index = True)
print("All features")
print(df1.columns)
print()
print()
df.drop(['Unnamed: 0', 'Unnamed: 0.1','Unnamed: 0.1.1','explicit','release_date','analysis_url','time_signature','track_href','type','uri'], axis = 1, inplace = True) 
print("Relevant Features")
print(df.columns)

index = {}
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness","loudness","mode","popularity","speechiness","tempo","valence","year"]

#iterate through all rows 
for ind, i in df.iterrows():

    if ind == 1:
        print("Songs read = ", ind)
        break

    i_vec = i[features].astype(float)

    iid = i['id']
    index[iid]={}

    for ind2, j in df.iterrows():
        jid = j['id']
        if jid != iid:

            j_vec = j[features].astype(float)
            score = distance.cosine(i_vec, j_vec)

            index[iid][j['name']] = score


sorted_index = dict(index)

for song in sorted_index:
    sorted_index[song] = sorted(index[song].items(), key=lambda x : x[1], reverse=True)

with open('index.txt', 'w') as outfile:
    json.dump(sorted_index, outfile)

