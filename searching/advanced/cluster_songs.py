'''
Cluster the songs using the network embedding 
vectors into clusters that can be then used for
mood based searching etc.

[Implement] :  Birch Clustering
'''

import pandas as pd
import numpy as np
import sys

import pickle
from pickle import dump

from numpy import unique
from numpy import where
from matplotlib import pyplot


data_dir = sys.argv[1]
emb_file = sys.argv[2]
VEC_DIM = 9


'''
Read the network embedding vecotrs and process the file
'''
print(data_dir+emb_file)
fet = ["f"+str(i) for i in range(VEC_DIM)]
emb_df = pd.read_csv(emb_file, sep = " ", names=["id"]+fet)
print(emb_df.head())

X = emb_df[fet].values
song_ids = emb_df['id'].values
print("X shape = ", X.shape)
print("Sizes of dfs = ",emb_df.shape[0])
print("Training clustering model now ...")

###################     BIRCH MODEL  ######################
# from sklearn.cluster import Birch
# define the model
# model = Birch(threshold=0.01, n_clusters=10)
# # fit the model
# model.fit(X)
# # assign a cluster to each example
# yhat = model.predict(X)
# # retrieve unique clusters
# clusters = unique(yhat)
# # create scatter plot for samples from each cluster
# for cluster in clusters:
# 	# get row indexes for samples with this cluster
# 	row_ix = where(yhat == cluster)
# 	# create scatter of these samples
# 	pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
# # show the plot
# pyplot.show()


#####################  K MEANS ALGO    ######################
from sklearn.cluster import KMeans
# define the model
model = KMeans(n_clusters=500)
# fit the model
print("fitting model")
model.fit(X)
# assign a cluster to each example
print("predicting classes")
yhat = model.predict(X)
# retrieve unique clusters
clusters = unique(yhat)
# create scatter plot for samples from each cluster
print("plotting now")

for cluster in clusters:

	# get row indexes for samples with this cluster
	row_ix = where(yhat == cluster)

	#subcluster a cluster (looking for cluster with a subset of songs)
	if "1ZeJNLoHSeOh0LIFXXDtxY" in song_ids[row_ix]:
		
		print("indices", row_ix)
		print(X[row_ix])

		print("entered submodel")
		X_sub = X[row_ix]
		song_ids_sub = song_ids[row_ix]
		model_sub = KMeans(n_clusters=10)
		
		print("fitting model")
		model_sub.fit(X_sub)
		
		print("predicting classes")
		yhat_sub = model_sub.predict(X_sub)
		clusters_sub = unique(yhat_sub)
		
		print("plotting now")

		for cluster_sub in clusters_sub:
			
			row_ix_sub = where(yhat_sub == cluster_sub)
			
			#write IDs to moods
			with open(data_dir+"mood_emb/mood_"+str(cluster_sub)+".txt", 'w+') as f:
				for i in range(len(song_ids_sub[row_ix_sub])):
					f.write(song_ids_sub[row_ix_sub][i]+":")
					f.write(' '.join(map(str, X_sub[row_ix_sub][i])))
					f.write("\n")
	
			#write embeddings to moods
			# with open(data_dir+"mood_emb/mood_"+str(cluster_sub)+".txt", 'w+') as f:
				# for emb in X_sub[row_ix_sub]:
				# 	f.write(emb+"\n")
			# np.savetxt(data_dir+"mood_emb/mood_"+str(cluster_sub)+".txt", X_sub[row_ix_sub], delimiter=" ")
		

			pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
		break


# show the plot
pyplot.show()

########################## DB SCAN METHOD #########################

# from sklearn.cluster import DBSCAN

# # define the model
# model = DBSCAN(eps=0.5, min_samples=40000)
# # fit model and predict clusters
# print("fit and predict now ...")
# yhat = model.fit_predict(X)
# # retrieve unique clusters
# print("get unique")
# clusters = unique(yhat)
# # create scatter plot for samples from each cluster
# print("plotting clusters")
# for cluster in clusters:
# 	# get row indexes for samples with this cluster
# 	row_ix = where(yhat == cluster)
# 	# create scatter of these samples
# 	pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
# # show the plot
# pyplot.show()