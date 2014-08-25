#!/usr/bin/env python


import os #so you can give path or directory
import mutagen.easyid3 # the mutagen module
import sys # for reading cli arguments

# This is for parsing and making json requests
import requests

clientKey = '123456789' # this is the unique ID key
APIKEY = 'SM5R9B9IVUQZKGYS9' # echoNest API key
songArray = [] # the array of songs

def start():
    if checkClientKey():
        scanDirectory()
    else:
        getClientKey()
        scanDirectory()



def checkClientKey():
    if clientKey.strip(): # checks if string is empty, but strip out whitespace
        return True
    else:
        return False


def getClientKey():
    # this function makes a request for a new client key
    r = requests.get('http://0.0.0.0:3000/clienthandler?key=new')
    response = r.json()
    clientKey = response['key']
    # object will be status: success, key: 123456789, very simple


def scanDirectory():
    # this will scan the files, then offload each file to the parser
    for files in os.walk("./tracks/"):
        tracks = files[2]
        for track in tracks:
            parseTrack(track)


def parseTrack(track):
    from mutagen.easyid3 import EasyID3

    audiofile = EasyID3('./tracks/'+track)
    artist = audiofile['artist']
    title = audiofile['title']

    print artist[0], title[0]

    fetchAudioData(artist[0], title[0])


def fetchAudioData(artist, title):
    payload = {
        'api_key': APIKEY,
        'artist': artist,
        'title': title,
        'bucket': 'audio_summary',
        'results': '5'
    }

    r = requests.get('http://developer.echonest.com/api/v4/song/search', params=payload)
    extractData(r.json())


def extractData(response):
    # add song to array of songs, if length of array = 20, then send the request
    if len(response['response']['songs']) != 0:
        song = response['response']['songs'][0]
        songObj = {
            'artist': song['artist_name'],
            'title': song['title'],
            'energy': song['audio_summary']['energy'],
            'valence': song['audio_summary']['valence']
        }
        songArray.append(songObj)

        if len(songArray) == 20:
            print 'A bundle of songs is being sent to the server'
            del songArray[:]
            print len(songArray)
        else:
            print len(songArray)


def uploadBundle():
    r.requests.post('http://0.0.0.0:3000/songindex', data=songArray)


#reader = start()
