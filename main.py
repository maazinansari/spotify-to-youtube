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
    sp_item_offset = 119 # start from +1 the last index of the previous run
    search_keywords = ["LIVE", "CONCERT", "PERFORM"]
    
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    
    # connect to yt
    yt_service = yt.connect_to_yt(yt_scopes)
    time.sleep(5)
    # create yt playlist from search list
    plist_id = yt.get_playlist_id(yt_service, yt_playlist)
    
    # create search list from sp playlist 
    x = sp.get_sp_playlist(token,
                           sp_username,
                           sp_plname,
                           page_item_limit= 5,
                           item_offset = sp_item_offset,
                           max_tracks = 60
                           )
    pp.pprint(x)
    y = sp.sort_track_list(x.values())
    
    existing_trackvids = {}
    try:
        for i,search_txt in enumerate(y):
            if search_txt in existing_trackvids:
                trackvid_id = existing_trackvids[search_txt]["videoId"]
                trackvid_title = existing_trackvids[search_txt]["title"]
                print("using existing video")
            else:
                track_searchListResponse = yt.search_for_track(yt_service, search_txt)
                trackvid_id = track_searchListResponse[0]["id"]["videoId"]
                trackvid_title = track_searchListResponse[0]["snippet"]["title"]
                existing_trackvids[search_txt] = {
                                                    "videoId": trackvid_id,
                                                    "title" : trackvid_title
                                                    }
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
    except Exception as e:
        print(e)
    finally:
        print("main.py done")