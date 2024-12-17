import pygame
from comet import Comet
import random
from health import HealthPack  # Importer la classe HealthPack


class CometFallEvent:

    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 7
        self.game = game
        self.fall_mode = False
        self.all_comets = pygame.sprite.Group()
        self.total_comets = 20
        self.comets_spawned = 0
        self.last_spawn_time = pygame.time.get_ticks()

    def add_percent(self):
        """Ajoute à la barre de progression."""
        self.percent += self.percent_speed / 100
        print(f"Barre de progression : {self.percent}%")

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
        self.fall_mode = True
        self.all_comets = pygame.sprite.Group()  # Réinitialiser les comètes
        self.comets_spawned = 0  # Réinitialiser le compteur
        self.last_spawn_time = pygame.time.get_ticks()  # Réinitialiser le timer
        self.game.is_comet_event_active = True  # Activer l'événement dans le jeu



    def update_comets(self):
        """Génère des comètes toutes les deux secondes."""
        if not self.fall_mode:
            return

        current_time = pygame.time.get_ticks()
        spawn_interval = 2000  # Intervalle de génération des comètes en millisecondes
        

        # Générer une nouvelle comète si le temps est écoulé
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

        # Ajouter une trousse de soins pendant l'évènement toutes les 5 manches
        if self.game.stats['rounds_completed'] % 5 == 0 and not hasattr(self, 'health_pack_added'):
            self.health_pack = HealthPack(self.game)
            self.game.health_packs.add(self.health_pack)
            self.health_pack_added = True  # Ajouter seulement une fois par événement

        # Si l'événement se termine, réinitialiser la trousse
        if self.comets_spawned >= self.total_comets and len(self.all_comets) == 0:
            self.health_pack_added = False  # Réinitialiser pour la prochaine manche
            
            # Ajouter une trousse de soin toutes les 5 manches
        if self.game.stats['rounds_completed'] % 5 == 0 and not hasattr(self, 'health_pack_added'):
            health_pack = HealthPack(self.game)
            health_pack.rect.x = random.randint(20, 800)  # Position aléatoire sur x
            self.all_comets.add(health_pack)  # Ajouter au même groupe que les comètes
            self.health_pack_added = True


    def reset_event(self):
        """Réinitialise l'événement de chute des comètes."""
        print("Fin de l'événement météorite.")
        self.fall_mode = False  # Désactiver le mode chute
        self.reset_percent()  # Réinitialiser la barre de progression
        self.comets_spawned = 0  # Réinitialiser le compteur de comètes générées
        self.all_comets.empty()  # Vider les comètes en cours
        self.last_spawn_time = pygame.time.get_ticks()  # Réinitialiser le timer de génération
        self.game.is_comet_event_active = False  # Désactiver l'événement météorite dans le jeu
        self.game.start_new_round()  # Démarrer une nouvelle manche




    def attempt_fall(self):
        """Déclenche l'événement météorite si la barre est pleine."""
        if self.is_full_loaded() and not self.fall_mode and len(self.game.all_monsters) == 0:
            print("Déclenchement de l'événement météorite.")
            self.meteor_fall()
            self.game.is_comet_event_active = True


    def update_bar(self, surface):
        """Met à jour la barre de progression."""
        self.add_percent()
        self.attempt_fall()

        # Logs pour vérifier l'état
        print(f"Barre pleine : {self.is_full_loaded()}, Fall Mode : {self.fall_mode}")

        # Barre noire
        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height() - 640, surface.get_width(), 10])
        # Barre rouge
        pygame.draw.rect(surface, (187, 11, 11), [0, surface.get_height() - 640, (surface.get_width() / 100) * self.percent, 10])

