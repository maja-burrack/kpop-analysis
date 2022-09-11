#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 16:06:08 2022

@author: majalarsen
"""

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysecrets

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(
    client_id = mysecrets.clientid, 
    client_secret = mysecrets.clientsecret
    )
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

blackpink = '41MozSoPIsD1dJM0CLPjZF'
artist_list = [blackpink]

feature_list = []

for artist in artist_list:
    artistalbums = sp.artist_albums(artist_id = artist, album_type='album')
    artistsingles = sp.artist_albums(artist_id = artist, album_type='single')
    artistalbums.update(artistsingles)
    
    # go to their individual albums
    for i in range(len(artistalbums['items'])):
        album_uri = artistalbums['items'][i]['uri']
        album_tracks = sp.album_tracks(album_uri)
        
        #go to their individual tracks
        for j in range(len(album_tracks['items'])):
            album_song = album_tracks['items'][j]['uri']
            audiofeatures = sp.audio_features(album_song)

            #extract individual audio features of individual tracks
            for feature in audiofeatures:
                feature_list.append([feature['danceability'], feature['energy'], feature['key'], feature['speechiness'],
                                     feature['acousticness'], feature['instrumentalness'], feature['liveness'], feature['valence'],
                                     feature['tempo'], feature['duration_ms'],feature['time_signature'], artistalbums['items'][i]['artists'][0]['name'], artistalbums['items'][i]['release_date'], album_tracks['items'][j]['name'], artistalbums['items'][i]['name']])


data = pd.DataFrame(feature_list, columns = ['danceability','energy','key','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature', 'artist_name', 'release_date', 'song_name', 'album_name'])
data = data.drop_duplicates()
data = data.groupby(['artist_name', 'release_date', 'song_name', 'album_name']).mean()

data.to_csv('data/song_features.csv')


