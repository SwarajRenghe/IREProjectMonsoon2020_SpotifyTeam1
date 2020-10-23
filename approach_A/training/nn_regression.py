'''
Script to train a regression model 
using NN to map every musical feature vector
to a vector in the network embedding vector space
'''

import pandas as pd
import numpy as np

from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df1 = pd.read_csv('../../data/custom/combined_features_1.csv')
df2 = pd.read_csv('../../data/custom/combined_features_2.csv', names=df1.columns)

#append csv parts into one dataframe
df = pd.DataFrame(columns = df1.columns)
df = df.append(df1, ignore_index = True) 
df = df.append(df2, ignore_index = True)
df.drop(['Unnamed: 0', 'Unnamed: 0.1','Unnamed: 0.1.1','explicit','release_date','analysis_url','time_signature','track_href','type','uri'], axis = 1, inplace = True) 

TRIAL_N = 100000
print("Number of rows = ", TRIAL_N)
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key","liveness","loudness","mode","popularity","speechiness","tempo","valence","year"]

#prepare features and ground truth sets
X = df[:TRIAL_N][features].values

#change this to network embeddings in final code
#assume that the network embeddigns have 5 features
y = np.random.rand(TRIAL_N,5)

# X =np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])
# y = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])

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

regr = MLPRegressor(random_state=1, max_iter=500).fit(X_train, y_train)

# print("Prediction on test ...")
# print(X_train,y_train)
# print()
# print(X_test, y_test)

y_hat = scalery.inverse_transform(regr.predict(X_test))
print(y_hat)

print()
print("Reg scores = ")
print(regr.score(X_test, y_test))