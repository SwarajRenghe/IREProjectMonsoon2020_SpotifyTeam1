'''
Script to extract all the musical features
associated with each unique song ID.
Uses Kaggle dataset and the spotify API endpoints
'''

import requests 
import json
import pandas as pd


#API endpoint 
URL = "https://api.spotify.com/v1/audio-features"

TOKEN = "BQA2NKgdVhA1DgSanbAV4Ffb4O6rLOg6rvxM_n3TwqBu6ZBJkk3i2zykW_Q_oiH7xXlYidrVZIJNjb5FZ_bW_mghtFf92FYiNJd2XhA0D6bSO9tXhSoUdLO5QZ9ozGEfSv7ZsI5OatSzSfml_FWE4g-JgSnOnfX3JEDU_2jiKG-jPqCvN-GLcczq1GfwoAnoIuAz_zQa0VA_T7nhcSxL6ZxJBGSoQeCQDxxm27xFuqyYjhn5mWK7N6SpvdbjVTaGexzV-cJDjbKnnWYVbGzXlvVLKNGWh5k1Xj0"
kaggle_file = './kaggle-data.csv'
kaggle = pd.read_csv(kaggle_file)

final = pd.DataFrame(columns = kaggle.columns)

total_nulls = 0
null_el = []
id_count = 0
i = 0
id_list = []
kaggle_count = 0
api_count = 0


def api_get():

    global null_el
    global final

    PARAMS = {'ids':','.join(id_list)} 
    r = requests.get(url = URL, params = PARAMS, headers={'Authorization': 'Bearer '+TOKEN})

    # extracting data in json format 
    data = r.json()

    if ('error' in data) and (data['error']['status']==401) :
        print("Token expired :( ")
        exit(0)
    
    if 'audio_features' not in data:
        print(data)

    if not data['audio_features'] :
        print(data)
    
    #get all nulls indices
    nulls_ind = [i for i in range(len(data['audio_features'])) if data['audio_features'][i] == None]

    if nulls_ind :

        null_el += [id_list[i] for i in nulls_ind]

    data['audio_features'] = list(filter(None, data['audio_features'])) 

    try:
        df = pd.DataFrame.from_records(data['audio_features'])

    except:
        print("Nones found!")
        print(data)
        print(id_list)
        exit(0)

    #append to final datafram
    final = final.append(df, ignore_index = True) 

    


with open('./part22.txt','r') as f:

    ID = f.readline().strip('\n')

    while (ID):

        i+=1

        #unique id tracker
        if i%1000 == 0:
            print("songs read = ", i)

        if ID in kaggle['id'].values :
            kaggle_count+=1
            # print(kaggle.loc[kaggle['id'] == ID])
            final = final.append(kaggle[kaggle['id'] == ID])

        else:

            api_count+=1
            id_count+=1
            id_list.append(ID)

            # make a GET request in bunches of 100
            if id_count == 100 :
                api_get()    

                #reset values
                id_count = 0
                id_list.clear()


        ID = f.readline().strip('\n')


#get features for residual API songs
if id_list :
    api_get()

    #reset values
    id_count = 0
    id_list.clear()



# print(final)
print("\nNULL SIZE = ", len(null_el))
with open('null22.txt', 'w') as f:
    for item in null_el:
        f.write("%s\n" % item)

print("======= All done  ============")
print("Kaggle songs = ", kaggle_count)
print("API songs =", api_count)
final.to_csv('./musical-features22.csv') 