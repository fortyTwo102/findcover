from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

from mutagen import File
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import requests
from bs4 import BeautifulSoup
import os, json
import shutil
import pylast

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

global img
global filepath

#from acrcloud.recognizer import ACRCloudRecognizer

'''def recogTrack(filepath):

    config = {
        #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host':'identify-ap-southeast-1.acrcloud.com',
        'access_key':'d2d750f49525d96f7f82ddcbb9bb51a7', 
        'access_secret':'M6Ka3VLOOYlAg8StsLQxzQdVpXgpTKqXpJjS7RRk',
        'timeout':10 # seconds
    }

    re = ACRCloudRecognizer(config)


    buf = open(filepath, 'rb').read() 

    result = re.recognize_by_filebuffer(buf, 0)
    d = json.loads(result)


    
    try:
        artist = d['metadata']['music'][0]['artists'][0]['name']
        error('clear')
    except:
        error('throw','ACR Cloud Recognizer') 


    album = d['metadata']['music'][0]['album']['name']
    title = d['metadata']['music'][0]['title']

    audio = EasyID3(filepath)

    audio['artist'] = artist
    audio['title'] = title

    audio['album'] = album
    audio.save()
    
    showMetadata(filepath)'''



def findFromStorage(filepath):
    error('clear')
    
    audio = ID3(filepath)
     
    file = filedialog.askopenfile()
    imageFilePath = file.name
    
    audio.delall('APIC')
    
    with open(imageFilePath, 'rb') as albumart:
        audio['APIC'] = APIC(
                          encoding=3,
                          mime='image/jpeg',
                          type=3, desc=u'Cover',
                          data=albumart.read()
                        )   
    audio.save()

    shutil.copy(file.name, filepath.replace('.mp3','.jpg'))
    showImage(file.name)
    
def download4mSpotify(filepath):
    error('clear')
    
    audio = EasyID3(filepath)
    
    client_credentials_manager = SpotifyClientCredentials(client_id='ad3b6e58606c4b1d91832ecd0c160557',client_secret='e3f68c9f1c2b42e5a48a1d61e10fa0ab')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    
    artistName = audio['artist'][0]
    trackName = audio['title'][0]
    
    song = sp.search(q='artist:' + artistName+' track:'+trackName,type='track')
    try:
        album_cover_url = song['tracks']['items'][0]['album']['images'][0]['url']
    except:
        error('throw','Spotify')     
    
    alcover = requests.get(album_cover_url)
    if alcover.status_code == 200:
        with open(filepath.replace('.mp3','.jpg'), 'wb') as f:
            f.write(alcover.content)

    audio = ID3(filepath)
    audio.delall('APIC')

    with open(filepath.replace('.mp3','.jpg'), 'rb') as albumart:
        audio['APIC'] = APIC(
                          encoding=3,
                          mime='image/jpeg',
                          type=3, desc=u'Cover',
                          data=albumart.read()
                        )   
    audio.save()
    
    extractCover(filepath)
   
    
def extractCover(filepath):
    showImage(filepath.replace('.mp3','.jpg'))

'''def extractCover(filepath):
    file = File(filepath) # mutagen can automatically detect format and type of tags
    alb = file.tags.get('APIC:')
    artwork = alb.data # access APIC frame and grab the image

    with open('extracted.jpg', 'wb') as image:
        image.write(artwork) # write artwork to new image
    
    showImage('extracted.jpg')'''
    
def downloadCover(filepath):
    error('clear')
    audio = EasyID3(filepath)
    '''print(os.path.dirname(os.path.realpath(__file__)))
    url = 'https://www.last.fm/music/' + artist.replace(' ', '+') + '/' + album.replace(' ','+')
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    albumcover = soup.find('img', {"id": "header-expanded-image"})['src'] '''

    artist = audio['artist'][0]
    track = audio['title'][0]

    API_KEY = "892faa221e068c23baea5e91bb66acec" 
    API_SECRET = "590a32f885aa52b4ff812a611d84514f"

    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    track = network.get_track(artist, track)
    try:
        albumcover = track.get_cover_image()
    except:
        error('throw','Last.fm')    
    
    # https://stackoverflow.com/questions/11205386/python-beautifulsoup-get-an-attribute-value-based-on-the-name-attribute
    alcover = requests.get(albumcover)
    if alcover.status_code == 200:
        with open(filepath.replace('.mp3','.jpg'), 'wb') as f:
            f.write(alcover.content)


    audio = ID3(filepath)
    audio.delall('APIC')

    with open(filepath.replace('.mp3','.jpg'), 'rb') as albumart:
        audio['APIC'] = APIC(
                          encoding=3,
                          mime='image/jpeg',
                          type=3, desc=u'Cover',
                          data=albumart.read()
                        )   
    audio.save()

    
    extractCover(filepath)
    

def showMetadata(filepath):  
    audiofile = EasyID3(filepath)
        
    titleName = audiofile['title'][0]
    artistName = audiofile['artist'][0]
    albumName = audiofile['album'][0]

    Label(text="TITLE: " + titleName + " "*100,font=('Ariel',15)).place(relx=0.3, rely=0.7)
    Label(text="ARTIST: " + artistName + " "*100,font=('Ariel',15)).place(relx=0.3, rely=0.75)
    Label(text="ALBUM: " + albumName + " "*100,font=('Ariel',15)).place(relx=0.3, rely=0.8)
    
def error(arg, supplier=None):
    if arg=='clear':
        Label(text=" "*1000,font=('Ariel',15)).place(relx=0.5, rely=0.6,anchor=CENTER)
    if arg=='throw':
        Label(text="Sorry :( "+supplier+" couldn't find a match. ",font=('Ariel',15)).place(relx=0.5, rely=0.6,anchor=CENTER)
            

    
def getfile():
    error('clear')
    file = filedialog.askopenfile()
    filepath = file.name
    Label(text=""*100).place(relx=0.5,rely=0.2,anchor=CENTER)
    Label(text=file.name).place(relx=0.5,rely=0.2,anchor=CENTER)

    Button(window, text="FIND FROM STORAGE", command=lambda: findFromStorage(filepath)).place(relx=0.2,rely=0.3,anchor=CENTER)
    #Button(window, text="RECOGNIZE SONG", command=lambda: recogTrack(filepath)).place(relx=0.86,rely=0.30,anchor=CENTER)
    Button(window, text="CHANGE SONG DETAILS", command=lambda: changeMetadata(filepath)).place(relx=0.86,rely=0.35,anchor=CENTER)
    Button(window, text="DOWNLOAD FROM LAST.FM", command=lambda: downloadCover(filepath)).place(relx=0.2,rely=0.4,anchor=CENTER)
    Button(window, text="DOWNLOAD FROM SPOTIFY", command=lambda: download4mSpotify(filepath)).place(relx=0.2,rely=0.5,anchor=CENTER)

    showMetadata(filepath)
    extractCover(filepath)
    
    #showImage(albumCover)
    
def showImage(filepath):

    canvas = Canvas(window,width=200, height=200)

    canvas.place(relx=0.5, rely=0.4, anchor=CENTER)
    im=Image.open(filepath)


    im.thumbnail([200,200], Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)


    canvas.create_image(0,0,anchor=NW, image=img)
    window.mainloop()
    #downloadCover(file.name)
  
def setMetadata(filepath,title,album,artist):

    audio = EasyID3(filepath)

    audio['artist'] = artist.get()
    audio['title'] = title.get()

    audio['album'] = album.get()
    audio.save()

    showMetadata(filepath)
    
            
    
def changeMetadata(filepath):
    Label(window, text="{:<10}".format("Set Title:")).place(anchor=CENTER, relx= 0.72, rely=0.41)
    Label(window, text="{:<10}".format("Set Artist:")).place(anchor=CENTER, relx= 0.715, rely=0.46)
    Label(window, text="{:<10}".format("Set Album:")).place(anchor=CENTER, relx= 0.71, rely=0.51)
    
    title = Entry(window)
    title.place(anchor=CENTER, relx= 0.86, rely=0.41)
    
    artist = Entry(window)
    artist.place(anchor=CENTER, relx= 0.86, rely=0.46)
    
    album = Entry(window)
    album.place(anchor=CENTER, relx= 0.86, rely=0.51)

    
    Button(window, text="UPDATE",command=lambda: setMetadata(filepath,title,album,artist)).place(relx=0.91, rely=0.55, anchor=CENTER)
        

window = Tk()
window.title("FIND COVER")

window.geometry("700x700")
Button(window,text="OPEN MP3 FILE",command=getfile).place(relx=0.5, rely=0.1, anchor=CENTER)
window.mainloop()
