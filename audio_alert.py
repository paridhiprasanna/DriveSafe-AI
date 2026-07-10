import pygame


class AudioAlert:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.wav")
        self.playing = False

    def play(self):
        if not self.playing:
            pygame.mixer.music.play(-1)  
            self.playing = True

    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False