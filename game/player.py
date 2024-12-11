import pygame
from projectile import Projectile
import animation

# creer une première classe qui va representer notre joueur
class Player(animation.AnimateSprite):

    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 3
        self.jump_velocity = 20  # Puissance du saut
        self.gravity = 2  # Gravité appliquée
        self.is_jumping = False
        self.velocity_y = 0  # Vitesse verticale
        self.ground_level = 500  # Niveau du sol
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = self.ground_level

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            # si le joueur n'a plus de points de vie
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def update_health_bar(self, surface):
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 7])

    def launch_projectile(self):
        # creer une nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectile(self))
        # demarrer l'anim du lancer
        self.start_animations()
        # jouer le son
        self.game.sound_manager.play('tir')

    def jump(self):
        if not self.is_jumping:  # Empêche le double saut
            self.is_jumping = True
            self.velocity_y = -self.jump_velocity  # Impulsion initiale vers le haut

    def apply_gravity(self):
        if self.is_jumping:
            self.rect.y += self.velocity_y  # Modifie la position verticale
            self.velocity_y += self.gravity  # Augmente la gravité pour la descente

            # Si le joueur touche le sol
            if self.rect.y >= self.ground_level:
                self.rect.y = self.ground_level
                self.is_jumping = False
                self.velocity_y = 0

    def update(self):
        self.apply_gravity()

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity