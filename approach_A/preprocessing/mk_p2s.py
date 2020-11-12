import json 
import pandas as pd
  
req_dict = {'track_uri':[], 'track_name':[], 'track_uri':[], 'album_name':[], 'album_uri':[], 'artist_name':[], 'artist_uri':[], 'duration_ms':[]}
track_uri = []
# Opening JSON file 


for k in range(40):
    with open(f'/home/prateek.pani/git/IREProjectMonsoon2020_SpotifyTeam1/data/10000 Playlists/30000 More Playlists/mpd.slice.{(960+k)*1000 + 0}-{(960+k)*1000 + 999}.json') as json_file: 
        data = json.load(json_file) 
    
        # Print the type of data variable 
        print("Type:", type(data)) 

    print(f'k : {k}\n')

    # iterate over all slices
    # kth slice
    for i in range(len(data['playlists'])):
        print(i,k)
        # ith playlist of a kth particular slice
        for track_ele in data['playlists'][i]['tracks']:
            # lth track of ith particular playlist
            # logic -- > Should I add/not?

            # check if track_ele present in set or not
            # if track_ele['track_uri'] not in bf_set:
            #     print(track_ele['track_uri'] not in bf_set)
            track_uri.append(track_ele['track_uri'])
            # req_dict['track_uri'].append(track_ele['track_uri'])
            # req_dict['track_name'].append(track_ele['track_name'])
            # req_dict['album_name'].append(track_ele['album_name'])
            # req_dict['album_uri'].append(track_ele['album_uri'])
            # req_dict['artist_name'].append(track_ele['artist_name'])
            # req_dict['artist_uri'].append(track_ele['artist_uri'])
            # req_dict['duration_ms'].append(track_ele['duration_ms'])
            # else:
            #     print('Not Appended')
            # print(len(track_uri),   len(req_dict['track_name']),   len(req_dict['album_name']),  len(req_dict['album_uri']),  len(req_dict['artist_name']),  len(req_dict['artist_uri']),  len(req_dict['duration_ms']))


            
            
    print(f'\nk: {k}')
    # print(f'\nk: {k}')
print(len(track_uri))
print(len(set(track_uri)))
unique_list = list(set(track_uri))
decision_dict = {le:'0' for le in unique_list}

print(decision_dict['spotify:track:1Gu4ATk5Bww5WBlwaWend6'])

# s = set(track_uri)

# decision_dict = {s:'1' for key in s}
# df = pd.DataFrame(decision_dict)
# df.to_csv('./decision.csv')
# ------------here I have the track_uri-------------------
# ---------------------Using this list create the decisionList----------------
# dec_dict = {le:[0] for le in track_uri}


# # reset track_uri
# track_uri = []


req_dict1 = {'track_uri':[], 'track_name':[], 'track_uri':[], 'album_name':[], 'album_uri':[], 'artist_name':[], 'artist_uri':[], 'duration_ms':[]}
# # based on this 
for k in range(40):
    with open(f'/home/prateek.pani/git/IREProjectMonsoon2020_SpotifyTeam1/data/10000 Playlists/30000 More Playlists/mpd.slice.{(960+k)*1000 + 0}-{(960+k)*1000 + 999}.json') as json_file: 
        data = json.load(json_file) 
    
        # Print the type of data variable 
        print("Type:", type(data)) 
  
    # Print the data of dictionary 

    # print(type(data['playlists'])) #<class 'list'>
    # print(type(data['playlists'][0])) #<class 'dict'>


    # print(data['playlists'][0]) #0th playlist
    # print(type(data['playlists'][0]['tracks']))

    
    # print(data['playlists'][0]['tracks'])
    # iterate over all slices
    # kth slice
    for i in range(len(data['playlists'])):
        print(i,k)
        # ith playlist of a kth particular slice
        for track_ele in data['playlists'][i]['tracks']:
            # lth track of ith particular playlist
            # logic -- > Should I add/not?
            # check if track_ele present in set or not
            if decision_dict[track_ele['track_uri']] == '0' :
                # print(track_ele['track_uri'] not in bf_set)
                req_dict1['track_uri'].append(track_ele['track_uri'])
                req_dict1['track_name'].append(track_ele['track_name'])
                req_dict1['album_name'].append(track_ele['album_name'])
                req_dict1['album_uri'].append(track_ele['album_uri'])
                req_dict1['artist_name'].append(track_ele['artist_name'])
                req_dict1['artist_uri'].append(track_ele['artist_uri'])
                req_dict1['duration_ms'].append(track_ele['duration_ms'])
                decision_dict[track_ele['track_uri']] = '1'
            # else:
            #     print('Not Appended')
            # print(len(track_uri),   len(req_dict['track_name']),   len(req_dict['album_name']),  len(req_dict['album_uri']),  len(req_dict['artist_name']),  len(req_dict['artist_uri']),  len(req_dict['duration_ms']))


            
            
    # print(track_uri[0],  req_dict['track_name'][0]) #track_uri is th CK and req_dict['track_name']
print(len(track_uri),   len(req_dict1['track_name']),   len(req_dict1['album_name']),  len(req_dict1['album_uri']),  len(req_dict1['artist_name']),  len(req_dict1['artist_uri']),  len(req_dict1['duration_ms']))
# print(len(set(track_uri)))

# prepare a pandas dictionary with col_name 'track_name' and so on....and track_uri store in file
df = pd.DataFrame(req_dict1)
print(df.head())
print(len(df))

# # saving a csv file in pandas <df_obj>.to_csv(path)
df.to_csv(path_or_buf = './playlist_info.csv', sep=' ')

