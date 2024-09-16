import sys
import spotipy
import spotipy.util as util
import re
import pprint

sp_scope = "playlist-read-private"
sp_username = "maazin5"
sp_plname = "SPOTIPY TEST"

# connect to spotify
token = "dummy"
token = util.prompt_for_user_token(sp_username, sp_scope)
print(token)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    
    # get playlist info
    all_playlists = sp.user_playlists(sp_username)
    playlist_ids = [item['id'] for item in all_playlists['items']]
    playlist_names = [item['name'] for item in all_playlists['items']]

    if sp_plname in playlist_names:
        pl_id = playlist_ids[playlist_names.index(sp_plname)]
        print(f'Playlist "{sp_plname}" was found')
    else:
        sys.exit(f'Playlist "{sp_plname}" not found')
    
    sp_plitems = sp.playlist_items(
        pl_id, 
        fields="total,limit,next,offset,items(added_at,track(id,artists,name,duration_ms,album(name,release_date)))", 
        limit=2, 
        offset=0
        )
    pprint.pprint(sp_plitems["items"])
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
if __name__ == "__main__":
    print("ABC XYZ")