import sys
import spotipy
import spotipy.util as util
import re
import pprint as pp

def get_sp_playlist(token, username, playlist_name):
    search_list = {}
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    
        # get playlist info
        all_playlists = sp.user_playlists(username)
        playlist_ids = [item['id'] for item in all_playlists['items']]
        playlist_names = [item['name'] for item in all_playlists['items']]

        if playlist_name in playlist_names:
            pl_id = playlist_ids[playlist_names.index(playlist_name)]
            print(f'Playlist "{playlist_name}" was found')
        else:
            sys.exit(f'Playlist "{playlist_name}" not found')
    
        sp_plitems = sp.playlist_items(
            pl_id, 
            fields="total,limit,next,offset,items(added_at,track(id,artists,name,duration_ms,album(name,release_date)))", 
            limit=3, 
            offset=0
            )
        # pp.pprint(sp_plitems["items"])
#   [{'added_at': '2021-03-14T02:39:01Z',
#     'track': {
#           'album': {'name': 'Quítate las Gafas',
#                     'release_date': '2016-11-11'},
#           'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/1EXjXQpDx2pROygh8zvHs4'},
#                        'href': 'https://api.spotify.com/v1/artists/1EXjXQpDx2pROygh8zvHs4',
#                        'id': '1EXjXQpDx2pROygh8zvHs4',
#                        'name': 'Melendi',
#                        'type': 'artist',
#                        'uri': 'spotify:artist:1EXjXQpDx2pROygh8zvHs4'}],
#           'duration_ms': 273293,
#           'id': '66VmioeXL4i1TCfHIO8R9t',
#           'name': 'Desde Que Estamos Juntos'}},
#    {'added_at': '2021-03-14T02:39:01Z',
#     'track': {
#           'album': {'name': 'The Band Perry', 'release_date': '2010-01-01'},
#           'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/75FnCoo4FBxH5K1Rrx0k5A'},
#                        'href': 'https://api.spotify.com/v1/artists/75FnCoo4FBxH5K1Rrx0k5A',
#                        'id': '75FnCoo4FBxH5K1Rrx0k5A',
#                        'name': 'The Band Perry',
#                        'type': 'artist',
#                        'uri': 'spotify:artist:75FnCoo4FBxH5K1Rrx0k5A'}],
#           'duration_ms': 222773,
#           'id': '4u26EevCNXMhlvE1xFBJwX',
#           'name': 'If I Die Young'}}]
        for item in sp_plitems["items"]:
            t = item["track"]
            track_id = t["id"]
            track_name = t["name"]
            main_artist = t["artists"][0]["name"]
            duration_ms = t["duration_ms"]
            search_txt = f"{main_artist.upper()} - {track_name.upper()}"
            search_list[track_id] = {
                "search_txt" : search_txt,
                "duration_ms" : duration_ms
            }
        return(search_list)
if __name__ == "__main__":
    sp_scope = "playlist-read-private"
    sp_username = "maazin5"
    sp_plname = "SPOTIPY TEST"
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    # create search list from sp playlist 
    x = get_sp_playlist(token, sp_username, sp_plname)
    pp.pprint(x)
    # create yt playlist from search list
    print("ABC XYZ")