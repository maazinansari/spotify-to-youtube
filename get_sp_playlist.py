import sys
import spotipy
import spotipy.util as util
import re
import pprint as pp

def get_sp_playlist(token, username, playlist_name, page_item_limit=20, item_offset = 0, max_tracks = None):
    track_list = {}
    no_more_pages = False
    page_counter = 0
    duplicate_counter = 0
    
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
        
        while not no_more_pages:
            
            sp_plitems = sp.playlist_items(
                pl_id, 
                fields="total,limit,next,offset,items(added_at,track(id,artists,name,duration_ms,album(name,release_date)))", 
                limit=page_item_limit, 
                offset=item_offset
                )
            #pp.pprint(sp_plitems)
            
# {'items':          
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
#           'name': 'If I Die Young'}}],
# 'limit': 20,
# 'next': None,
# 'offset': 900,
# 'total': 904}
            for item in sp_plitems["items"]:
                t = item["track"]
                track_id = t["id"]
                track_name = t["name"]
                main_artist = t["artists"][0]["name"]
                duration_ms = t["duration_ms"]
                search_txt = f"{main_artist.upper()} - {track_name.upper()}"
                
                if track_id in track_list:
                    duplicate_counter += 1
                    track_id = f"{track_id}_{duplicate_counter}"
                
                track_list[track_id] = {
                    "search_txt" : search_txt,
                    "duration_ms" : duration_ms
                }
                if max_tracks and len(track_list) >= max_tracks:
                    print(f"{len(track_list)} tracks in track_list")
                    no_more_pages = True
                    break
            
            print(f"======================={len(track_list)}==========================")
            no_more_pages = True if sp_plitems["next"] is None else no_more_pages
            #no_more_pages = True if len(sp_plitems["items"]) < page_item_limit else False
            #no_more_pages = True if len(track_list) > 35 else False
            page_counter += 1
            item_offset = page_counter * page_item_limit
                  
        return(track_list)
        
if __name__ == "__main__":
    sp_scope = "playlist-read-private"
    sp_username = "maazin5"
    sp_plname = "SPOTIPY TEST"
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    # create search list from sp playlist 
    x = get_sp_playlist(token, sp_username, sp_plname, item_offset = 550, max_tracks = 2)
    pp.pprint(x)
    # create yt playlist from search list
    print("ABC XYZ")