from pygame import mixer
import pygame
import tkinter as tk
import os
import threading
from tkinter import ttk
from tkinter import filedialog

pygame.init()

mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
cursor = 0
paused = 0
playback_button_pressed = 0
global sellib
selpl = 0
coords = []
dragfromlib=False
dragfrompl=False

global FOLDER_PATH, MUSIC_PATHS, MAIN_LIST, PLAYLISTS_LIST, ACTIVE_LIST
FOLDER_PATH = r'C:\\Users\\jasie\\source\\repos\\TeamProject\\TeamProject'
MUSIC_PATHS = [r'C:\\Users\\jasie\\source\\repos\\TeamProject\\TeamProject']
MAIN_LIST = PLAYLISTS_LIST = ACTIVE_LIST = []

def Change_Volume(current_volume):
    mixer.music.set_volume(current_volume)

global main_window
main_window = tk.Tk()
main_window.geometry("1280x720")
main_window.title("AIaudio")

program_menu = tk.Menu(main_window)

global library_string, playlist_string
library_string = tk.StringVar()
playlist_string = tk.StringVar()

current_volume = tk.DoubleVar()
current_volume.set(0.5)
changed_volume = 0.5
volume_slider = tk.Scale(main_window, from_=0, to=1, resolution=0.01, orient="horizontal", variable=current_volume, command=Change_Volume(current_volume.get()))

music_library = tk.LabelFrame(main_window, text="Music library")
music_library.grid(column=0, row=0, rowspan=4, sticky=tk.NW)

library_content = ttk.Treeview(music_library, height=33)
library_content.column('#0', width=410, minwidth=410, anchor='center')
library_content.heading('#0', text='All Music', anchor=tk.W)
library_content.grid(column=0, row=1, rowspan=3, sticky=tk.NW)

playlist_widget = tk.LabelFrame(main_window, text="Playlist")
playlist_widget.grid(column=6, row=0, rowspan=4, sticky=tk.NW)

playlist_contents = ttk.Treeview(playlist_widget, height=33, columns=('Artist', 'Title', 'Duration'))
playlist_contents.column('#0', width=20, minwidth=20, anchor='center')
playlist_contents.heading('#0', text='Pl', anchor=tk.W)
playlist_contents.column('Artist', width=130, minwidth=130, anchor='center')
playlist_contents.heading('Artist', text='Artist', anchor=tk.W)
playlist_contents.column('Title', width=220, minwidth=220, anchor='center')
playlist_contents.heading('Title', text='Title', anchor=tk.W)
playlist_contents.column('Duration', width=56, minwidth=56, anchor='center')
playlist_contents.heading('Duration', text='Duration', anchor=tk.W)
playlist_contents.grid(column=6, row=1, rowspan=3, sticky=tk.NW)

track_info = tk.LabelFrame(main_window, text="Track details")
track_info.grid(column=1, columnspan=6, row=0, rowspan=3, sticky=tk.NW)

track_info_contents = tk.Label(track_info, anchor=tk.NW, justify=tk.LEFT, text="\tFilename\tExample filename.mp3\n\tDuration\t\t4:20\n\tSample rate\t44.1 kHz\n\tChannels\t2\n\tCodec\t\tMP3\n\tBitrate\t\t320kbps", height=38, width=59)
track_info_contents.grid(column=1, columnspan=6, row=1, rowspan=2, sticky=tk.NW)

play_button = tk.Button(main_window, text='Play', width=8, height=1, command=lambda: Start_Playback())
pause_button = tk.Button(main_window, text='Pause', width=8, height=1, command=lambda: Pause_Playback())
stop_button = tk.Button(main_window, text='Stop', width=8, height=1, command=lambda: Stop_Playback())
previous_button = tk.Button(main_window, text='Previous', width=8, height=1, command=lambda: Previous_Track())
next_button = tk.Button(main_window, text='Next', width=8, height=1, command=lambda: Next_Track())

play_button.grid(column=1, row=3)
pause_button.grid(column=2, row=3)
stop_button.grid(column=3, row=3)
previous_button.grid(column=4, row=3)
next_button.grid(column=5, row=3)
volume_slider.grid(column=3, row=2)

main_window.columnconfigure(0, minsize=420)
main_window.columnconfigure(1, minsize=80)
main_window.columnconfigure(2, minsize=80)
main_window.columnconfigure(3, minsize=80)
main_window.columnconfigure(4, minsize=80)
main_window.columnconfigure(5, minsize=80)
main_window.columnconfigure(6, minsize=400)
main_window.rowconfigure(1, minsize=600)
main_window.rowconfigure(2, minsize=10)
main_window.rowconfigure(3, minsize=40)


def Start_Playback():
    global cursor, paused, playback_button_pressed
    if paused:
        mixer.music.unpause()
        paused = 0
        playback_button_pressed = 0
    else:
        playback_button_pressed = 1
        mixer.music.stop()
        mixer.music.load(ACTIVE_LIST[cursor].tr_path)
        mixer.music.play()
        playback_button_pressed = 0


def Pause_Playback():
    global paused, playback_button_pressed
    playback_button_pressed = 1
    mixer.music.pause()
    paused = 1


def Stop_Playback():
    global playback_button_pressed
    playback_button_pressed = 1
    mixer.music.stop()


def Set_Volume(volume):
    mixer.music.set_volume(volume)


def Next_Track():
    global cursor, playback_button_pressed
    playback_button_pressed = 1
    cursor += 1
    mixer.music.stop()
    if not cursor < len(ACTIVE_LIST):
        cursor = 0
    mixer.music.load(ACTIVE_LIST[cursor].tr_path)
    mixer.music.play()


def Previous_Track():
    global cursor, playback_button_pressed
    playback_button_pressed = 1
    cursor -= 1
    if not 0 <= cursor:
        cursor = 0
    mixer.music.stop()
    mixer.music.load(ACTIVE_LIST[cursor].tr_path)
    mixer.music.play()

def Add_Music_Path():
    dirname = filedialog.askdirectory()
    MUSIC_PATHS.append(dirname)

def Clear_Music_Paths():
    MUSIC_PATHS.clear

def Exit():
    exit()

def New_Playlist():
    ACTIVE_LIST.clear
    displayPlaylist(ACTIVE_LIST)


def Generate_Playlist():
    t=tk.Toplevel(main_window)
    t.title('Generate playlist')
    t.geometry('300x200-800+400')
    tag_entry_label=tk.Label(t, text='Search for tags to add:')
    tag_results=ttk.Treeview(t)
    tag_results.heading('#0', text='Search results', anchor=tk.W)
    tags_chosen=ttk.Treeview(t)
    tags_chosen.heading('#0', text='Tags chosen', anchor=tk.W)
    tag=tk.StringVar()
    tag_entry=tk.Entry(t, exportselection=0, textvariable=tag)
    search_button=tk.Button(t, text='Search', command=lambda:searchForTags(MAIN_LIST, tag, tag_results))
    add_tag=tk.Button(t, text='Add tag', command=lambda:tags_chosen.insert('', 'end', text=tag_results.item(tag_results.selection, 'text')))

#   JAKO COMMAND FUNKCJA DO GENEROWANIA PLAYLIST
#   generate_button=tk.Button(t, text='Generate playlist', command=)

#   LISTA TAGÓW DO GENEROWANIA PLAYLISTY
#   chosen_tags_list=[]
#   for i in tags_chosen.get_children():
#       chosen_tags_list.append(tags_chosen.item(i, 'text'))

    tag_entry_label.pack()
    tag_entry.pack()
    search_button.pack()
    tag_results.pack()
    add_tag.pack()
    tags_chosen.pack()
#   generate_button.pack()

def Load_Playlist():
    global ACTIVE_LIST
    filename = filedialog.askopenfilename().replace(r'/', r'\\')
    for instance in range(len(PLAYLISTS_LIST)):
        if filename == PLAYLISTS_LIST[instance].pl_path:
            path = PLAYLISTS_LIST[instance].pl_path
            ACTIVE_LIST = []

            with open(f'{path}', 'r') as file:
                for line in file:
                    line = line.replace('\n', '')

                    if not line.startswith('"'):
                        for instance2 in range(len(MAIN_LIST)):
                            if line == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                pl_path = filename
                                pl_name = PLAYLISTS_LIST[instance].pl_name
                                tr_path = MAIN_LIST[instance2].tr_path.replace(
                                    MAIN_LIST[instance2].tr_path.split(r'\\')[-1], line)
                                ACTIVE_LIST.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
            file.close()
            break
    if len(ACTIVE_LIST) == 0:
        global empty
        empty = [PLAYLISTS_LIST[instance].pl_path, PLAYLISTS_LIST[instance].pl_name]
    displayPlaylist(ACTIVE_LIST)

def Save_Playlist():
    try:
        path = ACTIVE_LIST[0].pl_path
        name = ACTIVE_LIST[0].pl_name
    except IndexError:
        global empty
        path = empty[0]
        name = empty[1]

    with open(f'{path}', 'w') as file:
        file.write(f'{name}\n')
        for instance in range(len(ACTIVE_LIST)):
            filename = ACTIVE_LIST[instance].tr_path.split(r'\\')[-1]
            file.write(f'{filename}\n')
    file.close()

def Add_Tag_To_Track(tag, tree):
    ACTIVE_LIST[playlist_contents.index(playlist_contents.selection())].tr_tags.append(tag)
    tree.delete(*tree.get_children())
    for i in ACTIVE_LIST[playlist_contents.index(playlist_contents.selection())].tr_tags:
        tree.insert('', 'end', text=i)

def Add_Tag():
    w=tk.Toplevel(main_window)
    w.title('Add tags')
    w.geometry('300x200-800+400')
    tag_to_add_label=tk.Label(w, text='Tag to add:')
    current_tags=ttk.Treeview(w)
    current_tags.heading('#0', text='Current tags', anchor=tk.W)
    tag_added=tk.StringVar()
    tag_to_add=tk.Entry(w, exportselection=0, textvariable=tag_added)
    for i in ACTIVE_LIST[playlist_contents.index(playlist_contents.selection())].tr_tags:
        tree.insert('', 'end', text=i)
    add_tag_button=tk.Button(w, text='Add tag', command = lambda:Add_Tag_To_Track(tag_added, current_tags))
    tag_to_add_label.pack()
    tag_to_add.pack()
    current_tags.pack()

def Clear_Tags():
    ACTIVE_LIST[playlist_contents.index(playlist_contents.selection())].tr_tags.clear()

def Clear_All_Tags():
    for i in ACTIVE_LIST:
        ACTIVE_LIST[i].tr_tags.clear()

file_menu = tk.Menu(program_menu, tearoff=0)
file_menu.add_command(label='Add music path', command=Add_Music_Path)
file_menu.add_command(label='Clear music paths', command=Clear_Music_Paths)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=Exit)

playlist_menu = tk.Menu(program_menu, tearoff=0)
sort_menu = tk.Menu(playlist_menu, tearoff=0)
playlist_menu.add_command(label='New empty', command=New_Playlist)
playlist_menu.add_command(label='Generate', command=Generate_Playlist)
playlist_menu.add_separator()
playlist_menu.add_command(label='Load', command=Load_Playlist)
playlist_menu.add_command(label='Save', command=Save_Playlist)
playlist_menu.add_separator()
playlist_menu.add_command(label='Clear', command=New_Playlist)

library_menu = tk.Menu(program_menu, tearoff=0)

playback_menu = tk.Menu(program_menu, tearoff=0)
playback_menu.add_command(label='Play', command=lambda:Start_Playback())
playback_menu.add_command(label='Pause', command=lambda:Pause_Playback())
playback_menu.add_command(label='Stop', command=lambda:Stop_Playback())
playback_menu.add_command(label='Next track', command=lambda:Next_Track())
playback_menu.add_command(label='Previous track', command=lambda:Previous_Track())

tag_menu = tk.Menu(program_menu, tearoff=0)
tag_menu.add_command(label='Add', command=Add_Tag)
tag_menu.add_command(label='Clear', command=Clear_Tags)
tag_menu.add_command(label='Clear all', command=Clear_All_Tags)

program_menu.add_cascade(label='File', menu=file_menu)
program_menu.add_cascade(label='Playlist', menu=playlist_menu)
program_menu.add_cascade(label='Playback', menu=playback_menu)
program_menu.add_cascade(label='Library', menu=library_menu)
program_menu.add_cascade(label='Tags', menu=tag_menu)

main_window.config(menu=program_menu)

class PLAYLIST:
    def __init__(self, playlist_filename, playlist_name):
        self.pl_path = FOLDER_PATH + r'\\{}'.format(playlist_filename)
        self.pl_name = playlist_name


class SOUND_FILE(PLAYLIST):
    def __init__(self, playlist_filename, playlist_name, track_path, track_tags):
        super().__init__(playlist_filename, playlist_name)
        self.pl_path = playlist_filename
        self.pl_name = playlist_name

        self.tr_path = track_path
        self.tr_tags = track_tags


# BASE FUNCTIONS:

def createList(first):  # NEW "MAIN LIST"
    open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'w')
    library_content.delete(*library_content.get_children())
    for path in range(len(MUSIC_PATHS)):
        fileNames = os.listdir(MUSIC_PATHS[path])

        with open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'a') as dirtyFile:  # "MAIN LIST" WITH DUPLICATES
            dirtyFile.write(f'"{MUSIC_PATHS[path]}"\r')
            for filename in range(len(fileNames)):
                for checkFormat in range(len(FORMATS)):
                    isascii = lambda s: len(s) == len(s.encode())
                    if isascii(fileNames[filename]):
                        if fileNames[filename].endswith(FORMATS[checkFormat]):
                            dirtyFile.write(f'{fileNames[filename]}\r')
                            break
        dirtyFile.close()

    names = []
    tags = []
    if not first:  # COPY TAGS FROM OLD "MAIN LIST"
        with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'r') as file:
            for line in file:
                if not line.startswith('"') and not line.startswith('<'):
                    names.append(line)
                elif line.startswith('<'):
                    tags.append(line)
        file.close()

    copyTags = dict(zip(names, tags))
    del names, tags

    lines_seen = set()
    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'w') as cleanFile:  # "MAIN LIST" WITHOUT DUPLICATES
        for line in open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'r'):
            if line not in lines_seen:
                cleanFile.write(line)
                if not line.startswith('"'):
                    if line in copyTags:
                        cleanFile.write(copyTags[line])
                    else:
                        cleanFile.write('< >\n')
                lines_seen.add(line)
        dirtyFile.close()
    cleanFile.close()

    os.remove(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'))


def readMainList():  # READ "MAIN LIST"
    try:
        open('main.ajr', 'r')
    except IOError:
        createList(True)

    MAIN_LIST = []
    id = 0
    with open('main.ajr', 'r') as file:  # ADD TRACK
        for line in file:
            id += 1
            line = line.replace('\n', '')
            if line.startswith('"'):
                MUSIC_PATH = line.replace('"', '')
            else:
                if not line.startswith('<'):
                    pl_path = FOLDER_PATH + r'\\{}'.format('main.ajr')
                    pl_name = '"All Songs"'
                    tr_path = MUSIC_PATH + r'\\{}'.format(line)
                    library_content.insert('', id, text=line)
                else:
                    tr_tags = []
                    if not line.startswith('< >'):
                        for tag in readTags(line):
                            tr_tags.append(tag.split(':')[0])
                    MAIN_LIST.append(SOUND_FILE(pl_path, pl_name, tr_path, tr_tags))
    file.close()

    return MAIN_LIST


def readTags(line):  # READ TAGS
    line = line.split()
    del line[0], line[-1]
    return line


def searchForTags(inList, toFind, tree):  # SEARCH ENGINE
    global tags
    tree.delete(*tree.get_children())
    results = []
    id = 0
    for instance in range(len(inList)):
        if set(toFind).issubset(inList[instance].tr_tags):
            results.append(inList[instance])
    tags = results
    for i in results:
        id += 1
        tree.insert('', id, text=i)


def readPlaylists():  # READ PLAYLIST NAMES
    PLAYLISTS_LIST = []
    fileNames = os.listdir(FOLDER_PATH)

    for filename in range(len(fileNames)):
        if fileNames[filename].startswith('playlist') and fileNames[filename].endswith('.ajr'):
            with open(FOLDER_PATH + r'\\{}'.format(fileNames[filename]), 'r') as file:
                pl_name = file.readline().replace('\n', '')
            file.close()
            pl_path = fileNames[filename]
            PLAYLISTS_LIST.append(PLAYLIST(pl_path, pl_name))

    return PLAYLISTS_LIST


def displayPlaylist(givenList):  # PRINT PLAYLIST
    id = 0
    playlist_contents.delete(*playlist_contents.get_children())
    for instance in range(len(givenList)):
        try:
            id+=1
            track_filename = givenList[instance].tr_path.split(r'\\')[-1]
            name = '{}'.format(track_filename.replace('.{}'.format(track_filename.split('.')[-1]), ''))
            playlist_contents.insert('', id, text='', values=('Artist',name,'Duration'))

        except IndexError:
            break

def bDown(event):
    global sellib
    tv = event.widget
    if tv.identify_row(event.y) not in tv.selection():
        tv.selection_set(tv.identify_row(event.y))
    sellib = tv.selection()

def bUp(event):
    global playlist_contents, library_content, sellib
    tv = event.widget
    try:
        pl_path = ACTIVE_LIST[0].pl_path
        pl_name = ACTIVE_LIST[0].pl_name
    except IndexError:
        global empty
        pl_path = empty[0]
        pl_name = empty[1]

    if library_content.item(sellib, 'text') != '':
        ACTIVE_LIST.append(SOUND_FILE(pl_path, pl_name, library_content.item(sellib, 'text'), ''))
        displayPlaylist(ACTIVE_LIST)

def bMove(event):
    tv = event.widget
    moveto = tv.index(tv.identify_row(event.y))
    for s in tv.selection():
        tv.move(s, '', moveto)


library_content.bind("<ButtonPress-1>",bDown)
library_content.bind("<ButtonRelease-1>",bUp, add='+')
playlist_contents.bind("<B1-Motion>",bMove, add='+')

# DERIVATIVE FUNCTIONS:

def sortPlaylist(how, playlist):  # SORT LIST
    if how == 'ALPHA':
        alphabet = []

        for instance in range(len(playlist)):
            alphabet.append(playlist[instance].tr_path.split(r'\\')[-1])

        alphabet.sort()

        for instance in range(len(alphabet)):
            for instance2 in range(len(playlist)):
                if alphabet[instance] == playlist[instance2].tr_path.split(r'\\')[-1]:
                    alphabet[instance] = playlist[instance2]
                    break

        sortedPlaylist = alphabet

    elif how == 'FORMAT':
        format = []

        for instance in range(len(FORMATS)):
            for instance2 in range(len(playlist)):
                if '.{}'.format(playlist[instance2].tr_path.split(r'\\')[-1].split('.')[-1]) == FORMATS[instance]:
                    format.append(playlist[instance2])

        sortedPlaylist = format

    elif how == 'FOLDER':
        MUSIC_PATHS.sort()

        createList(False)
        MAIN_LIST = readMainList()
        sortedPlaylist = MAIN_LIST

    playlist = sortedPlaylist
    displayPlaylist(playlist)


def findTags():  # FIND NEW TAGS ON THE INTERNET
    # for instance in range(len(MAIN_LIST)):
    # tags = ## DOWNLOAD TAGS
    # addTag([MAIN_LIST[instance].tr_path.split(r'\\')[-1]], tags, 0)

    # SIMULATED TAGS

    MAIN_LIST[0].tr_tags = ['2']
    MAIN_LIST[1].tr_tags = ['1', '2']
    MAIN_LIST[2].tr_tags = ['3']
    MAIN_LIST[3].tr_tags = ['3', '1', '2']


def addTag(tracks_filenames, tags, indicator):  # ADD NEW TAGS
    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'r') as file:
        contents = file.readlines()
    file.close()

    for filename in tracks_filenames:
        for instance in range(len(contents)):
            if contents[instance].replace('\n', '') == filename:
                for tag in tags:
                    if f'{tag}:' not in contents[instance + 1]:
                        contents[instance + 1] = contents[instance + 1].replace('>', f'{tag}:{indicator} >')

    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'w') as file:
        file.writelines(contents)
    file.close()


def removeTag(tracks_filenames, tags):  # REMOVE TAGS
    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'r') as file:
        contents = file.readlines()
    file.close()

    for filename in tracks_filenames:
        for instance in range(len(contents)):
            if contents[instance].replace('\n', '') == filename:
                for tag in tags:
                    if f'{tag}:' in contents[instance + 1]:
                        contents[instance + 1] = contents[instance + 1].replace(f'{tag}:0 ', '')

    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'w') as file:
        file.writelines(contents)
    file.close()


def createPlaylist(tag):  # NEW PLAYLIST
    if tag != '':
        if tag != 'EMPTY':
            RESULTS = searchForTags(MAIN_LIST, [tag])
        else:
            RESULTS = searchForTags(MAIN_LIST, [None])

    else:
        RESULTS = searchForTags(MAIN_LIST, [])

    if not RESULTS and tag == '':
        print("Nothing found!")
    else:
        name = input("Please enter your playlist's name: ").upper()

        for instance in range(len(PLAYLISTS_LIST)):
            while True:
                if f'"{name}"' == PLAYLISTS_LIST[instance].pl_name:
                    name = input("Choose another name: ").upper()
                    continue
                else:
                    break

        counter = 0
        while os.path.isfile(FOLDER_PATH + r'\\playlist{}.ajr'.format(counter)):
            counter += 1

        with open(FOLDER_PATH + r'\\playlist{}.ajr'.format(counter), 'w') as file:
            file.write(f'"{name}"\n')
            for result in RESULTS:
                result = result.tr_path.split(r'\\')[-1]
                file.write(f'{result}\n')
        file.close()


def choosePlaylist(playlist_name):  # CHANGE PLAYLISTS
    activeList = ACTIVE_LIST

    if playlist_name == 'ALL':
        activeList = MAIN_LIST

    else:
        for instance in range(len(PLAYLISTS_LIST)):
            if playlist_name == PLAYLISTS_LIST[instance].pl_name:
                path = PLAYLISTS_LIST[instance].pl_path
                activeList = []

                with open(f'{path}', 'r') as file:
                    for line in file:
                        line = line.replace('\n', '')

                        if not line.startswith('"'):
                            for instance2 in range(len(MAIN_LIST)):
                                if line == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                    pl_path = PLAYLISTS_LIST[instance].pl_path
                                    pl_name = playlist_name
                                    tr_path = MAIN_LIST[instance2].tr_path.replace(
                                        MAIN_LIST[instance2].tr_path.split(r'\\')[-1], line)
                                    activeList.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
                file.close()
                break

        if len(activeList) == 0:
            global empty
            empty = [PLAYLISTS_LIST[instance].pl_path, PLAYLISTS_LIST[instance].pl_name]

    return activeList

def removeFromPlaylist(file):  # REMOVE FROM PLAYLIST
    for instance in range(len(ACTIVE_LIST)):
        if file.tr_path == ACTIVE_LIST[instance].tr_path:
            ACTIVE_LIST.remove(ACTIVE_LIST[instance])
            break

def deletePlaylist(playlists_filenames):  # DELETE PLAYLIST
    for filename in playlists_filenames:
        path = FOLDER_PATH + r'\\{}'.format(filename)
        os.remove(f'{path}')

def Remove_From_Playlist(event):
    enum=0
    global empty
    empty = [ACTIVE_LIST[0].pl_path, ACTIVE_LIST[0].pl_name]

    for i in playlist_contents.selection():
        removeFromPlaylist(ACTIVE_LIST[playlist_contents.index(i)-enum])
        enum += 1

    displayPlaylist(ACTIVE_LIST)

def Remove_From_Playlist2():
    enum=0
    global empty
    empty = [ACTIVE_LIST[0].pl_path, ACTIVE_LIST[0].pl_name]

    for i in playlist_contents.selection():
        removeFromPlaylist(ACTIVE_LIST[playlist_contents.index(i)-enum])
        enum += 1

    displayPlaylist(ACTIVE_LIST)

def Refresh_Library():
    createList(True)
    readMainList()

playlist_contents.bind("<KeyPress-Delete>", Remove_From_Playlist)
sort_menu.add_command(label="Alphabetically", command=lambda:sortPlaylist('ALPHA', ACTIVE_LIST))
sort_menu.add_command(label="By format", command=lambda:sortPlaylist('FORMAT', ACTIVE_LIST))
sort_menu.add_command(label="By folder", command=lambda:sortPlaylist('FOLDER', ACTIVE_LIST))
playlist_menu.add_cascade(label='Sort', menu=sort_menu)
library_menu.add_command(label='Refresh', command=Refresh_Library)
popup_menu=tk.Menu(main_window, tearoff=0)
popup_menu.add_command(label='Remove', command=Remove_From_Playlist2)

def Context_Menu(event):
    try:
        popup_menu.tk_popup(event.x_root, event.y_root)
    finally:
        popup_menu.grab_release()

playlist_contents.bind("<Button-3>", Context_Menu)

def startup():
    global MAIN_LIST, PLAYLISTS_LIST, ACTIVE_LIST
    MAIN_LIST = readMainList()
    PLAYLISTS_LIST = readPlaylists()
    try:
        ACTIVE_LIST = choosePlaylist(PLAYLISTS_LIST[0].pl_name)
    except IndexError:
        ACTIVE_LIST = MAIN_LIST

    displayPlaylist(ACTIVE_LIST)

def pygameeventloop():
    global playback_button_pressed, changed_volume, current_volume
    while True:
        if(changed_volume != current_volume.get()):
            Change_Volume(current_volume.get())
            changed_volume=current_volume.get()
        for event in pygame.event.get():
            if event.type == SONG_END:
                if(playback_button_pressed==0):
                    Next_Track()
                else:
                    playback_button_pressed = 0

startup()

threading._start_new_thread(pygameeventloop,())

main_window.mainloop()
