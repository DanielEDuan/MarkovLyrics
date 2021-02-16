import configparser
import requests
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config["Client_Access_Token"]['token']

token = getAccessToken()

def searchArtist(name):
    api_url = "https://api.genius.com/search/?q={}".format(name)

    headers = {"authorization": token}

    r = requests.get(api_url, headers=headers)

    return r.json()

def getArtistID(name):
    r = searchArtist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id

def getTopSongs(name):
    id = getArtistID(name)

    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    headers={"authorization": token}

    params = {
        "sort":"popularity",
        "per_page": 30
    }

    r = requests.get(api_url,headers=headers,params=params)

    return r.json()

def getLyrics(name):
    r = getTopSongs(name) # get json from API

    songs = r["response"]["songs"] # get dictionary object for songs
    lyrics_array = [] # create blank array to hold urls

    for song in songs: # loop through dictionary
        lyrics_array.append(song["url"]) # append song urls

    return lyrics_array # return list of urls


def scrapeLyricsText(name):
    urls = getLyrics(name)
    # print(urls)

    lyrics = []

    for link in urls:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        lyrics_div = soup.find(class_="lyrics")

        anchor_tags = []

        if lyrics_div != None:
            anchor_tags = lyrics_div.find_all('a')

        lyric = []

        for tag in anchor_tags:
            text = tag.text
            if len(text) != 0 and text[0] != "[":
                lyric.append(text.replace("\n", " NEWLINE "))

        lyrics.append(lyric)

    return lyrics

