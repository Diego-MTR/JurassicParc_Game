import pygame
import math
from game import Game
pygame.init()

# définir une clock
clock = pygame.time.Clock()
FPS = 60

# générer la fenêtre de notre jeu
pygame.display.set_caption("Jurassic Park")
screen = pygame.display.set_mode((1080, 720))

# importer et charger l'arrière-plan de notre jeu
background = pygame.image.load('Assets/bg.jpg')
background = pygame.transform.scale(background, screen.get_size())

# importer et charger les bannières et boutons
banner_start = pygame.image.load('Assets/banner.png')
banner_start = pygame.transform.scale(banner_start, (525, 350))

banner_defeat = pygame.image.load('Assets/defeat.png')
banner_defeat = pygame.transform.scale(banner_defeat, (525, 350))

play_button_start = pygame.image.load('Assets/button.png')
play_button_start = pygame.transform.scale(play_button_start, (400, 150))

play_button_retry = pygame.image.load('Assets/retry.png')
play_button_retry = pygame.transform.scale(play_button_retry, (400, 150))

banner_rect = banner_start.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)
banner_rect.y = math.ceil(screen.get_height() / 8)

play_button_rect = play_button_start.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

# charger notre jeu
game = Game()
if not hasattr(game, 'is_game_over'):
    game.is_game_over = False  # Assurer l'initialisation correcte

# Gestion des sons
sound_manager = game.sound_manager
sound_manager.play('welcome')  # Jouer la musique d'accueil
# Définir un indicateur pour la première fois
first_time = True

running = True

# boucle principale
while running:
    screen.blit(background, (0, 0))

    if game.is_playing:
        sound_manager.stop('welcome')
        game.update(screen)
    else:
        if first_time:
            # Afficher l'écran de démarrage
            screen.blit(banner_start, banner_rect)
            screen.blit(play_button_start, play_button_rect)
        elif game.is_game_over:
            # Afficher l'écran de défaite
            screen.blit(banner_defeat, banner_rect)
            screen.blit(play_button_retry, play_button_rect)

            # Ajouter les statistiques
            font = pygame.font.Font(None, 30)
            stats_text = f"""
            Score : {game.stats['score']}
            Manches complétées : {game.stats['rounds_completed']}
            Dinosaures tués :
              Alanqa : {game.stats['dinosaurs_killed']['alanqa']}
              Baryonyx : {game.stats['dinosaurs_killed']['baryonyx']}
              Carnotaurus : {game.stats['dinosaurs_killed']['carnotaurus']}
              Oviraptor : {game.stats['dinosaurs_killed']['oviraptor']}
              Styracosaurus : {game.stats['dinosaurs_killed']['styracosaurus']}
            Dégâts infligés : {game.stats['damage_dealt']}
            Dégâts reçus : {game.stats['damage_received']}
            Comètes reçues : {game.stats['comets_received']}
            """
            y = 250
            for line in stats_text.splitlines():
                text = font.render(line.strip(), True, (255, 255, 255))
                screen.blit(text, (50, y))
                y += 25

    pygame.display.flip()

    # gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if game.is_playing:
                if event.key == pygame.K_UP:
                    game.player.jump()
                elif event.key == pygame.K_SPACE:
                    game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if first_time and play_button_rect.collidepoint(event.pos):
                # Premier lancement
                first_time = False
                game.start()
                sound_manager.play('click')
                sound_manager.stop('welcome')
            elif game.is_game_over and play_button_retry.get_rect(center=(540, 400)).collidepoint(event.pos):
                # Exporter les statistiques et réinitialiser le jeu
                first_time = False
                game.is_game_over = False
                game.score = 0
                game.player.health = game.player.max_health
                game.all_monsters.empty()
                game.comet_event.reset_percent()
                game.start()
                game.sound_manager.play('click')

    # Gestion des mouvements en continu (gauche/droite)
    if game.is_playing:
        if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
            game.player.move_right()
        elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
            game.player.move_left()

    clock.tick(FPS)

# Ajouter la méthode export_stats à la classe Game
if not hasattr(Game, 'export_stats'):
    def export_stats(self):
        with open("game_stats.txt", "w") as file:
            file.write("Statistiques du jeu :\n")
            file.write(f"Score : {self.stats['score']}\n")
            file.write(f"Manches complétées : {self.stats['rounds_completed']}\n")
            file.write("Dinosaures tués :\n")
            for dino, count in self.stats['dinosaurs_killed'].items():
                file.write(f"  {dino}: {count}\n")
            file.write(f"Dégâts infligés : {self.stats['damage_dealt']}\n")
            file.write(f"Comètes reçues : {self.stats['comets_received']}\n")
    Game.export_stats = export_stats
