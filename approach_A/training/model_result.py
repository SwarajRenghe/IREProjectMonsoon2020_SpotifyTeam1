'''
Script to train a predict the network embeddings
given a musical feature vector
'''

import pandas as pd
import numpy as np
import sys

import pickle
from pickle import load

from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

musical_vector = sys.argv[1]
musical_vector = np.array([float(fet) for fet in musical_vector.strip('][').split()]).reshape(1, -1)
# musical_vector = np.array([0.863,0.464,30453,0.26,0.0,4,0.102,-9.202,1,2.0,0.141,178.46099999999996,0.277, 2011.0]).reshape(1,-1)
print(musical_vector)

scaler = load(open('scaler.pkl', 'rb'))

filename='MLPRegressor_model.sav'
mlpreg_model =pickle.load(open(filename, 'rb'))
y_load_predit=scaler.inverse_transform(mlpreg_model.predict(musical_vector))

print(y_load_predit)