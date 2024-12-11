import pygame
from comet import Comet

# creer une classe pour gerer cet evenement
class CometFallEvent:

    # lors du chargement -> créer un compteur
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False

        # definir un groupe de sprite pour stocker nos cometes
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed / 100

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0
        self.comets_spawned = 0  # Réinitialiser le compteur
        self.total_comets = 20  # Réinitialiser la limite totale

       
    def update_comets(self):
        # Vérifier si on doit générer une nouvelle comète
        if self.comets_spawned < self.total_comets:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_delay > 500:  # Délai entre les spawns (500ms)
                # Ajouter une nouvelle comète
                self.all_comets.add(Comet(self))
                self.comets_spawned += 1
                self.spawn_delay = current_time
                print(f"Comète générée ({self.comets_spawned}/{self.total_comets})")


    def meteor_fall(self):
        self.total_comets = 20  # Nombre total de comètes à générer
        self.comets_spawned = 0  # Compteur pour suivre le nombre de comètes générées
        self.spawn_delay = pygame.time.get_ticks()  # Timer pour gérer le délai entre chaque comète
        print("Météorites prêtes à tomber !")
        
        # Fixer une limite totale de météorites à générer
        for i in range(1, 15):
            
            self.all_comets.add(Comet(self))

        
   




    def attempt_fall(self):
        # Vérifier si la barre est pleine et qu'il n'y a plus de monstres
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            print("Pluie de comètes !!")
            self.meteor_fall()  # Déclenche la pluie de météorites
            self.fall_mode = True  # Activer le mode chute
            self.game.is_comet_event_active = True  # Bloquer le spawn des monstres
        elif self.is_full_loaded() and len(self.game.all_monsters) > 0:
            print("Barre pleine, mais des monstres restent.")










    def update_bar(self, surface):

        # ajouter du pourcentage à la barre
        self.add_percent()
        
         # Déclencher l'événement si la barre est pleine
        self.attempt_fall()

        # barre noir (en arrière plan)
        pygame.draw.rect(surface, (0, 0, 0), [
            0, # l'axe des x
            surface.get_height() - 640, # l'axe des y
            surface.get_width(), # longueur de la fenetre
            10 # epaissur de la barre
        ])
        # barre rouge (jauge d'event)
        pygame.draw.rect(surface, (187, 11, 11), [
            0,  # l'axe des x
            surface.get_height() - 640,  # l'axe des y
            (surface.get_width() / 100) * self.percent ,  # longueur de la fenetre
            10  # epaissur de la barre
        ])
