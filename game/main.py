import pygame
import math
from game import Game
pygame.init()

def display_defeat_screen(screen, game):
    """Affiche l'écran de défaite avec un tableau centralisé et un bouton Retry fonctionnel."""

    # Charger le fond de l'écran de défaite
    bg_dark = pygame.image.load("Assets/bg_dark.jpg")
    bg_dark = pygame.transform.scale(bg_dark, screen.get_size())  # Adapter à la taille de l'écran

    # Charger les ressources localement
    banner_defeat = pygame.image.load("Assets/defeat.png")
    banner_defeat = pygame.transform.scale(banner_defeat, (400, 300))




    # Position de la bannière
    banner_width, banner_height = banner_defeat.get_size()
    banner_x = (screen.get_width() - banner_width) // 2
    banner_y = 30

    # Dimensions du tableau
    tableau_width = 275  # Largeur réduite
    tableau_height = 300  # Hauteur augmentée
    tableau_x = (screen.get_width() - tableau_width) // 2  # Centrage horizontal
    tableau_y = (screen.get_height() - tableau_height) // 2 + 100  # Centrage vertical avec décalage

    # Réduire la taille du bouton "Retry"
    play_button_retry = pygame.image.load("Assets/retry.png")
    play_button_retry = pygame.transform.scale(play_button_retry, (250, 250))  # Réduction de taille
    retry_width, retry_height = play_button_retry.get_size()


    # Position du bouton "Retry"
    # Positionner en haut à droite
    retry_x = screen.get_width() - retry_width - 20  # 20 pixels de marge à droite
    retry_y = 20  # 20 pixels de marge en haut
    retry_button_rect = pygame.Rect(retry_x, retry_y, retry_width, retry_height)
    screen.blit(play_button_retry, retry_button_rect)


    # Afficher la bannière
    screen.blit(banner_defeat, (banner_x, banner_y))

    # Fond gris du tableau
    tableau_rect = pygame.Rect(tableau_x, tableau_y, tableau_width, tableau_height)
    pygame.draw.rect(screen, (139, 69, 19), tableau_rect)  # Marron
    pygame.draw.rect(screen, (0, 0, 0), tableau_rect, 2)  # Bordure noire

    # Texte des statistiques
    font = pygame.font.Font("Assets/my_custom_font.ttf", 18)
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
    Comètes reçues : {game.stats['comets_received']}
    Comètes esquivées : {game.stats['comets_avoided']}
    """
    # Afficher chaque ligne au centre du tableau
    y = tableau_y + 20
    for line in stats_text.strip().splitlines():
        text_surface = font.render(line.strip(), True, (0, 0, 0))  # Texte noir
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
        screen.blit(text_surface, text_rect)
        y += 25

    # Afficher le bouton Retry
    screen.blit(play_button_retry, (retry_x, retry_y))

    # Retourner le rect du bouton Retry
    return pygame.Rect(retry_x, retry_y, retry_width, retry_height)


def display_rules_screen(screen):
    """Affiche l'écran des règles."""
    # Fond
    bg_dark = pygame.image.load("Assets/bg_dark.jpg")
    bg_dark = pygame.transform.scale(bg_dark, screen.get_size())  # Adapter à la taille de l'écran
    screen.blit(bg_dark, (0, 0))  # Afficher le fond

    # Titre "Rules"
    rules_title = pygame.image.load("Assets/rules.png")
    rules_title = pygame.transform.scale(rules_title, (400, 200))
    title_x = (screen.get_width() - rules_title.get_width()) // 2
    title_y = 50
    screen.blit(rules_title, (title_x, title_y))

    # Texte explicatif
    font = pygame.font.Font("Assets/my_custom_font.ttf", 20)
    rules_text = [
        "Bienvenue dans Jurassic Parc Game !",
        "",
        "Objectif :",
        " - Survivez aux manches le plus longtemps possible en évitant les comètes.",
        " - Éliminez les dinosaures pour marquer des points.",
        "",
        "Touches :",
        " - Flèche gauche : se déplacer à gauche.",
        " - Flèche droite : se déplacer à droite.",
        " - Flèche haut : sauter.",
        " - Barre espace : tirer.",
        "",
        "Bonne chance !"
    ]

    y_offset = 300
    for line in rules_text:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30

 # Bouton "Exit"
    exit_button = pygame.image.load("Assets/exit.png")
    exit_button = pygame.transform.scale(exit_button, (250, 250))  # Taille ajustée
    screen.blit(exit_button, exit_button_rect)

    return exit_button_rect

# définir une clock
clock = pygame.time.Clock()
FPS = 60

# générer la fenêtre de notre jeu
pygame.display.set_caption("Jurassic Park")
screen = pygame.display.set_mode((1080, 720))
# Charger l'image de fond sombre pour l'écran de défaite
bg_dark = pygame.image.load("Assets/bg_dark.jpg")
bg_dark = pygame.transform.scale(bg_dark, screen.get_size())  # Adapter l'image à la taille de l'écran

# importer et charger l'arrière-plan de notre jeu
background = pygame.image.load('Assets/bg.jpg')
background = pygame.transform.scale(background, screen.get_size())

# importer et charger les bannières et boutons
banner_start = pygame.image.load('Assets/banner.png')
banner_start = pygame.transform.scale(banner_start, (525, 350))

banner_defeat = pygame.image.load('Assets/defeat.png')
banner_defeat = pygame.transform.scale(banner_defeat, (525, 350))

play_button_start = pygame.image.load('Assets/button.png')
play_button_start = pygame.transform.scale(play_button_start, (400, 300))

play_button_retry = pygame.image.load('Assets/retry.png')
play_button_retry = pygame.transform.scale(play_button_retry, (250, 250))

# Bouton Exit
exit_button = pygame.image.load("Assets/exit.png")
exit_button = pygame.transform.scale(exit_button, (250, 250))  # Ajustez la taille selon vos besoins
exit_button_rect = exit_button.get_rect()

# Charger le bouton "Rules"
rules_button = pygame.image.load("Assets/rules.png")
rules_button = pygame.transform.scale(rules_button, (250, 250))  # Taille ajustée
rules_button_rect = rules_button.get_rect()

# Positionner en haut à droite
rules_button_rect.x = screen.get_width() - rules_button_rect.width - 20
rules_button_rect.y = 20


exit_x = ()
exit_y = ()

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
show_rules = False  # Initialiser l'état de l'écran des règles
first_time = True   # Initialiser l'état de l'écran principal

# boucle principale
while running:
    screen.blit(background, (0, 0))

    if game.is_playing:
        sound_manager.stop('welcome')
        game.update(screen)
    elif show_rules:
        # Afficher l'écran des règles
        exit_button_rect = display_rules_screen(screen)
    else:
        if first_time:
            # Afficher l'écran de démarrage
            screen.blit(banner_start, banner_rect)
            screen.blit(play_button_start, play_button_rect)
            screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit
            screen.blit(rules_button, rules_button_rect)

        elif game.is_game_over:
            # Afficher le fond sombre pour l'écran de défaite
            screen.blit(bg_dark, (0, 0))
            screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit
            # Afficher les autres éléments (tableau de scores, bouton Retry, etc.)
            retry_button_rect = display_defeat_screen(screen, game)


    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clic sur le bouton Play depuis l'écran principal
            if first_time and play_button_rect.collidepoint(event.pos):
                first_time = False
                screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit
                game.start()
                sound_manager.play('click')
                sound_manager.stop('welcome')

            # Clic sur le bouton Retry depuis l'écran de défaite
            elif game.is_game_over and retry_button_rect and retry_button_rect.collidepoint(event.pos):
                game.reset_game()
                game.start()  # Redémarrer une nouvelle partie directement
                sound_manager.play('click')
                screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit

            # Clic sur le bouton Exit depuis l'écran de défaite
            elif game.is_game_over and exit_button_rect and exit_button_rect.collidepoint(event.pos):
                running = False
                sound_manager.play('click')
                pygame.quit()
            # Clic sur le bouton Exit depuis l'écran principal (fermer le jeu)
            elif first_time and exit_button_rect.collidepoint(event.pos):
                running = False
                sound_manager.play('click')
                pygame.quit()

            # Clic sur le bouton Exit depuis l'écran des règles (retourner à l'écran principal)
            elif show_rules and exit_button_rect.collidepoint(event.pos):
                show_rules = False
                sound_manager.play('click')
                first_time = True

            # Clic sur le bouton Rules depuis l'écran principal (ouvrir l'écran des règles)
            elif first_time and rules_button_rect.collidepoint(event.pos):
                first_time = False
                sound_manager.play('click')
                show_rules = True

        # Afficher l'écran des règles si actif
        if show_rules:
            exit_button_rect = display_rules_screen(screen)

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if game.is_playing:
                if event.key == pygame.K_UP:
                    game.player.jump()
                elif event.key == pygame.K_SPACE:
                    game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                game.player.stop_moving()


        # Gestion des mouvements en continu (gauche/droite)
        if game.is_playing:
            if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
                game.player.move_right()
            elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
                game.player.move_left()
            else:
                game.player.stop_moving()

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


