'''
Script to train a regression model 
using NN to map every musical feature vector
to a vector in the network embedding vector space
'''

import pandas as pd
import numpy as np
import sys

import pickle
from pickle import dump

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data_dir = sys.argv[1]
emb_file = sys.argv[2]
Y_DIM = 9


features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness",
            "loudness","mode","popularity","speechiness","tempo","valence","year",'a0', 'a1','a2','a3']


'''
Read and process all the musical features
These will serve as the X values in the MLP
training process. The musical features are then 
mapped to a different vector space via regression.
'''

df1 = pd.read_csv(data_dir+'file1_updated.csv')
df2 = pd.read_csv(data_dir+'file2_updated.csv', names=df1.columns)

#append csv parts into one dataframe
music_df = pd.DataFrame(columns = df1.columns)
music_df = music_df.append(df1, ignore_index = True) 
music_df = music_df.append(df2, ignore_index = True)
music_df.drop(['Unnamed: 0', 'Unnamed: 0.1','Unnamed: 0.1.1','explicit','release_date','analysis_url','time_signature','track_href','type','uri'], axis = 1, inplace = True) 
print(music_df.head())
music_df = music_df.sort_values('id')
print(music_df.head())

DATA_SIZE = music_df.shape[0]

#prepare features and ground truth sets
X = music_df[features].values
print("X shape=", X.shape)
print(X[0])
print()
print()

'''
Read the network embedding vecotrs and process the file
Remove the null songs, and re-sort the vectors based on ID
change this to network embeddings in final code
assume that the network embeddigns have 5 features
'''

fet = ["f"+str(i) for i in range(Y_DIM)]
emb_df = pd.read_csv(data_dir + emb_file, sep = " ", names=["id"]+fet)
y = emb_df[fet].values
print("Y shape = ", y.shape)
print("Sizes of dfs = ",DATA_SIZE, emb_df.shape[0])



print("Training model ...")
X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=1)

# print("original ", X_train, y_train)
# print()
# print("original y", X_test, y_test)
# print()
# print()

sc = StandardScaler()
scalerX = StandardScaler().fit(X_train)
scalery = StandardScaler().fit(y_train)
X_train = scalerX.transform(X_train)
y_train = scalery.transform(y_train)
X_test = scalerX.transform(X_test)
y_test = scalery.transform(y_test)

regr = MLPRegressor(random_state=1, max_iter=1000).fit(X_train, y_train)

# print("Prediction on test ...")
# print(X_train,y_train)
# print()
# print(X_test, y_test)

# y_hat = scalery.inverse_transform(regr.predict(X_test))
# print(y_hat)

print()
print("Reg scores = ")
print(regr.score(X_test, y_test))
# print(regr.coefs_)

filename='MLPRegressor_model.sav'
dump(scalery, open('scalery.pkl', 'wb'))
dump(scalerX, open('scalerx.pkl', 'wb'))
pickle.dump(regr, open(filename, 'wb'))