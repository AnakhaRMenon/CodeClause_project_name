import os
import tkinter as tk
from tkinter import filedialog
import pygame


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        self.playlist = []
        self.current_index = 0
        self.paused = False

        pygame.init()

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        # Create buttons
        self.btn_load = tk.Button(
            self.root, text="Load Songs", command=self.load_songs
        )
        self.btn_play = tk.Button(
            self.root, text="Play", state=tk.DISABLED, command=self.play_music
        )
        self.btn_pause = tk.Button(
            self.root, text="Pause", state=tk.DISABLED, command=self.pause_music
        )
        self.btn_stop = tk.Button(
            self.root, text="Stop", state=tk.DISABLED, command=self.stop_music
        )

        # Create label for current song
        self.lbl_current_song = tk.Label(self.root, text="No song loaded")

        # Position buttons and label
        self.btn_load.pack(pady=20)
        self.btn_play.pack(pady=10)
        self.btn_pause.pack(pady=10)
        self.btn_stop.pack(pady=10)
        self.lbl_current_song.pack(pady=20)

    def load_songs(self):
        # Clear the current playlist
        self.playlist.clear()

        # Open a file dialog to select multiple audio files
        files = filedialog.askopenfilenames(
            initialdir="/", title="Select Songs", filetypes=(("Audio Files", "*.mp3"), ("All Files", "*.*"))
        )

        # Add selected files to the playlist
        for file in files:
            self.playlist.append(file)

        if self.playlist:
            self.btn_play.config(state=tk.NORMAL)
            self.lbl_current_song.config(text="Loaded {} songs".format(len(self.playlist)))

    def play_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
        else:
            self.load_song_from_playlist()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.paused = False

    def load_song_from_playlist(self):
        if self.current_index < len(self.playlist):
            current_song = self.playlist[self.current_index]
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
            self.lbl_current_song.config(text="Now playing: {}".format(os.path.basename(current_song)))
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.NORMAL)
            self.current_index += 1
        else:
            self.lbl_current_song.config(text="No more songs in the playlist")
            self.btn_play.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.DISABLED)


# Create the main window
root = tk.Tk()
root.geometry("300x200")

# Create an instance of the MusicPlayer
music_player = MusicPlayer(root)
