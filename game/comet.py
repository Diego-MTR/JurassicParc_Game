import pygame
import random

# creer une classe pour gérer cette comete
class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event):
        super().__init__()
        # definir l'image associée à cette comète
        self.image = pygame.image.load('Assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(1, 3)
        self.rect.x = random.randint(20, 800)
        self.rect.y = - random.randint(0, 800)
        self.comet_event = comet_event

    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            # Retirer le monstre
            self.game.all_monsters.remove(self)
            self.game.add_score(self.loot_amount)

            # Ne pas spawner de nouveaux monstres si l'événement météorite est actif ou si la barre est pleine
            if not self.game.is_comet_event_active and not self.game.comet_event.is_full_loaded():
                self.game.spawn_monster(self.game.get_random_monster())








    def remove(self):
        self.comet_event.all_comets.remove(self)
        self.comet_event.game.sound_manager.play('meteorite')

        # Si toutes les comètes sont tombées
        if len(self.comet_event.all_comets) == 0 : 
            print("L'événement météorite est terminé")
            self.comet_event.reset_percent()
            self.comet_event.fall_mode = False
            self.comet_event.game.is_comet_event_active = False  # Réactiver le spawn des monstres



    def fall(self):
        self.rect.y += self.velocity

        # Si la comète atteint le sol
        if self.rect.y >= 550:
            print("Comète au sol")
            self.remove()
            
        if len(self.comet_event.all_comets) == 0:
            self.comet_event.reset_percent()
            self.comet_event.fall_mode = False

        # Si la comète touche le joueur
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            print("Comète a touché le joueur")
            self.remove()
            self.comet_event.game.player.damage(10)



