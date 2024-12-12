import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {
    'click': pygame.mixer.Sound("Assets/sounds/click.ogg"),
    'game_over': pygame.mixer.Sound("Assets/sounds/game_over.ogg"),
    'tir': pygame.mixer.Sound("Assets/sounds/tir.ogg"),
    'jurassicpark': pygame.mixer.Sound("Assets/sounds/jurassicpark.ogg")
}


    def play(self, name):
        if name == 'jurassicpark':
            self.sounds[name].play(loops=-1)  # Jouer en boucle
        else:
            self.sounds[name].stop()  # Arrêter le son en cours
            self.sounds[name].play()


