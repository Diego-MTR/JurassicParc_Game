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
        self.attack = 30
        self.velocity = 3
        self.jump_velocity = 20  # Puissance du saut
        self.gravity = 2 # Gravité appliquée
        self.is_jumping = False
        self.velocity_y = 0  # Vitesse verticale
        self.ground_level = 500  # Niveau du sol
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = self.ground_level
        self.last_shot_time = 0  # Temps du dernier tir
        self.cooldown_time = 750  # Temps de recharge en millisecondes
        self.is_moving = False  # pour indiquer le mouvement
        self.default_orientation_right = True  # Orientation par défaut


    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.game_over()


    def update_animation(self):
        """Met à jour l'animation du joueur."""
        if self.is_moving:
            self.animate(loop=True)  # Jouer l'animation si le joueur est en mouvement
        else:
            # Revenir à l'image de base si le joueur est statique
            self.image = pygame.transform.scale(self.images[0], self.size)

            # Assurer que le joueur est orienté vers la droite par défaut
            if not self.default_orientation_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def update_health_bar(self, surface):
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 7])

    def launch_projectile(self):
        current_time = pygame.time.get_ticks()  # Temps actuel en millisecondes
        if current_time - self.last_shot_time >= self.cooldown_time:
            # Créer une nouvelle instance de la classe projectile
            self.default_orientation_right = True  # Forcer l'orientation vers la droite
            if self.flipped:  # Réinitialiser l'image si elle était inversée
                self.flip_images()
                self.flipped = False

            self.image = pygame.transform.scale(self.images[0], self.size)  # Forcer l'image 1
            self.all_projectiles.add(Projectile(self))  # Lancer le projectile
            self.start_animations()

            # Jouer le son
            self.game.sound_manager.play('tir')
            # Enregistrer le temps du tir
            self.last_shot_time = current_time
        else:
            print("L'arme est en recharge.")  # Debug facultatif

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

    def move_right(self):
        """Déplacer le joueur vers la droite."""
        self.is_moving = True
        self.default_orientation_right = True  # Définir l'orientation par défaut vers la droite
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
            if self.flipped:
                self.flip_images()
                self.flipped = False

    def move_left(self):
        """Déplacer le joueur vers la gauche."""
        self.is_moving = True
        self.default_orientation_right = False  # Définir l'orientation par défaut vers la gauche
        self.rect.x -= self.velocity
        if not self.flipped:
            self.flip_images()
            self.flipped = True

    def stop_moving(self):
        """Arrêter le mouvement."""
        self.is_moving = False

    def update(self):
        """Met à jour le joueur, y compris la gravité et l'animation."""
        self.apply_gravity()
        self.update_animation()