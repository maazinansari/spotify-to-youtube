import get_sp_playlist as sp
import make_yt_playlist as yt
import spotipy.util as util
import pprint as pp


if __name__ == "__main__":
    sp_scope = "playlist-read-private"
    sp_username = "maazin5"
    sp_plname = "SPOTIPY TEST"
    yt_scopes = ["https://www.googleapis.com/auth/youtube"]
    yt_playlist = "BIG TEST"
    
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    
    # connect to yt
    yt_service = yt.connect_to_yt(yt_scopes)
    # create yt playlist from search list
    plist_id = yt.get_playlist_id(yt_service, yt_playlist)
    
    # create search list from sp playlist 
    x = sp.get_sp_playlist(token, sp_username, sp_plname, item_offset = 14, max_tracks = 150)
    pp.pprint(x)
    y = sp.sort_track_list(x.values())
    
    for i,search_txt in enumerate(y):
        track_searchListResponse = yt.search_for_track(yt_service, search_txt)
        trackvid_id = track_searchListResponse[0]["id"]["videoId"]
        trackvid_title = track_searchListResponse[0]["snippet"]["title"]
        print(f'{i} : "{search_txt}" --> "{trackvid_title}"')
        yt.add_track_to_playlist(yt_service, plist_id, trackvid_id, 0)
    
    print("main.py done")