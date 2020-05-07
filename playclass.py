import os
from pygame import mixer
import sys

FORMATS = ['.mp3', '.wav', '.ogg', '.flac']

global FOLDER_PATH, MUSIC_PATHS, MAIN_LIST, PLAYLISTS_LIST, ACTIVE_LIST
FOLDER_PATH = r'C:\\Users\\[Username]\\PycharmProjects\\AIudio'
MUSIC_PATHS = [r'C:\\Users\\[Username]\\PycharmProjects\\AIudio\\Music',
               r'C:\\Users\\[Username]\\PycharmProjects\\AIudio\\Music2']
MAIN_LIST = PLAYLISTS_LIST = ACTIVE_LIST = []

mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


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

    with open('main.ajr', 'r') as file:  # ADD TRACK
        for line in file:
            line = line.replace('\n', '')
            if line.startswith('"'):
                MUSIC_PATH = line.replace('"', '')
            else:
                pl_path = FOLDER_PATH + r'\\{}'.format('main.ajr')
                pl_name = '"All Songs"'
                tr_path = MUSIC_PATH + r'\\{}'.format(line)
                MAIN_LIST.append(SOUND_FILE(pl_path, pl_name, tr_path, []))
    file.close()

    MAIN_LIST[0].tr_tags = ['2']  # ADD TAGS
    MAIN_LIST[1].tr_tags = ['1', '2']
    MAIN_LIST[2].tr_tags = ['3']
    MAIN_LIST[3].tr_tags = ['3', '1', '2']

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

        cursor = 0
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
