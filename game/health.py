import pygame
import random

class HealthPack(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("Assets/health_pack.png")  # Assurez-vous que l'image existe
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, 800)  # Position aléatoire sur l'axe x
        self.rect.y = -50  # Départ du haut de l'écran
        self.velocity = 2  # Vitesse de descente

    def fall(self):
        """Faire descendre la trousse de soin."""
        self.rect.y += self.velocity

        # Vérifier la collision avec le joueur
        if self.game.check_collision(self, self.game.all_players):
            print("Trousse de soin ramassée !")
            self.game.player.health = self.game.player.max_health  # Redonner la vie max
            self.remove()

        # Supprimer si elle dépasse le sol
        if self.rect.y > 550:
            self.remove()


    def remove(self):
        self.game.health_packs.remove(self)
