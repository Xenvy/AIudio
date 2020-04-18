import os
import sys

MUSIC_PATH = r"C:\\Users\\[user_name]\\PycharmProjects\\Aludio\\Music"
FOLDER_PATH = r"C:\\Users\\[user_name]\\PycharmProjects\\Aludio"
FORMATS = ['.mp3', '.wav', '.ogg', '.flac']


def createList():  # NEW "MAIN LIST"
    fileNames = os.listdir(MUSIC_PATH)

    with open('main.txt', 'w') as file:
        for line in range(len(fileNames)):
            for checkFormat in range(len(FORMATS)):
                if fileNames[line].endswith(FORMATS[checkFormat]):
                    file.write("{}\r".format(fileNames[line]))
    file.close()


def openList():  # OPEN "MAIN LIST"
    try:
        open('main.txt', 'r')
    except IOError:
        createList()

    main_names = []
    main_tags = []

    with open('main.txt', 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            main_names.append(line)
    file.close()

    for name in range(len(main_names)):  # ADD TAGS
        main_tags.append([])

    main_tags[0] = ['2']
    main_tags[1] = ['1', '2']
    main_tags[2] = ['3']
    main_tags[3] = ['3', '1', '2']

    MAIN_LIST = dict(zip(main_names, main_tags))
    return MAIN_LIST


def searchForTags(searchedDictionary, valueToFind):  # SEARCH ENGINE
    keys = []
    items = searchedDictionary.items()

    for item in items:
        if set(valueToFind).issubset(item[1]):
            keys.append(item[0])
    return keys


def namePlaylists():  # READ PLAYLIST NAMES
    fileNames = os.listdir(FOLDER_PATH)
    pl_path = []
    pl_name = []

    for line in range(len(fileNames)):
        if bool([check_format for check_format in ['txt'] if (check_format in fileNames[line])]) \
                and fileNames[line].startswith('playlist'):
            pl_path.append(fileNames[line])

    for path in pl_path:
        with open('{}'.format(path), 'r') as file:
            name = file.readline().replace('\n', '')
            pl_name.append(name)
        file.close()
        
    PLAYLIST_LIST = dict(zip(pl_name, pl_path))
    return PLAYLIST_LIST


def displayPlaylist(givenListName, givenList, scrolling):  # PRINT TRACK TITLES
    times = 5
    print(givenListName)
    for display in range(times):
        try:
            print("{}".format(givenList[display+scrolling]))
        except IndexError:
            break


def menu(start):
    MAIN_LIST = openList()
    PLAYLISTS_LIST = namePlaylists()

    if start:
        global cursor, scrolling, activeListName, activeList
        cursor = 0
        scrolling = 0
        activeListName = '"All Songs"'
        activeList = list(MAIN_LIST.keys())

    if not (cursor < len(activeList) - 1 or cursor > 0):
        cursor = 0

    print("\n***\n")

    print("CURSOR = {}\n".format(cursor))
    displayPlaylist(activeListName, activeList, scrolling)

    choice = input("Please enter your choice: ").upper()

    if choice == 'UP':  # CHANGE TRACK POSITION
        if not cursor - 1 < 0:
            activeList[cursor],  activeList[cursor - 1] = activeList[cursor - 1],  activeList[cursor]
        menu(False)

    elif choice == 'DOWN':
        if not cursor + 1 > len(activeList) - 1:
            activeList[cursor],  activeList[cursor + 1] = activeList[cursor + 1],  activeList[cursor]
        menu(False)

    elif choice == 'CUP':  # MOVE "SELECTED TRACK"
        cursor -= 1
        menu(False)

    elif choice == 'CDOWN':
        cursor += 1
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

    elif choice == 'NEWLIST':  # SCAN FOLDER
        createList()
        menu(False)

    elif choice == 'PLAYLIST':  # NEW PLAYLIST
        tag = input("Search for: ")
        result = searchForTags(MAIN_LIST, [tag])

        if tag == '':
            result = searchForTags(MAIN_LIST, [])

        if not result and not tag == '':
            print("Nothing found!")

        else:
            name = input("Please enter your playlist's name: ")

            counter = 0
            while os.path.isfile('playlist{}.txt'.format(counter)):
                counter += 1

            with open('playlist{}.txt'.format(counter), 'w') as file:
                file.write('"{}"\n'.format(name))
                for line in result:
                    file.write('{}\n'.format(line))
            file.close()
        menu(False)

    elif choice == 'CHOOSE':  # CHANGE PLAYLISTS
        name = input('')

        if name == 'all':
            activeListName = '"All Songs"'
            activeList = list(MAIN_LIST.keys())

        elif name in PLAYLISTS_LIST.keys():
            activeList = []
            path = PLAYLISTS_LIST.get(name)

            with open('{}'.format(path), 'r') as file:
                for line in file:
                    line = line.replace('\n', '')

                    if line.startswith('"'):
                        activeListName = line

                    else:
                        activeList.append(line)
            file.close()
        menu(False)

    elif choice == 'SAVE':  # SAVE CHANGES TO PLAYLIST
        if activeListName != '"All Songs"':
            path = PLAYLISTS_LIST[activeListName]

            with open('{}'.format(path), "w") as file:
                file.write('{}\n'.format(activeListName))
                for line in range(len(activeList)):
                    file.write('{}\n'.format(activeList[line]))
            file.close()
        menu(False)

    elif choice == 'ADDTO':  # ADDS TO PLAYLIST
        name = input('')
        if name in PLAYLISTS_LIST.keys():
            path = PLAYLISTS_LIST.get(name)

            with open('{}'.format(path), 'r+') as file:

                for line in file:
                    if activeList[cursor] in line:
                        break

                else:
                    file.write('{}\n'.format(activeList[cursor]))
            file.close()
        menu(False)

    elif choice == 'REMOVE':  # REMOVE FROM PLAYLIST
        name = input('')
        if name in PLAYLISTS_LIST.keys():
            path = PLAYLISTS_LIST.get(name)

            with open('{}'.format(path), 'r') as file:
                lines = file.readlines()
            file.close()

            with open('{}'.format(path), 'w') as file:
                for line in lines:
                    if line.strip('\n') != activeList[cursor]:
                        file.write(line)
            file.close()
        menu(False)

    elif choice == 'DELETE':  # DELETE PLAYLIST
        name = input('')
        if name in PLAYLISTS_LIST.keys():
            path = PLAYLISTS_LIST.get(name)
            os.remove('{}'.format(path))
        menu(False)

    elif choice == 'REFRESH':  # LOAD PLAYLIST AGAIN
        if activeListName == '"All Songs"':
            activeList = list(MAIN_LIST.keys())

        else:
            name = activeListName
            if name in PLAYLISTS_LIST.keys():
                activeList = []
                path = PLAYLISTS_LIST.get(name)

                with open('{}'.format(path), 'r') as file:
                    for line in file:
                        line = line.replace('\n', '')

                        if not line.startswith('"'):
                            activeList.append(line)
        menu(False)

    elif choice == 'QUIT':
        sys.exit()

    else:
        menu(False)


menu(True)
