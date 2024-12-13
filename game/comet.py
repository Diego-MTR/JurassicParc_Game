import pygame
import random

# creer une classe pour gérer cette comete
class Comet(pygame.sprite.Sprite):
    default_size = (150, 150)  # Taille par défaut des comètes

    def __init__(self, comet_event):
        super().__init__()
        self.image = pygame.image.load('Assets/comet.png')
        self.image = pygame.transform.scale(self.image, Comet.default_size)
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 3)
        self.rect.x = random.randint(20, 800)
        self.rect.y = -random.randint(50, 150)
        self.comet_event = comet_event
        self.update_velocity()  # Ajuster la vitesse dès la création


    def fall(self):
        """Gère la chute de la comète."""
        self.rect.y += self.velocity
        if self.rect.y >= 550:
            print(f"Comète touchée le sol à x={self.rect.x}, y={self.rect.y}")
            self.comet_event.game.stats['comets_avoided'] += 1
            self.remove()

        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print(f"Comète touchée le joueur à x={self.rect.x}, y={self.rect.y}")
            self.comet_event.game.stats['comets_received'] += 1
            self.remove()
            self.comet_event.game.player.damage(20)



        # Si la comète touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print(f"Comète a touché le joueur à x={self.rect.x}, y={self.rect.y}")
            self.comet_event.game.stats['comets_received'] += 1  # Comptabiliser comme touchée
            self.remove()
            self.comet_event.game.player.damage(20)

        print(f"Comète en chute : x={self.rect.x}, y={self.rect.y}")


    def remove(self):
        """Supprime la comète du groupe."""
        self.comet_event.all_comets.remove(self)

    def update_velocity(self):
        """Ajuste la vitesse en fonction de la manche actuelle."""
        base_velocity = 1  # Vitesse minimale
        increment = 0.2 * self.comet_event.game.stats['rounds_completed']  # Augmentation progressive
        self.velocity = random.randint(int(base_velocity + increment), int(base_velocity + increment + 2))