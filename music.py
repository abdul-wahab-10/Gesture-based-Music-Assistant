from pygame import mixer
import pygame
from main2 import *
import os
import cv2
import mediapipe as mp
import time
import threading


class Music:

    def __init__(self):
        mixer.init()
        pygame.init()
        self.music_list = []
        self.count = 0
        self.cap = cv2.VideoCapture(0)

    def go_previous(self, name):
        time.sleep(0.5)
        if self.count < 0:
            self.count = (len(self.music_list) - 1)
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")
            mixer.music.play()

        else:
            self.count -= 1
            self.count = self.count % (len(self.music_list))
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")
            mixer.music.play()

    def go_next(self, name):
        time.sleep(0.5)
        if self.count == (len(self.music_list) - 1):
            self.count = 0
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")
            mixer.music.play()

        else:
            self.count += 1
            self.count = self.count % (len(self.music_list))
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")
            mixer.music.play()

    def pause_music(self):
        mixer.music.pause()

    def resume(self):
        mixer.music.unpause()

    def exit_music(self):
        mixer.music.stop()
        pygame.quit()  # Clean up the pygame environment
        exit()

    def play_music(self, name):
        if name == "unknown":
            music_path = f"C:\\My_Python_Projects\\Gesture_Based_Music_Recommendation\\{name}"
            self.music_list = os.listdir(music_path)
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")

            mixer.music.set_volume(3)
            mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
        else:
            music_path = f"C:\\My_Python_Projects\\Gesture_Based_Music_Recommendation\\{name}"
            self.music_list = os.listdir(music_path)
            mixer.music.load(f"./{name}/{self.music_list[self.count]}")

            mixer.music.set_volume(3)
            mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)


if __name__ == '__main__':
    m = Music()
    name = "awwab"
    m.play_music(name=name)

    exit_requested = False


    def user_input():
        global exit_requested
        while not exit_requested:
            query = input("Press 'p' to pause\nPress 'r' to resume\nPress 'e' to exit\nPress 'n' to play next\n"
                          "Press 'm' to play next\n")

            if query == 'p':
                m.pause_music()

            elif query == 'r':
                m.resume()

            elif query == 'n':
                m.go_next(name)

            elif query == 'm':
                m.go_previous(name)

            elif query == 'e':
                exit_requested = True
                m.exit_music()

            else:
                mixer.music.stop()
                m.count += 1
                mixer.music.load(f"./{name}/{m.music_list[m.count]}")
                mixer.music.play()

        # return query


    input_thread = threading.Thread(target=user_input)
    input_thread.daemon = True
    input_thread.start()

    while not exit_requested:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                m.count += 1
                mixer.music.load(f"./{name}/{m.music_list[m.count]}")
                mixer.music.play()
