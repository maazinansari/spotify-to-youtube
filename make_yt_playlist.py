import os
import re
import pprint as pp
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors

class QuotaTracker:
    def __init__(self, quota_limit=10000, warn_threshold = 7500):
        self.quota_limit = quota_limit
        self.warn_threshold = warn_threshold
        self.counter = 0
        assert self.warn_threshold <= self.quota_limit, f"warn_threshold ({self.warn_threshold}) must be less than or equal to quota_limit ({self.quota_limit})"
    def increment(self, quota_cost):
        if self.counter + quota_cost < self.warn_threshold:
            self.counter += quota_cost
            #print(f"+{quota_cost} Quota usage: {self.counter}")
        elif self.counter + quota_cost < self.quota_limit:
            raise Exception(f"Quota limit has reached {self.warn_threshold}")
        else:
            raise Exception(f"Quota limit has reached {self.quota_limit}")
        

def connect_to_yt(scope_list, warn_threshold = 7500):
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
    q = QuotaTracker(10000,warn_threshold)
    setattr(youtube, "quota_tracker", q)
    
    return(youtube)

def get_playlist_id(yt_service, search_txt):
    
    request = yt_service.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    yt_service.quota_tracker.increment(1)
    
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
        yt_service.quota_tracker.increment(50)
        
        
        playlist_id = response["id"]
        print(f'Created new playlist "{search_txt}"')
        return(playlist_id)
        

def search_for_track(yt_service, search_txt):
    request = yt_service.search().list(
        part="snippet",
        maxResults=3,
        q=search_txt,
        regionCode="US",
        safeSearch="none",
        type="video"
    )
    response = request.execute()
    yt_service.quota_tracker.increment(100)
    
    search_list = response["items"]
    return(search_list)

def add_track_to_playlist(yt_service, playlist_id, track_id, position = None):
    request = yt_service.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "position": position,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": track_id
            }
          }
        }
    )
    response = request.execute()
    yt_service.quota_tracker.increment(50)
    
    return(response)

def list_playlist_items(yt_service, playlist_id, count = 10):
    count_init = count
    if count > 50:
        count = 50
    request = yt_service.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=count
    )
    response = request.execute()
    yt_service.quota_tracker.increment(1)
    playlist_vids = [
            {
            "name": vid["snippet"]["title"],
            "id": vid["snippet"]["resourceId"]["videoId"],
            "position": vid["snippet"]["position"]
            } 
            for vid in response["items"]
        ]
    no_more_pages = True if len(playlist_vids) == count_init else False
    while not no_more_pages:
        print(f"!!!!!!!!!!!!!!!     {len(playlist_vids)}     !!!!!!!!!!!!!!!!!!!")
        nextPageToken = response["nextPageToken"]
        request = yt_service.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            pageToken = nextPageToken
        )
        response = request.execute()
        yt_service.quota_tracker.increment(1)
        playlist_vids_next = [
            {
            "name": vid["snippet"]["title"],
            "id": vid["snippet"]["resourceId"]["videoId"],
            "position": vid["snippet"]["position"]
            } 
            for vid in response["items"]
        ]
        playlist_vids.extend(playlist_vids_next)
        if len(playlist_vids) >= count_init or "nextPageToken" not in response:
            no_more_pages = True
    return(playlist_vids)
    
if __name__ == '__main__':
    import csv
    search_txt = "ALVVAYS - ARCHIE, MARRY ME"
    scopes = [
        #"https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/youtube"
        ]

    yt_service = connect_to_yt(scopes)
    #plist_id = get_playlist_id(yt_service, "BIG TEST")
    #track_searchListResponse = search_for_track(yt_service, search_txt)
    #pp.pprint(track_searchListResponse[0])
    #trackvid_id = track_searchListResponse[0]["id"]["videoId"]
    #add_track_to_playlist(yt_service, plist_id, trackvid_id)
    playlist_id = "PLlh37htMYim47zUcLG4XXvwPTDm2t__QM" 
    x = list_playlist_items(yt_service, playlist_id, 500)
    with open('big1.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, 
                            fieldnames=x[0].keys()
                           )
        fc.writeheader()
        fc.writerows(x)

    print(yt_service.quota_tracker.counter)
    
    
    
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