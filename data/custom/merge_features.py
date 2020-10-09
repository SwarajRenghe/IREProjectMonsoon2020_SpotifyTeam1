'''
Script to merge the csv files that
are generated after extracting the different
kinds of features.
'''

import pandas as pd


#read all csv files

csv1_file = './extra-features11.csv'
df1 = pd.read_csv(csv1_file)

csv2_file = './extra-features12.csv'
df2 = pd.read_csv(csv2_file)

csv3_file = './extra-features21.csv'
df3 = pd.read_csv(csv3_file)

csv4_file = './extra-features22.csv'
df4 = pd.read_csv(csv4_file)


#create a new df and append all the mini dfs to it
final = pd.DataFrame(columns = df1.columns)

print("appending file 1 ...")
final = final.append(df1, ignore_index = True) 

print("appending file 2 ...")
final = final.append(df2, ignore_index = True)

print("appending file 3 ...")
final = final.append(df3, ignore_index = True) 

print("appending file 4 ...")
final = final.append(df4, ignore_index = True) 

final.to_csv('./extra-features.csv') 

