import pygame
import random
from sounds import SoundManager

# creer une classe pour gérer cette comete
class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event):
        super().__init__()
        self.image = pygame.image.load('Assets/comet.png')
        self.image = pygame.transform.scale(self.image, (150, 150))  # Taille par défaut
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 3)
        self.rect.x = random.randint(20, 800)  # Position horizontale aléatoire
        self.rect.y = -random.randint(50, 150)  # Commence juste au-dessus de l'écran
        self.comet_event = comet_event
        # gerer le son
        self.sound_manager = SoundManager()

    def fall(self):
        """Gère la chute de la comète."""
        self.rect.y += self.velocity

        # Si la comète atteint le sol
        if self.rect.y >= 550:
            print(f"Comète au sol à x={self.rect.x}, y={self.rect.y}")
            self.sound_manager.play("meteorite")
            self.remove()

        # Si la comète touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print(f"Comète a touché le joueur à x={self.rect.x}, y={self.rect.y}")
            self.remove()
            self.comet_event.game.player.damage(10)

        print(f"Comète en chute : x={self.rect.x}, y={self.rect.y}")


    def remove(self):
        """Supprime la comète du groupe."""
        self.comet_event.all_comets.remove(self)
