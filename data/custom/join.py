'''
Script to perform a join on the two sets of features
musical features and the extra features

NOTE : Merge mini files before using the script.
'''

import pandas as pd

musicalf = './musical-features.csv'
musicaldf = pd.read_csv(musicalf)

extraf = './extra-features.csv'
extradf = pd.read_csv(extraf)

musicaldf.sort_values('id',inplace=True)
musicaldf.set_index('id', inplace=True)

extradf.sort_values('id',inplace=True)
extradf.set_index('id', inplace=True)

musicaldf.loc[musicaldf.index.isin(extradf.index), ['name', 'artists','popularity','year']] = extradf[['name', 'artists','popularity','year']]
musicaldf.reset_index(inplace=True)


#get rid of null songs
null_files = ['null1e','null2e','null3e','null4e']
null_ids = []

for filename in null_files : 
    with open('./subfiles/'+filename+'.txt') as f:
        content = f.readlines()
    null_ids += [x.strip() for x in content]


# print(len(null_ids))
# print(null_ids)
musicaldf = musicaldf[~musicaldf['id'].isin(null_ids)]


musicaldf.to_csv('./combined-features-new.csv') 
