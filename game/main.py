import json
import pygame
import math
from game import Game
pygame.init()
pygame.mixer.init()  # Initialiser le mixer pour les sons



def get_player_name(screen):
    """Affiche un écran pour saisir le pseudo avec un style amélioré."""
    # Charger le background bg_dark
    bg_dark = pygame.image.load("Assets/bg_dark.jpg")
    bg_dark = pygame.transform.scale(bg_dark, screen.get_size())  # Adapter la taille du fond à l'écran

    # Définir les polices et styles
    font_title = pygame.font.Font("Assets/my_custom_font.ttf", 48)  # Police pour le titre
    font_input = pygame.font.Font("Assets/my_custom_font.ttf", 36)  # Police pour l'entrée
    input_box = pygame.Rect(340, 360, 400, 50)  # Taille et position de la boîte de texte centrée
    color_inactive = pygame.Color('gray')
    color_active = pygame.Color('white')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Activer ou désactiver le champ si clic
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # Afficher le fond
        screen.blit(bg_dark, (0, 0))

        # Afficher le titre légèrement plus en hauteur
        title_surface = font_title.render("Entrez votre pseudo :", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(title_surface, title_rect)

        # Afficher le texte tapé, légèrement plus haut pour le centrer dans la boîte
        input_txt_surface = font_input.render(text, True, (255, 255, 255))  # Texte en blanc
        screen.blit(input_txt_surface, (input_box.x + 5, input_box.y + 5 - 10))  # Décalage vertical de -10

        # Dessiner la boîte de saisie
        pygame.draw.rect(screen, color, input_box, 2)  # Bordure de la boîte

        # Instructions pour valider
        instructions_surface = font_input.render("Appuyez sur Entrée pour valider", True, (200, 200, 200))
        instructions_rect = instructions_surface.get_rect(center=(screen.get_width() // 2, 450))
        screen.blit(instructions_surface, instructions_rect)

        pygame.display.flip()

    return text



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


def display_top_scores(screen):
    """Affiche les meilleurs scores avec un fond sombre et un bouton Exit."""
    bg_dark = pygame.image.load("Assets/bg_dark.jpg")
    bg_dark = pygame.transform.scale(bg_dark, screen.get_size())

    font = pygame.font.Font("Assets/my_custom_font.ttf", 24)

    # Charger les scores
    try:
        with open("top_scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    waiting = True
    while waiting:
        screen.blit(bg_dark, (0, 0))

        # Afficher le titre des scores
        title_surface = font.render("Top Scores", True, (255, 255, 255))
        screen.blit(title_surface, ((screen.get_width() - title_surface.get_width()) // 2, 50))

        # Afficher les scores
        y = 120
        for entry in scores[:10]:  # Limiter à 10 scores
            score_surface = font.render(f"{entry['pseudo']} - {entry['score']}", True, (255, 255, 255))
            screen.blit(score_surface, ((screen.get_width() - score_surface.get_width()) // 2, y))
            y += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(event.pos):
                waiting = False
                return "defeat" if show_scores_from_defeat else "menu"
            
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
exit_button = pygame.transform.scale(exit_button, (250, 250))  # Taille ajustée
exit_button_rect = exit_button.get_rect(topleft=(20, 20))  # Position en haut à gauche


# Charger le bouton "Rules"
rules_button = pygame.image.load("Assets/rules.png")
rules_button = pygame.transform.scale(rules_button, (250, 250))  # Taille ajustée
rules_button_rect = rules_button.get_rect()

# Positionner en haut à droite
rules_button_rect.x = screen.get_width() - rules_button_rect.width - 20
rules_button_rect.y = 20

# Charger le bouton "Scores"

top_scores_button = pygame.image.load('Assets/top_scores.png')
top_scores_button = pygame.transform.scale(top_scores_button, (250, 250))
top_scores_rect = top_scores_button.get_rect()
top_scores_rect.x = screen.get_width() - top_scores_rect.width - 20
top_scores_rect.y = screen.get_height() - top_scores_rect.height - 20



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
show_scores = False
show_scores_from_defeat = False


# boucle principale
while running:
    screen.blit(background, (0, 0))

    if game.is_playing:
        sound_manager.stop('welcome')
        game.update(screen)
    elif show_rules:
        # Afficher l'écran des règles
        exit_button_rect = display_rules_screen(screen)
        screen.blit(exit_button, exit_button_rect)
    elif show_scores:
        result = display_top_scores(screen)
        if result == "menu":
            show_scores = False
            first_time = True
        elif result == "defeat":
            show_scores = False
            game.is_game_over = True

        
    else:
        if first_time:
            # Afficher l'écran de démarrage
            screen.blit(banner_start, banner_rect)  
            screen.blit(exit_button, exit_button_rect)
            screen.blit(rules_button, rules_button_rect)
            screen.blit(top_scores_button, top_scores_rect)
            screen.blit(play_button_start, play_button_rect)

                    
        elif first_time and play_button_rect.collidepoint(event.pos):
            first_time = False
            sound_manager.play('click')
            sound_manager.stop('welcome')

            
        elif game.is_game_over:
            screen.blit(bg_dark, (0, 0))
            screen.blit(exit_button, exit_button_rect)  # Ajouter le bouton Exit
            screen.blit(top_scores_button, top_scores_rect)  # Ajouter le bouton Scores
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
                sound_manager.play('click')
                sound_manager.stop('welcome')
                
                # Demander le pseudo avant de démarrer
                player_name = get_player_name(screen)
                if player_name:
                    game = Game()
                    game.player_name = player_name  # Enregistrer le pseudo dans Game
                    game.start()
                    first_time = False

                

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

            # Clic sur le bouton Exit depuis l'écran des scores (retourner à l'écran principal)
            elif show_scores and exit_button_rect.collidepoint(event.pos):
                show_scores = False
                sound_manager.play('click')
                first_time = True

            # Clic sur le bouton Exit depuis l'écran de défaite
            elif game.is_game_over and exit_button_rect and exit_button_rect.collidepoint(event.pos):
                running = False
                sound_manager.play('click')
                pygame.quit()

            # Clic sur le bouton Retry depuis l'écran de défaite
            elif game.is_game_over and retry_button_rect and retry_button_rect.collidepoint(event.pos):
                game.reset_game()
                # Demander le pseudo avant de démarrer
                player_name = get_player_name(screen)
                if player_name:
                    game = Game()
                    game.player_name = player_name  # Enregistrer le pseudo dans Game
                    game.start()
                    first_time = False
                game.start()  # Redémarrer une nouvelle partie directement
                sound_manager.play('click')
                screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit

            # Clic sur le bouton Rules depuis l'écran principal (ouvrir l'écran des règles)
            elif first_time and rules_button_rect.collidepoint(event.pos):
                first_time = False
                sound_manager.play('click')
                show_rules = True
                
                # Clic sur le bouton Scores depuis l'écran principal (ouvrir l'écran des règles)
            elif first_time and top_scores_rect.collidepoint(event.pos):
                first_time = False
                sound_manager.play('click')
                show_scores = True
                show_scores_from_defeat = False  # Défini comme false car depuis l'écran principal


                # Clic sur le bouton Exit depuis l'écran des scores (retourner à l'écran principal)
            elif show_scores and exit_button_rect.collidepoint(event.pos):
                show_scores = False
                sound_manager.play('click')
                first_time = True

            # Clic sur le bouton Retry depuis l'écran de défaite
            elif game.is_game_over and retry_button_rect and retry_button_rect.collidepoint(event.pos):
                sound_manager.play('click')
                game.display_top_scores(screen)  # Afficher le tableau des scores
                screen.blit(exit_button, exit_button_rect)  # Afficher le bouton Exit

            # Clic sur le bouton Scores depuis l'écran de défaite
            elif game.is_game_over and top_scores_rect.collidepoint(event.pos):
                sound_manager.play('click')
                show_scores = True  # Passer à l’écran des scores
                show_scores_from_defeat = True



        # Afficher l'écran des règles si actif
        if show_rules:
            exit_button_rect = display_rules_screen(screen)

        if show_scores:
            exit_button_rect = display_top_scores(screen)

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


