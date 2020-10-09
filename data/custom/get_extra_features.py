'''
Script to extract all the musical features
associated with each unique song ID.
Uses Kaggle dataset and the spotify API endpoints
'''

import requests 
import json
import pandas as pd


#API endpoint 
URL = "https://api.spotify.com/v1/tracks"

TOKEN = "BQA0ZyvYbRl7tl_FMv_SG2bGLBUxBK7xQamjguCUQ1JRarFaBUvqAYAdHz76BdwsBBDX5qmrGlRD2qMpDcB3pYHnf8xR8F_kh0hlp2c0XzntpKslXELe-3XlyW3l2dr-HYi4CddRY7WwYl1msk_w4iqIFEzGRv-cOrstZ1DM4vurHa007poLzVMbtxH-ZEzIgRVvhDH4Yo7470SH3l_joQkpweYhn5jSQYgYQlE1Pf-GcK_UY1NsfnijItNkxaFJPVs8mq_RwTjRPo0ypOaKoiHgeeo5Pe-jZBs"
kaggle_file = './kaggle-data.csv'
kaggle = pd.read_csv(kaggle_file)

columns = ['id','artists','year', 'popularity']

final = pd.DataFrame(columns = columns)

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
    
    if 'tracks' not in data:
        print(data)
        print(id_list)


    if not data['tracks'] :
        print(data)
        print(id_list)

    
    #get all nulls indices
    nulls_ind = [i for i in range(len(data['tracks'])) if data['tracks'][i] == None]

    if nulls_ind :

        null_el += [id_list[i] for i in nulls_ind]

    data['tracks'] = list(filter(None, data['tracks'])) 

    all_tracks = []
    for track in data['tracks']:
        artists = []
        for art in track['artists'] :
            artists.append(art['name'])
        
        all_tracks.append({"id":track['id'],"artists":artists, "year":track['album']['release_date'], "popularity":track['popularity']})

    try:
        df = pd.DataFrame.from_records(all_tracks)

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

        else:

            api_count+=1
            id_count+=1
            id_list.append(ID)

            # make a GET request in bunches of 50
            if id_count == 50 :
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
with open('null22e.txt', 'w') as f:
    for item in null_el:
        f.write("%s\n" % item)

print("======= All done  ============")
print("Kaggle songs = ", kaggle_count)
print("API songs =", api_count)
final.to_csv('./extra-features22.csv') 