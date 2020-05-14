from pygame import mixer
import tkinter as tk
import os
import sys

main_window = tk.Tk()
main_window.geometry("1280x720")
main_window.title("AIaudio")
mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']
cursor = 0
paused = 0

global FOLDER_PATH, MUSIC_PATHS, MAIN_LIST, PLAYLISTS_LIST, ACTIVE_LIST
FOLDER_PATH = r'C:\\Users\\jasie\\source\\repos\\TeamProject\\TeamProject'
MUSIC_PATHS = [r'C:\\Users\\jasie\\source\\repos\\TeamProject\\TeamProject',
               r'C:\\Users\\jasie\\source\\repos\\TeamProject']
MAIN_LIST = PLAYLISTS_LIST = ACTIVE_LIST = []

def Start_Playback():
    global MAIN_LIST, cursor, paused
    if paused:
        mixer.music.unpause()
        paused = 0
    else:
        mixer.music.stop()
        mixer.music.load(MAIN_LIST[cursor].tr_path)
        mixer.music.play()

def Pause_Playback():
    mixer.music.pause()
    paused=1

def Stop_Playback():
    mixer.music.stop()

def Set_Volume(volume):
    mixer.music.set_volume(volume)

def Next_Track():
    global cursor
    cursor += 1
    mixer.music.stop()
    if not cursor < len(MAIN_LIST):
        cursor = 0
    mixer.music.load(MAIN_LIST[cursor].tr_path)
    mixer.music.play()

def Previous_Track():
    global cursor
    cursor-=1
    if not 0 <= cursor:
        cursor = 0
    mixer.music.stop()
    mixer.music.load(MAIN_LIST[cursor].tr_path)
    mixer.music.play()

#Start_Playback("music1.ogg")

program_menu = tk.Menu(main_window)

library_string=tk.StringVar()
playlist_string=tk.StringVar()

file_menu = tk.Menu(program_menu, tearoff=0)
file_menu.add_command(label='Open')
file_menu.add_separator()
file_menu.add_command(label='Add folder')

edit_menu = tk.Menu(program_menu, tearoff=0)
edit_menu.add_command(label='Undo')
edit_menu.add_command(label='Redo')
edit_menu.add_separator()
edit_menu.add_command(label='Clear')
edit_menu.add_command(label='Sort')

playback_menu = tk.Menu(program_menu, tearoff=0)
playback_menu.add_command(label='Play')
playback_menu.add_command(label='Pause')
playback_menu.add_command(label='Stop')
playback_menu.add_command(label='Next track')
playback_menu.add_command(label='Previous track')

library_menu = tk.Menu(program_menu, tearoff=0)
library_menu.add_command(label='Search')
library_menu.add_separator()
library_menu.add_command(label='Configure')

program_menu.add_cascade(label='File', menu=file_menu)
program_menu.add_cascade(label='Edit', menu=edit_menu)
program_menu.add_cascade(label='Playback', menu=playback_menu)
program_menu.add_cascade(label='Library', menu=library_menu)

main_window.config(menu=program_menu)

music_library = tk.LabelFrame(main_window, text="Music library")
music_library.grid(column=0, row=0, rowspan=3, sticky=tk.NW)
 
library_content = tk.Label(music_library, anchor=tk.NW, justify=tk.LEFT, textvariable=library_string, height=32, width=60)
library_content.grid(column=0, row=1, rowspan=2, sticky=tk.NW)

visualization = tk.LabelFrame(main_window, text="Visualization")
visualization.grid(column=0, columnspan=7, row=3, rowspan=2, sticky=tk.NW)
 
visualization_inside = tk.Label(visualization, anchor=tk.NW, justify=tk.LEFT, text=" ", height=15, width=182)
visualization_inside.grid(column=0, columnspan=7, row=4, sticky=tk.NW)

playlist_widget = tk.LabelFrame(main_window, text="Playlist")
playlist_widget.grid(column=1, columnspan=6, row=1, rowspan=2, sticky=tk.NW)
 
playlist_contents = tk.Label(playlist_widget, anchor=tk.NW, justify=tk.LEFT, textvariable=playlist_string, height=32, width=80)
playlist_contents.grid(column=1, columnspan=6, row=1, rowspan=2, sticky=tk.NW)

track_info = tk.LabelFrame(main_window, text="Track details")
track_info.grid(column=6, row=1, rowspan=2, sticky=tk.NW)
 
track_info_contents = tk.Label(track_info, anchor=tk.NW, justify=tk.LEFT, text="\tFilename\tExample filename.mp3\n\tDuration\t\t4:20\n\tSample rate\t44.1 kHz\n\tChannels\t2\n\tCodec\t\tMP3\n\tBitrate\t\t320kbps", height=32, width=60)
track_info_contents.grid(column=6, row=1, rowspan=2, sticky=tk.NW)

play_button=tk.Button(main_window, text='Play', width=8, height=1, command = lambda:Start_Playback())
pause_button=tk.Button(main_window, text='Pause', width=8, height=1, command = lambda:Pause_Playback())
stop_button=tk.Button(main_window, text='Stop', width=8, height=1, command = lambda:Stop_Playback())
previous_button=tk.Button(main_window, text='Previous', width=8, height=1, command = lambda:Previous_Track())
next_button=tk.Button(main_window, text='Next', width=8, height=1, command = lambda:Next_Track())

play_button.grid(column=1, row=2)
pause_button.grid(column=2, row=2)
stop_button.grid(column=3, row=2)
previous_button.grid(column=4, row=2)
next_button.grid(column=5, row=2)

main_window.columnconfigure(0, minsize=420)
main_window.columnconfigure(1, minsize=80)
main_window.columnconfigure(2, minsize=80)
main_window.columnconfigure(3, minsize=80)
main_window.columnconfigure(4, minsize=80)
main_window.columnconfigure(5, minsize=80)
main_window.columnconfigure(6, minsize=400)
main_window.rowconfigure(1, minsize=440)
main_window.rowconfigure(2, minsize=20)
main_window.rowconfigure(4, minsize=240)



class PLAYLIST:
    def __init__(self, playlist_filename, playlist_name):
        self.pl_filename = playlist_filename
        self.pl_name = playlist_name


class SOUND_FILE(PLAYLIST):
    def __init__(self, playlist_filename, playlist_name, track_path, track_tags):
        super().__init__(playlist_filename, playlist_name)
        self.pl_filename = playlist_filename
        self.pl_name = playlist_name

        self.tr_path = track_path.replace('*', '.')
        track_filename = track_path.split(r'\\')[-1]
        self.tr_name = track_filename.split('.')[0].replace('*', '.')
        self.tr_format = '.{}'.format(track_filename.split('.')[1])
        self.tr_tags = track_tags


# BASE FUNCTIONS

def createList():  # NEW "MAIN LIST"
    open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'w')
    for path in range(len(MUSIC_PATHS)):
        fileNames = os.listdir(MUSIC_PATHS[path])

        with open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'a') as dirtyFile:  # "MAIN LIST" WITH DUPLICATES
            dirtyFile.write(f'"{MUSIC_PATHS[path]}"\r')
            for filename in range(len(fileNames)):
                for checkFormat in range(len(FORMATS)):
                    isascii = lambda s: len(s) == len(s.encode())
                    if isascii(fileNames[filename]):
                        if fileNames[filename].endswith(FORMATS[checkFormat]):
                            dirtyFile.write('{}\r'.format(
                                fileNames[filename].replace('.', '*', fileNames[filename].count('.') - 1)))
                            break
        dirtyFile.close()

    lines_seen = set()
    with open(FOLDER_PATH + r'\\{}'.format('main.ajr'), 'w') as cleanFile:  # "MAIN LIST" WITHOUT DUPLICATES
        for line in open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'r'):
            if line not in lines_seen:
                cleanFile.write(line)
                lines_seen.add(line)
        dirtyFile.close()
    cleanFile.close()

    os.remove(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'))


def openList():  # OPEN "MAIN LIST"
    try:
        open('main.ajr', 'r')
    except IOError:
        createList()

    MAIN_LIST = []
    temp_str="\t"

    with open('main.ajr', 'r') as file:  # ADD TRACK
        for line in file:
            line = line.replace('\n', '')
            if line.startswith('"'):
                MUSIC_PATH = line.replace('"', '')
            else:
                pl_path = FOLDER_PATH + r'\\{}'.format('main.ajr')
                pl_name = '"All Songs"'
                tr_path = MUSIC_PATH + r'\\{}'.format(line)
                temp_str=temp_str+"\n\t"+line
                MAIN_LIST.append(SOUND_FILE(pl_path, pl_name, tr_path, []))
    file.close()

    library_string.set(temp_str)
    MAIN_LIST[0].tr_tags = ['2']  # ADD TAGS
    MAIN_LIST[1].tr_tags = ['1', '2']
    MAIN_LIST[2].tr_tags = ['3']
#    MAIN_LIST[3].tr_tags = ['3', '1', '2']

    return MAIN_LIST


def searchForTags(inList, toFind):  # SEARCH ENGINE
    results = []

    for instance in range(len(inList)):
        if set(toFind).issubset(inList[instance].tr_tags):
            results.append(inList[instance])
    return results


def namePlaylists():  # READ PLAYLIST NAMES
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


def displayPlaylist(givenList, cursor, scrolling):  # PRINT TRACK TITLES
    times = 5
    temp_string="\t"

    try:
        print(ACTIVE_LIST[0].pl_name)
    except IndexError:
        print("This playlist is empty!")

    for display in range(times):
        display += scrolling

        if display == cursor:
            displayCursor = '>'
        else:
            displayCursor = ''
        
        
        try:
            print(f"{displayCursor}{givenList[display].tr_name}")
            temp_string+=f"\n\t{givenList[display].tr_name}"
            playlist_string.set(temp_string)
        except IndexError:
            break


# DERIVATIVE FUNCTIONS

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
                if FORMATS[instance] == playlist[instance2].tr_format:
                    format.append(playlist[instance2])

        sortedPlaylist = format

    elif how == 'FOLDER':
        MUSIC_PATHS.sort()

        createList()
        MAIN_LIST = openList()
        sortedPlaylist = MAIN_LIST

    return sortedPlaylist


def createPlaylist(tag):
    if tag != '':
        if tag != 'empty':
            RESULTS = searchForTags(MAIN_LIST, [tag])
        else:
            RESULTS = searchForTags(MAIN_LIST, [None])

    else:
        RESULTS = searchForTags(MAIN_LIST, [])

    if not RESULTS and tag == '':
        print("Nothing found!")
    else:
        name = input("Please enter your playlist's name: ")

        for instance in range(len(PLAYLISTS_LIST)):
            while True:
                if f'"{name}"' == PLAYLISTS_LIST[instance].pl_name:
                    name = input("Choose another name: ")
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
                file.write('{}\n'.format(result.replace('.', '*', result.count('.') - 1)))
        file.close()


def choosePlaylist(playlist_name):
    activeList = ACTIVE_LIST

    if playlist_name == 'all':
        activeList = MAIN_LIST

    else:
        for instance in range(len(PLAYLISTS_LIST)):
            if playlist_name == PLAYLISTS_LIST[instance].pl_name:
                path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)
                activeList = []

                with open(f'{path}', 'r') as file:
                    for line in file:
                        line = line.replace('\n', '')

                        if not line.startswith('"'):
                            for instance2 in range(len(MAIN_LIST)):
                                if line.replace('*', '.') == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                    pl_path = PLAYLISTS_LIST[instance].pl_filename
                                    pl_name = playlist_name
                                    tr_path = MAIN_LIST[instance2].tr_path.replace(
                                        MAIN_LIST[instance2].tr_path.split(r'\\')[-1], line)
                                    activeList.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
                file.close()
                break
    return activeList


def savePlaylist():
    path = FOLDER_PATH + r'\\{}'.format(ACTIVE_LIST[0].pl_filename)

    with open(f'{path}', 'w') as file:
        file.write(f'{ACTIVE_LIST[0].pl_name}\n')
        for instance in range(len(ACTIVE_LIST)):
            filename = ACTIVE_LIST[instance].tr_path.split(r'\\')[-1]
            file.write('{}\n'.format(filename.replace('.', '*', filename.count('.') - 1)))
    file.close()


def addToPlaylist(playlists_filenames, tracks_filenames):
    for filename in playlists_filenames:
        path = FOLDER_PATH + r'\\{}'.format(filename)

        for filename2 in tracks_filenames:
            with open(f'{path}', 'r+') as file:
                for line in file:
                    if line.startswith('"'):
                        continue
                    elif filename2 in line:
                        break
                else:
                    file.write('{}\n'.format(filename2.replace('.', '*', filename2.count('.') - 1)))
            file.close()


def removeFromPlaylist(playlist_filename, tracks_filenames):
    path = FOLDER_PATH + r'\\{}'.format(playlist_filename)

    with open(f'{path}', 'r') as file:
        file_lines = file.readlines()
    file.close()

    for filename in tracks_filenames:
        for line in file_lines:
            if line.replace('\n', '').replace('*', '.') == filename:
                file_lines.remove(line)

    with open('{}'.format(path), 'w') as file:
        for line in file_lines:
            file.write(line)
    file.close()


def deletePlaylist(playlists_filenames):
    for filename in playlists_filenames:
        path = FOLDER_PATH + r'\\{}'.format(filename)
        os.remove(f'{path}')


def refresh():  # LOAD PLAYLIST AGAIN
    global MAIN_LIST, PLAYLISTS_LIST
    createList()
    MAIN_LIST = openList()
    PLAYLISTS_LIST = namePlaylists()

    if not ACTIVE_LIST:
        pass

    else:
        if ACTIVE_LIST[0].pl_name == '"All Songs"':
            activeList = MAIN_LIST

        else:
            pl_name = ACTIVE_LIST[0].pl_name
            activeList = []

            for instance in range(len(PLAYLISTS_LIST)):
                if pl_name == PLAYLISTS_LIST[instance].pl_name:
                    path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)

                    with open(f'{path}', 'r') as file:
                        for line in file:
                            line = line.replace('\n', '')

                            if not line.startswith('"'):
                                for instance2 in range(len(MAIN_LIST)):
                                    if line.replace('*', '.') == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                        pl_path = PLAYLISTS_LIST[instance].pl_filename
                                        tr_path = MAIN_LIST[instance2].tr_path.replace(
                                            MAIN_LIST[instance2].tr_path.split(r'\\')[-1], line)
                                        activeList.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
                                        break
                    file.close()
                    break

        return activeList


def menu(start):
    if start:
        global MAIN_LIST, PLAYLISTS_LIST, ACTIVE_LIST, cursor, scrolling
        MAIN_LIST = openList()
        PLAYLISTS_LIST = namePlaylists()
        ACTIVE_LIST = MAIN_LIST

        scrolling = 0

    if not 0 <= cursor < len(ACTIVE_LIST):
        cursor = 0 + scrolling

    print("\n***")
    displayPlaylist(ACTIVE_LIST, cursor, scrolling)

    choice = input("\nPlease enter your choice: ").upper()

    if choice == 'UP' and ACTIVE_LIST:  # CHANGE TRACK POSITION
        if not cursor - 1 < 0:
            ACTIVE_LIST[cursor], ACTIVE_LIST[cursor - 1] = ACTIVE_LIST[cursor - 1], ACTIVE_LIST[cursor]
        menu(False)

    elif choice == 'DOWN' and ACTIVE_LIST:
        if not cursor + 1 > len(ACTIVE_LIST) - 1:
            ACTIVE_LIST[cursor], ACTIVE_LIST[cursor + 1] = ACTIVE_LIST[cursor + 1], ACTIVE_LIST[cursor]
        menu(False)

    elif choice == 'CUP' and ACTIVE_LIST:  # MOVE "SELECTED TRACK"
        cursor -= 1
        if not scrolling <= cursor:
            cursor = 4 + scrolling
        menu(False)

    elif choice == 'CDOWN' and ACTIVE_LIST:
        cursor += 1
        if not cursor < 5 + scrolling:
            cursor = 0 + scrolling
        menu(False)

    elif choice == '5UP' and ACTIVE_LIST:  # MOVE PLAYLIST 5 UP/DOWN
        if not scrolling - 5 < 0:
            cursor -= 5
            scrolling -= 5
        menu(False)

    elif choice == '5DOWN' and ACTIVE_LIST:
        if not scrolling + 5 > len(ACTIVE_LIST) - 1:
            cursor += 5
            scrolling += 5
        menu(False)

    elif choice == 'SORTBY' and ACTIVE_LIST:
        option = input('').upper()
        if option == 'ALPHA' or 'FORMAT' or 'FOLDER':
            ACTIVE_LIST = sortPlaylist(option, ACTIVE_LIST)
        menu(False)

    elif choice == 'PLAYLIST':  # NEW PLAYLIST
        if ACTIVE_LIST[0].pl_name == '"All Songs"':
            tag = input("Search for: ")
            createPlaylist(tag)
            refresh()
        menu(False)

    elif choice == 'CHOOSE':  # CHANGE PLAYLISTS
        name = input('')
        cursor = 0
        scrolling = 0

        ACTIVE_LIST = choosePlaylist(name)
        menu(False)

    elif choice == 'SAVE' and ACTIVE_LIST:  # SAVE CHANGES TO PLAYLIST
        if ACTIVE_LIST[0].pl_name != '"All Songs"':
            savePlaylist()
        menu(False)

    elif choice == 'ADDTO' and ACTIVE_LIST:  # ADD TO PLAYLIST
        if ACTIVE_LIST[0].pl_name == '"All Songs"':
            name = input('')
            for instance in range(len(PLAYLISTS_LIST)):
                if name == PLAYLISTS_LIST[instance].pl_name:
                    addToPlaylist([PLAYLISTS_LIST[instance].pl_filename],
                                  [ACTIVE_LIST[cursor].tr_path.split(r'\\')[-1]])
                    break
        menu(False)

    elif choice == 'REMOVE' and ACTIVE_LIST:  # REMOVE FROM PLAYLIST
        if ACTIVE_LIST[0].pl_name != '"All Songs"':
            removeFromPlaylist(ACTIVE_LIST[0].pl_filename, [ACTIVE_LIST[cursor].tr_path.split(r'\\')[-1]])
            ACTIVE_LIST = refresh()
        menu(False)

    elif choice == 'DELETE' and ACTIVE_LIST:  # DELETE PLAYLIST
        if ACTIVE_LIST[0].pl_name == '"All Songs"':
            name = input('')
            for instance in range(len(PLAYLISTS_LIST)):
                if name == PLAYLISTS_LIST[instance].pl_name:
                    deletePlaylist([PLAYLISTS_LIST[instance].pl_filename])
                    refresh()
                    break
        menu(False)

    elif choice == 'REFRESH' and ACTIVE_LIST:
        cursor = 0
        scrolling = 0

        ACTIVE_LIST = refresh()
        menu(False)

    elif choice == 'PLAY' and ACTIVE_LIST:  # MUSIC PLAYER
        mixer.music.stop()
        mixer.music.load(ACTIVE_LIST[cursor].tr_path)
        mixer.music.play()
        menu(False)

    elif choice == 'STOP' and ACTIVE_LIST:
        mixer.music.stop()
        menu(False)

    elif choice == 'PAUSE' and ACTIVE_LIST:
        mixer.music.pause()
        menu(False)

    elif choice == 'UNPAUSE' and ACTIVE_LIST:
        mixer.music.unpause()
        menu(False)

    elif choice == 'NEXT' and ACTIVE_LIST:
        cursor += 1
        if not cursor < len(ACTIVE_LIST):
            cursor = 0
            scrolling = 0
        else:
            if not cursor < 5 + scrolling:
                scrolling += 5

            mixer.music.stop()
            mixer.music.load(ACTIVE_LIST[cursor].tr_path)
            mixer.music.play()
        menu(False)

    elif choice == 'PREV' and ACTIVE_LIST:
        cursor -= 1
        if not 0 <= cursor:
            cursor = 0

        mixer.music.stop()
        mixer.music.load(ACTIVE_LIST[cursor].tr_path)
        mixer.music.play()
        menu(False)

    elif choice == 'QUIT':
        sys.exit()

    else:
        menu(False)

menu(True)

main_window.mainloop()
