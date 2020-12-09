# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

import tkinter
from pygame import mixer
import time
import os

DIR = os.getcwd()
MUSIC_DIR = os.path.join(DIR, 'misc', 'sound')
BG_DIR = os.path.join(DIR, 'misc')


def play_sound(file):
    mixer.music.load(file)
    mixer.music.play(0)


def play_bgsound(file, channel=0):
    mixer.Channel(channel).play(mixer.Sound(file))


def delay(length=float(3)):
    # todo:
    print('pause not implemented')
    start = time.time()
    while time.time() - start < length:
        pass


class StartScreen:
    def __init__(self):
        play_sound('intro.wav')