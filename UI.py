from pygame import mixer
import tkinter as tk

main_window = tk.Tk()
main_window.geometry("1280x720")
main_window.title("AIaudio")
mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def Start_Playback(filepath):
    mixer.music.load(filepath)
    mixer.music.play()

def Pause_Playback():
    mixer.music.pause()

def Unpause_Playback():
    mixer.music.unpause()

def Stop_Playback():
    mixer.music.stop()

def Set_Volume(volume):
    mixer.music.set_volume(volume)

#Start_Playback("music1.ogg")

program_menu = tk.Menu(main_window)

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
 
library_content = tk.Label(music_library, anchor=tk.NW, justify=tk.LEFT, text="\tExample folder\n\t\t|-Example_file.mp3\n\t\t|-Example_file_2.mp3", height=32, width=60)
library_content.grid(column=0, row=1, rowspan=2, sticky=tk.NW)

visualization = tk.LabelFrame(main_window, text="Visualization")
visualization.grid(column=0, columnspan=7, row=3, rowspan=2, sticky=tk.NW)
 
visualization_inside = tk.Label(visualization, anchor=tk.NW, justify=tk.LEFT, text=" ", height=15, width=182)
visualization_inside.grid(column=0, columnspan=7, row=4, sticky=tk.NW)

playlist_widget = tk.LabelFrame(main_window, text="Playlist")
playlist_widget.grid(column=1, columnspan=6, row=1, rowspan=2, sticky=tk.NW)
 
playlist_contents = tk.Label(playlist_widget, anchor=tk.NW, justify=tk.LEFT, text="\tExample artist - Example track\n\tExample artist2 - Example track2", height=32, width=80)
playlist_contents.grid(column=1, columnspan=6, row=1, rowspan=2, sticky=tk.NW)

track_info = tk.LabelFrame(main_window, text="Track details")
track_info.grid(column=6, row=1, rowspan=2, sticky=tk.NW)
 
track_info_contents = tk.Label(track_info, anchor=tk.NW, justify=tk.LEFT, text="\tFilename\tExample filename.mp3\n\tDuration\t\t4:20\n\tSample rate\t44.1 kHz\n\tChannels\t2\n\tCodec\t\tMP3\n\tBitrate\t\t320kbps", height=32, width=60)
track_info_contents.grid(column=6, row=1, rowspan=2, sticky=tk.NW)

play_button=tk.Button(main_window, text='Play', width=8, height=1)
pause_button=tk.Button(main_window, text='Pause', width=8, height=1)
stop_button=tk.Button(main_window, text='Stop', width=8, height=1)
previous_button=tk.Button(main_window, text='Previous', width=8, height=1)
next_button=tk.Button(main_window, text='Next', width=8, height=1)

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

main_window.mainloop()
