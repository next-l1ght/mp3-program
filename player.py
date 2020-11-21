# Creating Virtual Environment : python -m venv virt
# Activate the Virtual Environment : source virt/scripts/activate

from tkinter import *
from tkinter import filedialog
# to install pygame : pip install pygame
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x450")

# Initialiaze Pygame
pygame.mixer.init()

# Create a function with deal with time
def play_time():
	# Check to see if song is Stopped
	if stopped:
		return

	# Grab Current time song
	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert Song Time to Time formate
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Reconstruct Song With Directory Structure Stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'

	# Find Current Song Length
	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length

	# Convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
	# Set Slider to length to song length 
	# song_slider.config(to=song_length)
	# my_label.config(text=song_slider.get())
	# Cheak to See If song is Over
	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused:
		# Cheack to see if paused, is so -pass
		pass
	else:
		# Move Slider along 1 Second at a Time
		next_time = int(song_slider.get()) + 1

		# Output New Time Value To Slider and song length
		song_slider.config(to=song_length, value=next_time)
		#Convert Slider Position to Time Formate
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

		# Output Slider
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of{converted_song_length}  ')

	# my_label.config(text=converted_song_length)
	if current_time >=0:
		# Add Current Time Status Bar 
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of{converted_song_length}  ')

	# Create Loop to Check the time every second
	status_bar.after(1000, play_time)




#Create Function To Add One Song To playlist
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	# my_label.config(text=song)
	
	# Strip out direcory structur and .mp3 from song title
	song = song.replace("C:/mp3/audio/", "")
	song = song.replace(".mp3", "")

	#Add to End of playlist
	playlist_box.insert(END, song)



#create Function To Add Many Songs To Playlist
def add_many_song():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Add Many Songs", filetypes=(("mp3 Files", "*.mp3"), ))
	
	#loop thrugh songlist and replace directory structure and mp3 from son name
	for song in songs:

		# Strip out direcory structur and .mp3 from song title
		song = song.replace("C:/mp3/audio/", "")
		song = song.replace(".mp3", "")
		#Add to End of playlist
		playlist_box.insert(END, song)

#Delete Songs
def  delete_song():
	# Delete Highlited Song From Playlist
	playlist_box.delete(ANCHOR)

# Delete many song from Playlist
def  delete_all_song():
	# Delete All Song From Playlist
	playlist_box.delete(0, END)


# Create Play Functio
def play():
	#set Stopped to False since a song is now playing 
	global stopped
	stopped = False
	# Reconstruct Song With Directory Structure Stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	# my_label.config(text=song)

	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play Song With Pygame mixer
	pygame.mixer.music.play(loops=0)

	# Get Song Time
	play_time()


def stop():
	# Stop The Song
	pygame.mixer.music.stop()
	# Clear Playlist Bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	# Set our Slider to zero
	song_slider.config(value=0)

	# Set Stop Variable to True
	global stopped
	stopped = True

# Create Paused Variable
global paused
paused = False

# Create Pause Function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# UnPause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#Pause 
		pygame.mixer.music.pause()
		paused = True


# Create function for next song
def next_song():
	#Reset Slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0) 

	# Get Current Song number
	next_one = playlist_box.curselection()
	# my_label.config(text=next_one)

	# Add One To The Current Song Number Tuple
	next_one = next_one[0] + 1

	# Grab The Song Title fro the Playlist
	song = playlist_box.get(next_one)
	# Add Directory Structure stuff to the song title
	song = f'C:/mp3/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play Song With Pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set Active Bar To next song
	playlist_box.selection_set(next_one, last=None)

# Create Function to play Previous song
def previous_song():
	#Reset Slider position and status bar
	status_bar.config(text='')
	song_slider.config(value=0) 

	# Get Current Song number
	next_one = playlist_box.curselection()
	# my_label.config(text=next_one)

	# Subtract One To The Current Song Number Tuple
	next_one = next_one[0] - 1

	# Grab The Song Title fro the Playlist
	song = playlist_box.get(next_one)
	# Add Directory Structure stuff to the song title
	song = f'C:/mp3/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play Song With Pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear Active Bar in Playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set Active Bar To next song
	playlist_box.selection_set(next_one, last=None)

# Create Volume Function
def volume(x):
	# my_label.config(text=volume_slider.get())
	pygame.mixer.music.set_volume(volume_slider.get())

# Create Slide Function
def slide(x):
	# Reconstruct Song With Directory Structure Stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	# my_label.config(text=song)

	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play Song With Pygame mixer
	pygame.mixer.music.play(loops=0, start=song_slider.get())


# Create main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)


#Create Playlist Box
playlist_box = Listbox(main_frame,bg="black",fg="white", width=60, selectbackground="gray", selectforeground="black")
playlist_box.grid(row=0, column=0)

# Create Volume Slider Frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1,padx=20)

# Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, value=0.5, orient=VERTICAL, length=128, command=volume)
volume_slider.pack(pady=10)

# Create Song Slider Frame
song_slider = ttk.Scale(main_frame, from_=0, to=100, value=0, orient=HORIZONTAL, length=360, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#Define Button Images
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

#create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Creats Play/Stop Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0 , command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0,column=0, padx=10)
forward_button.grid(row=0,column=1, padx=10)
play_button.grid(row=0,column=2, padx=10)
pause_button.grid(row=0,column=3, padx=10)
stop_button.grid(row=0,column=4, padx=10)


#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Create Add Song Menu Dropdows
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu = add_song_menu)
#add One Song To playlist
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
#add many songs to the playlist
add_song_menu.add_command(label="Add Many Song To Playlist", command=add_many_song)

# Create Delete Song Menu Dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song Frok Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Song Frok Playlist", command=delete_all_song)

# Create Status Bar
status_bar = Label(root, text='nothing', bd=1, relief=GROOVE, anchor=E)
# ipady= internal pad y
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)



root.mainloop()