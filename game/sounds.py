import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {            
            'click': pygame.mixer.Sound("Assets/sounds/click.ogg"),
            'game_over': pygame.mixer.Sound("Assets/sounds/game_over.ogg"),
            'tir': pygame.mixer.Sound("Assets/sounds/tir.ogg"),
            'jurassicpark': pygame.mixer.Sound("Assets/sounds/jurassicpark.ogg"),
            'welcome': pygame.mixer.Sound("Assets/sounds/Welcome.ogg"),  # Ajouter la musique d'accueil
            'meteorite': pygame.mixer.Sound("Assets/sounds/meteorite.ogg"),
            'health': pygame.mixer.Sound("Assets/sounds/health.ogg"),
        }

    def play(self, name):
        if name in self.sounds:
            if name == 'jurassicpark' or name == 'welcome':  # Jouer en boucle pour certains sons
                self.sounds[name].play(loops=-1)
            else:
                self.sounds[name].stop()  # Arrêter le son en cours
                self.sounds[name].play()
    def stop(self, name):
        if name in self.sounds:
            self.sounds[name].stop()