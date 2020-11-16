'''
Script to create an index that stores all the song
IDs and the song names. 

Used for lookup later in the searching section.
'''

import pandas as pd
import numpy as np
import sys

data_dir = sys.argv[1]

df1 = pd.read_csv(data_dir+'combined_features_1.csv')
df2 = pd.read_csv(data_dir+'combined_features_2.csv', names=df1.columns)

#append csv parts into one dataframe
music_df = pd.DataFrame(columns = df1.columns)
music_df = music_df.append(df1, ignore_index = True) 
music_df = music_df.append(df2, ignore_index = True)
print(music_df.head())
music_df = music_df.sort_values('id')
print(music_df.head())

id2song = music_df[['id', 'name']]

print()
print(id2song.head())
id2song["name"].fillna("Unnamed Song", inplace = True) 
id2song.to_csv(data_dir+"id2song.csv",sep = ':',index=False)