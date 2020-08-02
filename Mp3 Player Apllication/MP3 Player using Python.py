from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

pygame.mixer.init()

def play_time():
	if stopped:
		return
	current_time = pygame.mixer.music.get_pos() / 1000
	
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	song = playlist_box.get(ACTIVE)
	song = f'C:\\path\\{song}.mp3'

	song_mut = MP3(song)
	global song_length
	song_length = song_mut.info.length
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
	
	if int(song_slider.get()) == int(song_length):
		stop()

	elif paused:
		pass
	
	else: 
		next_time = int(song_slider.get()) + 1
		song_slider.config(to=song_length, value=next_time)

		converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

	if current_time > 0:
		status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
	
	status_bar.after(1000, play_time)

def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), ))
	song = song.replace("C:\\path", "")
	song = song.replace(".mp3", "")
	playlist_box.insert(END, song)

def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), ))
	
	for song in songs:
		song = song.replace("C:\\path", "")
		song = song.replace(".mp3", "")
		playlist_box.insert(END, song)

def delete_song():
	playlist_box.delete(ANCHOR)

def delete_all_songs():
	playlist_box.delete(0, END)

def play():
	global stopped
	stopped = False

	song = playlist_box.get(ACTIVE)
	song = f'C:\\path....\\audio.mp3'
	
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	play_time()

global stopped
stopped = False 
def stop():
	pygame.mixer.music.stop()
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	song_slider.config(value=0)

	global stopped
	stopped = True

def next_song():
	status_bar.config(text='')
	song_slider.config(value=0)

	next_one = playlist_box.curselection()
	next_one = next_one[0] + 1

	song = playlist_box.get(next_one)
	song = f'C:\\path...\\audio.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)
	
	playlist_box.selection_clear(0, END)

	playlist_box.activate(next_one)

	playlist_box.selection_set(next_one, last=None)

def previous_song():
	status_bar.config(text='')
	song_slider.config(value=0)

	next_one = playlist_box.curselection()
	next_one = next_one[0] - 1

	song = playlist_box.get(next_one)
	song = f'C:\\path...\\audio.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	playlist_box.selection_clear(0, END)

	playlist_box.activate(next_one)

	playlist_box.selection_set(next_one, last=None)

global paused 
paused = False

def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True

def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

def slide(x):
	song = playlist_box.get(ACTIVE)
	song = f'C:\\path....\\audio.mp3'
	
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=song_slider.get())

main_frame = Frame(root)
main_frame.pack(pady=20)

playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground='black')
playlist_box.grid(row=0, column=0)

volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

back_btn_img = PhotoImage(file='backward.png')
forward_btn_img = PhotoImage(file='forward.png')
play_btn_img = PhotoImage(file='play.png')
pause_btn_img = PhotoImage(file='pause.png')
stop_btn_img = PhotoImage(file='stop50.png')


control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()
