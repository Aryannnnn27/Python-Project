import tkinter as tk
import tkinter.filedialog
import fnmatch
import os
from pygame import mixer

canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("791x755")
canvas.config(bg='black')

mixer.init()

# Load images
prev_img = tk.PhotoImage(file="previous.png")
stop_img = tk.PhotoImage(file="stop.png")
play_img = tk.PhotoImage(file="play.png")
pause_img = tk.PhotoImage(file="pause.png")
next_img = tk.PhotoImage(file="next.png")
volume_up_img = tk.PhotoImage(file="volume-up.png")
volume_down_img = tk.PhotoImage(file="volume-down.png")
folder_img = tk.PhotoImage(file="folder.png")

rootpath = ""
pattern = "*.mp3"
song_list = []  # Store the list of songs
current_song_index = 0  # Index of the currently playing song

# Functions
def select_folder():
    global rootpath, song_list, current_song_index
    rootpath = tk.filedialog.askdirectory()
    song_list = []  # Clear existing list
    current_song_index = 0
    listBox.delete(0, 'end')
    load_songs()

def load_songs():
    global song_list
    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            song_list.append(filename)
            listBox.insert('end', filename)

def play_music(song):
    mixer.music.load(os.path.join(rootpath, song))
    mixer.music.play()
    label.config(text=song)
    current_song_index = song_list.index(song)
    listBox.selection_clear(0, 'end')
    listBox.selection_set(current_song_index)

def play_next():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(song_list)
    next_song_name = song_list[current_song_index]
    label.config(text=next_song_name)
    play_music(next_song_name)

def play_prev():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(song_list)
    prev_song_name = song_list[current_song_index]
    label.config(text=prev_song_name)
    play_music(prev_song_name)

def play_next_direct():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(song_list)
    next_song_name = song_list[current_song_index]
    label.config(text=next_song_name)
    play_music(next_song_name)

def increase_volume():
    current_volume = mixer.music.get_volume()
    if current_volume < 1.0:
        mixer.music.set_volume(current_volume + 0.1)

def decrease_volume():
    current_volume = mixer.music.get_volume()
    if current_volume > 0.0:
        mixer.music.set_volume(current_volume - 0.1)

# UI components
listBox = tk.Listbox(canvas, fg="cyan", bg="black", width=100, font=('ds-digital', 14))
listBox.pack(padx=15, pady=15)

label = tk.Label(canvas, text='', bg='black', fg='yellow', font=('ds-digital', 18))
label.pack(pady=15)

top = tk.Frame(canvas, bg="black")
top.pack(padx=20, pady=5, anchor='center')

folderButton = tk.Button(canvas, image=folder_img, bg='black', borderwidth=0, command=select_folder)
folderButton.pack(padx=10, pady=10, in_=top, side='left')

prevButton = tk.Button(canvas, image=prev_img, bg='black', borderwidth=0, command=play_prev)
prevButton.pack(padx=10, pady=15, in_=top, side='left')

volumeDownButton = tk.Button(canvas, image=volume_down_img, bg='black', borderwidth=0, command=decrease_volume)
volumeDownButton.pack(padx=10, pady=15, in_=top, side='left')

stopButton = tk.Button(canvas, image=stop_img, bg='black', borderwidth=0, command=mixer.music.stop)
stopButton.pack(padx=10, pady=15, in_=top, side='left')

playButton = tk.Button(canvas, image=play_img, bg='black', borderwidth=0, command=lambda: play_music(song_list[current_song_index]))
playButton.pack(padx=10, pady=15, in_=top, side='left')

pauseButton = tk.Button(canvas, image=pause_img, bg='black', borderwidth=0, command=mixer.music.pause)
pauseButton.pack(padx=10, pady=15, in_=top, side='left')

volumeUpButton = tk.Button(canvas, image=volume_up_img, bg='black', borderwidth=0, command=increase_volume)
volumeUpButton.pack(padx=10, pady=15, in_=top, side='left')

nextButton = tk.Button(canvas, image=next_img, bg='black', borderwidth=0, command=play_next_direct)
nextButton.pack(padx=10, pady=15, in_=top, side='left')

canvas.mainloop()
