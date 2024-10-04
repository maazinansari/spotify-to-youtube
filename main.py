import get_sp_playlist as sp
import make_yt_playlist as yt
import spotipy.util as util
import pprint as pp
import time

def check_search_result(search_result, keywords):
    search_result_upper = search_result.upper()
    for keyword in keywords:
        if keyword.upper() in search_result_upper:
            return(True)
    return(False)

if __name__ == "__main__":
    sp_scope = "playlist-read-private"
    sp_username = "maazin5"
    sp_plname = "SPOTIPY TEST"
    yt_scopes = ["https://www.googleapis.com/auth/youtube"]
    yt_playlist = "BIG TEST"
    sp_item_offset = 34
    search_keywords = ["LIVE", "CONCERT", "PERFORM"]
    
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    
    # connect to yt
    yt_service = yt.connect_to_yt(yt_scopes)
    time.sleep(5)
    # create yt playlist from search list
    plist_id = yt.get_playlist_id(yt_service, yt_playlist)
    
    # create search list from sp playlist 
    x = sp.get_sp_playlist(token, sp_username, sp_plname, item_offset = sp_item_offset, max_tracks = 100)
    #pp.pprint(x)
    y = sp.sort_track_list(x.values())
    
    for i,search_txt in enumerate(y):
        track_searchListResponse = yt.search_for_track(yt_service, search_txt)
        trackvid_id = track_searchListResponse[0]["id"]["videoId"]
        trackvid_title = track_searchListResponse[0]["snippet"]["title"]
        flagged_title = check_search_result(trackvid_title, search_keywords)
        if flagged_title:
            print(f'''!!!!!
            {i+sp_item_offset} : "{search_txt}" --> 
                                "{trackvid_title}"
            '''
            )
        print(f'{i+sp_item_offset} : "{trackvid_title}"')
        time.sleep(10)
        yt.add_track_to_playlist(yt_service, plist_id, trackvid_id, 0)
        print(f"..............................................{yt_service.quota_tracker.counter}")
    
    print("main.py done")