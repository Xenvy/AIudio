import mutagen
import os
import csv
from tkinter import *
from tkinter.filedialog import askdirectory
import sys
# import librosa
import pygame

#File chooser
#root = Tk()
#root.minsize(300, 300)

list_of_songs = []
index = 0
current_file = "E:\\14 - Together In Electric Dreams.flac"
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
FOLDER_PATH = r'C:\Users\Lenovo PC\Documents\Sound-Traverse'

def directory_chooser():
    directory = askdirectory()
    os.chdir(directory)

    for format in FORMATS:
        for files in os.listdir(directory):
            if files.endswith(format):
                info(files)
                list_of_songs.append(files)

def make_base():
    with open(FOLDER_PATH + r'\\{}'.format('tags_base.txt'), 'a') as tempf:
        tempf.write("name; title; artist; album; tr_num; date; genre: len; format \n")

def info(current_file):
    flac_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    mp3_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    wav_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    ogg_tags = ['name', 'title', 'artist', 'album', 'date', 'genre']
    curr_tags = {}
    tempf = []
    current_audio = mutagen.File(current_file)
    if current_file.endswith('.flac'):
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
    try:
        open(FOLDER_PATH + r'\\{}'.format('tags_base.txt'), 'x')
    except FileExistsError:
        f = open("tags_base.txt", "a")
        for i in tempf:
            f.write(i)
        f.close()
    return curr_tags

def update_track(path):
    pass

def update_folder(path):
    pass

#directory_chooser()
tester = info(current_file)

print(tester)
print(tester['name'])
