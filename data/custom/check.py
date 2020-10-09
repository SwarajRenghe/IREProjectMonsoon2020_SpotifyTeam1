import pandas as pd

feature_file = './musical-features.csv'
musical_features_df = pd.read_csv(feature_file)

csv_ids = musical_features_df['id'].tolist()
txtfile_id =[]

with open('./unique_song_ids.txt','r') as f:
    ID = f.readline().strip('\n')
    while (ID):
        txtfile_id.append(ID)
        ID = f.readline().strip('\n')

'''
check if all IDs in the csv file belong 
to the unique IDs list of songs
'''
for ID in csv_ids :

    if ID not in txtfile_id :

        print(ID)