import pygame
from comet import Comet
import random

class CometFallEvent:

    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False
        self.all_comets = pygame.sprite.Group()
        self.total_comets = 20
        self.comets_spawned = 0
        self.last_spawn_time = pygame.time.get_ticks()

    def add_percent(self):
        """Ajoute à la barre de progression."""
        self.percent += self.percent_speed / 100

    def is_full_loaded(self):
        """Vérifie si la barre est pleine."""
        return self.percent >= 100

    def reset_percent(self):
        """Réinitialise la barre de progression et le compteur."""
        self.percent = 0
        self.comets_spawned = 0

    def meteor_fall(self):
        """Initialise la chute des météorites."""
        print("Début de l'événement météorite.")
        self.all_comets = pygame.sprite.Group()  # Réinitialiser les comètes
        self.comets_spawned = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.fall_mode = True

    def update_comets(self):
        """Génère des comètes toutes les deux secondes."""
        if not self.fall_mode:
            return

        current_time = pygame.time.get_ticks()
        spawn_interval = 2000  # 2 secondes

        # Générer une nouvelle comète toutes les 2 secondes
        if current_time - self.last_spawn_time > spawn_interval and self.comets_spawned < self.total_comets:
            num_comets = random.randint(1, 3)  # Générer 1 à 3 comètes
            for _ in range(num_comets):
                if self.comets_spawned < self.total_comets:
                    comet = Comet(self)
                    self.all_comets.add(comet)
                    self.comets_spawned += 1
                    print(f"Comète générée ({self.comets_spawned}/{self.total_comets}).")
            self.last_spawn_time = current_time

        # Mettre à jour chaque comète
        for comet in self.all_comets:
            comet.fall()

        # Terminer l'événement si toutes les comètes sont tombées
        if self.comets_spawned >= self.total_comets and len(self.all_comets) == 0:
            self.reset_event()


    def reset_event(self):
        """Réinitialise l'événement de chute des comètes."""
        print("Fin de l'événement météorite.")
        self.fall_mode = False
        self.reset_percent()
        self.game.is_comet_event_active = False

    def attempt_fall(self):
        """Déclenche l'événement météorite si la barre est pleine."""
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            if not self.fall_mode:  # Empêche le redémarrage continu de l'événement
                self.meteor_fall()
                self.game.is_comet_event_active = True

    def update_bar(self, surface):
        """Met à jour la barre de progression."""
        self.add_percent()
        self.attempt_fall()

        # Barre noire
        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height() - 640, surface.get_width(), 10])
        # Barre rouge
        pygame.draw.rect(surface, (187, 11, 11), [0, surface.get_height() - 640, (surface.get_width() / 100) * self.percent, 10])
