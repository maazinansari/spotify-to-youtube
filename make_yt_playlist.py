import os
import re
import pprint as pp
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors



def connect_to_yt(scope_list):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "yt_oauth_client.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scope_list)
    #credentials = flow.run_console()
    credentials = flow.run_local_server(port=0)
    youtube = build(
        api_service_name, api_version, credentials=credentials)
    
    return(youtube)

def get_playlist_id(yt_service, search_txt):
    
    request = yt_service.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    #QUOTA_COUNTER += 1
    
    r_items = response['items']
    pl_names = [item["snippet"]["title"] for item in r_items]
    pl_ids = [item["id"] for item in r_items]
    
    if search_txt in pl_names:
        playlist_id = pl_ids[pl_names.index(search_txt)]
        return(playlist_id)
    else:
        request = yt_service.playlists().insert(
            part="id,snippet",
            body={"snippet" : 
                     {"title" : search_txt} 
                 }
        )
        response = request.execute()
        #QUOTA_COUNTER += 50
        
        playlist_id = response["id"]
        print(f'Created new playlist "{search_txt}"')
        return(playlist_id)
        

def search_for_track(yt_service, search_txt):
    request = yt_service.search().list(
        part="snippet",
        maxResults=3,
        q=search_txt
    )
    response = request.execute()
    #QUOTA_COUNTER += 100
    
    search_list = response["items"]
    return(search_list)

def add_track_to_playlist(yt_service, playlist_id, track_id):
    request = yt_service.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": track_id
            }
          }
        }
    )
    response = request.execute()
    #QUOTA_COUNTER += 50
    
    return(response)
   
if __name__ == '__main__':
    search_txt = "THE KILLERS - MR. BRIGHTSIDE"
    scopes = [
        #"https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/youtube"
        ]

    yt_service = connect_to_yt(scopes)
    plist_id = get_playlist_id(yt_service, "BIG TEST")
    track_searchListResponse = search_for_track(yt_service, search_txt)
    trackvid_id = track_searchListResponse[0]["id"]["videoId"]
    add_track_to_playlist(yt_service, plist_id, trackvid_id)
    
    
    
# search_for_track() :   
#{'etag': 'MmZ9xsy85WaShugAtcSuIZajN2M',
# 'items': [{'etag': '9H6MK-7Zsx3vplfEXyh5qwL-qjc',
#            'id': {'kind': 'youtube#video', 'videoId': 'gGdGFtwCNBE'},
#            'kind': 'youtube#searchResult',
#            'snippet': {'channelId': 'UCjB3CzA-MwHrDzuXGweNiMg',
#                        'channelTitle': 'TheKillersVEVO',
#                        'description': "New Album 'Imploding The Mirage' Out "
#                                       'Now: '
#                                       'https://thekillers.lnk.to/ImplodingTheMirageID '
#                                       'Follow The Killers: Instagram: ...',
#                        'liveBroadcastContent': 'none',
#                        'publishTime': '2009-06-16T22:53:31Z',
#                        'publishedAt': '2009-06-16T22:53:31Z',
#                        'thumbnails': {'default': {'height': 90,
#                                                   'url': 'https://i.ytimg.com/vi/gGdGFtwCNBE/default.jpg',
#                                                   'width': 120},
#                                       'high': {'height': 360,
#                                                'url': 'https://i.ytimg.com/vi/gGdGFtwCNBE/hqdefault.jpg',
#                                                'width': 480},
#                                       'medium': {'height': 180,
#                                                  'url': 'https://i.ytimg.com/vi/gGdGFtwCNBE/mqdefault.jpg',
#                                                  'width': 320}},
#                        'title': 'The Killers - Mr. Brightside (Official Music '
#                                 'Video)'}},
#           {'etag': 'BUOQ6znqEix-zIquuDC687TiGJU',
#            'id': {'kind': 'youtube#video', 'videoId': 'pvIJyRkS9y0'},
#            'kind': 'youtube#searchResult',
#            'snippet': {'channelId': 'UCbQARXsT7pLvm-ifV0Itu6A',
#                        'channelTitle': 'Dank Music Channel',
#                        'description': 'Subscribe For More!',
#                        'liveBroadcastContent': 'none',
#                        'publishTime': '2017-09-24T13:00:02Z',
#                        'publishedAt': '2017-09-24T13:00:02Z',
#                        'thumbnails': {'default': {'height': 90,
#                                                   'url': 'https://i.ytimg.com/vi/pvIJyRkS9y0/default.jpg',
#                                                   'width': 120},
#                                       'high': {'height': 360,
#                                                'url': 'https://i.ytimg.com/vi/pvIJyRkS9y0/hqdefault.jpg',
#                                                'width': 480},
#                                       'medium': {'height': 180,
#                                                  'url': 'https://i.ytimg.com/vi/pvIJyRkS9y0/mqdefault.jpg',
#                                                  'width': 320}},
#                        'title': 'Mr. Brightside HQ (The Killers)'}},
#           {'etag': 'r7FXs24stFkHphL4nhqk7CoToZY',
#            'id': {'kind': 'youtube#video', 'videoId': 'j8tZs6G_h7U'},
#            'kind': 'youtube#searchResult',
#            'snippet': {'channelId': 'UCyh5g11KbG_YdbRw1ktAJqA',
#                        'channelTitle': 'Lost Panda',
#                        'description': 'Welcome to Lost Panda “The Killers - '
#                                       'Mr Brightside” Lyrics / Lyric Video by '
#                                       'Lost Panda ⏬ Stream “The Killers - Mr '
#                                       'Brightside” ...',
#                        'liveBroadcastContent': 'none',
#                        'publishTime': '2023-05-06T13:21:01Z',
#                        'publishedAt': '2023-05-06T13:21:01Z',
#                        'thumbnails': {'default': {'height': 90,
#                                                   'url': 'https://i.ytimg.com/vi/j8tZs6G_h7U/default.jpg',
#                                                   'width': 120},
#                                       'high': {'height': 360,
#                                                'url': 'https://i.ytimg.com/vi/j8tZs6G_h7U/hqdefault.jpg',
#                                                'width': 480},
#                                       'medium': {'height': 180,
#                                                  'url': 'https://i.ytimg.com/vi/j8tZs6G_h7U/mqdefault.jpg',
#                                                  'width': 320}},
#                        'title': 'The Killers - Mr Brightside (Lyrics)'}}],
# 'kind': 'youtube#searchListResponse',
# 'nextPageToken': 'CAMQAA',
# 'pageInfo': {'resultsPerPage': 3, 'totalResults': 1000000},
# 'regionCode': 'US'}    