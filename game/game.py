import pygame
from player import Player
from monster import Monster, Alanqa, Baryonyx, Carnotaurus, Oviraptor, Styracosaurus
from comet_event import CometFallEvent
from sounds import SoundManager


# creer une seconde classe qui va representer notre jeu
class Game:

    def __init__(self, starting_round=4):
        # definir si notre jeu à commencé ou non
        self.is_playing = False
        self.spawn_timer = 0  # Ajout d'un timer pour gérer les spawns
        self.spawn_interval = 3000  # Intervalle en millisecondes entre chaque spawn
        self.is_comet_event_active = False
        self.difficulty_level = 1  # Niveau de difficulté initial
        self.health_packs = pygame.sprite.Group() # Pack de soins
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
        self.stats = {
            'dinosaurs_killed': {'alanqa': 0, 'baryonyx': 0, 'carnotaurus': 0, 'oviraptor': 0, 'styracosaurus': 0},
            'damage_dealt': 0,
            'comets_received': 0,  # Comètes touchées par le joueur
            'comets_avoided': 0,  # Comètes esquivées
            'score': 0,
            'rounds_completed': starting_round  
        }
        
        
        # Charger les images pour la fenêtre de défaite
        self.defeat_image = pygame.image.load("Assets/defeat.png")
        self.defeat_image = pygame.transform.scale(self.defeat_image, (400, 200))
        self.defeat_rect = self.defeat_image.get_rect(center=(540, 200))

        self.retry_button = pygame.image.load("Assets/retry.png")
        self.retry_button = pygame.transform.scale(self.retry_button, (200, 100))
        self.retry_rect = self.retry_button.get_rect(center=(540, 400))


    def start(self):
        self.is_playing = True
        self.monsters_killed = 0  # Réinitialiser le compteur
        self.spawn_timer = pygame.time.get_ticks()  # Initialiser le timer
        a = True
        if a:
             self.spawn_monster(self.get_random_monster())
             self.spawn_monster(self.get_random_monster())
             a = False
        
        self.spawn_monster(self.get_random_monster())
        self.sound_manager.play('jurassicpark')  # Faire apparaître le premier monstre

    def add_score(self, points=10):
        self.score += points
        


    def game_over(self):
        """Met le jeu en état de défaite."""
        self.is_playing = False
        self.is_game_over = True  # Indiquer que le joueur est mort
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.is_comet_event_active = False
        self.sound_manager.play("game_over")
        self.sound_manager.sounds['jurassicpark'].stop()
        


    def handle_defeat_screen(self, screen, event):
        """Gère l'affichage et les interactions sur l'écran de défaite."""
        screen.blit(self.defeat_image, self.defeat_rect)
        screen.blit(self.retry_button, self.retry_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and self.retry_rect.collidepoint(event.pos):
            self.start()  # Relancer le jeu



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


            # Afficher le nombre de manches
            round_text = self.font.render(f"Manche: {self.stats['rounds_completed']}", 1, (0, 0, 0))
            screen.blit(round_text, (screen.get_width() - round_text.get_width() - 20, 20))

            # Dessiner la barre de progression
            self.comet_event.update_bar(screen)

            if not self.all_monsters and not self.comet_event.all_comets and not self.comet_event.fall_mode and not self.is_comet_event_active:
                print("Conditions remplies pour un nouveau round.")
                self.start_new_round()


            for health_pack in self.health_packs:
                health_pack.fall()
            self.health_packs.draw(screen)


    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self, monster_class_name):
        """Fait apparaître un monstre si les conditions sont remplies."""
        # Ne spawn pas de monstres si l'événement météorite est actif
        if not self.is_comet_event_active and not self.comet_event.fall_mode and len(self.all_monsters) < 3:
            monster = monster_class_name(self)
            self.all_monsters.add(monster)

    def get_random_monster(self):
        import random
        return random.choice([Alanqa, Baryonyx, Carnotaurus, Oviraptor, Styracosaurus])

    def increase_difficulty(self):
        """Augmente le niveau de difficulté."""
        self.difficulty_level += 1
        print(f"Niveau de difficulté augmenté : {self.difficulty_level}")

        # Augmenter la difficulté des météorites
        self.comet_event.total_comets += 5
        self.comet_event.percent_speed -= 1  # Barre de progression plus lente

        # Ajuster les monstres
        for monster in self.all_monsters:
            monster.max_health += 20 * self.difficulty_level  # Plus de santé
            monster.health = monster.max_health
            monster.velocity += 0.1 * self.difficulty_level  # Plus rapide
            self.all_monsters += 3
            
    def next_round(self):
        """Prépare la prochaine manche."""
        self.difficulty_level += 1
        self.comet_event.total_comets += 2
        for monster in self.all_monsters:
            monster.velocity += 0.2 * self.difficulty_level
            monster.max_health += 10 * self.difficulty_level
            monster.health = monster.max_health
 
 
    def handle_defeat_screen(self, screen):
        stats_text = f"""\
        Dinosaures tués:
            Alanqa: {self.stats['dinosaurs_killed']['alanqa']}
            Baryonyx: {self.stats['dinosaurs_killed']['baryonyx']}
            Carnotaurus: {self.stats['dinosaurs_killed']['carnotaurus']}
            Oviraptor: {self.stats['dinosaurs_killed']['oviraptor']}
            Styracosaurus: {self.stats['dinosaurs_killed']['styracosaurus']}
        Dégâts infligés: {self.stats['damage_dealt']}
        Comètes reçues: {self.stats['comets_received']}
        Score: {self.stats['score']}
        Manches complétées: {self.stats['rounds_completed']}
        """
        font = pygame.font.Font(None, 30)
        y = 250
        for line in stats_text.splitlines():
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (100, y))
            y += 30

    def reset_game(self):
        """Réinitialise complètement le jeu pour recommencer une nouvelle partie."""
        self.is_playing = False
        self.is_game_over = False
        self.score = 0
        self.difficulty_level = 1

        # Réinitialiser les statistiques
        self.stats = {
            'dinosaurs_killed': {'alanqa': 0, 'baryonyx': 0, 'carnotaurus': 0, 'oviraptor': 0, 'styracosaurus': 0},
            'damage_dealt': 0,
            'comets_received': 0,
            'comets_avoided': 0,  # Réinitialisation des comètes esquivées
            'score': 0,
            'rounds_completed': 0
    }

        # Vider tous les groupes de sprites
        self.all_monsters.empty()
        self.player.all_projectiles.empty()
        self.comet_event.all_comets.empty()

        # Réinitialiser la barre de progression des comètes
        self.comet_event.reset_percent()
        self.is_comet_event_active = False
        self.comet_event.fall_mode = False  # Désactiver le mode chute
        self.comet_event.comets_spawned = 0  # Réinitialiser le compteur des comètes générées
        self.comet_event.last_spawn_time = pygame.time.get_ticks()  # Réinitialiser le timer de génération des comètes

        # Réinitialiser le joueur
        self.player.health = self.player.max_health
        self.player.rect.x = 400
        self.player.rect.y = self.player.ground_level

        # Réinitialiser le timer de spawn des monstres
        self.spawn_timer = pygame.time.get_ticks()

        # Arrêter les sons actifs
        self.sound_manager.stop('jurassicpark')
        self.sound_manager.stop('game_over')


    def start_new_round(self):
        """Démarre une nouvelle manche et augmente la difficulté."""
        self.stats['rounds_completed'] += 1
        print(f"Manche {self.stats['rounds_completed']} démarrée!")

        # Logs pour vérifier les paramètres avant modification
        print(f"Avant : spawn_interval={self.spawn_interval}, cooldown_time={self.player.cooldown_time}, total_comets={self.comet_event.total_comets}")

        # Réduire l'intervalle de spawn des monstres
        self.spawn_interval = max(1000, self.spawn_interval - 200)

        # Augmenter la difficulté des monstres
        for monster in self.all_monsters:
            monster.velocity += 0.2 * self.stats['rounds_completed']
            monster.max_health += 10 * self.stats['rounds_completed']
            monster.health = monster.max_health

        # Augmenter la vitesse des comètes
        for comet in self.comet_event.all_comets:
            comet.velocity += 0.5 * self.stats['rounds_completed']

        # Réduire la vitesse de progression de la barre de météorites
        self.comet_event.percent_speed = max(1, self.comet_event.percent_speed - 1)

        # Augmenter le nombre total de comètes pour la manche suivante
        self.comet_event.total_comets += 2

        # Réduire le cooldown du joueur
        self.player.cooldown_time = max(100, self.player.cooldown_time - 50)

        # Faire apparaître un nouveau monstre pour le début de la manche
        self.spawn_monster(self.get_random_monster())

        # Logs pour vérifier les paramètres après modification
        print(f"Après : spawn_interval={self.spawn_interval}, cooldown_time={self.player.cooldown_time}, total_comets={self.comet_event.total_comets}")

