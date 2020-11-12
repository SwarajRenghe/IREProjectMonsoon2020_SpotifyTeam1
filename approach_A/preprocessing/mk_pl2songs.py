import json 
import pandas as pd
  
req_dict = {'track_uri':[], 'track_name':[], 'track_uri':[], 'album_name':[], 'album_uri':[], 'artist_name':[], 'artist_uri':[], 'duration_ms':[]}
track_uri = []
# Opening JSON file 
for k in range(1):
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
    print('\n')

    # iterate over all slices
    # kth slice
    for i in range(len(data['playlists'])):
        # ith playlist of a kth particular slice
        for track_ele in data['playlists'][i]['tracks']:
            # lth track of ith particular playlist
            # logic -- > Should I add/not?

            bf_set = set(track_uri)
            # print(len(track_uri),   len(prev_set))
            track_uri.append(track_ele['track_uri'])
            af_set = set(track_uri)
            flag = len(af_set.difference(bf_set))
            print(flag)
            if flag == 1: #unique song
                req_dict['track_uri'].append(track_ele['track_uri'])
                req_dict['track_name'].append(track_ele['track_name'])
                req_dict['album_name'].append(track_ele['album_name'])
                req_dict['album_uri'].append(track_ele['album_uri'])
                req_dict['artist_name'].append(track_ele['artist_name'])
                req_dict['artist_uri'].append(track_ele['artist_uri'])
                req_dict['duration_ms'].append(track_ele['duration_ms'])
            else:
                print('Not Appended')
                track_uri.pop()
            print(len(track_uri),   len(req_dict['track_name']),   len(req_dict['album_name']),  len(req_dict['album_uri']),  len(req_dict['artist_name']),  len(req_dict['artist_uri']),  len(req_dict['duration_ms']))

	
    
    print(f'\nk: {k}')
    print(len(track_uri))

    # print(track_uri[0],  req_dict['track_name'][0]) #track_uri is th CK and req_dict['track_name']
print(len(track_uri),   len(req_dict['track_name']),   len(req_dict['album_name']),  len(req_dict['album_uri']),  len(req_dict['artist_name']),  len(req_dict['artist_uri']),  len(req_dict['duration_ms']))
print(len(set(track_uri)))



# prepare a pandas dictionary with col_name 'track_name' and so on....and track_uri store in file
df = pd.DataFrame(req_dict)
print(df.head())
print(len(df))

# saving a csv file in pandas <df_obj>.to_csv(path)
df.to_csv(path_or_buf = './playlist_info.csv', sep=' ')

