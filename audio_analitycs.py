import eel
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
try     :

    import win32gui, win32con;

    frgrnd_wndw = win32gui.GetForegroundWindow();
    wndw_title  = win32gui.GetWindowText(frgrnd_wndw);
    if wndw_title.endswith("py.exe"):
        win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE);
    #endif
except  :
    pass

once = 0
prev_track_uri = ""
current_track_uri = ""

eel.init('web')

@eel.expose
def get_oauth(raw_auth, access, refresh):    
    global raw_auth_token
    global access_token
    global refresh_token
    raw_auth_token = raw_auth
    access_token = access
    refresh_token = refresh
    print(raw_auth_token)
    print(access_token)
    print(refresh_token)
    eel.blynk_tab()


@eel.expose
def confirmation():    
    global confirmation
    confirmation = True
    print(confirmation)

def spotify_auth():
    while True:
        print("I'm a thread")
              
        global once
        
        if (once == 0):
            once = 10
            eel.sleep(1)
            eel.req_oauth()
            eel.sleep(1)        
            break
                
                    
        eel.sleep(0.1)
        
                # Use eel.sleep(), not time.sleep()

def spotify_main():
    #print("spotify_main")
    global current_track_uri
    global current_track_progress
    global prev_track_progress
    global current_track_duration
    global prev_track_uri
    global raw_current_track_data    
    global raw_current_audio_features
    global current_audio_features_segments
    global current_audio_features_segments_array
    global current_segment
    global current_segment_time
    global numb_segments
    global min_loudness_segment
    global min_loudness
    global max_loudness
    global current_loudness
    global current_loudness_time
    global min_loudness_positive
    global max_loudness_positive
    global current_loudness_positive
    global bar_percentage
    global sp
    global once
    #search = input('search?')
                                                  
    sp = spotipy.Spotify(auth=access_token)
    raw_current_track_data = sp.current_playback()
    if (raw_current_track_data is not None) and ((raw_current_track_data.get("item")) is not None):
        #print(raw_current_track_data)
        #print(type(raw_current_track_data.get("item")))
        current_track_uri = (raw_current_track_data.get("item")).get("uri")
        current_track_progress = (raw_current_track_data.get("progress_ms"))/1000
        current_track_playing_status = raw_current_track_data.get("is_playing")
        #print(current_track_progress)
        #print(current_track_playing_status)
        
        
        if (current_track_uri != prev_track_uri):
            print("song switched! mehnat starts")
            print(current_track_uri)

            current_track_duration = (raw_current_track_data.get("item")).get("duration_ms")/100            
            raw_current_audio_features = sp.audio_analysis(current_track_uri)
            current_audio_features_segments = raw_current_audio_features.get("segments")
            current_audio_features_segments_array = np.array(current_audio_features_segments)
            numb_segments = len(current_audio_features_segments_array)
            current_segment = 0
            current_segment_time = 0
            prev_track_progress = 0
            min_loudness_segment = 0
            min_loudness = 0
            max_loudness = 0
            count = 0
            while (count < numb_segments):
                if((current_audio_features_segments_array[count]["loudness_max"]) < min_loudness):
                    min_loudness_segment = count
                    min_loudness = current_audio_features_segments_array[count]["loudness_max"]

                count = count + 1
                
            max_loudness_positive = max_loudness - min_loudness
            min_loudness_positive = min_loudness - min_loudness
            print(min_loudness_segment)
            print(min_loudness)
            print(current_track_duration)
        
        if (prev_track_progress > current_track_progress):
            current_segment = 0
            current_segment_time = 0
            
        while (current_segment_time < current_track_progress):            
            if (current_segment < numb_segments):
                #print(current_segment_time)
                current_loudness = current_audio_features_segments_array[current_segment]["loudness_max"]
                current_loudness_time = current_audio_features_segments_array[current_segment]["loudness_max_time"]
                current_confidence = current_audio_features_segments_array[current_segment]["confidence"]
                current_loudness_positive = current_loudness - min_loudness
                #print(current_loudness)
                #print(current_loudness_positive)
                #print(current_loudness_time)
                
                bar_percentage = round(((current_loudness_positive/max_loudness_positive) * 100)* current_confidence)
                print (("#" * bar_percentage))
                #print(bar_percentage,"%")
                current_segment = current_segment + 1
                #print(current_segment)
                if (current_segment < numb_segments):
                    current_segment_time = current_audio_features_segments_array[current_segment]["start"]

            else:
                print("song data end")
                break
            
        prev_track_uri = current_track_uri
        prev_track_progress = current_track_progress
            
def blynk_main():
    #print("blynk_main")
    jjjj = 1
    
eel.spawn(spotify_auth)
eel.start('start.html', block=False)

while True:
    #print("I'm a main loop")
    if (confirmation == True):
            eel.spawn(blynk_main)
            eel.spawn(spotify_main)    


    eel.sleep(0.01)
    







