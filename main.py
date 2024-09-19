from get_sp_playlist import get_sp_playlist 
import spotipy.util as util
import pprint as pp


if __name__ == "__main__":
    sp_scope = "playlist-read-private"
    sp_username = "maazin5"
    sp_plname = "SPOTIPY TEST"
    # connect to spotify 
    token = util.prompt_for_user_token(sp_username, sp_scope)
    # create search list from sp playlist 
    x = get_sp_playlist(token, sp_username, sp_plname)
    pp.pprint(x)
    
    # connect to yt
    # create yt playlist from search list
    print("main.py done")