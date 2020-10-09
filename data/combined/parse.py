"""
    pretty printer for the MPD
    Usage:
        python show.py - show all the playlists in the MPD
        python show.py 1008 1120 4356 - show the playlists with the given pids
        python show.py 1000-1020 1989 99870-99999 - show the playlists in the given range
"""


import sys
import json
import codecs
import datetime


pretty = True
compact = False
cache = {}
file_num = 0

def print_playlist(playlist, song_network):
    song_ids = set()
    if pretty:
        wt = int(playlist['num_followers'])
    if not compact:
            for track in playlist['tracks']:
                song_ids.add(track['track_uri'][14:]) 
    for song_id in song_ids:
        if song_id in song_network:
            pass
        else:
            song_network[song_id] = {}
		
        for adjac_song_id in song_ids:
            if adjac_song_id in song_network[song_id]:
                song_network[song_id][adjac_song_id] += wt
            else:
                song_network[song_id][adjac_song_id] = wt

def show_playlist(pid, song_network):
    if pid >=0 and pid < 1000000:
        low = 1000 * int(pid / 1000)
        high = low + 999
        offset = pid - low
        path = "mpd.slice." + str(low) + '-' + str(high) + ".json"
        if not path in cache:
            f = codecs.open(path, 'r', 'utf-8')
            js = f.read()
            f.close()
            playlist = json.loads(js)
            cache[path] = playlist

        playlist = cache[path]['playlists'][offset]
        print_playlist(playlist, song_network)


def show_playlists_in_range(start, end):
    print(start, end)
	#return
    song_network = {}
    try:
        istart = int(start)
        iend = int(end)
        if istart <= iend and istart >= 0 and iend <= 1000000:
            for pid in xrange(istart, iend):
                show_playlist(pid, song_network)
    except:
        raise
        print "bad pid"
    write_to_file(song_network) 
    print(len(song_network))

def write_to_file(song_network):
	global file_num
	#f = open("network/file"+str(file_num)+".txt","w+")
	#for song_id in sorted(song_network):
		#print(song_id, file_num)
		#f.write(song_id+"=")
		#for adj_sid in sorted(song_network[song_id]):
			#f.write(adj_sid+":"+str(song_network[song_id][adj_sid])+",")
		#f.write("\n")
	#f.close()
	file_num += 1

if __name__ == '__main__':
    file_num = 0
    for arg in sys.argv[1:]:
        if arg == '--pretty':
            pretty = True
        elif arg == '--compact':
            compact = True
        elif arg == '--raw':
            pretty = False
        elif '-' in arg:
            fields = arg.split('-')
            if len(fields) == 2:
                start = int(fields[0])
                temp_end = start + 999
                end = int(fields[1])

                while start <= end:
                    show_playlists_in_range(str(start), str(temp_end))
                    start = temp_end + 1
                    temp_end = start + 999
        else:
            pid = int(arg)
            show_playlist(pid)

