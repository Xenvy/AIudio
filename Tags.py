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
import csv
from tinytag import TinyTag
import beets
import musicbrainzngs as mbz


#File chooser
#root = Tk()
#root.minsize(300, 300)

list_of_songs = []
index = 0
current_file = "E:\\05 Perfect Strangers2.wav"
current_file_2 = "E:\\04 - Les chants magnetiques IV.flac"
current_file_3 = "E:\\Gabriel's Oboe.mp3"
current_file_4 = "E:\\01 - The RobotsOGG.ogg"
current_path = ''
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
FOLDER_PATH = r'E:\\Python'
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
    curr_tags = {}
    tempf = []
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in FIELDNAMES:
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
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in FIELDNAMES:
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
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                try:
                    curr_tags[curr_key] = str(current_audio[key])
                    tempf.append(curr_tags[curr_key] + ';')
                except TypeError:
                    try:
                        current_audio_aux = TinyTag.get(current_file)
                        if curr_key == 'title':
                            curr_tags[curr_key] = current_audio_aux.title
                        if curr_key == 'artist':
                            curr_tags[curr_key] = current_audio_aux.artist
                        if curr_key == 'album':
                            curr_tags[curr_key] = current_audio_aux.album
                        if curr_key == 'date':
                            curr_tags[curr_key] = current_audio_aux.year
                        if curr_key == 'genre':
                            curr_tags[curr_key] = current_audio_aux.genre
                    except KeyError:
                        curr_tags[curr_key] = "None"
                        tempf.append(curr_tags[curr_key] + ';')
                    except TypeError:
                        curr_tags[curr_key] = "None"
                        tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
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
                    curr_tags[curr_key] = "None"
                    tempf.append(curr_tags[curr_key] + ';')
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

def update_track(current_file, new_tags):
    curr_tags = {}
    tempf = []
    if current_file.endswith('.flac'):
        current_audio = FLAC(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
                tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.mp3'):
        current_audio = EasyID3(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
                tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.wav'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                #current_audio[curr_key] = new_tags[key]
                #current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
                tempf.append(curr_tags[curr_key] + ';')
    elif current_file.endswith('.ogg'):
        current_audio = mutagen.File(current_file)
        for key in FIELDNAMES:
            curr_key = key.strip('\'')
            if key == 'name':
                curr_tags[curr_key] = str(current_file)
                tempf.append(curr_tags[curr_key] + ';')
            else:
                current_audio[curr_key] = new_tags[key]
                current_audio.save()
                curr_tags[curr_key] = str(new_tags[key])
                tempf.append(curr_tags[curr_key] + ';')
    temp_path = FOLDER_PATH + r'\\{}'.format('tags_base.csv')
    templist = []
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            for row in csv_reader:
                if row['name'] == curr_tags['name']:
                    templist.append((curr_tags))
                elif row['name'] == 'name;title;artist;album;date;genre':
                    pass
                else:
                    templist.append((row))
        os.remove(temp_path)
        make_base()
        with open(temp_path, 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            for row in templist:
                csv_writer.writerow(row)
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


new_tags_1 = {'title': 'Oboj Gabriel', 'artist': 'No i co teraz', 'album': 'TeTe', 'date': '2000', 'genre': 'C&G'}



#directory_chooser()
#add_to_base()
#tester = update_track(current_file, new_tags_1)
#tester2 = info(current_file)
#print(tester2)




