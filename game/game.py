import pygame
from player import Player
from monster import Monster, Alanqa, Baryonyx, Carnotaurus, Oviraptor, Styracosaurus
from comet_event import CometFallEvent
from sounds import SoundManager


# creer une seconde classe qui va representer notre jeu
class Game:

    def __init__(self):
        # definir si notre jeu à commencé ou non
        self.is_playing = False
        self.spawn_timer = 0  # Ajout d'un timer pour gérer les spawns
        self.spawn_interval = 3000  # Intervalle en millisecondes entre chaque spawn
        self.is_comet_event_active = False 
        # generer notre joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        # generer l'evenement
        self.comet_event = CometFallEvent(self)
        self.comet_event.percent_speed = 10 # Par exemple, augmenter la vitesse à 10%        
        # groupe de monstres
        self.all_monsters = pygame.sprite.Group()
        # gerer le son
        self.sound_manager = SoundManager()
        # mettre le score à 0
        self.font = pygame.font.Font("Assets/my_custom_font.ttf", 25)
        self.score = 0
        self.pressed = {}

    def start(self):
        self.is_playing = True
        self.monsters_killed = 0  # Réinitialiser le compteur
        self.spawn_timer = pygame.time.get_ticks()  # Initialiser le timer
        self.spawn_monster(self.get_random_monster())  # Faire apparaître le premier monstre

    def add_score(self, points=10):
        self.score += points

    def game_over(self):
        # Remettre le jeu à neuf
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_comet_event_active = False  # Réinitialiser l'événement météorite
        self.is_playing = False
        self.score = 0
        self.monsters_killed = 0  # Réinitialiser les monstres tués
        self.spawn_timer = 0  # Réinitialiser le timer de spawn
        # Jouer le son
        self.sound_manager.play("game_over")

    def update(self, screen):
        if self.is_playing:
            # Gestion des comètes
            if self.comet_event.fall_mode:
                self.comet_event.update_comets()

            # Dessiner les comètes
            self.comet_event.all_comets.draw(screen)

            # Mise à jour du joueur
            self.player.update()  # Met à jour la gravité
            screen.blit(self.player.image, self.player.rect)
            self.player.update_health_bar(screen)
            self.player.update_animation()
            
            
            # Gestion des mouvements
            if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
                self.player.move_right()
            elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
                self.player.move_left()

            # Mise à jour des projectiles
            for projectile in self.player.all_projectiles:
                projectile.move()

            # Mise à jour des monstres
            for monster in self.all_monsters:
                monster.forward()
                monster.update_health_bar(screen)
                monster.update_animation()

            # Dessiner les projectiles et monstres
            self.player.all_projectiles.draw(screen)
            self.all_monsters.draw(screen)

            # Afficher le score
            score_text = self.font.render(f"Score: {self.score}", 1, (0, 0, 0))
            screen.blit(score_text, (20, 20))

            # Dessiner la barre de progression
            self.comet_event.update_bar(screen)



    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        # Ne spawn pas de monstres si l'événement météorite est actif
        if not self.is_comet_event_active and len(self.all_monsters) < 3:
            monster = monster_class_name(self)
            self.all_monsters.add(monster)

    def get_random_monster(self):
        import random
        return random.choice([Alanqa, Baryonyx, Carnotaurus, Oviraptor, Styracosaurus])
