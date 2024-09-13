import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import musicbrainzngs
import ssl
import pandas as pd
from itertools import combinations
import pickle
import time
import json

ssl._create_default_https_context = ssl._create_unverified_context
musicbrainzngs.set_useragent('a', '1.0')
client_id = "ba462f450a74477d9dfdb692fffeb594"
client_secret = "03bc75813f8b4589b3a1c01c0e7a55d6"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

songs_artist = {}
featurings_list = []
path = 'C:\\Users\\fedep\\OneDrive\\Desktop\\Universita\'\\Year 1\\I Semester\\Data Visualization\\Assignment\\Extracting Data\\ExportData'




# Gets songs list from playlist

def songs_list_from_playlist_name(name):
    songs_list = []
    songs_artist = []
    playlist_href = sp.search(name, type='playlist', limit=1)['playlists']['items'][0]['id']
    for songs in sp.playlist(playlist_href)['tracks']['items']:
        release_date = songs['track']['album']['release_date']
        for artist in songs['track']['artists']:
            songs_artist.append(artist['name'])
        songs_list.append({'Title': songs['track']['name'], 'Artists': songs_artist, 'Release Date': release_date,
                           'Popularity': songs['track']['popularity']})
        songs_artist = []
    print(songs_list)





def get_popularity_from_artist_id(id):
    return sp.artist(id)['popularity']



def get_country_from_artist_name(name):
    data = musicbrainzngs.search_artists(name, limit=1)
    if len(data['artist-list'])>0:
        data = data['artist-list'][0]
        if 'country' in data:
            return data['country']
        else:
            return 'NA'

def get_artists_info_from_playlist(playlist_name):
    songs_list = []
    fin_dict = {}
    name_list = []
    pop_list = []
    country_list = []
    playlist_href = sp.search(playlist_name, type='playlist', limit=1)['playlists']['items'][0]['id']
    for songs in sp.playlist(playlist_href)['tracks']['items']:
        for artist in songs['track']['artists']:
            if artist['name'] not in songs_artist:
                print(artist['name'])
                songs_artist[artist['name']] = ({'ID': artist['id'], 'Name': artist['name'], 'Popularity': get_popularity_from_artist_id(artist['id']), 'Country': get_country_from_artist_name(artist['name'])})
    return
    

def Merge(dict1, dict2):
    artists_list = list(dict2.keys())
    for key in artists_list:
        if key not in dict1:
            dict1[key] = dict2[key]
    return dict1

def get_top_artists():
    get_artists_info_from_playlist('Top 50 Stati Uniti')
    get_artists_info_from_playlist('Top 50 Italia')
    get_artists_info_from_playlist('Top 50 Spagna')
    get_artists_info_from_playlist('Top 50 Regno Unito')
    get_artists_info_from_playlist('Top 50 Francia')
    get_artists_info_from_playlist('Top 50 Messico')
    get_artists_info_from_playlist('Top 50 Argentina')
    get_artists_info_from_playlist('Top 50 Globale')
    df = pd.DataFrame.from_dict(songs_artist).T
    path = path+'\\artists.csv'
    df.to_csv(path, index=False)



def read_artists():
    df = pd.read_csv(path+'\\artists.csv')
    return df


def get_top_artists_album():
    album_list = {}
    df_init = read_artists()
    id_list = df_init['ID'].tolist()
    for index, id in enumerate(id_list):
        print(index)
        add_album_to_albumlist(id, album_list)
    df = pd.DataFrame.from_dict(album_list).T
    print(df)
    path = path+'\\albums.csv'
    df.to_csv(path, index=False)
    return

def add_album_to_albumlist(id, dic):
    print(id)
    artist_album_list = sp.artist_albums(id)['items']
    for data in artist_album_list:
        print(data['name'])
        if data['id'] not in dic:
            dic[data['id']] = {'ID': data['id'], 'Name': data['name'], 'Date': data['release_date'], 'Main artist': data['artists'][0]['name'], 'Cover': data['images'][0]['url'], 
                                }
            
def read_albums():
    df = pd.read_csv(path+'\\albums.csv')
    print(df)
    return df

def get_top_artists_songs():
    songs_list = {}
    df_init = read_albums()
    id_list = df_init['ID'].tolist()
    for index, id in enumerate(id_list):
        print(index)
        add_song_to_songslist(id, songs_list)
    df = pd.DataFrame.from_dict(songs_list).T
    print(df)
    path = path+'\\songs.csv'
    df.to_csv(path, index=False)
    return

def collect_songs_id():
    songs_list = {}
    df_init = read_albums()
    id_list = df_init['ID'].tolist()
    for index, id in enumerate(id_list):
        print(index)
        if index>=4500:
            for track in sp.album_tracks(id)['items']:
                if track['id'] not in songs_list:
                    songs_list[track['id']] = {'ID': track['id']}
    df = pd.DataFrame.from_dict(songs_list).T
    print(df)
    path = path+'\\songs.csv'
    df.to_csv(path, index=False)
    return

def add_song_to_songslist(id, dic):
    print(id)
    artist_album_list = sp.artist_albums(id)['items']
    for data in artist_album_list:
        print(data['name'])
        if data['id'] not in dic:
            dic[data['id']] = {'ID': data['id'], 'Name': data['name'], 'Date': data['release_date'], 'Main artist': data['artists'][0]['name'], 'Cover': data['images'][0]['url']}
    return

def read_songs():
    df = pd.read_csv(path+f'\\songs.csv')
    print(df)
    return df

def read_songs_dict(index):
    df = pd.read_csv(path+f'\\songs_dict{index}.csv')
    print(df)
    return df


def get_songs_data(init, end):
    songs_dict = {}
    feat_dict = {}
    df = read_songs()
    print(df)
    songs_id_list = df['ID'].tolist()
    for index, id in enumerate(songs_id_list):
        print(index)
        if index>init and index<=end:
            if id not in songs_dict:
                song_data = sp.track(id)
                if 'genres' in song_data['artists']:
                    genere = song_data['artists'][0]['genres'][0]
                else:
                    genere = 'NA'

                songs_dict[id] = {'ID': id, 'Name': song_data['name'], 'Main Artist': song_data['artists'][0]['name'], 'Album ID': song_data['album']['id'], 'Album Name': song_data['album']['name'], 'Genere': genere, 'Popularity': song_data['popularity'], 'Duration': song_data['duration_ms']}
    df = pd.DataFrame.from_dict(songs_dict).T
    print(df)
    path = 'C:\\Users\\fedep\\OneDrive\\Desktop\\Universita\'\\Year 1\\I Semester\\Data Visualization\\Assignment\\Extracting Data\\ExportData\\songs_dict2.csv'
    df.to_csv(path, index=False)
    return

def merge_dictionaries(ind1, ind2, ind3):
    df1 = read_songs_dict(ind1)
    df2 = read_songs_dict(ind2)
    result = pd.concat([df1, df2])
    print(result)
    pat = path+ f'\\songs_dict{ind3}.csv'
    result.to_csv(pat, index=False)

def get_artist_genre_and_image():
    df = read_artists()
    dic = pd.DataFrame.to_dict(df)
    cover_img_dict = {}
    main_genre_dict = {}
    id_list = df['ID'].tolist()
    for index, id in enumerate(id_list):
        print(id)
        data = sp.artist(id)
        cover_img_dict[index] = data['images'][0]['url']
        main_genre_dict[index] = data['genres'][0]
    dic['Genre'] = main_genre_dict
    dic['Image'] = cover_img_dict
    df = pd.DataFrame.from_dict(dic).T
    print(df)
    return

def get_featuring_from_song():
    df = read_songs()
    feat_dict = {}
    artists_list = []
    artist_id = []
    id_list = df['ID'].tolist()
    for index, id in enumerate(id_list):
        if index>=26000:
            track_data = sp.track(id)
            artists_list = track_data['artists']
            print(index)
            if len(artists_list)>1:
                for artist in artists_list:
                    artist_id.append(artist['id'])
                feat_dict[id] = artist_id
                artist_id = []
    save_feat_dic(feat_dict)
    return 

def save_feat_dic(dic):
    with open(f'./ExportData/person_data_fin.pkl', 'wb') as fp:
        pickle.dump(dic, fp)
        print('dictionary saved successfully to file')

def read_feat_dic(index):
    with open(f'./ExportData/person_data_{index}.pkl', 'rb') as fp:
        feat = pickle.load(fp)
        print('Feat dictionary')
        return feat

def insert_genre():
    df = read_artists().to_dict()
    genre_dict = {}
    id_list = (df['ID'])
    indexes = id_list.keys()
    for index in indexes:
        artist_info = sp.artist(id_list[index])
        if 'genres' in artist_info and len(artist_info['genres'])>0:
            genre = artist_info['genres'][0]
            genre_dict[index] = genre
            print(genre)
        else:
            genre_dict[index] = 'NA'
    df['Genre'] = genre_dict
    df = pd.DataFrame.from_dict(df)
    print(df)
    path = 'C:\\Users\\fedep\\OneDrive\\Desktop\\Universita\'\\Year 1\\I Semester\\Data Visualization\\Assignment\\Extracting Data\\ExportData\\songs_dict2.csv'
    df.to_csv(path, index=False)

def insert_image():
    df = read_artists().to_dict()
    genre_dict = {}
    id_list = (df['ID'])
    indexes = id_list.keys()
    for index in indexes:
        artist_img = sp.artist(id_list[index])['images'][0]['url']
        print(artist_img)
    df['Image'] = genre_dict
    df = pd.DataFrame.from_dict(df)
    print(df)
    path = 'C:\\Users\\fedep\\OneDrive\\Desktop\\Universita\'\\Year 1\\I Semester\\Data Visualization\\Assignment\\Extracting Data\\ExportData\\songs_dict2.csv'
    df.to_csv(path, index=False)

def fill_missing_artists():
    dic = {}
    with open('./ExportData/missing_artist.txt', 'r', encoding='utf-8') as missing_artists:
        for line in missing_artists:
            result = sp.search(line.strip(), limit=1, type='artist')['artists']['items'][0]
            print(result)
            if len(result['genres'])>0:
                genre = result['genres'][0]
            else:
                genre = 'NA'
            dic[result['id']] = {'ID': result['id'], 'Name': line.strip(), 'Popularity': result['popularity'], 'Country': 'NA', 'Genre': genre}
    df = pd.DataFrame.from_dict(dic).T
    df.to_csv('./ExportData/missing_artists.csv', index=False)


def get_df_from_couples_dic():
    feat = None
    fin_dic = {}
    with open(f'./ExportData/feat_couples_dic_fin.pkl', 'rb') as fp:
        feat = pickle.load(fp)
        print('Feat dictionary')
    print(feat)
    index = 0
    for key in (list(feat.keys())):
        feats_couples = feat[key]
        for couple in feats_couples:
            fin_dic[index] = {'SongID': key, 'Artist1': couple[0], 'Artist2': couple[1]}
            index = index+1
        index = index+1
    df = pd.DataFrame.from_dict(fin_dic).T
    df.to_csv('./ExportData/feat_couples_14000.csv', index=False)


def get_couples_from_dict(dic):
    final_list = []
    songs_id_list = list(dic.keys())
    for index, key in enumerate(songs_id_list):
        combinations_list = list(combinations(dic[key], 2))
        for couple in combinations_list:
            final_list.append([key, couple[0], couple[1]])
    df = pd.DataFrame(final_list, columns=['SongID', 'Artist1', 'Artist2'])
    df.to_csv('./ExportData/feat_couples.csv', index=False)
    return df


def get_real_names_and_artists():
    list_real_names = []
    df_feat = pd.read_csv(path+'\\feat_couples.csv')
    df_artists = pd.read_csv(path+'\\artists.csv')
    df_songs_dict = pd.read_csv(path+'\\songs_dict.csv')
    for index, row in df_feat.iterrows():
        print(index)
        
        artist1_id = df_artists['ID']
        song_name = df_songs_dict[df_songs_dict['ID']==row['SongID']]['Name'].values[0]
        artist1_name = df_artists[df_artists['ID']==row['Artist1']]['Name'].values
        artist2_name = df_artists[df_artists['ID']==row['Artist2']]['Name'].values
        if len(artist1_name)>0 and len(artist2_name)>0:
            list_real_names.append([row['SongID'], song_name, row['Artist1'], artist1_name[0], row['Artist2'], artist2_name[0]])
    df = pd.DataFrame(list_real_names, columns=['SongID', 'SongName', 'Artist1ID', 'Artist1Name', 'Artist2ID', 'Artist2Name'])
    df.to_csv('./ExportData/feat_couples_real_data.csv', index=False)
    print(df)

get_real_names_and_artists()




