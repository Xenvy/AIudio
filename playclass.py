import os
from pygame import mixer
import sys

FORMATS = ['.mp3', '.wav', '.ogg', '.flac']

global FOLDER_PATH, MUSIC_PATHS
FOLDER_PATH = r'C:\\Users\\[user_name]\\PycharmProjects\\AIudio'
MUSIC_PATHS = [r'C:\\Users\\[user_name]\\PycharmProjects\\AIudio\\Music', r'C:\\Users\\[user_name]\\PycharmProjects\\AIudio\\Music2']

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


def createList():  # NEW "MAIN LIST"
    open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'w')

    for path in range(len(MUSIC_PATHS)):
        fileNames = os.listdir(MUSIC_PATHS[path])

        with open(FOLDER_PATH + r'\\{}'.format('main_raw.ajr'), 'a') as dirtyFile:  # "MAIN LIST" WITH DUPLICATES
            dirtyFile.write('"{}"\r'.format(MUSIC_PATHS[path]))
            for filename in range(len(fileNames)):
                for checkFormat in range(len(FORMATS)):
                    isascii = lambda s: len(s) == len(s.encode())
                    if isascii(fileNames[filename]):
                        if fileNames[filename].endswith(FORMATS[checkFormat]):
                            dirtyFile.write('{}\r'.format(fileNames[filename].replace('.', '*', fileNames[filename].count('.') - 1)))
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
    RESULTS = []

    for instance in range(len(inList)):
        if set(toFind).issubset(inList[instance].tr_tags):
            RESULTS.append(inList[instance])
    return RESULTS


def namePlaylists():  # READ PLAYLIST NAMES
    PLAYLIST_LIST = []
    fileNames = os.listdir(FOLDER_PATH)

    for filename in range(len(fileNames)):
        if fileNames[filename].startswith('playlist') and fileNames[filename].endswith('.ajr'):
            with open(FOLDER_PATH + r'\\{}'.format(fileNames[filename]), 'r') as file:
                pl_name = file.readline().replace('\n', '')
            file.close()
            pl_path = fileNames[filename]
            PLAYLIST_LIST.append(PLAYLIST(pl_path, pl_name))

    return PLAYLIST_LIST


def displayPlaylist(givenListName, givenList, cursor, scrolling):  # PRINT TRACK TITLES
    times = 5
    print(givenListName)
    for display in range(times):
        display += scrolling

        if display == cursor:
            displayCursor = '>'
        else:
            displayCursor = ''

        try:
            print("{}{}".format(displayCursor, givenList[display].tr_name))
        except IndexError:
            break


def menu(start):
    MAIN_LIST = openList()
    PLAYLISTS_LIST = namePlaylists()

    if start:
        global cursor, scrolling, activeList
        cursor = 0
        scrolling = 0
        activeList = MAIN_LIST

    if not 0 <= cursor < len(activeList):
        cursor = 0 + scrolling

    print("\n***")
    displayPlaylist(activeList[0].pl_name, activeList, cursor, scrolling)

    choice = input("\nPlease enter your choice: ").upper()

    if choice == 'UP':  # CHANGE TRACK POSITION
        if not cursor - 1 < 0:
            activeList[cursor], activeList[cursor - 1] = activeList[cursor - 1], activeList[cursor]
        menu(False)

    elif choice == 'DOWN':
        if not cursor + 1 > len(activeList) - 1:
            activeList[cursor], activeList[cursor + 1] = activeList[cursor + 1], activeList[cursor]
        menu(False)

    elif choice == 'CUP':  # MOVE "SELECTED TRACK"
        cursor -= 1
        if not scrolling <= cursor:
            cursor = 4 + scrolling
        menu(False)

    elif choice == 'CDOWN':
        cursor += 1
        if not cursor < 5 + scrolling:
            cursor = 0 + scrolling
        menu(False)

    elif choice == '5UP':  # MOVE PLAYLIST 5 UP/DOWN
        if not scrolling - 5 < 0:
            cursor -= 5
            scrolling -= 5
        menu(False)

    elif choice == '5DOWN':
        if not scrolling + 5 > len(activeList) - 1:
            cursor += 5
            scrolling += 5
        menu(False)

    elif choice == 'SORTBY':  # SORT LIST
        option = input('').upper()
        if option == 'ALPHA':
            alphabet = []

            for instance in range(len(activeList)):
                alphabet.append(activeList[instance].tr_path.split(r'\\')[-1])

            alphabet.sort()

            for instance in range(len(alphabet)):
                for instance2 in range(len(activeList)):
                    if alphabet[instance] == activeList[instance2].tr_path.split(r'\\')[-1]:
                        alphabet[instance] = activeList[instance2]
                        break

            activeList = alphabet

        elif option == 'FORMAT':
            format = []

            for instance in range(len(FORMATS)):
                for instance2 in range(len(activeList)):
                    if FORMATS[instance] == activeList[instance2].tr_format:
                        format.append(activeList[instance2])

            activeList = format

        elif option == 'FOLDER':
            MUSIC_PATHS.sort()

            createList()
            MAIN_LIST = openList()
            activeList = MAIN_LIST
        menu(False)

    elif choice == 'PLAYLIST':  # NEW PLAYLIST
        tag = input("Search for: ")

        if tag != '':
            RESULTS = searchForTags(MAIN_LIST, [tag])
        else:
            RESULTS = searchForTags(MAIN_LIST, [])

        if not RESULTS and tag == '':
            print("Nothing found!")
        else:
            name = input("Please enter your playlist's name: ")

            for instance in range(len(PLAYLISTS_LIST)):
                while True:
                    if '"{}"'.format(name) == PLAYLISTS_LIST[instance].pl_name:
                        name = input("Choose another name: ")
                        continue
                    else:
                        break

            counter = 0
            while os.path.isfile(FOLDER_PATH + r'\\playlist{}.ajr'.format(counter)):
                counter += 1

            with open(FOLDER_PATH + r'\\playlist{}.ajr'.format(counter), 'w') as file:
                file.write('"{}"\n'.format(name))
                for result in RESULTS:
                    result = result.tr_path.split(r'\\')[-1]
                    file.write('{}\n'.format(result.replace('.', '*', result.count('.') - 1)))
            file.close()
        menu(False)

    elif choice == 'CHOOSE':  # CHANGE PLAYLISTS
        pl_name = input('')
        cursor = 0
        scrolling = 0

        if pl_name == 'all':
            activeList = MAIN_LIST

        else:
            for instance in range(len(PLAYLISTS_LIST)):
                if pl_name == PLAYLISTS_LIST[instance].pl_name:
                    path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)
                    activeList = []

                    with open('{}'.format(path), 'r') as file:
                        for filename in file:
                            filename = filename.replace('\n', '')

                            if not filename.startswith('"'):
                                for instance2 in range(len(MAIN_LIST)):
                                    if filename.replace('*', '.') == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                        pl_path = PLAYLISTS_LIST[instance].pl_filename
                                        tr_path = MAIN_LIST[instance2].tr_path.replace(MAIN_LIST[instance2].tr_path.split(r'\\')[-1], filename)
                                        activeList.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
                    file.close()
                    break
        menu(False)

    elif choice == 'SAVE':  # SAVE CHANGES TO PLAYLIST
        if activeList[0].pl_name != '"All Songs"':
            path = FOLDER_PATH + r'\\{}'.format(activeList[0].pl_filename)

            with open('{}'.format(path), "w") as file:
                file.write('{}\n'.format(activeList[0].pl_name))
                for line in range(len(activeList)):
                    file.write('{}\n'.format(activeList[line].tr_path.split(r'\\')[-1]))
            file.close()
        menu(False)

    elif choice == 'ADDTO':  # ADD TO PLAYLIST
        name = input('')
        for instance in range(len(PLAYLISTS_LIST)):
            if name == PLAYLISTS_LIST[instance].pl_name:
                path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)

                with open('{}'.format(path), 'r+') as file:
                    for line in file:
                        if activeList[cursor].tr_name in line:
                            break
                    else:
                        file.write('{}\n'.format(activeList[cursor].tr_path.split(r'\\')[-1]))
                file.close()
        menu(False)

    elif choice == 'REMOVE':  # REMOVE FROM PLAYLIST
        name = input('')
        for instance in range(len(PLAYLISTS_LIST)):
            if name == PLAYLISTS_LIST[instance].pl_name:
                path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)

                with open('{}'.format(path), 'r') as file:
                    file_lines = file.readlines()
                file.close()

                with open('{}'.format(path), 'w') as file:
                    for line in file_lines:
                        if line.strip('\n') != activeList[cursor].tr_path.split(r'\\')[-1]:
                            file.write(line)
                file.close()
        menu(False)

    elif choice == 'DELETE':  # DELETE PLAYLIST
        name = input('')
        for instance in range(len(PLAYLISTS_LIST)):
            if name == PLAYLISTS_LIST[instance].pl_name:
                path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)
                os.remove('{}'.format(path))
                break
        menu(False)

    elif choice == 'REFRESH':  # LOAD PLAYLIST AGAIN
        cursor = 0
        scrolling = 0

        if activeList[0].pl_name == '"All Songs"':
            createList()
            MAIN_LIST = openList()
            activeList = MAIN_LIST

        else:
            pl_name = activeList[0].pl_name
            for instance in range(len(PLAYLISTS_LIST)):
                if pl_name == PLAYLISTS_LIST[instance].pl_name:
                    path = FOLDER_PATH + r'\\{}'.format(PLAYLISTS_LIST[instance].pl_filename)
                    activeList = []

                    with open('{}'.format(path), 'r') as file:
                        for filename in file:
                            filename = filename.replace('\n', '')

                            if not filename.startswith('"'):
                                for instance2 in range(len(MAIN_LIST)):
                                    if filename == MAIN_LIST[instance2].tr_path.split(r'\\')[-1]:
                                        pl_path = PLAYLISTS_LIST[instance].pl_filename
                                        tr_path = MAIN_LIST[instance2].tr_path
                                        activeList.append(SOUND_FILE(pl_path, pl_name, tr_path, None))
                    file.close()
                    break
        menu(False)

    elif choice == 'PLAY':  # MUSIC PLAYER
        mixer.music.stop()
        mixer.music.load(activeList[cursor].tr_path)
        mixer.music.play()
        menu(False)

    elif choice == 'STOP':
        mixer.music.stop()
        menu(False)

    elif choice == 'PAUSE':
        mixer.music.pause()
        menu(False)

    elif choice == 'UNPAUSE':
        mixer.music.unpause()
        menu(False)

    elif choice == 'NEXT':
        cursor += 1
        if not cursor < len(activeList):
            cursor = 0
            scrolling = 0
        else:
            if not cursor < 4 + scrolling:
                scrolling += 5
            mixer.music.stop()
            mixer.music.load(activeList[cursor].tr_path)
            mixer.music.play()
        menu(False)

    elif choice == 'PREV':
        cursor -= 1
        if not 0 <= cursor:
            cursor = 0
        mixer.music.stop()
        mixer.music.load(activeList[cursor].tr_path)
        mixer.music.play()
        menu(False)

    elif choice == 'QUIT':
        sys.exit()

    else:
        menu(False)


menu(True)
