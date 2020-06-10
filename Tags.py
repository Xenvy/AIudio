import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3



import os
import csv
from tkinter import *
from tkinter.filedialog import askdirectory
import sys
# import librosa
import pygame
import csv

#File chooser
#root = Tk()
#root.minsize(300, 300)

list_of_songs = []
index = 0
current_file = "E:\\05 Perfect Strangers.wav"
current_file_2 = "E:\\1. Muzyka\ABBA\\1976 - Arrival\\04. Dum Dum Diddle.flac"
current_file_3 = "E:\\Gabriel's Oboe.mp3"
current_path = ''
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
FOLDER_PATH = r'C:\Users\Lenovo PC\Documents\Sound-Traverse'
FIELDNAMES = ['name', 'title', 'artist', 'album', 'date', 'genre']

def directory_chooser():
    directory = askdirectory()
    os.chdir(directory)

    current_path = directory

    list_of_paths = []

    for format in FORMATS:
        for files in os.listdir(directory):
            if files.endswith(format):
                list_of_paths.append(directory + files)

    return list_of_paths

def make_base():
    with open(FOLDER_PATH + r'\\{}'.format('tags_base.csv'), 'w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=';')
        csv_writer.writeheader()


def info(current_file):
    flac_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    mp3_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    wav_tags = ['name']
    ogg_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    curr_tags = {}
    tempf = []
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in flac_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in mp3_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in wav_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in ogg_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    temp_path = FOLDER_PATH + r'\\{}'.format('tags_base.csv')
    flag = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            ct = 0
            for row in csv_reader:
                 if row['name'] == curr_tags['name']:
                    flag = 1
        if flag == 0:
            with open(temp_path, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
                csv_writer.writerow(curr_tags)
    else:
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            csv_writer.writerow(curr_tags)

    return curr_tags

def update_track(current_file):
    flac_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    mp3_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    wav_tags = ['name']
    ogg_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    curr_tags = {}
    tempf = []
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in flac_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                pass
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in mp3_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.write(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in wav_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in ogg_tags:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except KeyError:
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    print("Typ się wywalił z rowerka")
    temp_path = FOLDER_PATH + r'\\{}'.format('tags_base.csv')
    flag = 0
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            ct = 0
            for row in csv_reader:
                if row['name'] == curr_tags['name']:
                    flag = 1
        if flag == 0:
            with open(temp_path, 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
                csv_writer.writerow(curr_tags)
    else:
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            csv_writer.writerow(curr_tags)

    return curr_tags

def update_folder(path):
    pass

def add_to_base():
    list_of_songs = []
    list_of_songs = directory_chooser()
    print(list_of_songs)
    for song in list_of_songs:
        info(song)





#directory_chooser()
#add_to_base()
#tester = info(current_file)
#print(tester)

#audio = mutagen.StreamInfo(current_file)
#print(audio)

#tester = info(current_file)

#print(EasyID3.valid_keys.keys())

#audio = mutagen.(current_file)
#audio.add_tags()
#audio.save()




"""
audio["title"] = u"Perfect Strangers"
audio.pprint()
audio.save()
"""
"""
audio = MP3(current_file_3)
audio.pprint()
print(audio)
"""
#tester2 = info(current_file_2)


#print(tester['name'])
#print(tester['title'])
